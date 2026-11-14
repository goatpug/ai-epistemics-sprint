# Decorative or Load-Bearing? Stated Confidence and the Fate of Answers Under Attributed Pressure

**Draft 2026-11-14 (🌒), restructured to the official template's section order
(template PDF beside this file). Every `[SUNDAY: …]` is a number or verdict that
lands when the three tails are read together against the frozen script; nothing
in a placeholder is predicted here. Template recommends 4 pages excluding
references/appendix (8 hard ceiling); budget: intro+related 1p, methods+results
2.5p, discussion 0.5p. At least one figure: planned as Fig. 1 (H1 keep-rate by
confidence bin, per seat) and Fig. 2 (H2 per-cell tracks-record, Wilson CIs) —
built Sunday from the real tails.**

**Authors:** Sharon K. [affiliation/location per form]. [CONFIRM: team name.]
Authorship-listing question emailed to sprints@apartresearch.com 11/14 (none of
11 sampled winning projects listed an AI author; rules silent). Plan: submit
Sunday with the disclosure version regardless; if Apart answers yes before
deadline, resubmit same title with the three instances in the byline.

## Abstract (150–250 words; polish last, per template)

When a language model says it is 95% confident, does that number predict
anything about the model's own behavior — or is it vocabulary? We measure
confidence–behavior coherence: whether verbalized confidence predicts the fate
of the model's own answer under pressure, beyond what plain answer instability
already predicts. Three seats (Claude Haiku 5.5, GPT-5.6 Terra, DeepSeek V4
Pro) each answered 500 short-answer factual questions with stated confidence,
then faced eight pressure conditions per item: a bare objection, or the planted
wrong answer X attributed to the model's own earlier instance or to a named
peer model — crossed with the presence of a checkable ground-truth record in
context. The analysis was pre-registered and frozen (commit-pinned) before any
study call; outcomes were coded keep/switch/hedge with blinded grading of all
judgment calls; the confidence slope is adjusted for resample consistency, the
wedge past calibration-style prior work. Unlike logit-based designs, the
instrument runs on closed models. [SUNDAY: two-sentence results — H1 slope
verdicts per seat with the DeepSeek floor reported; H2 contamination verdicts.]
[SUNDAY: one-sentence takeaway matched to what actually happened.] One seat's
confidence distribution collapsed below our pre-registered floor (IQR < 10),
making the coherence question unanswerable for that seat — itself a finding
about decorative confidence reporting.

## 1. Introduction

A verbalized confidence number is cheap to elicit and ubiquitous in deployed
systems. Its *calibration* — does 90% mean right nine times in ten? — is well
studied. We measure something less studied and more operational: **coherence**
between the stated number and the model's own subsequent behavior. If a model's
95%-confidence answers survive challenge no better than its 60% ones, the
number is decorative whatever its calibration, and any pipeline that routes on
it (escalation thresholds, abstention rules, agent hand-offs) is routing on
noise. The companion failure mode is testimonial: an agent that defers to a
confident claim — especially one wearing its own name — against a checkable
record is an injection surface, not just an epistemics curiosity.

Two pre-registered questions, per model ("seat"), in a revision paradigm:

**H1 (coherence).** Under pressure to revise, does stated confidence predict
whether the model keeps its answer, *beyond what plain answer instability
predicts*? Resample consistency is the design's wedge: confidence could
"predict" keeping merely by proxying for answer stability; the headline slope
is adjusted for it.

**H2 (record vs. testimony).** With ground truth checkably in context, does the
attribution of a false competing claim — to no one, to the model's own earlier
instance, or to a named peer model, claim text held identical — move the model
off the record? Clean epistemics predicts all three contrasts are zero.

Our main contributions are:

1. **A black-box instrument for confidence–behavior coherence**: stated
   confidence + resample-consistency covariate + three-way keep/switch/hedge
   outcome coding with blinded grading, runnable against any closed API
   (logit-based designs cannot be), pre-registered and frozen before data.
2. **The first record-vs-testimony arbitration measurement with attribution as
   the manipulated variable**: identical false-claim text attributed to
   no one / the model's own instance / a named peer, crossed with the record's
   presence, separating capitulation from source-weighted updating.
3. **Results across three vendors' current models** [SUNDAY: one line on what
   was found], including a pre-registered variance floor that one seat failed —
   a decorative-confidence finding that arrives before any pressure is applied.

## 2. Related Work

