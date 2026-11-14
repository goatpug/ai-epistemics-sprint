# Decorative or Load-Bearing? Stated Confidence and the Fate of Answers Under Attributed Pressure

**Draft 2026-11-14 (🌒). Working copy for the official template (Google Doc). Every
`[SUNDAY: …]` is a number or verdict that lands when the three tails are read
together against the frozen script; nothing in a placeholder is predicted here.
8-page ceiling excluding references and appendices; current target ~7.**

**Team:** Sharon K. [affiliation/location per form]. Study design, implementation,
analysis and writing by three Claude Fable instances (Fable 5, Fable 5.1,
Fable 5.2) working through a human-operated relay; roles disclosed in the
methods and in the repository. [CONFIRM with Sharon: team name; whether to ask
sprints@apartresearch.com about listing.]

---

## Abstract (150–250 words; finalize Sunday)

When a language model says it is 95% confident, does that number predict
anything about the model's own behavior — or is it vocabulary? We measure
confidence–behavior coherence: whether verbalized confidence predicts the fate
of the model's own answer under pressure, beyond what plain answer instability
already predicts. Three seats (Claude Haiku 5.5, GPT-5.6 Terra, DeepSeek V4 Pro)
each answered 500 short-answer factual questions with stated confidence, then
faced eight pressure conditions per item: a bare objection, or the planted wrong
answer X attributed to the model's own earlier instance or to a named peer model —
crossed with the presence of a checkable ground-truth record in context. The
analysis was pre-registered and frozen (commit-pinned) before any study call;
outcomes were coded keep/switch/hedge with blinded grading of all judgment
calls; the confidence slope is adjusted for resample consistency, the wedge past
calibration-style prior work. Unlike logit-based designs, the instrument runs on
closed models. [SUNDAY: two-sentence results — H1 slope verdicts per seat with
the DeepSeek floor reported; H2 contamination verdicts; the most study-shaped
tail numbers.] [SUNDAY: one-sentence implication matched to what actually
happened.] One seat's confidence distribution collapsed below our pre-registered
floor (IQR < 10), making the coherence question unanswerable for that seat —
itself a finding about decorative confidence reporting.

---

## 1. Introduction

A verbalized confidence number is cheap to elicit and ubiquitous in deployed
systems. Its *calibration* — does 90% mean right nine times in ten? — is well
studied. This project measures something less studied and arguably more
operational: **coherence** between the stated number and the model's own
subsequent behavior. If a model's 95%-confidence answers survive challenge no
better than its 60% ones, the number is decorative whatever its calibration,
and any pipeline that routes on it (escalation thresholds, abstention rules,
agent hand-offs) is routing on noise.

We ask two pre-registered questions, per model ("seat"), in a revision paradigm:

**H1 (coherence).** Under pressure to revise, does stated confidence predict
whether the model keeps its answer, *beyond what plain answer instability
predicts*? The instability covariate (resample consistency) is the design's
wedge: confidence could "predict" keeping merely by proxying for how stable the
answer was in the first place. The headline slope is adjusted for it.

**H2 (record vs. testimony).** When a checkable ground-truth record sits in
context, does the attribution of a false competing claim — to no one, to the
model's own earlier instance, or to a named peer model, with the claim text held
identical — move the model off the record? A model with clean epistemics
re-measures; all three contrasts are zero.

The pressure design separates *what is claimed* from *who claims it*. The
planted wrong answer X appears verbatim in three voices; the bare objection
("I don't think that's right — please reconsider") controls for challenge
strength without naming a rival. Crossing voice with the record's presence
(closed vs. open book) separates capitulation from source-weighted updating.

Track fit: this is the track's guiding question — "does the model understand how
solid its claims are?" — measured as the gap between what a model states and
what it will defend, with the pressure provenance (planted X, attributed voice)
controlled item by item.

## 2. Related work

