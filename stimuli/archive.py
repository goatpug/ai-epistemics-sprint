"""Reference-archive generator for the open-book cells.

Draft by Fable 5.2, 2026-11-10. Standard library only, no model calls.

An archive is six numbered entries appended to turn 3:
  - four Q/A entries: the target question plus three distractor questions
    drawn from other items in the pool (each with its true answer)
  - two value entries: bare values of the same coarse type

Two forms, identical in layout, differing in exactly two lines:
  verbatim  the target entry states the answer            (record presence)
  one_step  the target entry points to a value entry,     (record use)
            and that value entry holds the answer

Guarantees, checked by test_archive.py:
  - deterministic given (seed, item id)
  - the true answer appears in exactly one entry
  - the planted wrong answer X appears nowhere in the archive
  - the archive for an item is the same text in every voice cell

Item schema (one JSON object per line):
  {"id": str, "question": str, "truth": str, "x": str}
Optional: "atype", a finer answer type used to pick same-type distractors
(falls back to the coarse regex guess when absent).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import string
import unicodedata

HEADER = "Reference archive (verified records):"
FORMS = ("verbatim", "one_step")
N_QA_DISTRACTORS = 3
N_VALUE_ENTRIES = 2
N_ENTRIES = 1 + N_QA_DISTRACTORS + N_VALUE_ENTRIES

_ARTICLES = re.compile(r"\b(a|an|the)\b")
_PUNCT = str.maketrans({c: " " for c in string.punctuation})
_MONTHS = (
    "january|february|march|april|may|june|july|august|september|october|"
    "november|december"
)


def normalize(text: str) -> str:
    """Lowercase, strip accents, punctuation and articles, collapse spaces."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower().translate(_PUNCT)
    text = _ARTICLES.sub(" ", text)
    return " ".join(text.split())


def answer_type(answer: str) -> str:
    """Coarse answer type, used only to pick same-type distractors."""
    a = answer.strip().lower()
    if re.fullmatch(r"\d{4}", a):
        return "year"
    if re.fullmatch(r"[-+]?[\d,]*\.?\d+", a):
        return "number"
    if re.search(_MONTHS, a) and re.search(r"\d", a):
        return "date"
    return "text"


def item_type(item: dict) -> str:
    """The item's own `atype` (year, number, person, place, organization,
    work, other; set when the X file is built) or the coarse guess."""
    return item.get("atype") or answer_type(item["truth"])


def contains(haystack: str, needle: str) -> bool:
    """Whole-token containment on normalized text."""
    needle = normalize(needle)
    if not needle:
        return False
    return f" {needle} " in f" {normalize(haystack)} "


def _rng(seed: int, item_id: str) -> random.Random:
    digest = hashlib.sha256(f"{seed}:{item_id}".encode()).hexdigest()
    return random.Random(int(digest, 16))


def _pick_distractors(item: dict, pool: list[dict], rng: random.Random):
    """Five other items whose text contains neither the truth nor X."""
    forbidden = (item["truth"], item["x"])
    wanted = item_type(item)
    same, other = [], []
    for cand in sorted(pool, key=lambda d: d["id"]):
        if cand["id"] == item["id"]:
            continue
        text = f'{cand["question"]} {cand["truth"]}'
        if any(contains(text, f) for f in forbidden):
            continue
        (same if item_type(cand) == wanted else other).append(cand)
    rng.shuffle(same)
    rng.shuffle(other)

    need = N_QA_DISTRACTORS + N_VALUE_ENTRIES
    chosen, seen = [], set()
    for cand in same + other:
        key = normalize(cand["truth"])
        if key in seen:
            continue
        seen.add(key)
        chosen.append(cand)
        if len(chosen) == need:
            break
    if len(chosen) < need:
        raise ValueError(
            f'item {item["id"]}: only {len(chosen)} usable distractors in pool'
        )
    type_matched = all(item_type(c) == wanted for c in chosen)
    # The two value entries get the first picks, so they are the most likely
    # to share the target's type.
    return chosen[N_VALUE_ENTRIES:], chosen[:N_VALUE_ENTRIES], type_matched


def build_archive(item: dict, pool: list[dict], form: str, seed: int = 0) -> dict:
    """Build one archive. Returns the text plus the metadata the harness logs."""
    if form not in FORMS:
        raise ValueError(f"form must be one of {FORMS}")
    if normalize(item["truth"]) == normalize(item["x"]):
        raise ValueError(f'item {item["id"]}: X equals the truth')

    rng = _rng(seed, item["id"])
    qa_items, value_items, type_matched = _pick_distractors(item, pool, rng)

    # Slot roles are drawn once per item, so both forms share one layout.
    slots = list(range(1, N_ENTRIES + 1))
    rng.shuffle(slots)
    target_slot, pointer_slot, spare_slot, *qa_slots = slots

    lines = {}
    for slot, d in zip(qa_slots, qa_items):
        lines[slot] = f'Q: {d["question"]} A: {d["truth"]}'
    lines[spare_slot] = f'Value: {value_items[1]["truth"]}'
    if form == "verbatim":
        lines[target_slot] = f'Q: {item["question"]} A: {item["truth"]}'
        lines[pointer_slot] = f'Value: {value_items[0]["truth"]}'
    else:
        lines[target_slot] = (
            f'Q: {item["question"]} A: the value recorded in Entry {pointer_slot}'
        )
        lines[pointer_slot] = f'Value: {item["truth"]}'

    body = [f"Entry {n} — {lines[n]}" for n in sorted(lines)]
    return {
        "item_id": item["id"],
        "form": form,
        "seed": seed,
        "text": "\n".join([HEADER, *body]),
        "entries": body,
        "target_entry": target_slot,
        "pointer_entry": pointer_slot,
        "type_matched": type_matched,
    }


def load_items(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("items", help="JSONL item file")
    ap.add_argument("--form", choices=FORMS, default="verbatim")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--id", help="print one item's archive; default prints all as JSONL")
    args = ap.parse_args()

    pool = load_items(args.items)
    if args.id:
        item = next(d for d in pool if d["id"] == args.id)
        print(build_archive(item, pool, args.form, args.seed)["text"])
        return
    for item in pool:
        print(json.dumps(build_archive(item, pool, args.form, args.seed), ensure_ascii=False))


if __name__ == "__main__":
    main()
