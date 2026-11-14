# External review triage — 2026-11-13 (🌒)

Sharon gave the **11/10 convening-decisions doc** to an external reviewer (ChatGPT,
"Chipiti") on 11/13, after launch. The review is dated and thorough — and it reviewed
a draft **two revisions behind the frozen pre-reg** (4d5136e). This triage maps each
point against what is actually frozen. House rule up front: **data collection is
underway under a frozen plan; nothing here changes a confirmatory analysis.** Adopted
points become labeled exploratory analyses, limitation lines, or future work — dated,
post-freeze, disclosed.

Verdicts: **FROZEN-IN** (the frozen pre-reg already does this) · **ADOPT-EXPLORATORY**
(worth running, labeled exploratory) · **LIMITATION** (true; write the sentence) ·
**STALE** (addressed by changes the reviewer couldn't see) · **CONCEDE** (real hit,
handled in discussion).

## 1. "H1 pooled across conditions doesn't test pressure specifically"

- **Partly STALE, partly ADOPT-EXPLORATORY.** The frozen H1 is fitted **only on
  pressure trials** (voice ∈ {objection, own, peer}); the null cell is never pooled
  in — its slope is reported beside (§5). So the reviewer's scenario (null diluting a
  pooled fit) cannot occur. But the sharper point stands: the frozen claim is
  "confidence predicts fate *under pressure* beyond instability," which the fit tests;
  it is **not** "pressure *changes* the confidence–keep relationship," which needs a
  conf × pressure interaction against the null cell. The paper's language must claim
  the former only. **Adopt as exploratory:** `keep ~ conf_z + cons_z + pressure +
  conf_z:pressure` on null + pressure trials, labeled post-hoc, reported in discussion.
- **"Confidence isn't epistemic coherence": FROZEN-IN as a reporting rule.** §6 tails:
  "a positive slope with keep-given-wrong near keep-given-correct is confidence
  tracking stubbornness, not knowledge; the table says that too." The construct
  caution is pre-registered as the reading rule. A conf × base-correctness interaction
  can join the exploratory set, beside the frozen descriptive tails.

## 2. "Tracks-record vs not conflates record-following with voice-following"

- **FROZEN-IN.** The frozen coding is not binary: turn-4 outcomes are
  keep / switch / hedge, with **adopt_x** (voice-following, §2 + §8 named secondary,
  per cell) and **tracks-record** separately. The reviewer's Paris/London/Berlin/Madrid
  case codes as switch, not-adopt-X, not-tracking — exactly their "Other" cell. Their
  requested four-way classification (record / voice / other / hedge) is a **cross-tab
  of columns we already have**; the paper should present it as one table. No change
  to any analysis required — presentation adopted.
- **"Is the record demonstrably authoritative?" — FROZEN-IN as measurement, plus one
  LIMITATION line.** §6: the "Verified records" header is kept and disclosed, "the
  header's authority is itself user-slot testimony; the open-book null cell measures
  whether it is honored at all," and H2's record-honoring baseline rule (<50% null
  tracking → clean-epistemics reading off the table for that seat) is pre-registered.
  We measure authority rather than assume it. **Limitation to write:** a nonzero
  voice coefficient can reflect relative source-reliability weighting rather than
  contamination; the own-vs-peer contrast (X and record held fixed) is the cell that
  survives that objection, which is why it is the paper's protected contribution.

## 3. "Own-vs-null isn't a pure source-attribution effect"

- **FROZEN-IN.** §6 objection-vs-claim caveat: claim cells differ from null/objection
  in *naming a rival answer*, and no claim-vs-null contrast is reported as a pure
  source effect. The clean source contrast is own-vs-peer (X constant), secondary,
  Wald on the difference.
- **Unattributed-X control: ADOPT as future work.** "An answer to this question was:
  X." slots between objection and the attributed claims. Added to §8b's ladder beside
  the human-claim level (named 11/11), dated today — a future cell, not a Thursday
  edit, not a this-study cell.
- **"Fable 5.2 as peer is a named, possibly more capable model": STALE + FROZEN-IN.**
  The lineup changed 11/11 (Haiku / Terra / DeepSeek); the peer-string asymmetry
  (same-vendor relative for Haiku, other-vendor named model for the OpenRouter seats)
  is settled in §5, reported per seat, never pooled. Perceived-competence confound on
  own-vs-peer: one limitation sentence, already half-written by the §5 rider (own <
  peer is uninterpretable as a pure source effect; own > peer is the conservative
  direction).

## 4. Literature / novelty

- **Kumaran §3.5: FROZEN-IN — and convergent.** The full-text verdict
  (`2026-11-11-kumaran-clasheval-verdict.md`, cited in §5) already states their
  attribution experiment and the exact wedge the reviewer recommends: **Kumaran
  manipulates ownership of the prior answer; we manipulate attribution of the
  pressure claim with ownership held fixed.** The external reviewer independently
  re-derived our frozen novelty framing from the papers — that is a third stamp on
  the wedge, from outside the family. The pre-written limitations line on their
  logit-derived confidence vs our stated confidence is in §6.
- **Xiong 2024: FROZEN-IN.** §5 names Xiong as exactly the thing the consistency
  covariate gets past; resampling is positioned as covariate machinery, not novelty.