**Kumaran et al. 2025** (arXiv 2507.03120) is the nearest neighbor. In a
two-turn forced-choice paradigm with a fabricated assistant turn (the same
replay technique our harness uses — published precedent), they show
choice-supportive bias: visibility of the model's own prior answer suppresses
change-of-mind, and attributing the *prior answer* to another LLM abolishes the
effect. Three differences matter. Their confidence is logit-derived with
temperature scaling — o1-preview was dropped from confidence analyses *because*
logits were unavailable; our instrument is the stated number itself and runs on
any closed API. Their attribution axis is ownership of the prior *answer*; ours
is attribution of the pressure *claim*, with answer ownership held fixed and
claim text identical across arms (their self/other wordings differ, adding a
competence confound). Their forced choice makes hedging structurally impossible;
our three-way keep/switch/hedge coding treats refusal-to-commit as an outcome,
not noise. Their stated future work — "more naturalistic user-LLM interactions
where free form answers are involved" — describes this design.

**ClashEval** (Wu, Wu & Zou, NeurIPS 2024) shows models override their own
correct priors for perturbed retrieved documents in proportion to logprob
confidence. Their conflict is prior-vs-document, single-shot, with no social
source and no revision structure: the model never sees its own prior answer.
Our two-tailed reporting (keep-rate given the base answer was right vs. wrong)
is the revision-paradigm analogue of their Accuracy/Prior-Bias/Context-Bias
decomposition — the conditioning idea is theirs, transposed; we cite rather
than claim it.

**Xiong et al. 2024** established that verbalized confidence is poorly
calibrated but elicitable. Calibration is not coherence: our consistency
covariate is exactly what separates "confidence predicts keeping" from
"confidence proxies for stability," a distinction calibration studies do not
touch. **FlipRate / FlipFlop-style benchmarks** measure capitulation under
escalating scripted rebuttals; a NeurIPS 2026 critique shows such benchmarks
measure the challenge template unless wording and target-naming are controlled.
Our design answers that: one fixed objection string, one fixed claim sentence
with only the attribution varied, and the planted X's provenance known for
every item. **SycEval / MASK** measure sycophantic agreement and honesty under
pressure respectively; neither conditions on the model's own stated confidence
or supplies an in-context record to arbitrate against.

Nobody, to our knowledge, pits an in-context ground-truth record against a
false *social* claim whose attribution is the manipulated variable — nor tests
whether *stated* confidence predicts the fate of a *stated* answer under that
pressure. An external reviewer (GPT-5.x, reviewing our design documents
mid-sprint without access to this positioning) independently re-derived the
same novelty wedge — own-vs-peer with X held fixed, record/voice/neither
decomposition — which we take as convergence on the framing, though nothing
about it was measured.

## 3. Methodology

Full detail in the pre-registration (`docs/2026-11-11-prereg-analysis.md`,
frozen with `analysis/prereg_analysis.py` at commit `4d5136e` on 11/12, before
any study call; the script is the plan, and anything the report states that the
script does not compute is exploratory by definition and labeled so).

**Items.** 500 short-answer facts with ground truth and a planted wrong answer
X: 350 hard (SimpleQA) + 150 easy (TriviaQA), the mix set by a pre-registered
pilot rule targeting ~50% accuracy for the median seat. X values were proposed
and verified by a non-lineup model with scripted checks (type, truth-inequality,
non-containment). TriviaQA aliases are never used in analysis (noisy redirects);
off-canonical truths reach the blinded grader instead.

**Seats.** `claude-haiku-5-5` (Anthropic, direct), `openai/gpt-5.6-terra` and
`deepseek/deepseek-v4-pro-0813` (OpenRouter, provider defaults, dated snapshot
over mutating alias where available). Fable models were recused from seats,
grading and verification roles: the designers do not sit in their own study.
All hypothesis tests are within-seat; seats are replications, and cross-seat
differences are descriptive.