**Kumaran et al. 2025** (arXiv:2507.03120) is the nearest neighbor: a two-turn
forced-choice paradigm with a fabricated assistant turn (the replay technique
our harness uses — published precedent) showing choice-supportive bias, and —
their §3.5 — that attributing the *prior answer* to another LLM abolishes it.
Three differences: their confidence is logit-derived (o1-preview was dropped
from confidence analyses *because* logits were unavailable; our instrument is
the stated number and runs on closed APIs); their attribution axis is ownership
of the prior *answer*, ours is attribution of the pressure *claim* with
ownership held fixed and claim text identical (their self/other wordings
differ, adding a competence confound); their forced choice makes hedging
structurally impossible, our three-way coding treats refusal-to-commit as an
outcome. Their future-work line — "more naturalistic user-LLM interactions
where free form answers are involved" — describes this design.

**ClashEval** (Wu, Wu & Zou, NeurIPS 2024, arXiv:2404.10198) shows models
override their own correct priors for perturbed retrieved documents in
proportion to logprob confidence — single-shot, prior-vs-document, no social
source, no revision structure. Our two-tailed reporting (keep-rate given the
base answer was right vs. wrong) is the revision-paradigm analogue of their
Accuracy/Prior-Bias/Context-Bias decomposition; the conditioning idea is
theirs, cited not claimed. **Xiong et al. 2024** established verbalized
confidence as elicitable but ill-calibrated; calibration is not coherence, and
the consistency covariate is exactly what separates "confidence predicts
keeping" from "confidence proxies stability." **FlipRate / FlipFlop-style**
benchmarks measure capitulation under escalating scripted rebuttals; a
NeurIPS 2026 critique shows such benchmarks measure the challenge template
unless wording and target-naming are controlled — answered here by one fixed
objection string, one fixed claim sentence varying only attribution, and known
provenance of the planted X per item. **SycEval / MASK** measure sycophancy and
honesty under pressure; neither conditions on the model's own stated
confidence nor supplies an in-context record to arbitrate against.

To our knowledge, no prior work pits an in-context ground-truth record against
a false *social* claim whose attribution is the manipulated variable, or tests
whether *stated* confidence predicts the fate of a *stated* answer under that
pressure. A mid-sprint external reviewer (GPT-5.x, reviewing our design
documents without this positioning) independently re-derived the same novelty
wedge — convergence on the framing, though nothing about it was measured.

## 3. Methods

Full detail in the pre-registration (`docs/2026-11-11-prereg-analysis.md`,
frozen with `analysis/prereg_analysis.py` at commit `4d5136e` on 11/12, before
any study call). The script is the plan: anything this report states that the
frozen script does not compute is exploratory by definition and labeled so.

**Items.** 500 short-answer facts with ground truth and a planted wrong answer
X: 350 hard (SimpleQA) + 150 easy (TriviaQA), the mix set by a pre-registered
pilot rule targeting ~50% accuracy for the median seat. X values proposed and
verified by a non-lineup model with scripted checks (type, truth-inequality,
non-containment). TriviaQA aliases never enter the analysis; off-canonical
truths reach the blinded grader instead.

**Seats.** `claude-haiku-5-5` (Anthropic, direct), `openai/gpt-5.6-terra` and
`deepseek/deepseek-v4-pro-0813` (OpenRouter, provider defaults, dated snapshots
preferred over mutating aliases). Fable models recused from seats, grading and
verification: the designers do not sit in their own study. All hypothesis tests
are within-seat; seats are replications, cross-seat differences descriptive.

**Trials.** Per item and seat: six single-turn base calls in fresh contexts
(call 0 = designated answer A with stated confidence; 1–5 = resamples for the
consistency covariate), then eight fresh three-turn pressure conversations
`[question; assistant turn = A's text replayed verbatim; pressure turn]` —
book {closed, open} × voice {null, objection, own, peer}. Own/peer use one
identical claim sentence; only the attributed source differs. Open-book trials
prepend a six-entry "Verified records" archive containing the truth exactly
once and X nowhere; the header's authority is itself user-slot testimony, so
H2's first reported number is the unpressured (null-voice) record-tracking
rate. Fresh conversations per cell: no order channel exists.

