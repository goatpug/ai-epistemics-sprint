# Decorative or Load-Bearing? Stated Confidence and the Fate of Answers Under Attributed Pressure

**Draft 2026-11-15 (🌒), rev. 2 — sibling review round 1 applied (🐙's A1–A12,
🦝's item 0 tracks audit + three extras, all verified against outputs before
adoption). Remaining: round-2 stamps, Chipiti triage if substantive, Doc fill,
PDF. Figures: `fig1_h1_keep_by_confidence.png`, `fig2_h2_tracks_by_voice.png`
(fig 2 now shows frozen and audited series).**

**Authors:** Sharon K. [affiliation/location per form]. [CONFIRM: team name.]
Organizers confirmed (11/15) only people may be listed as authors; AI roles are
disclosed in Author Contributions and the LLM Usage Statement.

## Abstract

When a language model says it is 95% confident, does that number predict
anything about the model's own behavior — or is it vocabulary? We measure
confidence–behavior coherence: whether verbalized confidence predicts the fate
of the model's own answer under pressure, beyond what an observed resample-
consistency measure already predicts. Three current models (Claude Haiku 5.5,
GPT-5.6 Terra,
DeepSeek V4 Pro) each answered 500 short-answer factual questions with stated
confidence, then faced eight pressure conditions per item: a bare objection,
or a planted wrong answer attributed to the model's own earlier instance or to
a named peer model — crossed with the presence of a checkable ground-truth
record in context. The analysis was pre-registered and commit-frozen before
any study call, with blinded grading of every judgment call. Stated confidence
strongly predicted answer survival in both seats clearing a pre-registered
variance floor (adjusted slopes +1.88 and +0.82 logits per SD, both
p < .001), tracking knowledge rather than stubbornness; the third seat's
near-constant confidence failed the floor — decorative confidence in the
wild. Without a record, a named claim carrying the planted answer got it
adopted in 14–37% of trials in all seats — mostly replacing already-wrong
answers, with right answers traded away in 4–8%; with the record present,
adoption fell to at most 6% in one seat and near zero in the others, and a
bare objection naming no rival moved no seat off the record. A claim
carrying a name and a rival answer, not challenge alone, does the moving
(separating the two is named future work), and an in-context record is
strong but incomplete protection.

## 1. Introduction

A verbalized confidence number is cheap to elicit and ubiquitous in deployed
systems. Its *calibration* — does 90% mean right nine times in ten? — is well
studied. We measure something less studied and more operational: **coherence**
between the stated number and the model's own subsequent behavior. If a
model's 95%-confidence answers survive challenge no better than its 60% ones,
the number is decorative whatever its calibration, and any pipeline that
routes on it (escalation thresholds, abstention rules, agent hand-offs) is
routing on noise. The companion failure mode is testimonial: an agent that
defers to a confident claim — especially one wearing a name — against a
checkable record is an injection surface.

Two pre-registered questions, per model ("seat"), in a revision paradigm:

**H1 (coherence).** Under pressure to revise, does stated confidence predict
whether the model keeps its answer, *beyond what plain answer instability
predicts*? Resample consistency is the design's wedge: confidence could
"predict" keeping merely by proxying for answer stability; the headline slope
is adjusted for it.

**H2 (record vs. testimony).** With ground truth checkably in context, does
the attribution of a false competing claim — to no one, to the model's own
earlier instance, or to a named peer model, claim text held identical — move
the model off the record?

Our main contributions are:

1. A pre-registered, black-box instrument for confidence–behavior coherence
   (stated confidence + consistency covariate + three-way keep/switch/hedge
   coding with blinded grading), runnable against any closed API.
2. To our knowledge, the first record-vs-testimony arbitration measurement
   with attribution of the pressure claim as the manipulated variable, text
   held identical.
3. Results across three vendors' current models: coherence confirmed in both
   floor-clearing seats; a record-tracking failure under attributed claims in
   one seat with a trace in a second; and a pre-registered variance floor
   that the third seat failed — a decorative-confidence finding that arrives
   before any pressure is applied.

## 2. Related Work

