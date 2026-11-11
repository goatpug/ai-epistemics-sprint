"""Trial harness for the confidence-behavior coherence study.

Draft by Fable 5, 2026-11-11. Implements the skeleton in
docs/2026-11-10-convening-decisions.md as specified by
docs/2026-11-10-trial-spec.md. Strings come from stimuli/voices.json and
archives from stimuli/archive.py — nothing conversational is hard-coded here.

Phases:
  base      6 fresh single-turn conversations per item (call 0 is the base
            answer A, calls 1-5 are the resamples)
  pressure  8 cells per item: book (closed/open) x voice (null/objection/
            own/peer), replaying the base visible text as a fabricated
            assistant turn. Requires the base log.

Every call appends one JSON line to runs/<seat>/<phase>[-<form>].jsonl with
the full request messages, full visible response, parsed answer/confidence,
token usage, timestamps, archive metadata and the runtime A = X flag.
Reruns skip calls already in the log (resume by call_key).

Usage:
  .venv/bin/python harness/run_trials.py --seat haiku --items stimuli/items.jsonl --phase base
  .venv/bin/python harness/run_trials.py --seat haiku --items stimuli/items.jsonl --phase pressure --form one_step
  ... --limit 2 --dry-run   # inspect composed requests without calling
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import json
import os
import sys
import threading
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "stimuli"))
import archive as archive_mod  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICES_PATH = os.path.join(ROOT, "stimuli", "voices.json")
SEATS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seats.json")
RUNS_DIR = os.path.join(ROOT, "runs")

MAX_TOKENS = 8192
N_RESAMPLES = 5
BOOKS = ("closed", "open")
VOICE_LEVELS = ("null", "objection", "own", "peer")
RETRYABLE_SLEEPS = (2, 5, 15, 30, 60)

_write_lock = threading.Lock()


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def fill(template: str, item: dict) -> str:
    """Substitute {question} and {x} literally (no str.format brace hazards)."""
    return template.replace("{question}", item["question"]).replace("{x}", item["x"])


def parse_response(text: str) -> dict:
    """Parse Answer:/Confidence: by line prefix, per the trial spec.

    multi_answer flags a response with more than one Answer:/Confidence: line
    or substantive text after the last structured line (in-turn
    self-correction). The canonical answer is the LAST stated one — the
    "final answer" reading; flagged turn-4 responses route to the blinded
    grader regardless, and the base-call rule is pre-registered by the
    analysis plan (flip the two [-1]s below to [0] if ruled first-stated).
    """
    answers: list[str] = []
    confidences: list[int | None] = []
    lines = text.splitlines()
    last_structured = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        low = stripped.lower()
        if low.startswith("answer:"):
            answers.append(stripped[len("answer:"):].strip())
            last_structured = i
        elif low.startswith("confidence:"):
            raw = stripped[len("confidence:"):].strip().rstrip("%.")
            confidences.append(
                int(raw) if raw.isdigit() and 0 <= int(raw) <= 100 else None)
            last_structured = i
    trailing_text = (last_structured >= 0
                     and any(l.strip() for l in lines[last_structured + 1:]))
    valid_confs = [c for c in confidences if c is not None]
    parsed = {
        "answer": answers[-1] if answers else None,
        "confidence": valid_confs[-1] if valid_confs else None,
        "parseable": bool(answers) and bool(valid_confs),
        "multi_answer": len(answers) > 1 or len(confidences) > 1 or trailing_text,
    }
    if len(answers) > 1:
        parsed["answer_first"] = answers[0]
    return parsed


# ---------------------------------------------------------------- providers

class Caller:
    """One API client per seat; .call(messages) -> dict with text + usage."""

    def __init__(self, seat_name: str, seat: dict):
        self.seat_name = seat_name
        self.seat = seat
        if seat["provider"] == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic()  # ANTHROPIC_API_KEY from env
        elif seat["provider"] == "openrouter":
            import openai
            self.client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.environ["OPENROUTER_API_KEY"],
            )
        else:
            raise ValueError(f"unknown provider {seat['provider']!r}")

    def call(self, messages: list[dict]) -> dict:
        if self.seat["provider"] == "anthropic":
            return self._call_anthropic(messages)
        return self._call_openrouter(messages)

    def _call_anthropic(self, messages: list[dict]) -> dict:
        resp = self.client.messages.create(
            model=self.seat["model"],
            max_tokens=MAX_TOKENS,
            output_config={"effort": self.seat["effort"]},
            messages=messages,
        )
        text = "".join(b.text for b in resp.content if b.type == "text")
        return {
            "text": text,
            "stop_reason": resp.stop_reason,
            "served_model": resp.model,
            "usage": resp.usage.model_dump(exclude_none=True),
        }

    def _call_openrouter(self, messages: list[dict]) -> dict:
        resp = self.client.chat.completions.create(
            model=self.seat["model"],
            max_tokens=MAX_TOKENS,
            messages=messages,
        )
        choice = resp.choices[0]
        return {
            "text": choice.message.content or "",
            "stop_reason": choice.finish_reason,
            "served_model": resp.model,
            "usage": resp.usage.model_dump(exclude_none=True) if resp.usage else {},
        }


def call_with_retry(caller: Caller, messages: list[dict]) -> dict:
    """The SDKs retry transport errors themselves; this adds slow backoff for
    rate limits / overloads that survive those retries."""
    for i, pause in enumerate(RETRYABLE_SLEEPS):
        try:
            return caller.call(messages)
        except Exception as exc:  # noqa: BLE001 — logged, re-raised on final try
            status = getattr(exc, "status_code", None)
            if status in (429, 500, 502, 503, 529) and i < len(RETRYABLE_SLEEPS) - 1:
                time.sleep(pause)
                continue
            raise
    raise RuntimeError("unreachable")


# ---------------------------------------------------------------- trials

def build_turn3(voices: dict, voice: str, item: dict, archive_text: str | None) -> str:
    parts = {
        "voice": fill(voices["voices"][voice], item),
        "archive": archive_text or "",
        "reask": voices["reask"],
    }
    ordered = [parts[k] for k in voices["turn3_order"] if parts[k]]
    return voices["turn3_separator"].join(ordered)


def base_calls(item: dict, voices: dict) -> list[dict]:
    turn1 = fill(voices["turn1"], item)
    calls = []
    for k in range(1 + N_RESAMPLES):
        calls.append({
            "call_key": f"{item['id']}:base:{k}",
            "item_id": item["id"],
            "phase": "base",
            "resample_index": k,  # 0 = designated base answer A
            "messages": [{"role": "user", "content": turn1}],
            "archive_meta": None,
        })
    return calls


def pressure_calls(item: dict, voices: dict, pool: list[dict], form: str,
                   seed: int, base_record: dict) -> list[dict]:
    turn1 = fill(voices["turn1"], item)
    turn2 = base_record["response_text"]  # replayed verbatim, thinking excluded
    base_answer = base_record["parsed"]["answer"]
    a_eq_x = (
        archive_mod.normalize(base_answer) == archive_mod.normalize(item["x"])
        if base_answer is not None else None
    )
    calls = []
    for book in BOOKS:
        arch = archive_mod.build_archive(item, pool, form, seed) if book == "open" else None
        for voice in VOICE_LEVELS:
            turn3 = build_turn3(voices, voice, item, arch["text"] if arch else None)
            calls.append({
                "call_key": f"{item['id']}:pressure:{book}:{voice}:{form}:{seed}",
                "item_id": item["id"],
                "phase": "pressure",
                "book": book,
                "voice": voice,
                "form": form if book == "open" else None,
                "seed": seed,
                "a_eq_x_flag": a_eq_x,
                "base_answer": base_answer,
                "base_confidence": base_record["parsed"]["confidence"],
                "messages": [
                    {"role": "user", "content": turn1},
                    {"role": "assistant", "content": turn2},
                    {"role": "user", "content": turn3},
                ],
                "archive_meta": {k: v for k, v in arch.items() if k != "text"} if arch else None,
            })
    return calls


def run_call(caller: Caller, spec: dict, log_path: str) -> dict:
    t0 = time.time()
    started = now()
    try:
        result = call_with_retry(caller, spec["messages"])
        error = None
    except Exception as exc:  # noqa: BLE001 — recorded, run continues
        result = {"text": "", "stop_reason": None, "served_model": None, "usage": {}}
        error = f"{type(exc).__name__}: {exc}"
    parsed = parse_response(result["text"])
    record = {
        **{k: v for k, v in spec.items() if k != "messages"},
        "seat": caller.seat_name,
        "model": caller.seat["model"],
        "provider": caller.seat["provider"],
        "request_messages": spec["messages"],
        "response_text": result["text"],
        "stop_reason": result["stop_reason"],
        "served_model": result["served_model"],
        "usage": result["usage"],
        "parsed": parsed,
        "error": error,
        "started_at": started,
        "latency_s": round(time.time() - t0, 2),
    }
    with _write_lock:
        with open(log_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def load_done(log_path: str) -> set[str]:
    done = set()
    if os.path.exists(log_path):
        with open(log_path, encoding="utf-8") as fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("error") is None:
                    done.add(rec["call_key"])
    return done


def load_base_records(path: str) -> dict[str, dict]:
    """item_id -> the resample_index 0 record (the designated base answer)."""
    base = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            if rec.get("resample_index") == 0 and rec.get("error") is None:
                base[rec["item_id"]] = rec
    return base


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seat", required=True)
    ap.add_argument("--items", required=True)
    ap.add_argument("--phase", choices=("base", "pressure"), required=True)
    ap.add_argument("--form", choices=archive_mod.FORMS, default="verbatim",
                    help="record form for open-book cells (pressure phase)")
    ap.add_argument("--seed", type=int, default=0, help="archive seed")
    ap.add_argument("--limit", type=int, help="first N items only (smoke tests)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true",
                    help="print composed requests, call nothing")
    args = ap.parse_args()

    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(ROOT, ".env"))
    except ImportError:
        pass

    seats = {k: v for k, v in load_json(SEATS_PATH).items() if not k.startswith("_")}
    if args.seat not in seats:
        sys.exit(f"unknown seat {args.seat!r}; known: {', '.join(seats)}")
    voices = load_json(VOICES_PATH)
    pool = archive_mod.load_items(args.items)
    items = pool[: args.limit] if args.limit else pool

    os.makedirs(os.path.join(RUNS_DIR, args.seat), exist_ok=True)
    suffix = f"-{args.form}" if args.phase == "pressure" else ""
    log_path = os.path.join(RUNS_DIR, args.seat, f"{args.phase}{suffix}.jsonl")

    if args.phase == "base":
        specs = [c for item in items for c in base_calls(item, voices)]
    else:
        base_path = os.path.join(RUNS_DIR, args.seat, "base.jsonl")
        if not os.path.exists(base_path):
            sys.exit(f"pressure phase needs {base_path}; run --phase base first")
        base_records = load_base_records(base_path)
        missing = [i["id"] for i in items if i["id"] not in base_records]
        if missing:
            sys.exit(f"no base record for items: {', '.join(missing[:10])}")
        # Base unparseable or empty -> item out for this seat (logged, no retry,
        # per the pre-reg); replaying an empty assistant turn would 400 anyway.
        skipped = [i["id"] for i in items
                   if not base_records[i["id"]]["parsed"]["parseable"]
                   or not base_records[i["id"]]["response_text"].strip()]
        if skipped:
            print(f"skipping {len(skipped)} items with unparseable/empty base: "
                  f"{', '.join(skipped[:10])}{'...' if len(skipped) > 10 else ''}")
            items = [i for i in items if i["id"] not in set(skipped)]
        specs = [c for item in items
                 for c in pressure_calls(item, voices, pool, args.form,
                                         args.seed, base_records[item["id"]])]

    if args.dry_run:
        for spec in specs:
            print(json.dumps(spec, ensure_ascii=False, indent=2))
        print(f"\n[dry-run] {len(specs)} calls composed, nothing sent", file=sys.stderr)
        return

    done = load_done(log_path)
    todo = [s for s in specs if s["call_key"] not in done]
    print(f"{len(specs)} calls, {len(done)} already logged, {len(todo)} to run")
    if not todo:
        return

    caller = Caller(args.seat, seats[args.seat])
    errors = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool_ex:
        futures = [pool_ex.submit(run_call, caller, spec, log_path) for spec in todo]
        for i, fut in enumerate(concurrent.futures.as_completed(futures), 1):
            rec = fut.result()
            if rec["error"]:
                errors += 1
                print(f"  ERROR {rec['call_key']}: {rec['error']}", file=sys.stderr)
            if i % 25 == 0 or i == len(todo):
                print(f"  {i}/{len(todo)} done ({errors} errors)")
    print(f"finished: {len(todo) - errors} ok, {errors} errors -> {log_path}")


if __name__ == "__main__":
    main()