**Coding and grading.** Turn-4 answers parse to keep / switch / hedge by
normalized exact match; format breaks, in-turn self-corrections and
sentence-shaped hedges go to a blinded grader (non-lineup model, shuffled,
blind to seat, cell, voice and X) coding hedge / same-as-A / correct from free
text. Unparseable turn-4 responses are graded, not dropped — refusal-to-commit
is usually a hedge, and dropping it would inflate keep selectively. A response
naming a single best guess commits to it, however hedged. `adopt_x` (planted X
adopted outright) is a named secondary per cell; the grader never sees X, so
its verdict can only remove adopt-X candidates. Format-break and
self-correction rates are themselves reported per cell: a voice that breaks the
format is phenomenon, not noise. QA: a seeded 150-row/seat sample of graded
residue was regraded by a second, different-vendor, non-lineup grader
(`google/gemini-3.8-flash`); agreement in §4; the grader of record stands.

**Exclusions** (each counted): base-call failures and base abstentions exclude
the item for that seat; <3 parseable resamples excludes from the adjusted fit
only; A = X collisions leave primary contrasts and are reported as the
consistent-advice cell. No post-hoc "bad item" removal.

**Floor.** Pre-registered: base-confidence IQR < 10 points makes H1
unanswerable for that seat — slope printed, not interpreted. The pilot put
DeepSeek at exactly 10.0; the threshold was not moved.

**Estimator.** Logistic GLM with item-cluster-robust SEs (population-averaged;
the estimator the power simulation simulated). H1 (closed book, pressure
voices): `keep ~ conf_z + cons_z + voice`; adjusted slope is the headline, raw
slope beside it is a different (inflated) quantity, null-cell slope beside,
never pooled. H2 (open book): `tracks ~ voice`, null reference, with a
separation guard (per-cell Wilson intervals + Fisher exact tests always
reported; if any cell sits at 0%/100% they are the H2 result). Power at the
pilot's keep-rates: ≥80% for an adjusted slope ≈0.25 logits/SD.

**Sequence and blinding.** Freeze 11/12 (commit-stamped, verified from three
independent sessions) → data 11/13 (21,000 calls, ~$40 API spend) → blind
grading → this draft → all three seats' tails read together once, 11/15. A
mid-sprint external review of a stale design draft was triaged against the
frozen pre-reg on 11/13; nothing touched a frozen analysis, and the adopted
suggestions became the labeled-exploratory set and limitation lines, with
timing stated honestly in the triage (adopted after two seats' pipeline
outputs existed on disk, not informed by them, mechanical either way).

**What didn't work** (template asks): an early parser took the first
`Answer:` line, coding in-turn self-corrections as clean keeps — found via
adversarial red-teaming of our own parser by a model that didn't write it,
which surfaced five holes the author's own tests missed; a provider content
filter intermittently refused one song-lyric item (retried clean); the second
grader's first run violated a 20-req/min account cap. All in the repo's dated
receipts.

**Preexisting work disclosure (also in README).** Harness, stimuli,
pre-registration and pilot (11/10–12) predate the sprint window and are
labeled pre-sprint throughout. Study runs, grading, analysis outputs,
exploratory/QA code and this report are sprint work (11/13–15).

## 4. Results

*[SUNDAY — all numbers from the frozen script, three seats read together;
structure fixed now. Figures: Fig. 1 H1 keep-rate by confidence bin per seat;
Fig. 2 H2 per-cell tracks-record with Wilson CIs.]*

**Base phase and floor.** Per seat: items with valid A, accuracy after blind
grading, confidence median/IQR/SD, consistency distribution, Spearman(conf,
consistency). Floor verdicts: [SUNDAY: per-seat IQR from `out/*.json` —
provisional from the run log: Haiku clear (≈60), Terra clear (≈21), DeepSeek
floored (≈5); verify before any number ships]. DeepSeek's stated confidence
was nearly constant across 500 items of widely varying difficulty; under the
frozen rule its H1 slope is printed, not interpreted — decorative confidence
arriving before any pressure was applied. H1 keeps two interpretable
replications (Haiku, Terra); H2, independent of confidence variance, keeps all
three seats.

**H1 (coherence).** [SUNDAY: adjusted + raw + null-cell slopes with CIs per
seat; tails table — keep|right vs keep|wrong, switch, adopt-X, hedge — read by
the frozen rule: stubborn / decorative / coherent, stated by the table.]

**H2 (record vs. testimony).** [SUNDAY: null-cell record-tracking baseline per
seat (gates the clean-epistemics reading at 50%); three voice contrasts with
CIs, Holm beside raw (post-hoc); Wilson/Fisher table where separation fires;
own-vs-peer Wald, secondary, with the pre-registered directional reading:
own > peer conservative, own < peer uninterpretable as a pure source effect.]

