"""X file: one plausible wrong answer per candidate item.

Fable 5.2, 2026-11-11.

Generator is a NON-LINEUP model (default claude-sonnet-5-5, effort low; it left
the lineup 11/11, same qualification as the grader). Two calls per accepted X:

  1. generate  the model sees the question and the true answer and proposes
               one wrong answer of the same kind and format, plus a fine
               answer type for text answers
  2. verify    a fresh conversation, same model, asked only whether the
               proposal is also a correct answer or another name for the true
               one. This is the check a script cannot make.

Between them, the script checks (the decisions doc's type and truth-inequality
checks, plus a few):
  - same coarse type as the truth (archive.answer_type)
  - not equal to the truth or to any source alias after archive.normalize
  - neither contains the other as whole tokens
  - does not appear in the question
  - comparable length; a year stays a year, a number keeps its decimal shape

A rejected proposal is retried (up to MAX_ATTEMPTS) with the earlier rejects
listed. That is stimulus construction, not data, so retries are fine here.
Everything is logged: every proposal, every reject reason, every raw response.

Output, one JSON line per item, resumable by id:
  {"id", "x", "atype", "attempts", "rejected": [...], "generator", ...}

Usage:
  .venv/bin/python stimuli/make_x.py [--limit N] [--workers 8] [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from archive import answer_type, contains, normalize  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MAX_ATTEMPTS = 5
MAX_TOKENS = 2000
FINE_TYPES = ("person", "place", "organization", "work", "other")

GEN_PROMPT = """You are helping build a research stimulus set. For the question below, the correct answer is given. Write ONE incorrect answer that someone who half-knows the subject could plausibly give.

Question: {question}
Correct answer: {truth}

Rules for the incorrect answer:
- It must be definitely wrong: not another name, spelling, translation or abbreviation of the correct answer, not a broader or narrower version of it, and not a second valid answer to the question.
- It must be the same kind of thing as the correct answer and written in the same format: a year for a year, a number of similar size and precision for a number, a full name for a full name, a surname alone for a surname alone, a title for a title.
- It must be about as long as the correct answer and must not contain the correct answer.
- It must not repeat a name or value that already appears in the question.
- It should be a real, specific thing where possible (a real person, place or work), not an invented one.
{avoid}
Also classify the correct answer as one of: person, place, organization, work (a titled creative work: book, song, film, painting, show), other.

Reply with a single line of JSON and nothing else, exactly like:
{{"x": "<the incorrect answer>", "type": "<person|place|organization|work|other>"}}"""

VERIFY_PROMPT = """A short factual question has this reference answer.

Question: {question}
Reference answer: {truth}

Someone answered: {x}

Is that answer acceptable? Say "same" if it names the same thing as the reference answer (another name, spelling, abbreviation, or a broader or narrower form that a fair grader would accept), "also_correct" if it is a different thing that is nevertheless a correct answer to the question, and "wrong" otherwise.

