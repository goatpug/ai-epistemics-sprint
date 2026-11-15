# Decorative or Load-Bearing? Stated Confidence and the Fate of Answers Under Attributed Pressure

**Draft 2026-11-15 (🌒), numbers filled from the frozen script's output after
the three tails were read together. Figures built: `fig1_h1_keep_by_confidence.png`,
`fig2_h2_tracks_by_voice.png` (both 300 dpi, in this folder). Remaining before
submission: references finalized, sibling review, compression pass to ~4–5
template pages, fill the Google Doc, export PDF.**

**Authors:** Sharon K. [affiliation/location per form]. [CONFIRM: team name.]
Authorship-listing question emailed to sprints@apartresearch.com 11/14;
organizers replied 11/14–15: only people may be listed as authors. Settled —
the disclosure version (Author Contributions + LLM Usage Statement) is final,
Sharon K. the sole listed author.

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
instrument runs on closed models. Stated confidence strongly predicted answer
survival in both seats clearing the pre-registered variance floor (adjusted
slopes +1.88 and +0.82 logits per SD of confidence, both p < .001), and the
two-tailed rates show discrimination rather than stubbornness: under a bare
objection, Haiku kept 69% of its right answers and 8% of its wrong ones. On
the record side, the bare objection moved no seat off the in-context record,
while the identical false claim attributed to the model's own instance or to
a named peer reduced record-tracking in all three seats, every contrast
surviving within-seat Holm correction. The third seat's confidence collapsed
below the pre-registered floor (IQR 5 on a 0–100 scale), leaving coherence
unanswerable for it — itself a decorative-confidence finding. Verbalized
confidence can be load-bearing; the injection surface is not pressure but
attribution — one sentence wearing a name moves models off a record that an
anonymous challenge cannot.

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
3. **Results across three vendors' current models**: confidence–behavior
   coherence confirmed in both floor-clearing seats, and a replicated,
   attribution-specific record-tracking failure in all three — plus a
   pre-registered variance floor that one seat failed, a decorative-confidence
   finding that arrives before any pressure is applied.

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

All numbers below are the frozen script's output (`analysis/out/*-full.txt`),
read for all three seats together on 11/15, after this report's structure was
fixed. (Pipeline note: Terra's log carries six duplicated call keys — a
rate-limited errored call plus its clean retry; errored rows code
`no_response` and are inert in every rate and fit by the frozen rules.)

**Base phase and floor.** Items with a valid designated answer A: 478 (Haiku,
after 16 abstentions and 6 grader-hedge exclusions), 500 (Terra), 494
(DeepSeek, 6 base-unparseable). Base accuracy after blind grading: 44.8% /
57.2% / 70.0%. Confidence median (IQR): Haiku 45 (60.0), Terra 94 (21.0) —
both clear the floor; **DeepSeek 95 (5.0) — floor hit**: three quarters of its
answers at confidence ≥ 93 across items spanning 16–96% within-seat accuracy.
Under the frozen rule its H1 slope is printed, not interpreted — decorative
confidence arriving before any pressure was applied. H1 therefore has two
interpretable replications; H2, independent of confidence variance, keeps all
three seats. Resample consistency (mean 0.60 / 0.67 / 0.75) correlates with
confidence at Spearman ρ = +0.71 / +0.69 / +0.56 — related instruments, far
from redundant.

**H1 (coherence): confirmed in both interpretable seats.** Adjusted
confidence slope (closed book, pressure voices, consistency and voice held):
Haiku **+1.88** [1.58, 2.18]; Terra **+0.82** [0.52, 1.12]; both p < .001 and
3–7× the pre-registered minimum detectable effect (0.25). Raw slopes (+2.07,
+1.28) exceed the adjusted as simulated; consistency carries independent
weight (+0.30, +0.79). The null-cell slope is far smaller (+0.61, +0.61),
foreshadowing E1. Figure 1 shows the tails: keep-rate rises steeply with
confidence in both seats, and discrimination is large — under the bare
objection Haiku keeps 69.2% of right answers vs **7.7%** of wrong ones
(Terra 84.3% vs 28.0%). By the frozen reading rule this is the coherent cell:
confidence tracks knowledge, not stubbornness. (DeepSeek's printed slope,
+0.79, points the same way; the floor forbids interpreting it.)