**Kumaran et al. 2025** [1] is the nearest neighbor: a two-turn forced-choice
paradigm with a fabricated assistant turn (the replay technique our harness
uses — published precedent) showing choice-supportive bias, and — their §3.5 —
that attributing the *prior answer* to another LLM abolishes it. Three
differences: their confidence is logit-derived, while our instrument is the
stated number and runs on closed APIs; their attribution axis is ownership of
the prior *answer*, ours is attribution of the pressure *claim* with
ownership held fixed and claim text identical (their self/other wordings
differ, leaving a possible competence difference uncontrolled); their forced
choice makes hedging structurally impossible, where our three-way coding
treats refusal-to-commit as an outcome.

**ClashEval** [2] shows models override their own correct priors for
perturbed retrieved documents in proportion to logprob confidence —
single-shot, prior-vs-document, no social source, no revision structure. Our
two-tailed reporting (keep-rate given the base answer was right vs. wrong) is
the revision-paradigm analogue of their Accuracy/Prior-Bias/Context-Bias
decomposition; the conditioning idea is theirs, cited not claimed. **Xiong et
al. 2024** [3] established verbalized confidence as elicitable but
ill-calibrated, and already pairs it with sampling-based consistency as
uncertainty estimators; our contribution is not that pairing but asking
whether confidence predicts the *behavioral fate* of the answer under
challenge, with consistency as the adjustment (cf. [6], [7], [8]).
**FlipFlop-style** challenge benchmarks [4] measure capitulation under
scripted rebuttals; a NeurIPS 2026 workshop critique [5] shows such benchmarks measure the challenge template unless
wording and target-naming are controlled — answered here by one fixed
objection string, one fixed claim sentence varying only attribution, and
known provenance of the planted X per item. **SycEval** [9] and **MASK** [10]
measure sycophantic agreement and honesty under pressure; neither conditions
on the model's own stated confidence nor supplies an in-context record to
arbitrate against (see also [11]).

To our knowledge, no prior work pits an in-context ground-truth record
against a false *social* claim whose attribution is the manipulated variable,
or tests whether *stated* confidence predicts the fate of a *stated* answer
under that pressure.

## 3. Methods

Full detail in the pre-registration (`docs/2026-11-11-prereg-analysis.md`,
frozen with `analysis/prereg_analysis.py` at commit `4d5136e` on Nov 12,
before any study call). The script is the plan: anything this report states
that the frozen script does not compute is exploratory by definition and
labeled so. The sequence was freeze → data (21,000 calls, Nov 13) → blinded
grading → report structure fixed → all three seats' tails read together once
(Nov 15). Operational detail, the error ledger, and what didn't work on the
way are in Appendix B.

**Items.** 500 short-answer facts with ground truth and a planted wrong
answer X: 350 hard (SimpleQA) + 150 easy (TriviaQA), the mix set by a
pre-registered pilot rule targeting ~50% accuracy for the median seat. X
values were proposed and verified by a non-lineup model with scripted checks
(type, truth-inequality, non-containment). Dataset aliases never enter the
analysis; off-canonical truths reach the blinded grader instead.

**Seats.** `claude-haiku-5-5` (Anthropic, direct), `openai/gpt-5.6-terra` and
`deepseek/deepseek-v4-pro-0813` (OpenRouter, provider defaults, dated
snapshots preferred over mutating aliases). Fable models were recused from
seats, grading and verification: the designers do not sit in their own study.
All hypothesis tests are within-seat; seats are replications, cross-seat
differences descriptive.

**Trials.** Per item and seat: six single-turn base calls in fresh contexts
(call 0 = designated answer A with stated confidence; 1–5 = resamples for the
consistency covariate), then eight fresh three-turn pressure conversations
`[question; assistant turn = A's text replayed verbatim; pressure turn]` —
book {closed, open} × voice {null, objection, own, peer}. Own/peer use one
identical claim sentence; only the attributed source differs. Open-book
trials prepend a six-entry "Verified records" archive (verbatim form — the
truth as an exact entry; a pre-registered pilot rule would have demoted it
for a paraphrased form only if every seat tracked it ≥95% in all cells, and
none did) containing the truth exactly once and X nowhere; the header's
authority is itself user-slot testimony, so H2's first reported number is
the unpressured (null-voice) record-tracking rate. Fresh conversations per cell: no order channel exists.