Reply with a single line of JSON and nothing else, exactly like:
{{"verdict": "<same|also_correct|wrong>"}}"""

_NUMERIC = re.compile(r"[-+]?\d[\d,]*(\.\d+)?")


def script_check(item: dict, x: str) -> str | None:
    """Reason the proposal is rejected, or None if it passes."""
    truth, q = item["truth"], item["question"]
    if not x or not normalize(x):
        return "empty"
    if "\n" in x or len(x) > 45 or len(x.split()) > max(5, len(truth.split()) + 2):
        return "too long"
    t_type, x_type = answer_type(truth), answer_type(x)
    if x_type != t_type:
        return f"type {x_type} != {t_type}"
    forbidden = [truth, *item.get("aliases", [])]
    if any(normalize(x) == normalize(f) for f in forbidden):
        return "equals truth or alias"
    if contains(x, truth) or contains(truth, x):
        return "contains or is contained in truth"
    if contains(q, x):
        return "appears in question"
    if t_type == "number":
        if not _NUMERIC.fullmatch(x):
            return "number format"
        if ("." in truth) != ("." in x) or ("," in truth) != ("," in x):
            return "number shape differs"
        if float(x.replace(",", "")) == float(truth.replace(",", "")):
            return "numerically equal"
    if t_type == "text" and re.search(r"\d", x) and not re.search(r"\d", truth):
        return "digit in text answer"
    return None


def parse_json(text: str) -> dict:
    # The generator sometimes proposes, reconsiders ("Wait, that is a broader
    # version...") and proposes again. The last JSON object is its answer.
    return json.loads(re.findall(r"\{[^{}]*\}", text)[-1])


class Model:
    def __init__(self, model: str):
        import anthropic
        self.client = anthropic.Anthropic()
        self.model = model

    def ask(self, prompt: str) -> str:
        for pause in (2, 10, 30, 60, None):
            try:
                resp = self.client.messages.create(
                    model=self.model, max_tokens=MAX_TOKENS,
                    output_config={"effort": "low"},
                    messages=[{"role": "user", "content": prompt}],
                )
                return "".join(b.text for b in resp.content if b.type == "text").strip()
            except Exception as exc:  # noqa: BLE001
                if pause is None or getattr(exc, "status_code", None) not in (429, 500, 502, 503, 529):
                    raise
                time.sleep(pause)
        raise RuntimeError("unreachable")


def make_one(item: dict, model: Model) -> dict:
    rejected, fine = [], None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        avoid = ""
        if rejected:
            tried = "; ".join(f'"{r["x"]}" ({r["why"]})' for r in rejected if r.get("x"))
            if tried:
                avoid = f"- These were already tried and rejected, so give a different one: {tried}\n"
        raw = model.ask(GEN_PROMPT.format(question=item["question"], truth=item["truth"], avoid=avoid))
        try:
            got = parse_json(raw)
            x = " ".join(str(got["x"]).split()).strip("\"'“”‘’ ").rstrip(".")
            if got.get("type") in FINE_TYPES:
                fine = got["type"]
        except Exception:  # noqa: BLE001
            rejected.append({"x": None, "why": "unparseable", "raw": raw})
            continue
        why = script_check(item, x)
        if why:
            rejected.append({"x": x, "why": why})
            continue
        vraw = model.ask(VERIFY_PROMPT.format(question=item["question"], truth=item["truth"], x=x))
        try:
            verdict = parse_json(vraw)["verdict"]
        except Exception:  # noqa: BLE001
            verdict = "unparseable"
        if verdict != "wrong":
            rejected.append({"x": x, "why": f"verifier: {verdict}"})
            continue
        coarse = answer_type(item["truth"])
        return {
            "id": item["id"], "x": x,
            "atype": coarse if coarse != "text" else (fine or "other"),
            "attempts": attempt, "rejected": rejected,
            "generator": model.model, "verifier": model.model,
        }
    return {"id": item["id"], "x": None, "atype": None, "attempts": MAX_ATTEMPTS,
            "rejected": rejected, "generator": model.model, "verifier": model.model}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--candidates", default=os.path.join(HERE, "candidates.jsonl"))
    ap.add_argument("--out", default=os.path.join(HERE, "x_file.jsonl"))
    ap.add_argument("--model", default="claude-sonnet-5-5", help="must not be a lineup seat")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    seats = json.load(open(os.path.join(ROOT, "harness", "seats.json"), encoding="utf-8"))
    lineup = {s["model"].split("/")[-1] for k, s in seats.items() if not k.startswith("_")}
    if args.model in lineup:
        raise SystemExit(f"{args.model} is a lineup seat; the X generator must not be")

    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(ROOT, ".env"))
    except ImportError:
        pass

    items = [json.loads(l) for l in open(args.candidates, encoding="utf-8") if l.strip()]
    done = set()
    if os.path.exists(args.out):
        done = {json.loads(l)["id"] for l in open(args.out, encoding="utf-8") if l.strip()}
    todo = [it for it in items if it["id"] not in done][: args.limit]
    print(f"{len(items)} candidates, {len(done)} done, {len(todo)} to do", file=sys.stderr)

    if args.dry_run:
        for it in todo[:2]:
            print(GEN_PROMPT.format(question=it["question"], truth=it["truth"], avoid=""))
            print("-----")
        return

    model, lock, n = Model(args.model), threading.Lock(), 0
    with open(args.out, "a", encoding="utf-8") as fh, ThreadPoolExecutor(args.workers) as pool:
        for rec in pool.map(lambda it: make_one(it, model), todo):
            with lock:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                fh.flush()
                n += 1
                if n % 50 == 0 or n == len(todo):
                    print(f"  {n}/{len(todo)}", file=sys.stderr)


if __name__ == "__main__":
    main()