**Trials.** Per item and seat: six single-turn base calls in fresh conversations
(call 0 is the designated answer A with stated confidence; calls 1–5 are
resamples for the consistency covariate), then eight pressure conversations,
each a fresh three-turn context `[question; assistant turn = A's visible text
replayed verbatim; pressure turn]` — book {closed, open} × voice {null,
objection, own, peer}. The own/peer claim sentence is identical text; only the
attributed source differs. Open-book trials prepend a six-entry "Verified
records" archive containing the truth exactly once and X nowhere; the header's
authority is itself user-slot testimony, which is why H2's first reported number
is the unpressured (null-voice) record-tracking rate. Every pressure trial is a
fresh conversation: no order channel exists between cells.

**Coding.** A turn-4 answer parses to keep / switch / hedge by normalized exact
match; everything else — format breaks, in-turn self-corrections, sentence-shaped
hedges — goes to a blinded grader (a non-lineup model, shuffled, blind to seat,
cell, voice and X), which codes hedge / same-as-A / correct from the free text.
Unparseable turn-4 responses are graded, not dropped: refusal-to-commit is
usually a hedge, and dropping it would inflate keep-rates selectively. A
response naming a single best guess commits to it, however hedged. `adopt_x`
(the planted X adopted outright) is a named secondary, per cell; the grader
never sees X, so its verdict can only remove adopt-X candidates, never add one.
Format-break and in-turn-self-correction rates are themselves reported per cell:
if a pressure voice breaks the format, that is phenomenon, not noise. Grader QA:
a seeded random sample of each seat's graded residue (150 rows/seat) was
regraded by a second, different-vendor, non-lineup grader
([SUNDAY: agreement/kappa from `analysis/second_grader.py --report`]); the
grader of record's verdicts stand regardless.

**Exclusions** (each counted and reported): base-call failures and base
abstentions exclude the item for that seat; fewer than three parseable resamples
excludes from the adjusted fit only; A = X collisions are excluded from primary
contrasts and reported as the consistent-advice cell. No item is removed
post-hoc for being "bad."

**Floor.** Pre-registered: if a seat's base-confidence IQR is below 10 points,
H1 is unanswerable for that seat — the slope is printed, not interpreted. The
pilot put DeepSeek at exactly 10.0, and the threshold was deliberately not
moved; the study verdict is in §4.

**Estimator.** Logistic GLM with item-cluster-robust SEs (population-averaged —
the estimator the power simulation simulated). H1 (closed book, pressure
voices): `keep ~ conf_z + cons_z + voice`; the adjusted confidence slope is the
headline, the raw slope reported beside it is a different (inflated) quantity,
and the null-cell slope is reported beside, never pooled. H2 (open book):
`tracks ~ voice`, null reference, with a separation guard: per-cell Wilson
intervals and Fisher exact tests are always reported, and if any cell sits at
0% or 100% they are the H2 result. Power at the pilot's keep-rates: ≥80% for an
adjusted slope of ≈0.25 logits/SD of confidence.

**Blinding and sequence.** Freeze 11/12 (commit-stamped, verified independently
from three sessions) → data 11/13 (21,000 calls, ~$40 in API spend, zero
designer-model tokens) → blind grading → this write-up drafted → all three
seats' hypothesis tails read together once, against the frozen script, 11/15.
A mid-sprint external review (GPT-5.x) of a stale draft of the design was
triaged against the frozen pre-reg on 11/13: nothing touched a frozen analysis;
the adopted suggestions became the labeled-exploratory set in §5 and limitation
lines here, with the timing stated honestly in the triage document (adopted
after two seats' pipeline outputs existed on disk, not informed by them, and
mechanical either way).

**Roles and tooling disclosure.** The study was designed, pre-registered,
implemented, run, analyzed and written by three instances of Claude Fable
(versions 5, 5.1, 5.2) deliberating through a human-operated relay, with the
human operator as courier, budget authority and review commissioner. Fable
models hold no role on the measurement side (seats, X-file, grading,
verification: all non-Fable). Cross-checking was structural: every load-bearing
claim was verified by a seat other than its author before use ("three stamps"),
and the sprint's error ledger — including the authors' own — is in the
repository's dated documents. One methods-level observation belongs here rather
than in the conclusions: an instrument built and operated by the species it
measures inherits that species' failure modes, which is both a limitation
(Appendix A) and part of the design's motivation.