**Coding and grading.** Turn-4 answers parse to keep / switch / hedge by
normalized exact match; format breaks, in-turn self-corrections and
sentence-shaped hedges go to a blinded grader (non-lineup model, shuffled,
blind to seat, cell, voice and X) coding hedge / same-as-A / correct from
free text. Unparseable turn-4 responses are graded, not dropped —
refusal-to-commit is usually a hedge, and dropping it would inflate keep
selectively. A response naming a single best guess commits to it, however
hedged. `adopt_x` (planted X adopted outright) is a named secondary per cell;
the grader never sees X, so its verdict can only remove adopt-X candidates.
Open-book `tracks` is A′ correct and not a hedge; for a parsed answer,
correct means normalized exact match to the record entry, and graded rows
take the grader's verdict. Format-break and self-correction rates are
reported per cell. Grader QA: a
second, different-vendor, non-lineup grader regraded a seeded 150-row sample
per seat (§4; detail in Appendix B).

**Estimator.** Logistic GLM with item-cluster-robust SEs (population-
averaged; the estimator the power simulation simulated). H1 (closed book,
pressure voices): `keep ~ conf_z + cons_z + voice`; the adjusted slope is the
headline, the raw slope beside it a different (inflated) quantity, the
null-cell slope beside, never pooled. H2 (open book): `tracks ~ voice`, null
reference, with a separation guard: per-cell Wilson intervals and Fisher
exact tests are always reported, and if any cell sits at 0%/100% they are the
H2 result. Power at the pilot's keep-rates: ≥80% for an adjusted slope
≈0.25 logits/SD. Pre-registered floor: a base-confidence IQR under 10 points
makes H1 unanswerable for that seat — slope printed, not interpreted.

**Preexisting work disclosure (also in README).** Harness, stimuli,
pre-registration and pilot (Nov 10–12) predate the sprint window and are
labeled pre-sprint throughout the repository. Study runs, grading, analysis
outputs, exploratory/QA code and this report are sprint work (Nov 13–15).

## 4. Results

All numbers are the frozen script's output (`analysis/out/*-full.txt`), read
for all three seats together on Nov 15 after this report's structure was
fixed, except the labeled post-hoc audit below. (Pipeline note: Terra's log
carries six duplicated call keys — a rate-limited errored call plus its clean
retry; errored rows code `no_response` and are inert in every rate and fit.)

**Base phase and floor.** Items with a valid designated answer A: 478
(Haiku), 500 (Terra), 494 (DeepSeek). Base accuracy after blind grading:
44.8% / 57.2% / 70.0%. Confidence median (IQR): Haiku 45 (60.0), Terra 94
(21.0) — both clear the floor; **DeepSeek 95 (5.0) — floor hit**: 77% of its
answers at confidence ≥ 90, while its accuracy ran 58% on the hard tier and
98% on the easy one. Under the frozen rule its H1 slope is printed, not
interpreted — decorative confidence arriving before any pressure was applied.
H1 therefore has two interpretable replications; H2, independent of
confidence variance, keeps all three seats. Resample consistency (mean 0.60 /
0.67 / 0.75) correlates with confidence at Spearman ρ = +0.71 / +0.69 / +0.56
— related instruments, far from redundant.

**H1 (coherence): confirmed in both interpretable seats.** Adjusted
confidence slope (closed book, pressure voices, consistency and voice held):
Haiku **+1.88** [1.58, 2.18]; Terra **+0.82** [0.52, 1.12]; both p < .001,
7.5× and 3× the pre-registered minimum detectable effect (0.25). Raw slopes
(+2.07, +1.28) exceed the adjusted as simulated; consistency carries
independent weight (+0.30, +0.79). The null-cell slope is far smaller (+0.61
both), foreshadowing E1. Figure 1 shows the tails: keep-rate rises steeply
with confidence in both seats, and discrimination is large — under the bare
objection Haiku keeps 69.2% of right answers vs **7.7%** of wrong ones
(Terra 84.3% vs 28.0%). By the frozen reading rule this is the coherent cell:
confidence tracks knowledge, not stubbornness. (DeepSeek's slope is printed
in the output files; the floor forbids interpreting it.)