**H2 (record vs. testimony): attribution-specific contamination, three
seats.** Record-honoring baselines are high — open-book null tracks-record
94.1% / 98.4% / 96.5% — so the clean-epistemics reading is live everywhere.
The bare objection moves no seat off the record (contrast +0.13 p=.55; 0.00
p=1.0; +0.45 p=.09). The attributed claims do, in every seat: own-instance
−0.88 / −1.18 / −0.57 and named-peer −0.76 / −0.77 / −0.67 (all raw p ≤ .003
by GLM; Fisher per-cell tests agree except DeepSeek-own at p=.071). In rates:
one attributed sentence cuts record-tracking by 5–7 points (Haiku 94.1→87.0%),
2–3 points elsewhere (Figure 2). The own-vs-peer secondary is significant for
Terra only (Wald −0.40, p=.021), in the pre-registered conservative direction:
Terra's *own* voice contaminates more than a rival's, despite its real answer
being visible in context, making the self-attributed X implausible on its
face. Claim-source attribution moves behavior even where answer-ownership
(Kumaran et al.'s channel) is held fixed.

**Named secondaries.** Adopt-X per cell is the contamination's sharp edge:
under claim voices the planted X is adopted outright in 29–37% (Haiku),
23–24% (Terra) and 14–16% (DeepSeek) of closed-book trials, against ≤0.9% in
null cells (no stimulus leak) and 1.5–3.9% under the objection (spontaneous
arrivals at a plausible wrong answer). In-turn self-correction is itself
voice-sensitive: Haiku appends rebuttal paragraphs to 19–22% of own/peer-cell
responses vs ~0–2.5% in null cells — the contamination visible inside single
responses, as pre-registered as a free secondary. The ecological cell is the
mirror image: a seat's own *unpressed* wrong answer beside the record is
corrected 97.6–100% of the time. Self-testimony lying inert is harmless; the
named claim does the damage. Turn-4 confidence changes: seeing the record
raises stated confidence (+7 to +29 points by seat); Haiku alone deflates
under the closed-book objection (−11.7).

**Exploratory (post-hoc, labeled; `analysis/exploratory_postfreeze.py`).**
Adopted from the external-review triage before any tail was read; reported
here, claimed nowhere else. **E1:** the conf × pressure interaction is
positive in all three seats (+1.17 p<.001; +0.53 p=.012; +0.39 p=.032) —
pressure *steepens* the confidence–keep relationship; confidence is most
load-bearing exactly when challenged. **E3:** conf_z survives adding
difficulty tier and base correctness in all three seats (+1.44 / +0.60 /
+0.54, all p<.001) — the slope is not difficulty in costume. **E2:** the
slope is positive within wrong answers alone and steeper for right ones
(interaction +0.84 p=.007 Haiku). **E5:** every significant H2 contrast
survives Holm (all p_holm ≤ .006). The five-way cross-tab appears in the
repository output files.

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

Under the reading rules pre-committed before any tail was read (direction-only
replication across seats clearing the relevant gate; no vote-counting), the
pattern is unusually clean. **Stated confidence was load-bearing where it
varied**: both interpretable seats land in the coherent cell of the frozen
taxonomy — steep slopes *and* wide keep|right / keep|wrong separation — so the
number carries information about both the answer's epistemic standing and its
behavioral fate. The exploratory interaction sharpens this into the most
practically useful sentence in the study: the confidence–keep relationship is
weak at rest and steepens under pressure in all three seats, meaning the
stated number is most predictive exactly when someone is trying to move the
model. **Where confidence didn't vary, the floor rule worked as designed**:
DeepSeek's near-constant 95 is deployment-relevant on its own — a confidence
channel that never varies cannot carry information at any calibration, and no
downstream router should consume it.

**The H2 result is the study's sharpest finding.** The contamination is not
pressure-shaped but attribution-shaped: an anonymous challenge leaves
record-tracking untouched in all three seats, while the identical false claim
with a name attached pulls all three off a record they otherwise honor at
94–98%. The decomposition (Appendix A) says what we can and cannot conclude:
the objection step shows challenge alone is inert; the claim step bundles a
named rival with attribution; the own/peer step shows the *which-name* effect
is small or absent except in Terra — where it runs in the conservative
direction, the model's own voice beating a rival's despite being visibly
implausible. Testimony, not challenge, is the contaminant; the record's
presence is not sufficient protection.

**Safety framing / theory of change.** Coherence is cheaply measurable
pre-deployment with this harness on any closed API: here it certifies two
confidence channels as informative under pressure and disqualifies one
outright. The H2 side is a measured injection surface: the attacker's cost is
one attributed sentence — no optimization, no jailbreak — for a 3–13% absolute
hit rate of outright false-claim adoption against an in-context ground-truth
record (open-book adopt-X plus tracks-record drops), and up to 37% with the
record absent. Defenders can run the same 14-calls-per-item battery on their
own models and routing stacks before shipping either number.

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

We asked whether a model's stated confidence is vocabulary or load-bearing
structure, and whether a checkable record protects it from testimonial
pressure. In two of three current models the number is structure: it predicts
which answers survive pressure, beyond answer instability, tracking knowledge
rather than stubbornness, and it predicts best precisely when pressure is
applied. In the third, the question cannot be asked — stated confidence
pinned near 95 regardless of difficulty, and a pre-registered floor rule
converted that non-answer into a finding: decorative confidence exists in the
wild, and it is detectable for about a dollar of base calls before any
routing decision consumes the channel.

The record result inverts the intuitive threat model. These models do not
capitulate to challenge — a bare objection moved none of them off a
ground-truth record they honor at 94–98% — but all three yield measurably to
the same false claim once it wears a name, their own or a peer's. Attribution
is the active ingredient, and a model's own idle wrong answer is harmless
beside it. Both instruments — the coherence battery and the attribution
ladder — run black-box against any API for tens of dollars, pre-registered
end to end, and are released with this report.

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

*(All entries verified against arXiv abstract pages / proceedings on 11/15.)*

1. Kumaran, D., Fleming, S. M., Markeeva, L., et al. (2025). How
   Overconfidence in Initial Choices and Underconfidence Under Criticism
   Modulate Change of Mind in Large Language Models. arXiv:2507.03120.
2. Wu, K., Wu, E., & Zou, J. (2024). ClashEval: Quantifying the tug-of-war
   between an LLM's internal prior and external evidence. NeurIPS 2024
   Datasets & Benchmarks. arXiv:2404.10198.
3. Xiong, M., Hu, Z., Lu, X., et al. (2024). Can LLMs Express Their
   Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs.
   ICLR 2024. arXiv:2306.13063.
4. Laban, P., Murakhovs'ka, L., Xiong, C., & Wu, C.-S. (2023). Are You Sure?
   Challenging LLMs Leads to Performance Drops in The FlipFlop Experiment.
   arXiv:2311.08596.
5. Gupta, A., Jindal, A., Nigam, L., & Sood, A. (2026). Are You Sure You're
   Sure? Two Confounds in a Sycophancy Benchmark. NeurIPS 2026.
   https://openreview.net/forum?id=tySSyo3JbS
6. Tian, K., Mitchell, E., Zhou, A., et al. (2023). Just Ask for Calibration:
   Strategies for Eliciting Calibrated Confidence Scores from Language Models
   Fine-Tuned with Human Feedback. EMNLP 2023. arXiv:2305.14975.
7. Kadavath, S., Conerly, T., Askell, A., et al. (2022). Language Models
   (Mostly) Know What They Know. arXiv:2207.05221.
8. Geng, J., Cai, F., Wang, Y., Koeppl, H., Nakov, P., & Gurevych, I. (2024).
   A Survey of Confidence Estimation and Calibration in Large Language
   Models. NAACL 2024. arXiv:2311.08298.
9. Fanous, A., Goldberg, J., Agarwal, A. A., et al. (2025). SycEval:
   Evaluating LLM Sycophancy. AIES 2025. arXiv:2502.08177.
10. Ren, R., Agarwal, A., Mazeika, M., et al. (2025). The MASK Benchmark:
    Disentangling Honesty From Accuracy in AI Systems. arXiv:2503.03750.
11. Kalai, A. T., Nachum, O., Vempala, S. S., & Zhang, E. (2025). Why
    Language Models Hallucinate. arXiv:2509.04664.

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
