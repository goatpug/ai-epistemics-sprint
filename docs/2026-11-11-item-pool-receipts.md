# Item pool and X file — receipts, 2026-11-11 (🦝)

My Wednesday deliverables from the convening decisions doc: the item pool, the X file, the pilot items. Everything here is stimulus construction. No seat has seen a question, and no study data exists.

## What landed

| File | Rows | What it is |
|---|---|---|
| `stimuli/candidates.jsonl` | 860 | Ordered candidates: 530 hard, 330 easy. No model was involved |
| `stimuli/x_file.jsonl` | 860 | One wrong answer and one answer type per candidate, with every rejected proposal logged |
| `stimuli/items.jsonl` | 500 | Study items at a **provisional** hard share of 0.6 (300 hard, 200 easy) |
| `stimuli/pilot_items.jsonl` | 50 | Pilot items, 25 hard and 25 easy |

Scripts: `build_pool.py`, `make_x.py`, `compose_items.py`, all in `stimuli/`. Raw downloads go in `stimuli/raw/` (gitignored); URLs and pinned SHA-256 hashes are in the `build_pool.py` docstring, and the script refuses to run on a file that doesn't match.

## Sources

- **Hard: SimpleQA** (OpenAI simple-evals test set, MIT, 4,326 questions).
- **Easy: TriviaQA** (rc.nocontext validation split, Apache-2.0, 9,960 unique questions).

Both were picked for difficulty alone. What accuracy each seat gets on each source is unknown until the pilot, and the 0.6 share is a placeholder, not an estimate.

## Form filters (no correctness screening)

An item passes on its shape only: answer of at most four words and 40 characters; no lists, ranges, yes/no answers or tolerance bands ("plus or minus one minute"); question between 25 and 300 characters ending in a question mark; no time-sensitive wording ("current", "latest", "as of"); the answer not already in the question. Numbers must be plain numerals. **Full dates are out and year-only dates are in**, because "29 July 1931" against "July 29, 1931" fails exact match and would push a whole answer type onto the grader.

2,770 SimpleQA and 7,528 TriviaQA questions pass. Each source is shuffled once with a fixed seed, and one item is kept per distinct answer across both sources.

## The order is the design

Hard ranks 0–499 and easy ranks 0–299 are study candidates. The 30 ranks after each are the pilot reserve, and the pilot uses the first 25 usable ones. `compose_items.py --hard-share h` takes the first `500h` usable hard items and the first `500(1−h)` usable easy items. Changing `h` after the pilot reshuffles nothing, and a pilot item can't become a study item at any share.

"Usable" drops nine hard candidates whose truth or X collides with the archive's own scaffolding. An answer of "4" sitting beside "Entry 4" breaks both archive guarantees, and I only found that because the composer asserts them for all 500 items in both forms. So the hard share can go as high as 0.98 and as low as 0.4.

## X file

Generator and verifier: `claude-sonnet-5-5`, effort low, which left the lineup 11/11 (🐙's tip, same qualification as the grader). `make_x.py` refuses to run with a model that is in `harness/seats.json`.

Per item: the model sees the question and the truth and proposes one wrong answer of the same kind and format. The script checks type, inequality with the truth and with TriviaQA's aliases, containment either way, absence from the question, and number shape. Then a fresh conversation with the same model is asked only whether the proposal is the same thing as the reference or also correct.

- 860 of 860 items have an X. 837 on the first proposal, 23 needed two to four.
- Rejections: 19 unparseable, 4 by the verifier (3 "also correct", 1 "same"), 6 by script checks.
- The unparseable ones were mostly the generator catching itself: it proposes, writes "Wait, that is a broader version of silk factory," and proposes again. The parser now takes the last JSON object.
- 36 study items have an X that is another item's truth (years, mostly). The archive generator already refuses any distractor containing the target's X, so this never reaches a prompt.

## Answer types (trial spec open question 4, closed)

Each item has an `atype`: year or number by regex, otherwise the generator's label from person, place, organization, work, other. `archive.py` matches distractors on it and falls back to the old coarse guess when the field is absent, so the toy fixtures and its 12 tests are unchanged. All 500 study archives are fully type-matched. In the 50-item pilot file, 13 archives have at least one distractor of another type because the pool is small.

## Checks run

- `compose_items.py` builds both archive forms for every study and pilot item and asserts: X nowhere in the archive, truth in exactly one entry.
- `test_archive.py`: 12 of 12 pass after the `atype` change.
- `run_trials.py --dry-run` composes base calls from `pilot_items.jsonl` for all three seats.

## For Thursday's table

1. **Hard-share rule, proposed, to be agreed before the pilot runs:** take each seat's base accuracy on the 25 hard and 25 easy pilot items, and pick the share in steps of 0.1 that puts the middle seat's expected accuracy closest to 50%. If 🐙's ceiling response fires (pilot keep ≥ 0.85), move one step harder. Twenty-five items per source is a coarse estimate, about ±10 points, and the rule should say so.
2. **Two files, not one.** The harness uses the whole items file as the distractor pool, so study and pilot live apart. The trial spec is updated.
3. **TriviaQA truths are messy** ("The Oasis", "South Caucasus" for the range Tbilisi sits in). Items carry TriviaQA's `aliases`, which are Wikipedia redirects and noisy. X is checked against them. Whether the exact-match stage should accept them is 🐙's call; nothing uses them now.
4. **The verifier is the generator's own model.** A second opinion from a different non-lineup model would be stronger. I think it's fine for a wrong-answer file, and it should be disclosed.
5. **Pilot archives are less type-matched than study archives** (13 of 50). The pilot decides the record-form rule, and a mismatched value entry makes one-step easier to shortcut. Small, in the conservative direction for that rule, and disclosed.
6. **A one-step archive has two value entries, so the pointer can be guessed at 50%** even with perfect type matching. That was always true of the design; type matching removed the cases where it was 100%.
7. **`grade_residue.py` sends `max_tokens=200`.** If adaptive thinking draws on the same budget, a verdict could be cut off. I didn't test it. `make_x.py` uses 2,000 for the same model and had no truncations.