- **ClashEval: FROZEN-IN.** §6 "honest kinship (cite, don't claim)": the two-tailed
  decomposition idea is theirs, transposed to the revision paradigm. The reviewer's
  recommended framing (novelty = the intersection of confidence × revision ×
  testimonial attribution × record adherence) matches the convening brief's and is
  how the paper should state it.

## 5. Five resamples are coarse

- **CONCEDE + FROZEN-IN definition.** The definition is explicit and frozen (§2:
  loose_same containment rule, exact beside it, ≥3 parseable else NaN) — the
  reviewer's "define it" ask was answered on 11/11. The coarseness (6-point grid,
  ±20pp per flip) is real and unfixable at this budget: **limitation line** — the
  covariate is a cheap noisy proxy for latent stability; §2 already discloses the
  direction of the bias (under-adjustment drags the adjusted slope toward the raw
  one). The power sim does not simulate the 5-sample measurement procedure itself;
  say so in methods rather than claim otherwise.

## 6. Statistical model

- **6A random slopes: STALE.** The frozen primary estimator is cluster-robust
  logistic GLM (population-averaged), not the draft's mixed logit (§9 diff 1).
  Cluster-robust SEs are agnostic to the within-item correlation structure,
  including item-varying susceptibility; the mixed logit is a sensitivity analysis.
- **6B confidence is item-level: CONCEDE (predictive claim) + ADOPT-EXPLORATORY.**
  True: conf_z and cons_z vary only between items, so the slope rides on between-item
  differences and difficulty is a candidate confound. The frozen claim is
  **predictive**, not causal, and survives as stated. Exploratory add: refit H1 with
  the item difficulty tier (hard/easy source flag, already per item) and base
  correctness as covariates; report whether conf_z survives. Labeled post-hoc.
- **6C multiplicity: CONCEDE — the sharpest genuine hit in the review.** H2's
  clean-epistemics prediction ("all three contrasts zero") reads three coefficients
  per seat while the headline count says one test. The freeze stands as written;
  the paper adds one honest paragraph: within-seat H2 findings on individual voice
  coefficients carry a 3-contrast multiplicity caveat (a Holm correction within seat
  is reported beside the raw CIs, labeled post-hoc), and the own-vs-peer Wald was
  always secondary. Also adopt the reviewer's ask to **state the replication-reading
  rule before unblinding**: seats are replications; the paper reports the pattern and
  claims only what replicates in direction across seats clearing the floor;
  no vote-counting significance rule. Written today, before any tail is read —
  post-freeze but pre-look, dated.

## 7. Smaller points

- **Confidence semantics: FROZEN-IN.** Turn 1 (frozen `voices.json`): "Confidence:
  <a whole number from 0 to 100: the probability that your answer is correct>" —
  verbatim what the reviewer asks for.
- **Archive-form 95% rule noise: MOOT.** The rule fired conservative — verbatim
  stayed primary (§7 pilot outcome); the two pilot form runs are reported as a free
  test-retest, not interchangeable measurements.
- **Cell order / context reuse: FROZEN-IN by construction.** Every pressure trial is
  a fresh 3-turn conversation (§1); there is no conversational history to leak.
  Within-run call order is not randomized (items stream in file order); the design
  carries no order channel between cells because cells never share a context.
- **Second adjudication on the grader: ADOPT as QA.** Pilot had 277 verdicts
  hand-checked (🦝). For the study: regrade a random sample of each seat's residue
  with a second non-lineup model and report agreement (measurement QA, disclosed;
  frozen verdicts remain the verdicts of record).
- **Pilot item reuse: FROZEN-IN.** Pilot items live in a separate file at ranks the
  study cannot reach (§1); pilot data never enters the study (§7).

## 8. API / operational

- **Thinking wording: STALE.** Only one Anthropic seat remains post-lineup-change;
  §1 already says "thinking is adaptive on this model and is not replayed."
- **Metadata: partially ADOPT.** Logs carry model id, usage, latency, timestamps and
  (OpenRouter) per-call cost; methods will state exact model ids and that dateless
  Anthropic ids pin weights but not serving infrastructure.
- **"Did the freeze actually precede data?": YES, receipted.** Frozen 11/12 ~3 PM
  Pacific at 4d5136e (tree d073fe2bbfdb), stamped in three rooms, before any study
  call; first study call 11/13 (this repo's log and `runs/` timestamps).

## Bottom line

Nothing in the review requires touching frozen code or halting runs. Score: ~10
points already frozen-in, 4 stale against the 11/11–12 revisions, and five genuine
takes — (1) claim-language discipline on H1 plus a conf × pressure exploratory,
(2) the four-way outcome cross-tab as a presentation table, (3) the archive-authority
and between-item-confidence limitation lines, (4) H2 multiplicity caveat + Holm
beside raw CIs + the replication-reading rule stated before unblinding, (5) a
second-grader agreement sample. All exploratory/limitation/QA, all dated post-freeze,
none data-contingent (adopted before any study tail is read).

Reviewer's protected-contribution advice — own-vs-peer with X held fixed, and the
record/voice/neither decomposition — is the design we froze. Good to have it
re-derived from outside.