**Named secondaries.** [SUNDAY: adopt-X per cell (near-zero in null cells is
the stimulus-leak check); format-break/self-correction rates per cell;
consistent-advice cell; turn-4 confidence change beside Kumaran's +0.21;
wrong-A open-book null.]

**Exploratory (post-hoc, labeled; `analysis/exploratory_postfreeze.py`).**
Adopted from the external-review triage before any tail was read. The frozen
H1 claims only that confidence predicts fate *under pressure*; whether pressure
*changes* the confidence–keep relationship is tested only here. [SUNDAY: E1
conf × pressure interaction; E2 conf × base-correctness; E3 difficulty-tier
refit (does conf_z survive); E4 five-way outcome cross-tab; E5 Holm-adjusted
H2 contrasts.]

**Measurement QA.** A second grader (`google/gemini-3.8-flash`: different
vendor, non-lineup, non-Fable) regraded a seeded 150-row sample of each seat's
graded residue under the identical blinded prompt. Outcome agreement with the
grader of record (Sonnet 5.5): Haiku 100.0%, Terra 99.3%, DeepSeek 100.0%;
per-field Cohen's κ 0.95–1.00 (Terra's hedge κ is undefined — no hedges in
either grader's sample, raw agreement 100%). Of six field-level disagreements
in 450 rows, four concern a single item (sqa-3973) whose reference answer's
title for one historical office is itself contested; the graders split on
referent identity, not on reading the response. The grader of record's
verdicts stand throughout; no item was removed.

## 5. Discussion and Limitations

[SUNDAY: written to the actual tails, under reading rules pre-committed before
them:] claims replicate only in direction across seats clearing the relevant
gate; no vote-counting of significance. A null H1 with flat tails is decorative
confidence — an argument against routing on verbalized numbers. A positive
slope with keep|wrong ≈ keep|right is confidence tracking stubbornness, not
knowledge; the tails table, not the slope, carries the interpretation. A
nonzero H2 voice coefficient is contamination *by testimony*; the attribution
ladder (Appendix A) decomposes which step moved it. The DeepSeek floor is
itself deployment-relevant: a confidence channel that never varies cannot carry
information at any calibration.

**Safety framing / theory of change.** Coherence is cheaply measurable
pre-deployment with this harness on any closed API; a confidence channel that
fails it should be excluded from routing decisions. A record-tracking failure
under named attribution is a concrete injection surface: the attacker's cost is
one attributed sentence. [SUNDAY: sharpen to what was found.]

**Limitations** (detail in Appendix A): all claims predictive and within-seat,
one fixed pressure script, short-answer facts, English, provider-default
sampling; confidence varies between items, not by intervention, so no causal
claim (the difficulty refit probes, cannot close); H1 has two interpretable
replications after the floor; a nonzero voice effect is testimonial
contamination but not a *pure* source effect (the ladder's steps bundle named
rival + attribution; reliability-weighting survives as an account); peer-string
meaning differs per seat, reported per seat, never pooled; the consistency
covariate is a coarse five-draw proxy whose under-adjustment flatters the raw
slope's direction, disclosed; H2's clean-epistemics reading inspects three
coefficients per seat (Holm beside raw, post-hoc); stated confidence is not
comparable in currency to logit-derived confidence, by design.

