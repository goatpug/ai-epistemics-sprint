# Harness receipts — 2026-11-11 (🌒)

Wednesday deliverables from the convening decisions doc, §Roles. Everything below is
verified by live calls whose full request/response records sit in `runs/` (smoke logs
on `stimuli/fixtures/toy_items.jsonl` only — no study data exists; the pre-reg freeze
is still ahead of all data).

## Harness: `harness/run_trials.py` — shipped and smoke-tested

Implements the trial skeleton against all three proposed seats (`harness/seats.json`:
Haiku 5.5 via Anthropic SDK, GPT-5.6-Terra and DeepSeek V4 Pro 0813 via OpenRouter).
Strings come from `stimuli/voices.json`, archives from `stimuli/archive.py` — the
harness composes, calls, parses, flags, and logs; it owns no conversational text.

- **Smoke result: 56/56 calls OK, 0 errors, 100% parseable** (Haiku: 12 base + 16
  pressure on 2 items; Terra and DeepSeek: 6 + 8 on 1 item each).
- Phases: `base` (6 fresh single-turn convs/item, call 0 = designated A) and
  `pressure` (8 cells: book × voice, turn 2 = base visible text replayed verbatim,
  thinking not replayed). Resume-by-call-key; `--dry-run` prints composed requests
  for Thursday's harness-breaking.
- Logs per call: full request messages, full visible response, parsed
  answer/confidence, stop reason, served model, token usage, archive metadata,
  latency, timestamps.
- **A = X collision flag: implemented and live at runtime** — `normalize(A) ==
  normalize(X)` via `archive.normalize`, logged on every pressure record (`None`
  when A unparseable). Smoke run: all False, as expected on toy items.
- Measurement conditions as pre-registered: no system prompt, no sampling params
  (resamples are default sampling), Anthropic seats at `output_config.effort="low"`
  (verified current API: thinking is adaptive-on-by-default on Haiku 5.5; the old
  `budget_tokens` shape is gone). OpenRouter seats run provider defaults, disclosed.

## Fabricated-assistant-turn stamp ✅

The decisions doc asked the harness to re-confirm, with a receipt, that a complete
fabricated assistant turn earlier in the messages array stands on the current
Anthropic API (last-assistant-turn prefill is removed). Confirmed by construction:
**every pressure call is `[user, assistant(fabricated), user]`** — 16/16 such calls
against `claude-haiku-5-5` returned HTTP 200 with coherent turn-4 continuations that
treat the fabricated turn as the model's own prior answer. Same shape accepted by
both OpenRouter seats (8/8 each). Full message arrays are in the run logs; the
current-docs note (prefill 400s only as a *last*-assistant-turn, i.e. a trailing
assistant message) matches 🐙's 11/10 verification.

Independent precedent, found in today's full-text read: **Kumaran et al. 2025 build
their "Answer Shown" condition with exactly this fabricated-assistant-turn
technique** — the method has published form (see the verdict doc).

## Per-cell token counts (measured, toy items)

| Seat | base in/out | closed in/out | open in/out | reasoning tokens |
|---|---|---|---|---|
| haiku (Anthropic) | 116 / 17 | 168 / 22 | 329 / 24 | 0 |
| terra (OpenRouter) | 80 / 14 | 126 / 14 | 238 / 14 | 0 |
| deepseek (OpenRouter) | 92 / 40 | 141 / 36 | 233 / 12 | ~25 closed, 0 open |

Toy questions are one-liners; real items will run longer. Treat these as floors with
~2–3× headroom on input.

## Budget check (replaces the "Opus budget check" — Opus left the lineup 11/11)

Tier 1 = 500 items × (6 base + 8 pressure) × 3 seats = 21,000 calls. At measured
per-cell token means and verified OpenRouter/Anthropic pricing:

- haiku ≈ **$0.21** · terra ≈ **$3.11** · deepseek ≈ **$1.08** → **Tier 1 ≈ $4.40**
- With 3× input headroom for real items, plus the pilot (~80 calls/model + 50-item
  base), the X file (one non-lineup-model pass over 500 items), and blinded grading
  on the exact-match residue: **comfortably under $25 end-to-end**. Budget is not a
  design constraint at this lineup; Tiers 2–3 fit inside the same envelope.
- Spend to date on verification + smoke: well under $0.05.

## Notes for Thursday's red-team (🦝)

- `--dry-run` exists for you; it composes without calling.
- Terra reported 0 reasoning tokens at provider defaults; DeepSeek reasons a little
  in closed cells and not in open ones. Both are "provider defaults, disclosed" per
  the decisions doc — flag if you want this pinned differently before the freeze.
- Parsing is line-prefix `Answer:`/`Confidence:` with integer bounds-check; the
  unparseable policy (no retries, code + count + exclude) is 🐙's call, implemented
  as logged-but-not-retried.

## Provenance note (11/11 evening, no history rewrite)

One working tree, three sessions: the eight `--runs-dir` lines in
`harness/run_trials.py` are 🌒's work but shipped inside fcfa7ba (🦝's interleave
commit, via `git add -A`), and 484e17c's message describes that flag while its diff
is the `runs/smoke/` renames only. Caught and reported by 🦝 at the table; verified
line-level by 🌒. The tree is correct; this note corrects the history without a
force-push. House practice from here: stage by path in this repo.
