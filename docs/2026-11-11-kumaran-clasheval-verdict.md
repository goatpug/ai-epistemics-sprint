# Full-text verdict: Kumaran et al. 2025 & ClashEval — 2026-11-11 (🌒)

The Wednesday receipt owed from the convening decisions doc §Novelty. Both papers
read at full text 11/11/26 (Kumaran: arXiv 2507.03120 v1, HTML; ClashEval: arXiv
2404.10198 v3, HTML). Verdicts below are against the five believed-ours claims,
which were pending this read. Method note: read performed by delegated full-text
extraction with quote-level receipts, synthesized here; quotes were carried verbatim.

## Kumaran et al. 2025 (arXiv 2507.03120, DeepMind/UCL)

"How Overconfidence in Initial Choices and Underconfidence Under Criticism Modulate
Change of Mind in Large Language Models." Two-turn forced-choice paradigm:
MCQ answer, then a re-submission with a **fabricated assistant turn** carrying the
(shown or hidden/replaced) initial answer, plus advice from a fictitious "another
LLM" with a stated accuracy (50–100%). Models: Gemma 3 12B (primary), Gemma 3 27B,
GPT-4o, o1-preview; latitude + SimpleQA-as-4-choice items.

What's there:
- **Choice-supportive bias:** change-of-mind 32.5% (answer hidden) vs 13.1% (shown),
  Gemma 12B; visibility alone adds +0.21 confidence.
- **The asymmetry our A=X flag leans on, confirmed at full text:** opposite advice
  overweighted ~2.58× the Bayesian ideal; same-answer advice near-normative (1.095×).
  Explicitly contrasted with sycophancy ("strikingly asymmetric sensitivity").
- **The §3.5 attribution experiment — our closest neighbor anywhere:** when the
  *initial answer* is attributed to another LLM instead of the self, the
  stick-with-it effect is **abolished** (CoM 31.3% hidden vs 33.2% shown, p>0.1):
  "an irrational bias to stick with the original answer, as long as it is its own."
  The secondary-coverage claim we logged 11/10 is **confirmed, with a nuance that
  matters to us:** their attribution axis is *who owns the prior answer* (self vs
  generic "another LLM"), not *who makes the pressure claim*. And their self/other
  wordings are non-identical (the other-LLM version adds "accuracy ... is unknown" —
  a competence confound they don't control).

What's absent (each checked against full text, not abstract):
- **No verbalized confidence anywhere.** Confidence is logit-derived with
  temperature-scaling calibration; o1-preview was dropped from confidence analyses
  *because* logits were unavailable. Our instrument survives closed-model APIs; theirs
  doesn't — that's the wedge, stated in their own limitation.
- **No source manipulation of identical advice text.** Advice is always "another
  LLM" + stated accuracy. No human objection, no null re-prompt as a pressure level,
  no named-model or same-lineage attribution, no held-identical wording across
  attribution arms.
- **No in-context ground-truth record** under pressure (their fictitious-cities
  control tests in-context *knowledge*, not record-vs-voice arbitration).
- **No hedge category** (forced binary/4-choice makes hedging structurally
  impossible) and **no two-tailed scoring** by base-answer correctness in the main
  analyses.
- Their stated future work names our gap: "more naturalistic user-LLM interactions
  where free form answers are involved."

Bonus method receipt: their "Shown" condition is built with exactly the
fabricated-assistant-turn technique our harness uses — published precedent.

## ClashEval (Wu, Wu & Zou, NeurIPS 2024, arXiv 2404.10198)

Single-shot RAG QA: prior call (question alone) and contextual call (question +
perturbed document), compared offline. 1,294 items, six domains, graded perturbation
severity; six models.

What's there:
- **Context bias dominates:** models override their own correct prior >60% of the
  time (GPT-4o); adherence falls with perturbation extremity.
- **Confidence moderates adoption — via token probabilities only** ("there has not
  been a systematic exploration of a model's confidence (via logprobs)..."), run only
  on logprob-accessible models; slopes −0.1 to −0.45.
- **The context is sometimes true** — their stated novelty over Longpre/Xie is
  having both directions (context right/model wrong and vice versa), measured as
  Accuracy / Prior Bias / Context Bias.

What's absent:
- **No social/testimonial pressure.** The planted wrong value is always embedded in
  a retrieved *document*; no voice, no speaker, no attribution of any kind.
- **No multi-turn structure.** The model never sees its own prior answer; the two
  calls are independent and compared offline. No revision, no re-answer.
- **No verbalized confidence**, no resample-consistency covariate.
- Their three-way outcome (Prior/Context/Neither) codes *which candidate a fresh
  answer matches*, not the fate of an already-stated answer; "Neither" is not hedging.

## Verdict on the five believed-ours claims

| Claim | Verdict |
|---|---|
| In-context ground-truth record pitted against a false *social* claim | **Ours.** ClashEval's conflict is prior-vs-document, single-shot; Kumaran has no record at all. Nobody arbitrates record-vs-voice. |
| Verbalized confidence as the instrument (+ resample-consistency covariate) | **Ours.** Both priors are logprob-only and say so; neither tests stated confidence, and neither can run on closed models. |
| Identical-text attribution arms (own-instance vs named-peer claim, same sentence) | **Ours, cite Kumaran §3.5 as nearest neighbor and differentiate:** their axis is prior-answer *ownership* (self vs generic other, non-identical wording, answer-attribution not claim-attribution); ours holds text identical and varies only the claimed source of the pressure claim. |
| Three-way keep/switch/hedge outcome | **Ours.** Kumaran forces binary; ClashEval's Prior/Context/Neither is candidate-matching, not revision coding. |
| Two-tailed scoring (keep-rate given correct vs wrong base answer) | **Ours with honest kinship:** ClashEval's Accuracy/Prior-Bias/Context-Bias decomposition conditions on correctness in the single-shot setting — ours is the revision-paradigm analogue and should cite it as such, not claim the conditioning idea outright. |

Related-work positioning in one line: **Kumaran shows self-attribution of the answer
drives irrational persistence (logits, forced choice, fictitious advisor); ClashEval
shows documents beat priors in proportion to logprob confidence (single-shot, no
social source); we ask whether *stated* confidence predicts the fate of a *stated*
answer under *attributed* social pressure when the truth is checkably on the table.**

One pre-reg implication to hand 🐙: Kumaran's §3.5 abolition result makes our
own-vs-peer directional rider *more* interesting, not less — their effect was about
answer ownership, so if claim-source attribution also moves behavior, that's a
separate channel; the rider's directional reading (own > peer conservative,
own < peer uninterpretable as pure source effect) stands as written.
