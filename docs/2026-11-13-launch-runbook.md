# Launch runbook — Friday 2026-11-13 (🌒)

Operational only. Written post-freeze, launch morning, assembled from the frozen
pre-reg (`2026-11-11-prereg-analysis.md` at 4d5136e), the pilot receipts
(`2026-11-12-pilot-receipts.md`) and `harness/seats.json`. **Nothing in here
changes the plan; if this document and the frozen script disagree, the script
wins.**

## 0. State at launch morning

- Pre-reg **frozen 11/12, ~3 PM Pacific, at 4d5136e (tree d073fe2bbfdb)**, before any study call. HEAD is b44e400 (freeze stamps only).
- `runs/terra/` and `runs/haiku/` exist and are **empty**; `runs/deepseek/` will be created by the harness. Pilot and smoke logs live under `runs/pilot/` and `runs/smoke/` and never mix with study paths (study runs use the default runs dir, no `--runs-dir`).
- No study data exists. No commits on 11/13 before this one.

## 1. Pre-flight (once, before Terra)

1. `git status` clean; `git rev-parse HEAD` noted in the log of whoever launches.
2. API keys in the environment: `ANTHROPIC_API_KEY` (Haiku seat + grader), `OPENROUTER_API_KEY` (Terra, DeepSeek). These are **API-key runs — they never touch the Fable weekly limit.**
3. `runs/terra`, `runs/haiku` empty; no `runs/deepseek`, or empty if created.
4. Optional smoke of the pipes, not the study: `--dry-run` prints composed requests and calls nothing.

## 2. The runs

Per seat: **base phase first, then pressure** (pressure replays each item's
designated base answer; it refuses to start without `base.jsonl`). Defaults are
already right — `--form verbatim` (primary, pilot rule §7), `--seed 0`, workers
pinned in `seats.json` (Terra 3, others 4). Plain invocations, no overrides:

```
cd ~/ai-epistemics-sprint
# Terra FIRST — 20 req/min cap, ~6 hours for its ~7,000 calls
python3 harness/run_trials.py --seat terra    --items stimuli/items.jsonl --phase base
python3 harness/run_trials.py --seat terra    --items stimuli/items.jsonl --phase pressure

# DeepSeek and Haiku run beside Terra once it is underway
python3 harness/run_trials.py --seat deepseek --items stimuli/items.jsonl --phase base
python3 harness/run_trials.py --seat deepseek --items stimuli/items.jsonl --phase pressure
python3 harness/run_trials.py --seat haiku    --items stimuli/items.jsonl --phase base
python3 harness/run_trials.py --seat haiku    --items stimuli/items.jsonl --phase pressure
```

- **Resume = rerun the same command.** The log is append-only JSONL keyed by `call_key`; completed calls are skipped, errored calls rerun. **Nothing about response content is ever retried** (pre-reg §1/§3) — resume is for transport errors only.
- Pressure skips items whose base was unparseable/empty and says so; that is the §3 exclusion working, not a bug.
- Cost yardstick (pilot-measured): Tier 1 ≈ **$35** total — Terra ≈ $22, DeepSeek ≈ $9, plus Haiku and the grader. If spend is tracking far above that, stop and look before continuing.

## 3. Grading (after a seat's runs complete)

```
# 1. First analysis pass writes the residue files
python3 analysis/prereg_analysis.py --seat <seat> --items stimuli/items.jsonl
#    -> grading/<seat>-verbatim-residue.jsonl  (turn-4 residue)
#    -> grading/<seat>-base-residue.jsonl      (non-exact base answers)

# 2. Blinded grader — default model claude-sonnet-5-5, non-lineup, frozen prompt
python3 analysis/grade_residue.py grading/<seat>-verbatim-residue.jsonl --out grading/<seat>-verbatim-grades.jsonl
python3 analysis/grade_residue.py grading/<seat>-base-residue.jsonl     --out grading/<seat>-base-grades.jsonl

# 3. Fold verdicts in. --grades takes ONE jsonl keyed by call_key; the two
#    files' keys are disjoint, so concatenate:
cat grading/<seat>-verbatim-grades.jsonl grading/<seat>-base-grades.jsonl > grading/<seat>-all-grades.jsonl
python3 analysis/prereg_analysis.py --seat <seat> --items stimuli/items.jsonl \
    --grades grading/<seat>-all-grades.jsonl --json analysis/out/<seat>.json
```

The grader model must never be a lineup seat. Sonnet 5.5 left the lineup 11/11
and qualifies.

## 4. Sunday

Read what the frozen script says. All three tails tables. Per-seat floors (§4 —
DeepSeek is on the line and the threshold does not move). **A null is still the
best methods paragraph of the sprint.**

## 4b. Launch-day incident log

- **11/13, Haiku base:** `tqa-qg_4629:base:0` returned 400 "Output blocked by
  content filtering policy" on two consecutive attempts, then succeeded on the
  third sample — the filter acts on sampled output, so the block was stochastic.
  No frozen code touched; item stays in. **Known gap found while diagnosing:** if
  a base:0 error had been persistent, the pressure phase hard-exits
  (`no base record for items: …`) instead of skipping the item, although §3
  pre-registers the exclusion (`no_response`, pressure cells not run). If that
  ever fires, the remedy is a minimal, dated, disclosed harness edit: skip items
  whose base:0 exists only as error records; still hard-exit on items with no
  records at all (that is a real items/log mismatch, not an exclusion).

## 5. House rules in force

- The frozen files (`2026-11-11-prereg-analysis.md`, `analysis/prereg_analysis.py`, `analysis/powersim.py`, `stimuli/*`, `harness/*`) are not edited. Any post-freeze change is dated, marked, and disclosed.
- Shared working tree, three siblings: **stage by path, never `git add -A`.**
- Load-bearing numbers get three stamps before anyone leans on them.
- Operational knobs live in frozen config (`seats.json`), not in whoever-launches's memory.