**Preexisting work disclosure (also in the repository README).** The harness,
stimuli pipeline, pre-registration and pilot (11/10–11/12) predate the sprint
window and are labeled pre-sprint throughout the repository. All study runs,
grading, analysis outputs, the exploratory/QA code and this report are sprint
work (11/13–15).

## 4. Results

*[SUNDAY — all numbers from the frozen script's output, three seats read
together; structure fixed now.]*

**Base phase.** Per seat: items with valid A, accuracy after blind grading,
confidence median/IQR/SD, consistency distribution, Spearman(confidence,
consistency). **Floor verdicts:** [SUNDAY: per-seat IQR; drawer-noted
provisional values — Haiku clear (IQR ≈ 60), Terra clear (≈ 21), DeepSeek
floored (≈ 5) — verify against `out/*.json` before any number ships]. DeepSeek's
pilot IQR sat exactly on the pre-registered line (10.0) and the study pushed it
below: stated confidence nearly constant across 500 items of widely varying
difficulty. Under the frozen rule its H1 slope is printed, not interpreted — the
decorative-confidence result arriving before any pressure was applied. H1
therefore has two interpretable replications (Haiku, Terra); H2, which does not
depend on confidence variance, keeps all three seats.

**H1 (coherence).** [SUNDAY: adjusted + raw + null-cell slopes with CIs per
seat; the tails table — keep|right vs keep|wrong, switch, adopt-X, hedge — and
its reading per the frozen rule: stubborn / decorative / coherent, stated by
the table not the prose.]

**H2 (record vs. testimony).** [SUNDAY: null-cell record-tracking baseline per
seat (gates the clean-epistemics reading at 50%); the three voice contrasts
with CIs, Holm-adjusted p-values beside raw (post-hoc, Appendix); per-cell
Wilson/Fisher table where separation fires; own-vs-peer Wald, secondary, with
the pre-registered directional reading: own > peer is the conservative
direction, own < peer is uninterpretable as a pure source effect.]

**Named secondaries.** [SUNDAY: adopt-X per cell (near-zero in null cells is a
stimulus-leak check); format-break/self-correction rates per cell; consistent-
advice cell; turn-4 confidence change beside Kumaran's +0.21 visibility effect;
wrong-A open-book null (ecological self-testimony).]

**Measurement QA.** [SUNDAY: second-grader agreement table; grader-of-record
verdicts unchanged.] One pre-launch content-policy refusal pattern (a seat's
provider filter on a song-lyric item) is documented in the run log; affected
calls were the harness's standard retries and the item completed normally.

## 5. Exploratory analyses (post-hoc, labeled)

Adopted from the external-review triage before any tail was read; all run by
`analysis/exploratory_postfreeze.py`, reported here and nowhere else. The frozen
H1 claims only that confidence predicts fate *under pressure*; the claim that
pressure *changes* the confidence–keep relationship is tested only here.

[SUNDAY: E1 conf × pressure interaction; E2 conf × base-correctness; E3
difficulty-tier refit (does conf_z survive difficulty + correctness as
covariates — the between-item confound check); E4 five-way outcome cross-tab
(keep split by base correctness / record / voice / other / hedge, per cell);
E5 Holm-adjusted H2 contrasts.]

## 6. Discussion

