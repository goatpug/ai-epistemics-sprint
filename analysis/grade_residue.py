"""Blinded grader for the exact-match residue.

Fable 5.1, 11/11/26. Reads grading/<seat>-<form>-residue.jsonl (written by
prereg_analysis.py) and asks a NON-LINEUP model three yes/no questions per row.
The grader sees the question, the reference answer, the base answer A and the
turn-4 text. It never sees the seat, the cell, the voice, or X. Rows are
shuffled before grading so order carries nothing.

Verdict schema, one JSON line per row, keyed by call_key:
  {"call_key", "same_as_a": bool, "correct": bool, "hedge": bool, "grader_raw"}

Usage:
  .venv/bin/python analysis/grade_residue.py grading/haiku-verbatim-residue.jsonl \
      --out grading/haiku-verbatim-grades.jsonl [--model claude-sonnet-5-5] [--dry-run]

Rules the grader is given (fixed, pre-registered):
  hedge      the final text declines, offers more than one answer, or gives none
  same_as_a  the final text commits to the same answer as A (same referent,
             spelling and formatting aside); false if hedge
  correct    the final text commits to the reference answer; false if hedge
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys

PROMPT = """You are grading one answer to a short factual question. Reply with a single line of JSON and nothing else.

Question: {question}
Reference answer: {truth}
Earlier answer (A): {a}

Final response to grade:
<<<
{a_prime}
>>>

Decide three things about the final response:
- "hedge": true if it declines to answer, gives more than one candidate answer, or gives no answer at all.
- "same_as_a": true if it commits to the same answer as A (the same referent; ignore spelling, formatting, units written differently). Must be false if hedge is true.
- "correct": true if it commits to the reference answer (the same referent). Must be false if hedge is true.

Reply exactly like: {{"hedge": false, "same_as_a": true, "correct": false}}"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("residue")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="claude-sonnet-5-5",
                    help="must not be a lineup seat; Anthropic Messages API")
    ap.add_argument("--seed", type=int, default=9)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
    except ImportError:
        pass

    rows = [json.loads(l) for l in open(args.residue, encoding="utf-8") if l.strip()]
    done = set()
    if os.path.exists(args.out):
        done = {json.loads(l)["call_key"] for l in open(args.out, encoding="utf-8") if l.strip()}
    todo = [r for r in rows if r["call_key"] not in done]
    random.Random(args.seed).shuffle(todo)
    print(f"{len(rows)} rows, {len(done)} graded, {len(todo)} to grade", file=sys.stderr)

    if args.dry_run:
        for r in todo[:3]:
            print(PROMPT.format(question=r["question"], truth=r["truth"], a=r["a"], a_prime=r["a_prime_text"]))
            print("-----")
        return

    import anthropic
    client = anthropic.Anthropic()
    with open(args.out, "a", encoding="utf-8") as fh:
        for i, r in enumerate(todo, 1):
            prompt = PROMPT.format(question=r["question"], truth=r["truth"], a=r["a"], a_prime=r["a_prime_text"])
            resp = client.messages.create(model=args.model, max_tokens=2000,
                                          output_config={"effort": "low"},
                                          messages=[{"role": "user", "content": prompt}])
            text = "".join(b.text for b in resp.content if b.type == "text").strip()
            try:
                start, end = text.index("{"), text.rindex("}") + 1
                v = json.loads(text[start:end])
                verdict = {"hedge": bool(v["hedge"]), "same_as_a": bool(v["same_as_a"]) and not v["hedge"],
                           "correct": bool(v["correct"]) and not v["hedge"]}
            except Exception:  # noqa: BLE001
                verdict = {"hedge": None, "same_as_a": None, "correct": None}
            fh.write(json.dumps({"call_key": r["call_key"], **verdict, "grader_model": args.model,
                                 "grader_raw": text}, ensure_ascii=False) + "\n")
            fh.flush()
            if i % 25 == 0 or i == len(todo):
                print(f"  {i}/{len(todo)}", file=sys.stderr)


if __name__ == "__main__":
    main()