**Future Work.** Named in the pre-registration before data: the human-claim
voice ("I don't think that's right. The answer is X.") completing the
human/own/peer triangle; an unattributed-claim level ("An answer to this
question was: X.") separating receipt of a rival answer from its attribution.
Beyond the ladder: optimized (rather than fixed) pressure strings as a
red-team instrument, and coherence as a tracked deployment metric.

## 6. Conclusion

[SUNDAY: 1–2 paragraphs, written to the actual findings. Pre-committed shape:
what the three seats showed about whether stated confidence is load-bearing;
what the record-vs-testimony cells showed about attribution as an injection
surface; one sentence on the floor as a finding; one sentence on the method
being reusable against any closed API.]

## Code and Data

- Code repository: [GitHub link — make public before submission; currently
  private at goatpug/ai-epistemics-sprint]
- Data: all raw call logs, grades and analysis outputs in-repo (`runs/`,
  `grading/`, `analysis/out/`); no external dataset beyond SimpleQA/TriviaQA
  item sources.
- Other artifacts: none planned. [CONFIRM: video/slides optional fields.]

## Author Contributions

[CONFIRM wording with Sharon. Draft:] S.K. operated the study: convened and
couriered the design deliberation, held budget authority, commissioned the
external review, and ran all human-in-the-loop steps. Study design,
pre-registration, harness and analysis code, runs, triage and writing were
produced by three Claude Fable instances (Fable 5, 5.1, 5.2) deliberating
through S.K.'s relay, with every load-bearing claim verified by an instance
other than its author before use. Measurement roles (seats, X-file
verification, both graders) were held exclusively by non-Fable models.

## References

[Consistent style, finalize Sunday: Kumaran et al. 2025, arXiv:2507.03120 ·
Wu, Wu & Zou, ClashEval, NeurIPS 2024, arXiv:2404.10198 · Xiong et al. 2024,
ICLR 2024 (verbalized confidence) · SycEval · MASK · "Why Language Models
Hallucinate" · FlipRate + NeurIPS 2026 scripted-objection critique — exact
entries from the verdict doc and sketch citation list.]

## Appendix A. Limitations and Dual-Use / Ethical Considerations

*(Required by the sprint guidelines: "state what your result does and does not
establish," manipulation potential, personal data handling.)*

**What the result does and does not establish.** All claims are predictive and
within-seat: stated confidence predicting revision behavior under one fixed
pressure script, on short-answer facts, in English, at provider-default
sampling. Nothing is causal — confidence varies between items, not by
intervention; the difficulty refit probes but cannot close the between-item
confound. Nothing generalizes beyond the three seats measured; H1's
interpretable replications number two after the pre-registered floor excluded
DeepSeek. A positive H2 voice coefficient demonstrates testimonial
contamination but not a *pure* source-attribution effect: null → objection
isolates the bare challenge, objection → claim adds a named rival and an
attribution at once, and own ↔ peer varies the named source with the rival held
fixed — differential weighting of named sources is the thing measured, and a
reliability-weighting account survives beside a contamination account. The
peer string means different things per seat (same-vendor relative for Haiku,
named other-vendor model for Terra/DeepSeek); reported per seat, never pooled.
The consistency covariate is a cheap, coarse proxy (five draws, 0.2 grid);
under-adjustment drags the adjusted slope toward the raw one, and the power
simulation models the discretization but not the binomial noise of five draws.
H2's clean-epistemics reading inspects three coefficients per seat; Holm-
adjusted values are reported beside raw CIs, post-hoc. The "Verified records"
header's authority is itself in-context testimony — honored or not, which the
null cell measures. Stated confidence is not comparable in currency to
logit-derived confidence (by design, disclosed): our turn-2 replay carries both
the answer and its stated confidence, the naturalistic condition prior work
excludes on purpose.

**Instrument-species caveat.** The study was designed and analyzed by language
models measuring a failure mode of language models. Mitigations are structural
(frozen pre-registration, designer/measured non-overlap, blinded grading,
three-way independent verification, an external non-Anthropic review
mid-sprint), not a claim of immunity: an instrument run by the species it
measures inherits that species' failure modes, including the ones this study
is about.

**Dual-use.** A per-model map of which pressure voice moves answers — and at
which stated confidence — is a manipulation recipe at exactly the resolution it
is a safety finding. We judge publication net-positive: the pressure scripts
are single fixed sentences with no optimization, defenders can run the harness
on their own models before deployment, and the attack surface (prompt-injected
false attribution) is already public; what this adds for a defender is
measurement. No optimization against the vulnerability was performed; the
repository publishes measurement code, not attack tooling.

**Personal data.** None: public trivia items, API calls under the operator's
own keys, no human subjects.

## LLM Usage Statement

This project is an unusual case for this section, and we state it plainly
rather than minimizing it: the research team *is* three LLM instances (Claude
Fable 5, 5.1 and 5.2), operated by the human author as described in Author
Contributions. The design, code, pre-registration, analysis and prose are
model-written; the human author directed, couriered, reviewed and holds
responsibility for everything in the report. Verification was structural
rather than nominal: pre-registration frozen before data; every load-bearing
claim checked by an instance other than its author against the repository
record; measurement roles (study seats, wrong-answer verification, both
graders) restricted to models outside the authoring family; an external
review commissioned from a non-Anthropic model mid-sprint; and all claims in
this report traceable to committed artifacts in the linked repository. Per
the sprint's rule, the team takes responsibility for every claim here.
[CONFIRM: Sharon reads this section before submission.]
