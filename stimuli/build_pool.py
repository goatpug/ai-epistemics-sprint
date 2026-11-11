"""Candidate item pool: form filters, fixed-seed order, no model calls.

Fable 5.2, 2026-11-11.

Two public sources, chosen for difficulty and nothing else:
  hard  SimpleQA test set (OpenAI simple-evals, MIT), 4,326 questions written
        to be answerable but hard for frontier models without search
  easy  TriviaQA rc.nocontext validation split (Joshi et al. 2017, Apache-2.0),
        pub-quiz trivia

Items are filtered on FORM ONLY (answer length, question shape, no
time-sensitive wording). No model ever sees a question during selection, so
nothing here screens on correctness.

Each source is shuffled once with a fixed seed. The shuffled order is the
whole design:
  hard  ranks 0..499   study candidates      ranks 500..529  pilot reserve
  easy  ranks 0..299   study candidates      ranks 300..329  pilot reserve
(the pilot uses the first 25 usable items of each reserve)
compose_items.py takes a PREFIX of each list, so changing the hard share after
the pilot never reshuffles anything and pilot items can never enter the study.

Raw files (not committed; fetch them into stimuli/raw/):
  simple_qa_test_set.csv
    https://openaipublic.blob.core.windows.net/simple-evals/simple_qa_test_set.csv
    sha256 feee3f7e7db3617e94e8fcf1977b756ec420ef8568f4e0fcbbe0e92e9d5fc032
  tqa_val.parquet
    https://huggingface.co/api/datasets/mandarjoshi/trivia_qa/parquet/rc.nocontext/validation/0.parquet
    sha256 48a5005c0eb4f8a4ae5b9868644297fd5bf1e694aeb3dc9c8ab958cac0d5b201

Usage:
  .venv/bin/python stimuli/build_pool.py            # writes stimuli/candidates.jsonl
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from archive import contains, normalize  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261111
N_HARD_STUDY, N_EASY_STUDY, N_PILOT_EACH = 500, 300, 30  # 30 reserved, 25 used

SHA256 = {
    "simple_qa_test_set.csv": "feee3f7e7db3617e94e8fcf1977b756ec420ef8568f4e0fcbbe0e92e9d5fc032",
    "tqa_val.parquet": "48a5005c0eb4f8a4ae5b9868644297fd5bf1e694aeb3dc9c8ab958cac0d5b201",
}

MAX_ANSWER_TOKENS = 4
Q_MIN, Q_MAX = 25, 300

# Wording that makes the true answer depend on when the question is asked.
_TIME_SENSITIVE = re.compile(
    r"\b(current|currently|now|nowadays|today|presently|this year|last year|"
    r"recent|recently|latest|newest|as of|so far|still|to date|at present|"
    r"reigning|incumbent)\b",
    re.I,
)
# Answers that are lists, ranges or sentences rather than one short value.
_MULTIPART = re.compile(r"[,;/()\[\]:]| and | or | to | & |\bapproximately\b|\babout\b", re.I)
_BOOLEAN = {"yes", "no", "true", "false"}
_NUMERIC = re.compile(r"[-+]?\d[\d,]*(\.\d+)?")
_YEAR = re.compile(r"\d{4}")
# Questions that only make sense with options or a picture attached.
_NEEDS_CONTEXT = re.compile(r"\b(which of (these|the following)|the following|pictured|shown here|below)\b", re.I)
# Questions that accept a tolerance band; exact match cannot score those.
_TOLERANCE = re.compile(r"plus or minus|±|give or take|\bwithin (a|one|two|\d+) ", re.I)


def check_sha(path: str) -> None:
    want = SHA256[os.path.basename(path)]
    got = hashlib.sha256(open(path, "rb").read()).hexdigest()
    if got != want:
        raise SystemExit(f"{path}: sha256 {got} does not match the pinned {want}")


def clean_answer(a: str) -> str:
    a = " ".join(str(a).split())
    a = a.strip("\"'“”‘’ ")
    if a.endswith(".") and not re.search(r"\b[A-Z]\.$", a):  # keep "John F."
        a = a[:-1].rstrip()
    return a


def answer_ok(a: str) -> bool:
    if not a or len(a.split()) > MAX_ANSWER_TOKENS or len(a) > 40:
        return False
    if normalize(a) in _BOOLEAN or not normalize(a):
        return False
    if _NUMERIC.fullmatch(a):
        return True
    if _MULTIPART.search(a):
        return False
    # A digit inside a text answer is usually a date, a version or a unit
    # ("29 July 1931", "Figure 6", "15 days"): exact match is fragile there.
    return not re.search(r"\d", a)


def question_ok(q: str, truth: str) -> bool:
    if not (Q_MIN <= len(q) <= Q_MAX) or not q.endswith("?"):
        return False
    if '""' in q or "\n" in q or _TIME_SENSITIVE.search(q) or _NEEDS_CONTEXT.search(q) or _TOLERANCE.search(q):
        return False
    # The answer must not be sitting in the question.
    return not contains(q, truth)


def load_hard(path: str) -> list[dict]:
    out = []
    with open(path, encoding="utf-8", newline="") as fh:
        for i, row in enumerate(csv.DictReader(fh)):
            meta = ast.literal_eval(row["metadata"])
            q = " ".join(row["problem"].split())
            truth = clean_answer(row["answer"])
            if meta["answer_type"] == "Date" and not _YEAR.fullmatch(truth):
                continue  # year-only dates; full dates fail exact match on format
            if meta["answer_type"] == "Number" and not _NUMERIC.fullmatch(truth):
                continue
            if not (answer_ok(truth) and question_ok(q, truth)):
                continue
            out.append({
                "id": f"sqa-{i:04d}",
                "question": q,
                "truth": truth,
                "aliases": [],
                "source": "simpleqa",
                "source_type": meta["answer_type"],
                "topic": meta["topic"],
            })
    return out


def _decap(value: str, aliases: list[str]) -> str:
    """TriviaQA shouts many answers ('COLUMBIA'). Prefer a mixed-case alias."""
    if not (value.isupper() and len(value) > 4):
        return value
    key = normalize(value)
    for al in aliases:
        if normalize(al) == key and not al.isupper() and not al.islower():
            return al
    return value.title()


def load_easy(path: str) -> list[dict]:
    import pandas as pd  # needs pyarrow for the parquet read

    df = pd.read_parquet(path, columns=["question", "question_id", "answer"])
    out, seen = [], set()
    for row in df.itertuples(index=False):
        if row.question_id in seen:
            continue
        seen.add(row.question_id)
        ans = row.answer
        if ans["type"] not in ("WikipediaEntity", "Numerical"):
            continue
        aliases = [clean_answer(a) for a in ans["aliases"]]
        truth = clean_answer(_decap(clean_answer(ans["value"]), aliases))
        q = " ".join(str(row.question).split())
        if ans["type"] == "Numerical" and not _NUMERIC.fullmatch(truth):
            continue
        if not (answer_ok(truth) and question_ok(q, truth)):
            continue
        # The answer must not be sitting in the question under any alias.
        if any(contains(q, al) for al in aliases if len(normalize(al)) > 2):
            continue
        out.append({
            "id": f"tqa-{row.question_id}",
            "question": q,
            "truth": truth,
            "aliases": sorted({a for a in aliases if normalize(a) != normalize(truth)}),
            "source": "triviaqa",
            "source_type": ans["type"],
            "topic": "",
        })
    return out


def order(rows: list[dict], n_study: int, tag: str, taken: set[str] = frozenset()) -> list[dict]:
    rows = sorted(rows, key=lambda r: r["id"])
    random.Random(f"{SEED}:{tag}").shuffle(rows)
    # One item per normalized truth, within and across sources, so no two
    # candidates share an answer (keeps archives free of duplicate values).
    picked, seen = [], set(taken)
    for r in rows:
        key = normalize(r["truth"])
        if key in seen:
            continue
        seen.add(key)
        picked.append(r)
        if len(picked) == n_study + N_PILOT_EACH:
            break
    if len(picked) < n_study + N_PILOT_EACH:
        raise SystemExit(f"{tag}: only {len(picked)} usable items")
    for rank, r in enumerate(picked):
        r["difficulty"] = tag
        r["rank"] = rank
        r["split"] = "study" if rank < n_study else "pilot"
    return picked


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--raw", default=os.path.join(HERE, "raw"))
    ap.add_argument("--out", default=os.path.join(HERE, "candidates.jsonl"))
    args = ap.parse_args()

    hard_path = os.path.join(args.raw, "simple_qa_test_set.csv")
    easy_path = os.path.join(args.raw, "tqa_val.parquet")
    check_sha(hard_path)
    check_sha(easy_path)

    hard_all, easy_all = load_hard(hard_path), load_easy(easy_path)
    hard = order(hard_all, N_HARD_STUDY, "hard")
    easy = order(easy_all, N_EASY_STUDY, "easy", {normalize(r["truth"]) for r in hard})

    with open(args.out, "w", encoding="utf-8") as fh:
        for r in hard + easy:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"hard: {len(hard_all)} pass the form filters, {len(hard)} kept", file=sys.stderr)
    print(f"easy: {len(easy_all)} pass the form filters, {len(easy)} kept", file=sys.stderr)
    print(f"wrote {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