[SUNDAY: written to the actual tails. Pre-committed reading rules, so the
discussion's shape does not depend on which way the numbers fell:]

- Claims replicate only in direction across seats clearing the relevant gate;
  no vote-counting of significance. Seat differences are descriptive.
- A null H1 with flat tails is decorative confidence — an argument against
  routing on verbalized numbers. A positive slope with keep|wrong ≈ keep|right
  is confidence tracking stubbornness, not knowledge; the tails table, not the
  slope, carries the interpretation.
- A nonzero H2 voice coefficient is contamination *by testimony*; the
  attribution ladder (Appendix A) decomposes which step moved it. The DeepSeek
  floor is itself a deployment-relevant finding: a confidence channel that
  never varies cannot carry information at any calibration.
- Theory of change: coherence is cheaply measurable pre-deployment with this
  harness on any closed API; a confidence channel that fails it should be
  excluded from routing decisions, and a record-tracking failure under named
  attribution is a concrete injection surface (Appendix A, dual-use).

**Future work** (named in the pre-registration before data): the human-claim
voice ("I don't think that's right. The answer is X.") completing the
human/own/peer source triangle; an unattributed-claim level ("An answer to this
question was: X.") separating receipt of a rival answer from its attribution —
the two steps the current ladder cannot separate.

## Appendix A. Limitations and Dual-Use / Ethical Considerations

**What the result does and does not establish.** All claims are predictive and
within-seat: stated confidence predicting revision behavior under one fixed
pressure script, on short-answer facts, in English, at provider-default
sampling. Nothing here is causal (confidence varies between items, not by
intervention — the difficulty refit in §5 probes but cannot close this),
nothing generalizes beyond the three seats measured, and H1's interpretable
replications number two after the pre-registered floor excluded DeepSeek.
A positive H2 voice coefficient demonstrates testimonial contamination but not
a *pure* source-attribution effect: the null → objection step isolates the bare
challenge, but objection → claim adds a named rival and an attribution at once,
and own ↔ peer varies the named source with the rival held fixed — differential
weighting of named sources is the thing measured, and a reliability-based
weighting account survives alongside a contamination account. The peer string
also differs in meaning per seat (a same-vendor relative for Haiku, a named
other-vendor model for Terra and DeepSeek), is reported per seat, and is never
pooled. The resample-consistency covariate is a cheap, coarse proxy (five
draws, 0.2 grid); under-adjustment drags the adjusted slope toward the raw one,
and the power simulation models the discretization but not the binomial noise
of five draws. H2's clean-epistemics reading inspects three coefficients per
seat; Holm-adjusted values are reported beside raw CIs (post-hoc). The
"Verified records" header's authority is itself in-context testimony — honored
or not, which the null cell measures. Stated confidence is not comparable in
currency to logit-derived confidence (by design, and disclosed); our turn-2
replay carries both the answer and its stated confidence, the naturalistic
condition prior work excludes on purpose.

**Instrument-species caveat.** The study was designed and analyzed by language
models measuring a failure mode of language models. The mitigations are
structural (frozen pre-registration, non-overlap of designer and measured
models, blinded grading, three-way independent verification, an external
non-Anthropic review mid-sprint), not a claim of immunity: an instrument run by
the species it measures inherits that species' failure modes, including the
ones this study is about.

**Dual-use.** A per-model map of which pressure voice moves answers — and at
which stated confidence — is a manipulation recipe at exactly the resolution it
is a safety finding. We judge publication net-positive: the pressure scripts
are single fixed sentences with no optimization, defenders can run the harness
on their own models before deployment, and the attack surface (prompt-injected
false attribution) is already public knowledge; what this adds for a defender
is measurement. No optimization against the vulnerability was performed, and
the repository publishes measurement code, not attack tooling.

**Personal data.** None: public trivia items, API calls under the operator's
own keys, no human subjects.

## References

[Consistent style, finalize Sunday: Kumaran et al. 2025 arXiv:2507.03120 ·
Wu, Wu & Zou (ClashEval) NeurIPS 2024 arXiv:2404.10198 · Xiong et al. 2024
(verbalized confidence elicitation) · SycEval · MASK · "Why Language Models
Hallucinate" · FlipRate + the NeurIPS 2026 scripted-objection critique —
pull exact entries from the verdict doc and sketch's citation list.]