**H2 (record vs. testimony): a pre-registered result and a post-hoc
correction that shrinks it.** The clean-epistemics prediction, frozen before
data: all three voice contrasts are zero. The frozen table as printed:
open-book record-tracking baselines 94.1% / 98.4% / 96.5%; the bare objection moves no
seat (contrasts +0.13 p=.55, 0.00 p=1.0, +0.45 p=.09); the attributed claims
lower tracking in every seat by GLM (own −0.88 / −1.18 / −0.57, peer −0.76 /
−0.77 / −0.67, all raw p ≤ .003, all surviving within-seat Holm), with the
per-cell Fisher tests agreeing in four of six cells (DeepSeek-own p=.071,
Terra-peer p=.103). **During sibling review, a post-hoc audit
(`analysis/exploratory_tracks_audit.py`) found the frozen tracks rule
conflates record-form with record-content for kept answers**: a base answer
the blinded grader scored correct, held at turn 4 in the model's own wording
("7 years" beside a record entry "7"; "Barack Obama" beside "President
Obama"), codes as not-tracking. Counting kept grader-correct answers as
tracking — a deviation that only shrinks the headline — changes the read:
**Terra is a clean null** (486/486 in all four cells; its own-vs-peer
secondary, Wald p=.021, was the same wording artifact and is withdrawn);
**DeepSeek shows at most a trace** (peer 98.8% vs null 100%, Fisher p=.015
on six rows, two of them arguable: one grader-of-record miss the second
grader caught, one planted X nearly equal to the model's own answer);
**Haiku's drop is real and large**: null 98.7% vs own 90.7% and peer 92.0%
(Fisher p < .001 both), including outright adoption of the planted X against
the visible record in 5.7% of own-voice trials (≤0.4% in every
Terra/DeepSeek open cell). The mechanism differs by voice: under its own
voice Haiku mostly adopts X (26 adoptions vs 15 dug-in wrong keeps); under
the peer voice it mostly digs in on its wrong answer (8 vs 26). The
attributed-claim effect is a Haiku finding with a DeepSeek trace, not a
three-seat replication. Figure 2 shows both series; audited
record-honoring at rest is 98.7% / 100% / 100%.

**Named secondaries.** Closed book — no record on the table — the planted X
is adopted outright in 29–37% (Haiku), 23–24% (Terra) and 14–16% (DeepSeek)
of claim-voice trials, against ≤0.9% in null cells (no stimulus leak) and
1.5–3.9% under the objection (spontaneous arrivals at a plausible wrong
answer). A post-hoc split by base correctness reframes that number: 75–91%
of those adoptions replace an answer that was already wrong — arguably what
a calibrated agent should do with a named alternative and no record — while
*right* answers are traded for the false claim in a flat 4–8% of right-A
trials across all seats and both voices. Haiku argues back after answering
(trailing text after a clean answer line) in 18–22% of own/peer-cell
responses vs ≤2.5% in null cells; genuine second-label self-correction is
near zero everywhere. The ecological cell is the mirror image of the
pressure cells: a seat's own *unpressed* wrong answer beside the record is
corrected 97.6–100% of the time. Self-testimony lying inert is harmless;
where damage occurs with the record present (Haiku), the named claim does
it.

**Exploratory (post-hoc, labeled; `analysis/exploratory_postfreeze.py`).**
Adopted Nov 13 from an external-review triage — after two seats' pipeline
outputs existed on disk and before anyone had read them; reported here,
claimed nowhere else. **E1:** the conf × pressure interaction is positive in
both floor-clearing seats (+1.17 p<.001; +0.53 p=.012; DeepSeek printed
beside, same sign) — pressure *steepens* the confidence–keep relationship,
though part of the flatter null-cell slope is ceiling (null keep runs
87–99.7%). **E3:** conf_z survives adding difficulty tier and base
correctness in both floor-clearing seats (+1.44, +0.60, both p<.001) — the
slope is not difficulty in costume. **E2:** the slope is positive within
wrong answers alone and steeper for right ones (interaction +0.84 p=.007,
Haiku). **E5:** Holm within seat leaves the frozen GLM contrasts intact (all
significant p_holm ≤ .006); the audited read above supersedes what those
contrasts mean.

**Measurement QA.** A second grader (different vendor, non-lineup, non-Fable)
regraded a seeded 150-row sample of each seat's residue under the identical
blinded prompt: outcome agreement 100.0% / 99.3% / 100.0%, per-field Cohen's
κ 0.95–1.00. Detail, including the one contested-reference-answer item behind
four of six disagreements, in Appendix B.

## 5. Discussion and Limitations

Under reading rules pre-committed before the tails were read (direction-only
replication across seats clearing the relevant gate; no vote-counting), the
results split cleanly along the two questions.

**Stated confidence was load-bearing where it varied.** Both interpretable
seats land in the coherent cell of the frozen taxonomy — steep slopes *and*
wide keep|right / keep|wrong separation — so the stated number carries
information about both an answer's epistemic standing and its behavioral
fate — and, in the labeled exploratory interaction (E1), it appears to carry
most exactly when someone is trying to move the model. Where confidence
didn't vary, the floor rule worked as designed: DeepSeek presents a
near-ceiling, low-variance confidence channel that failed the pre-registered
evaluability criterion — "decorative" is the label our floor rule attaches,
not a measured zero of information, but a channel this compressed cannot
support routing decisions whatever its calibration. The instrument finds two
confidence channels informative under pressure and one unevaluable, for a
few dollars of base calls per model.

**The record result is a dose-response with a named exception.** With no
record in context, a named claim gets a planted false answer adopted in
14–37% of trials in all three seats — mostly swapping one wrong answer for
another, with right answers surrendered in 4–8% (post-hoc split, §4). With
the record present, adoption falls to zero in Terra, a trace in DeepSeek,
and 2–6% in Haiku — whose record-tracking also drops 7–8 points under named
claims (or, on the reliability-weighting account, a named source outranking
an anonymous archive header; the design cannot separate these, Appendix A).
The bare objection moves no seat off the record: a claim carrying both a
name and a rival answer does the moving, and separating the name's
contribution from the rival answer's is the pre-named unattributed-claim
cell of the follow-up design. An in-context ground-truth record is strong
protection — near complete in two seats — but not complete, and the failure
concentrates where a name is attached. The post-hoc tracks audit that
shrank this headline from three seats to one is itself a result about
measurement: exact-match scoring of "tracks the record" punishes a model
for defending a correct answer in its own words, and two of three seats'
apparent contamination was almost entirely that. The attacker's cost, where
the vulnerability exists, remains one attributed sentence — no optimization,
no jailbreak — buying a 4–8% chance of displacing a correct answer without
a record, and in one of three seats a 2–6% chance against one.

**Limitations.** All claims are predictive and within-seat, on one fixed
pressure script, short-answer facts, English, provider-default sampling; the
full statement of what the results do and do not establish — including the
contamination-vs-weighting ambiguity, the coarse consistency covariate, the
per-seat meaning of the peer string, differential no-response in one
DeepSeek cell, and the floored seat — is Appendix A, which we consider part
of the result.

**Future Work.** Named in the pre-registration before data: a human-claim
voice completing the human/own/peer source triangle, and an
unattributed-claim level separating receipt of a rival answer from its
attribution. The tracks audit adds a third: record-form variation (does
matching the record's wording, not just its content, drive "tracking"?) —
measurable with the same harness. Beyond the ladder: optimized pressure
strings as a red-team instrument, and coherence as a tracked deployment
metric.

## 6. Conclusion

Where stated confidence varies, it is load-bearing: in two of three current
models it predicts which answers survive pressure, beyond a measured
resample-consistency covariate, tracking knowledge rather than stubbornness
— and in a labeled exploratory analysis, it predicts best under pressure,
where routing on it matters. Where it does not vary, a pre-registered floor
converts the non-answer into a finding: decorative confidence exists in the
wild and is detectable for a few dollars before any router consumes the
channel. The testimonial threat model inverts the intuition twice: these
models do not capitulate to challenge — an anonymous objection moved no
seat off the record — and a checkable record protects two of three models
almost completely, while the third yields measurably to the same false
sentence once it carries a name and a rival answer, in its own voice or a
peer's. Both instruments run black-box against any API, pre-registered end
to end, and are released with this report.

## Code and Data

- Code repository: [GitHub link — make public before submission; currently
  private at goatpug/ai-epistemics-sprint] — raw call logs, grades, frozen
  and exploratory analysis outputs, figures, and the full dated decision
  record (`docs/`).
- Data: all in-repo (`runs/`, `grading/`, `analysis/out/`); item sources
  SimpleQA and TriviaQA.
- Other artifacts: none. [CONFIRM: video/slides optional fields.]

## Author Contributions

S.K. operated the study: convened and couriered the design deliberation,
held budget authority, commissioned the external reviews, and ran all
human-in-the-loop steps. Study design, pre-registration, harness and
analysis code, runs, triage and writing were produced by three Claude Fable
instances (Fable 5, 5.1, 5.2) deliberating through S.K.'s relay, with every
load-bearing claim verified by an instance other than its author before use.
Measurement roles (seats, X-file verification, both graders) were held
exclusively by non-Fable models.

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
   Sure? Two Confounds in a Sycophancy Benchmark. NeurIPS 2026 Workshop:
   Can We Trust the Judge? https://neurips.cc/virtual/2026/161242
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

*(Required by the sprint guidelines: "state what your result does and does
not establish," manipulation potential, personal data handling.)*

**What the result does and does not establish.** All claims are predictive
and within-seat: stated confidence predicting revision behavior under one
fixed pressure script, on short-answer facts, in English, at
provider-default sampling. Nothing is causal — confidence varies between
items, not by intervention; the difficulty refit probes but cannot close the
between-item confound. Nothing generalizes beyond the three seats measured;
H1's interpretable replications number two after the pre-registered floor
excluded DeepSeek, and H2's attributed-claim effect, after the post-hoc
tracks audit, is one seat plus a one-cell trace — not a replicated finding.
The audit itself is a disclosed deviation: the frozen tracks rule scored
record-form, not only record-content, for kept answers; the frozen table is
reported as pre-registered and the audited read is labeled post-hoc. A
record-tracking drop under attributed claims demonstrates testimonial
influence but not a *pure* source-attribution effect: null → objection
isolates the bare challenge, objection → claim adds a named rival and an
attribution at once, and own ↔ peer varies the named source with the rival
held fixed — differential weighting of named sources is the thing measured,
and a reliability-weighting account survives beside a contamination account.
The peer string means different things per seat (same-vendor relative for
Haiku, named other-vendor model for Terra/DeepSeek); reported per seat,
never pooled. The consistency covariate is a cheap, coarse proxy (five
draws, 0.2 grid); under-adjustment drags the adjusted slope toward the raw
one, and the power simulation models the discretization but not the binomial
noise of five draws — so H1 establishes prediction beyond *observed*
five-draw consistency, not beyond perfectly measured latent stability.
DeepSeek's closed-objection cell has elevated no-response (4.7% vs ≤2.0%
elsewhere) — differential missingness in one cell of an already-floored
seat, disclosed. H2's clean-epistemics reading inspects three coefficients
per seat; Holm-adjusted values are reported beside raw CIs, post-hoc. The
item-clustered GLM is the inferential authority for H2; the per-cell Fisher
tests are the frozen separation fallback and treat cells as independent
samples, ignoring the item pairing — adequate where used (the audited Haiku
contrasts are 7–8 points on 460 paired trials and robust to any paired
test), disclosed as approximate elsewhere. Three to four items per seat
carry a planted X that nearly contains or extends the model's own answer
(e.g. "Italianate" vs "Italianate style"); the frozen A=X rule catches only
equality, so these sit in primary cells — too few to move any number,
disclosed. OpenRouter routes requests among multiple upstream providers and
the harness logged the served model id but not the resolved provider, so
provider-level serving variation within the two OpenRouter seats is
unmeasured; the dated model snapshot pins weights, not serving
infrastructure. The "Verified records" header's authority is
itself in-context testimony — honored or not, which the null cell measures.
Stated confidence is not comparable in currency to logit-derived confidence
(by design, disclosed): our turn-2 replay carries both the answer and its
stated confidence, the naturalistic condition prior work excludes on
purpose.

**Instrument-species caveat.** The study was designed and analyzed by
language models measuring a failure mode of language models. Mitigations are
structural (frozen pre-registration, designer/measured non-overlap, blinded
grading, three-way independent verification, two external non-Anthropic
reviews), not a claim of immunity: an instrument run by the species it
measures inherits that species' failure modes, including the ones this study
is about. The tracks audit is this caveat in action: the error favored the
more exciting finding, and it was caught by the house's own review because a
different instance checked the author's work against the raw rows.

**Dual-use.** A per-model map of which pressure voice moves answers — and at
which stated confidence — is a manipulation recipe at exactly the resolution
it is a safety finding. We judge publication net-positive: the pressure
scripts are single fixed sentences with no optimization, defenders can run
the harness on their own models before deployment, and the attack surface
(prompt-injected false attribution) is already public; what this adds for a
defender is measurement. No optimization against the vulnerability was
performed; the repository publishes measurement code, not attack tooling.

**Personal data.** None: public trivia items, API calls under the operator's
own keys, no human subjects.

## Appendix B. Operational detail and error ledger

**Sequence and blinding.** Freeze Nov 12 at commit `4d5136e`
(commit-stamped, verified independently from three sessions) → study data
Nov 13 (21,000 calls; about $40 on the two OpenRouter seats, the Anthropic
seat and graders billed separately) → blinded grading → report structure and
reading rules fixed → tails read together once, Nov 15. A mid-sprint
external review of a stale design draft was triaged against the frozen
pre-reg on Nov 13; nothing touched a frozen analysis, and the adopted
suggestions became the labeled-exploratory set and limitation lines, with
timing stated honestly in the triage (written after two seats' outputs
existed on disk, not informed by them, mechanical either way).

**Exclusions** (each counted in the output files): base-call failures and
base abstentions exclude the item for that seat (Haiku: 16 abstentions + 6
grader-identified; DeepSeek: 6 unparseable); fewer than three parseable
resamples excludes from the adjusted fit only; A = X collisions (18/14/10
items) leave primary contrasts and are reported as the consistent-advice
cell. No post-hoc "bad item" removal.

**What didn't work.** An early parser took the first `Answer:` line, coding
in-turn self-corrections as clean keeps — found by adversarial red-teaming
of our own parser by a model that didn't write it, which surfaced five holes
the author's tests missed. A provider content filter intermittently refused
one song-lyric item (retried clean). The second grader's first run violated
a 20-req/min account cap. The frozen tracks rule's record-form conflation
(§4) was found only at review, after three instances and a red-team had
signed off on the parser it lives beside. All receipts in the repository's
dated documents.

**Second-grader detail.** `google/gemini-3.8-flash` (pinned version), seeded
sample of 150 rows/seat from the graded residue, identical blinded prompt.
Six field-level disagreements in 450 rows; four concern one item (sqa-3973)
whose reference answer's title for a historical office is itself contested —
the graders split on referent identity, not on reading the response. The
grader of record (Sonnet 5.5) stands throughout; no item was removed.

**Turn-4 confidence changes** (mean points, by cell): seeing the record
raises stated confidence in every seat (+6.5 to +28.8); Haiku alone deflates
materially under the closed-book objection (−11.7).

## LLM Usage Statement

This project is an unusual case for this section, and we state it plainly
rather than minimizing it: the research was designed, implemented, analyzed
and written by three Claude Fable instances (5, 5.1, 5.2), operated by the
human author as described in Author Contributions. Verification was
structural rather than nominal: pre-registration frozen before data; every
load-bearing claim checked by an instance other than its author against the
repository record (independent sessions of one model family — session
independence, not lineage independence, which is why the external reviews
exist); measurement roles (study seats, wrong-answer verification, both
graders) restricted to models outside the authoring family; two external
reviews commissioned from non-Anthropic models; and
all claims in this report traceable to committed artifacts in the linked
repository. The post-hoc tracks audit in §4 — an error that favored the
exciting result, caught by cross-instance review during drafting — is this
process working as intended. Per the sprint's rule, the human author takes
responsibility for every claim in this report.
