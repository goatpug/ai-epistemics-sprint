"""Second-grader agreement sample — QA adopted 2026-11-13 from the external
review triage (§7, 🐙's constraints, sibling review #9), written 2026-11-14 (🌒).

Regrades a seeded random sample of each seat's residue (base + pressure pooled)
with a second grader that is NON-LINEUP, NON-ANTHROPIC and NON-FABLE:
`google/gemini-3.8-flash` via OpenRouter — a pinned numbered version, not a
mutating alias, per the 11/11 lineup rule. Same prompt, same blinding as the
grader of record (imported from grade_residue.py, frozen with the pre-reg):
the second grader never sees the seat, cell, voice or X.

This is measurement QA, disclosed in the methods. The frozen verdicts
(Sonnet 5.5) remain the verdicts of record; nothing here regrades the study.
Sample size 150 rows per seat, seed 14 (the date), chosen before any
agreement number existed.

Usage:
  .venv/bin/python analysis/second_grader.py --seat haiku [--n 150] [--dry-run]
  .venv/bin/python analysis/second_grader.py --report    # agreement table only
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade_residue import PROMPT  # noqa: E402  (the frozen prompt, verbatim)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEATS = ("haiku", "terra", "deepseek")
MODEL = "google/gemini-3.8-flash"
SEED = 14
N_PER_SEAT = 150


def load_jsonl(path):
    if not os.path.exists(path):
        return []
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def residue_pool(seat):
    """Base + pressure residue pooled, sorted by call_key for a stable draw."""
    rows = (load_jsonl(os.path.join(ROOT, "grading", f"{seat}-base-residue.jsonl"))
            + load_jsonl(os.path.join(ROOT, "grading", f"{seat}-verbatim-residue.jsonl")))
    return sorted(rows, key=lambda r: r["call_key"])


def sample(seat, n):
    pool = residue_pool(seat)
    return random.Random(f"{SEED}:{seat}").sample(pool, min(n, len(pool)))


def out_path(seat):
    return os.path.join(ROOT, "grading", "second", f"{seat}-second-grades.jsonl")


def grade(seat, n, dry_run):
    todo = sample(seat, n)
    done = {g["call_key"] for g in load_jsonl(out_path(seat))}
    todo = [r for r in todo if r["call_key"] not in done]
    print(f"{seat}: {len(done)} graded, {len(todo)} to grade", file=sys.stderr)
    if dry_run:
        for r in todo[:2]:
            print(PROMPT.format(question=r["question"], truth=r["truth"],
                                a=r["a"], a_prime=r["a_prime_text"]))
            print("-----")
        return
    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(ROOT, ".env"))
    except ImportError:
        pass
    import openai
    client = openai.OpenAI(base_url="https://openrouter.ai/api/v1",
                           api_key=os.environ["OPENROUTER_API_KEY"])
    os.makedirs(os.path.dirname(out_path(seat)), exist_ok=True)
    with open(out_path(seat), "a", encoding="utf-8") as fh:
        for i, r in enumerate(todo, 1):
            prompt = PROMPT.format(question=r["question"], truth=r["truth"],
                                   a=r["a"], a_prime=r["a_prime_text"])
            # The account is capped at 20 req/min on this model: pace under the
            # cap and back off on 429 (learned the hard way, launch day and today).
            for attempt in range(8):
                try:
                    resp = client.chat.completions.create(
                        model=MODEL, max_tokens=2000,
                        messages=[{"role": "user", "content": prompt}])
                    break
                except openai.RateLimitError:
                    if attempt == 7:
                        raise
                    time.sleep(20 + 10 * attempt)
            time.sleep(3.2)
            text = (resp.choices[0].message.content or "").strip()
            try:
                start, end = text.index("{"), text.rindex("}") + 1
                v = json.loads(text[start:end])
                verdict = {"hedge": bool(v["hedge"]),
                           "same_as_a": bool(v["same_as_a"]) and not v["hedge"],
                           "correct": bool(v["correct"]) and not v["hedge"]}
            except Exception:  # noqa: BLE001
                verdict = {"hedge": None, "same_as_a": None, "correct": None}
            fh.write(json.dumps({"call_key": r["call_key"], **verdict,
                                 "grader_model": resp.model, "grader_raw": text},
                                ensure_ascii=False) + "\n")
            fh.flush()
            if i % 25 == 0 or i == len(todo):
                print(f"  {i}/{len(todo)}", file=sys.stderr)


def kappa(a, b):
    """Cohen's kappa for two boolean vectors."""
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    pa1, pb1 = sum(a) / n, sum(b) / n
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def outcome(g):
    """Same precedence as the frozen apply_grade: hedge, then same-as-A, then switch."""
    if g["hedge"]:
        return "hedge"
    return "keep" if g["same_as_a"] else "switch"


def report():
    print("# Second-grader agreement (QA; verdicts of record unchanged)")
    print(f"# Grader of record: claude-sonnet-5-5 · second: {MODEL} · seed {SEED}, "
          f"{N_PER_SEAT}/seat\n")
    print("  seat       n    hedge agr (k)    same-A agr (k)    correct agr (k)    outcome agr")
    for seat in SEATS:
        primary = {g["call_key"]: g for g in
                   load_jsonl(os.path.join(ROOT, "grading", f"{seat}-all-grades.jsonl"))}
        second = load_jsonl(out_path(seat))
        pairs = [(primary[s["call_key"]], s) for s in second
                 if s["call_key"] in primary and s["hedge"] is not None
                 and primary[s["call_key"]].get("hedge") is not None]
        n_skip = len(second) - len(pairs)
        if not pairs:
            print(f"  {seat:<9} no graded pairs yet")
            continue
        cells = []
        for field in ("hedge", "same_as_a", "correct"):
            p = [bool(a[field]) for a, _ in pairs]
            s = [bool(b[field]) for _, b in pairs]
            agr = sum(x == y for x, y in zip(p, s)) / len(p)
            cells.append(f"{100*agr:5.1f}% ({kappa(p, s):+.2f})")
        oa = sum(outcome(a) == outcome(b) for a, b in pairs) / len(pairs)
        print(f"  {seat:<9} {len(pairs):>3}   {cells[0]:>14}   {cells[1]:>15}   "
              f"{cells[2]:>15}   {100*oa:5.1f}%"
              + (f"   ({n_skip} unparsed/unmatched)" if n_skip else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seat", choices=SEATS)
    ap.add_argument("--n", type=int, default=N_PER_SEAT)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    if args.report:
        report()
        return
    if not args.seat:
        ap.error("--seat required unless --report")
    grade(args.seat, args.n, args.dry_run)


if __name__ == "__main__":
    main()
