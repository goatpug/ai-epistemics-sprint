# Decorative or Load-Bearing? Stated Confidence Under Attributed Pressure

Apart Research × Epistemics sprint (Nov 13–15, 2026), Track 1. We measure
**confidence–behavior coherence** — whether a model's verbalized confidence
predicts the fate of its own answer under pressure, beyond what plain answer
instability predicts (H1) — and **record-vs-testimony arbitration** — whether
attributing a false claim to the model's own earlier instance or to a named
peer moves it off a checkable in-context record (H2). Three seats
(Claude Haiku 5.5, GPT-5.6 Terra, DeepSeek V4 Pro 0813), 500 items, 14 calls
per item per seat, pre-registered and frozen before any study call.

## Preexisting work disclosure (sprint rule)

The sprint window opened **Nov 13**. Work that predates it, labeled pre-sprint
here and in the report:

- **Pre-sprint (Nov 10–12):** design convening and decisions (`docs/2026-11-10-*`),
  harness (`harness/`), stimuli pipeline and item files (`stimuli/`),
  pre-registration and power simulation (`docs/2026-11-11-prereg-analysis.md`,
  `analysis/prereg_analysis.py`, `analysis/powersim.py`, `analysis/grade_residue.py`),
  pilot runs and receipts (`runs/pilot/`, `docs/2026-11-12-pilot-receipts.md`).
  Frozen at commit `4d5136e` (11/12, before any study call).
- **Sprint work (Nov 13–15):** all study runs (`runs/haiku|terra|deepseek/`),
  blinded grading (`grading/`), analysis outputs (`analysis/out/`), the
  external-review triage (`docs/2026-11-13-*`), post-freeze exploratory and QA
  code (`analysis/exploratory_postfreeze.py`, `analysis/second_grader.py`),
  and the report (`paper/`).

## Repository map

| Path | What |
|---|---|
| `docs/` | Dated design, pre-registration, receipts, reviews — the sprint's paper trail |
| `harness/` | Trial runner (`run_trials.py`), seat registry, parser unit tests |
| `stimuli/` | Items, planted-X files, voice strings, archive generator |
| `runs/` | Raw call logs per seat (base + pressure), pilot and smoke included |
| `grading/` | Blinded-grader residue and verdicts; `second/` = second-grader QA |
| `analysis/` | `prereg_analysis.py` (frozen: the plan), exploratory + QA scripts, outputs |
| `paper/` | Report draft |

## Reproduce

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
# keys in .env: ANTHROPIC_API_KEY, OPENROUTER_API_KEY
.venv/bin/python harness/run_trials.py --seat haiku --phase base --items stimuli/items.jsonl
.venv/bin/python harness/run_trials.py --seat haiku --phase pressure --form verbatim --items stimuli/items.jsonl
.venv/bin/python analysis/prereg_analysis.py --seat haiku --items stimuli/items.jsonl   # writes grading residue
.venv/bin/python analysis/grade_residue.py grading/haiku-verbatim-residue.jsonl --out grading/haiku-verbatim-grades.jsonl
.venv/bin/python analysis/prereg_analysis.py --seat haiku --items stimuli/items.jsonl \
    --grades grading/haiku-all-grades.jsonl --json analysis/out/haiku.json             # verdicts of record
.venv/bin/python analysis/exploratory_postfreeze.py --seat haiku --items stimuli/items.jsonl \
    --grades grading/haiku-all-grades.jsonl                                            # post-hoc, labeled
```

The frozen script is the analysis plan: anything the report states that
`prereg_analysis.py` does not compute is exploratory by definition and labeled so.

## Roles

Designed, implemented, analyzed and written by three Claude Fable instances
(Fable 5, 5.1, 5.2) deliberating through a human-operated relay; the human
operator (Sharon K.) is courier, budget authority and review commissioner.
Fable models hold no measurement role: seats, X-file verification and both
graders are non-Fable models, and an external non-Anthropic review of the
design was commissioned mid-sprint (`docs/2026-11-13-external-review-*`).
