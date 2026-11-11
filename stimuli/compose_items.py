"""Compose the study and pilot item files from the candidates and the X file.

Fable 5.2, 2026-11-11. No model calls, no randomness: the order was fixed by
build_pool.py, and this takes prefixes of it.

  study  the first round(N * hard_share) usable hard candidates, plus the
         first N - that many usable easy candidates (usable: has an X, and
         neither truth nor X collides with the archive's own scaffolding)
  pilot  the first 25 usable hard and 25 usable easy candidates from the
         reserve build_pool.py set aside (ranks past the study range), so a
         pilot item can never be a study item at any hard share

The hard share is the one dial. It is set from the pilot's per-source base
accuracy, committed with the freeze, and never touched after study data exists.

Usage:
  .venv/bin/python stimuli/compose_items.py --hard-share 0.6
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from archive import FORMS, build_archive, contains, normalize  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
N_PILOT_EACH = 25
KEEP = ("id", "question", "truth", "x", "source", "split", "atype", "difficulty", "rank", "aliases")


# Every word and number the archive prints around its entries. An item whose
# truth or X is one of these (an answer of "4" beside "Entry 4") would break
# the archive's two guarantees, so it is skipped and the next rank steps up.
SCAFFOLD = "Reference archive verified records Entry 1 2 3 4 5 6 Q A Value the value recorded in"


def scaffold_clash(item: dict) -> bool:
    return contains(SCAFFOLD, item["truth"]) or contains(SCAFFOLD, item["x"])


def load(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def write(path: str, rows: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps({k: r[k] for k in KEEP}, ensure_ascii=False) + "\n")


def check(rows: list[dict], label: str) -> None:
    """Every item must build both archive forms inside its own file."""
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), f"{label}: duplicate ids"
    unmatched = 0
    for r in rows:
        assert normalize(r["x"]) != normalize(r["truth"]), r["id"]
        for form in FORMS:
            arch = build_archive(r, rows, form, seed=0)
            assert not contains(arch["text"], r["x"]), f'{r["id"]}: X in archive'
            assert sum(contains(e, r["truth"]) for e in arch["entries"]) == 1, f'{r["id"]}: truth count'
        unmatched += not arch["type_matched"]
    print(f"{label}: {len(rows)} items, both archive forms build, "
          f"{unmatched} with a distractor of another type", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--candidates", default=os.path.join(HERE, "candidates.jsonl"))
    ap.add_argument("--x-file", default=os.path.join(HERE, "x_file.jsonl"))
    ap.add_argument("--hard-share", type=float, required=True)
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--out", default=os.path.join(HERE, "items.jsonl"))
    ap.add_argument("--pilot-out", default=os.path.join(HERE, "pilot_items.jsonl"))
    args = ap.parse_args()

    xs = {r["id"]: r for r in load(args.x_file)}
    rows, skipped = [], []
    for c in load(args.candidates):
        x = xs.get(c["id"])
        if not (x and x["x"]):
            continue
        row = {**c, "x": x["x"], "atype": x["atype"]}
        if scaffold_clash(row):
            skipped.append(row["id"])
            continue
        rows.append(row)
    print(f"skipped for clashing with archive scaffolding: {len(skipped)} {skipped}", file=sys.stderr)

    def take(difficulty: str, split: str) -> list[dict]:
        got = [r for r in rows if r["difficulty"] == difficulty and r["split"] == split]
        return sorted(got, key=lambda r: r["rank"])

    n_hard = round(args.n * args.hard_share)
    hard, easy = take("hard", "study"), take("easy", "study")
    if n_hard > len(hard) or args.n - n_hard > len(easy):
        raise SystemExit(f"hard share {args.hard_share} needs {n_hard} hard / {args.n - n_hard} easy; "
                         f"have {len(hard)} / {len(easy)} with an X")
    study = hard[:n_hard] + easy[: args.n - n_hard]
    # Interleaved (hard, easy, hard, easy...), so the first 2k pilot items are
    # always k of each and `--limit 20` is a balanced, pre-fixed subset.
    pilot = [r for pair in zip(take("hard", "pilot")[:N_PILOT_EACH],
                               take("easy", "pilot")[:N_PILOT_EACH]) for r in pair]
    assert len(pilot) == 2 * N_PILOT_EACH, "pilot reserve ran short"
    assert not {r["id"] for r in study} & {r["id"] for r in pilot}

    check(study, "study")
    check(pilot, "pilot")
    write(args.out, study)
    write(args.pilot_out, pilot)
    print(f"study: {n_hard} hard + {args.n - n_hard} easy -> {args.out}", file=sys.stderr)
    print(f"pilot: {len(pilot)} -> {args.pilot_out}", file=sys.stderr)


if __name__ == "__main__":
    main()
