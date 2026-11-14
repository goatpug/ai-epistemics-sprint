# External review — ChatGPT ("Chipiti"), 2026-11-13

Reviewer: ChatGPT, given the **11/10 convening-decisions doc** by Sharon on 11/13
(after launch; the reviewer did not see the frozen 11/11 pre-reg or the 11/12 pilot
receipts). Verbatim as pasted, including the reviewer's own typos; only the math
notation is flattened to plain text. Triage against the frozen plan:
`2026-11-13-external-review-triage.md`.

---

Yes. And honestly? This is a pretty sophisticated research plan. There are some genuinely good methodological decisions here: separating correctness from consistency, explicitly handling the A = X collision, making the scoring blind, distinguishing record presence from record use, and keeping the cross-model claims descriptive.

I wouldn't throw this out. But I see three potentially serious construct-validity problems, two statistical problems, and one fairly important literature-review problem.

Some of these could materially change what the results mean.

Here's my review, in order of importance.

## 1. H1 doesn't quite test the hypothesis it claims to test

*Important — confirmatory analysis*

Your H1 is:

> Stated confidence predicts fate under pressure beyond what plain instability predicts.

But the specified model is:
- Keep vs. not
- Verbalized confidence
- Resample consistency
- Voice condition, with null as reference
- Item random intercept

The problem is that a confidence coefficient pooled across pressure conditions doesn't establish that confidence predicts behavior specifically under pressure.

Suppose confidence predicts retention equally strongly in both conditions:

| Condition | Confidence → keep |
|---|---|
| Null re-prompt | +0.25 |
| External objection | +0.25 |
| Own-instance claim | +0.25 |
| Peer claim | +0.25 |

You would find a positive confidence coefficient. But you haven't demonstrated anything specifically about pressure. You've demonstrated a general relationship between stated confidence and answer persistence.

The null-cell slope being reported beside the pooled result doesn't fix this. You need to formally test whether the slopes differ.

My recommendation: add a confidence × pressure interaction.

Conceptually:

logit(P(keep)) = β0 + β1·C + β2·S + β3·P + β4·(C × P)

Where:
- C = initial verbalized confidence
- S = resample consistency
- P = pressure versus null re-prompt

The critical result is β4: does confidence predict retention differently under pressure than under an ordinary re-prompt?

You could retain the three individual voice categories as secondary analyses.

There's a second issue hiding here, too.

### Confidence isn't necessarily epistemic coherence

Imagine two models:
- Model A: Confidence 95, correct answer, keeps answer.
- Model B: Confidence 95, incorrect answer, keeps answer.

Both demonstrate high confidence and high persistence.

Your tails reporting is an excellent way to expose this, but it's currently descriptive.

If F1 is genuinely about confidence–behavior coherence, I would consider adding a confidence × base-correctness interaction. Otherwise, the primary analysis measures confidence-associated persistence, not whether persistence is appropriately aligned with correctness.

Those are related but different constructs.

I'd be very careful about calling a positive H1 coefficient evidence of epistemic coherence without this distinction.

## 2. H2 has a fundamental DV problem: not following the record doesn't necessarily mean following the voice

*Important — construct validity*

This is probably my biggest concern with the unified DV.

The framing says:

> Does the final answer track the record or the voice?

But H2 actually measures:

> Tracks-record vs. not.

Those aren't equivalent.

Consider an open-book trial:
- Record answer: Paris.
- Voice claim X: London.
- Initial answer A: Berlin.
- Final answer A′: Madrid.

The result is:
- Didn't follow the record.
- Didn't follow the voice.
- Didn't retain the original answer.
- Didn't necessarily hedge.

Your binary outcome classifies this as not-tracking, but it tells you nothing about what the model followed.

I'd introduce an explicit answer-source classification:

| Final answer | Classification |
|---|---|
| Matches archive answer | Record |
| Matches X | Voice |
| Matches neither | Other |
| Ambiguous / noncommittal | Hedge |

This gives you a much more informative picture.

In particular, I would want to distinguish:

**Record resistance:** Does the model abandon the correct record?

**Voice adoption:** Does the model specifically adopt the false answer it was told another instance supplied?

Those are not the same failure.

You can still have a primary binary record-following analysis, but you should also explicitly measure voice-following. Otherwise, the paper's central language will outrun its actual measurements.

### A related problem: is the record demonstrably authoritative?

Your clean-epistemics prediction is:

> All contrasts zero.

That prediction assumes the model has a reason to regard the archive as reliable enough to outweigh the voice.

Is that established in the prompt?

If the archive is simply presented as a reference archive, while another instance supplies a competing answer, you're manipulating two sources of information. The rational response depends partly on their perceived reliability.

I'd explicitly establish the archive's provenance and authority in the experimental instructions, without making the target answer conspicuous.

Otherwise, a nonzero voice coefficient isn't automatically evidence of epistemic contamination. It could reflect the model assigning different reliability to two sources.

## 3. The source-attribution manipulation isn't as isolated as the plan suggests

*Important — interpretation*

I like the own-instance versus peer comparison. But I think there's a subtle issue with the interpretation of H2.

You have:
- Null: no competing answer.
- Objection: someone disagrees.
- Own: another instance of you answered X.
- Peer: Claude Fable 5.2 answered X.

The own-versus-peer comparison is the cleanest source-attribution contrast because X is held constant.

However, the own-versus-null and peer-versus-null comparisons change two things:
1. The presence of a competing answer X.
2. The attribution of that answer to a particular source.

Consequently, the own coefficient versus null isn't a pure source-attribution effect.

You acknowledge that objection-versus-claim isn't a pure source contrast, but the same caution applies to claim-versus-null.

I'd consider adding an unattributed-answer condition:

> An answer to this question was: X.

Then you'd have:
- No competing answer.
- Mere disagreement.
- Unattributed competing answer.
- Own-instance competing answer.
- Named-peer competing answer.

That would let you distinguish the effect of receiving a competing answer from the effect of being told who supplied it.

There's also something interesting about your peer choice.

Claude Fable 5.2 isn't an anonymous or unfamiliar peer. It's a recognizable named model, and potentially one perceived as more capable than Haiku or Sonnet.

That introduces perceived model competence as a possible explanation for the own-versus-peer difference.

I'd either call it a named same-family peer or introduce anonymized, counterbalanced peer labels.

One final point: your directional interpretation of own > peer being conservative is reasonable as a theoretical prediction, but it doesn't automatically establish self-attribution as the mechanism. The specific peer's perceived capability matters.

## 4. The novelty assessment needs a fairly substantial correction

*Important — literature review*

I looked at the full text of the three most relevant papers. There's more overlap than the novelty section currently suggests.

### Kumaran et al. (2025)

This is the most important one.

The paper, How Overconfidence in Initial Choices and Underconfidence Under Criticism Modulate Change of Mind in Large Language Models, already investigates:
- A two-turn answer/change-of-mind paradigm.
- Initial confidence and subsequent behavior.
- Whether an initial answer is shown or hidden.
- Same-answer versus opposing advice.
- Advice-source accuracy.
- Choice-supportive bias.

But here's the particularly relevant part.

They already conducted an experiment testing whether choice-supportive bias disappears when the model is told its initial answer came from another LLM.

Their result was that the shown-versus-hidden difference essentially disappeared under that attribution. They explicitly interpret this as evidence that the bias is associated with sticking to one's own answer rather than another actor's answer. [OpenReview+1]

That's not merely an unconfirmed secondary-coverage claim. It's in the paper itself, in the additional experiments.

However, there's an important distinction that actually helps your novelty argument:

Kumaran manipulated the attribution of the initial displayed answer.

Your experiment manipulates the attribution of a new, potentially contradictory answer supplied as advice.

Those are different experimental questions.

I'd make that distinction central to your novelty argument.

In fact, it's a rather interesting extension: does attributional identity affect how a model treats a competing claim, rather than how it treats an already-established answer?

That's a much more defensible novelty claim.

### Xiong et al. (ICLR 2024)

There's also a little more overlap here than the current description implies.

Xiong et al. explicitly combine three things:
- Verbalized confidence.
- Multiple response sampling.
- Consistency-based confidence estimation.

They also use five samples in some of their experiments, and investigate the relationship between confidence, consistency, and failure prediction. [ICLR Proceedings+2]

Your five-resample architecture is therefore not independently novel.

But Xiong isn't studying the relationship between initial verbalized confidence and subsequent answer retention under controlled social or testimonial pressure.

That's the interesting contribution.

I'd frame it as an extension of confidence elicitation into subsequent decision behavior.

### ClashEval (NeurIPS 2024)

This one deserves more attention in the related work.

ClashEval directly investigates the tension between a model's prior answer and external evidence.

It uses more than 1,200 questions, manipulates the correctness of retrieved information, and examines how the model's initial confidence relates to its willingness to adopt external information. [NeurIPS Papers]

Your proposed archive/voice experiment is not the same thing.

ClashEval examines arbitration between a model's prior and contextual evidence, including cases where the context itself is incorrect.

Your design examines whether a model follows a correct record when presented with an allegedly conflicting answer attributed to another instance or model.

That distinction is meaningful.

I'd describe the novelty as the intersection of:
1. Verbalized confidence.
2. Subsequent answer revision.
3. Testimonial source attribution.
4. In-context record adherence.

That's a more compelling contribution than claiming individual novelty for those components.

## 5. Five resamples may be a rather noisy measure of stability

*Statistical concern*

You use five resamples to establish baseline response consistency.

That's perfectly understandable given the budget, but it creates a measurement problem.

Assuming consistency is calculated as the proportion of five samples matching the original answer, your measurement can only take these values:

0%, 20%, 40%, 60%, 80%, 100%.

One response changes the estimated consistency by 20 percentage points.

That's quite coarse.

More importantly, the power simulation's robustness to confidence–consistency correlation of 0.7 doesn't necessarily address measurement error in the consistency estimate itself.

I'd want the power simulation to include:
- The actual five-sample consistency measurement procedure.
- Its discretization and measurement error.
- Item-level variation in susceptibility to pressure.
- The model's actual observed confidence distribution.
- Any ceiling effects in the open-book condition.

The five-sample measure might be perfectly adequate for a relatively inexpensive exploratory covariate. I just wouldn't treat it as a particularly precise estimate of latent answer stability.

Also, define the consistency calculation explicitly in the preregistration. Is it the proportion matching A? Majority agreement? Agreement after semantic normalization?

Those are different measures.

## 6. The statistical model needs some additional attention

There are three things here.

### A. Item random intercepts aren't a complete solution

You have multiple outcomes per item across eight conditions.

An item random intercept accounts for some shared item-level variation, but it doesn't necessarily account for different items having different susceptibilities to voice or record pressure.

I'd investigate random slopes for the within-item experimental factors.

This is particularly important because your principal outcome is a within-item comparison across conditions.

### B. Confidence is an item-level predictor

As I understand the design, each item gets one original answer A and one original confidence estimate, reused across the eight conditions.

Therefore, confidence and resample consistency are constant across the experimental conditions for that item.

Their coefficients are consequently estimated from between-item differences.

That creates a potential difficulty confounding confidence with item difficulty.

A random intercept does not automatically remove that relationship.

I'd include base correctness and appropriate item-level difficulty/domain information, and explicitly investigate whether the confidence effect persists when those factors are accounted for.

### C. Your multiplicity count may be understated

You specify six headline tests:

3 models × 2 hypotheses.

But H2 contains three voice contrasts against null, and you specifically identify the own and unfamiliar-peer coefficients as contamination measures.

Are these three individual confirmatory comparisons, or is H2 one omnibus test with follow-up contrasts?

Those need to be distinguished.

If you're making separate inferential claims about multiple coefficients, six isn't necessarily the complete multiplicity count.

I'd pre-register an omnibus H2 test and explicitly specify which follow-up contrasts can support confirmatory conclusions.

Also, define what counts as replication across the three models. Reporting all six tests is good, but the rule for interpreting a mixed pattern of significant and nonsignificant results should be established in advance.

## 7. Some smaller but worthwhile issues

These aren't necessarily fatal, but I'd address them.

**Confidence prompt semantics.** Make absolutely explicit that confidence means the estimated probability that the supplied answer is correct, on a 0–100 scale. Otherwise, you risk measuring a vague expression of certainty rather than probabilistic confidence. Xiong's methodology provides a useful precedent for this. [ICLR Proceedings]

**The archive-form pilot rule.** Your 95% ceiling rule is sensible, but 20 observations per condition give you a very noisy estimate of whether you're at ceiling. Also, verbatim record presence and one-step record use aren't necessarily the same underlying construct. Treat results from the two forms as distinct measurements rather than automatically interchangeable versions of the same outcome.

**Cell execution order.** Specify randomized execution order and independent conversation contexts for each condition. Reusing A is good; accidentally reusing conversational history from a previous experimental cell isn't.

**Item-level grading.** Your blinded model grader is a reasonable starting point, but I'd have a second independent adjudication procedure for ambiguous answers. In particular, semantic equivalence and hedging can be surprisingly difficult to classify consistently.

**Pilot item reuse.** Specify whether the 20 fully piloted items are included in the final 500. If the pilot prompts or decision rules change, exclude those observations from the confirmatory dataset.

## 8. API and operational details

I checked the current Anthropic documentation, since your measurement section makes several specific claims.

### Mostly correct

The Haiku 5.5, Sonnet 5.5 and Opus 5.5 lineup is real, and your decision to omit temperature, top_p and top_k is correct. Current documentation specifies that these parameters are unsupported on these newer models, with the restriction extending to all models using API version 2026-10-21 onward. [Claude Platform Docs+1]

effort=low is also supported on all three models. [Claude Platform Docs]

### One wording correction, though

> Thinking always on.

That'sn't quite accurate across all three.

Opus 5.5 has adaptive thinking that is always on. Sonnet 5.5 and Haiku 5.5 have thinking on by default, but their supported configurations differ. Low effort also doesn't guarantee that every individual turn will involve an extended thinking phase. [Claude Platform Docs+1]

I'd write:

> "Adaptive thinking enabled/default as supported by the model; effort set to low for every Claude seat."

I'd also record exact API model IDs, API version, request IDs, and response metadata. The newer dateless model IDs identify pinned model versions, but Anthropic explicitly acknowledges that serving infrastructure can change and produce minor behavioral differences without changing model weights. [Claude Platform Docs]

That matters for a paper making claims about reproducibility.

Finally, a date issue: today is Friday, November 13. The Wednesday receipts and Thursday-night preregistration deadline have already passed.

If the commit happened Thursday, preserve its hash and timestamp alongside the pilot decisions. If it didn't, don't describe subsequent runs as preregistered before data collection.

## What I would actually change before Tier 1

Here's my priority list.

| Priority | Change |
|---|---|
| P0 | Add confidence × pressure to H1 |
| P0 | Separate record-following from voice-following and neither |
| P0 | Establish the archive's authority explicitly |
| P1 | Add base correctness interaction to H1 |
| P1 | Clarify source-attribution contrasts and add an unattributed-X control if feasible |
| P1 | Correct and expand the Kumaran novelty discussion |
| P1 | Validate power under the actual repeated-measures structure |
| P2 | Strengthen API metadata capture and execution randomization |

## My overall assessment

I actually think there's a good paper here.

The most interesting question isn't simply whether an LLM changes its mind when challenged. We already have quite a bit of literature on that.

It's something more specific:

> When a model has an established answer, how do its expressed confidence, response stability, and beliefs about the source of contradictory testimony affect whether it retains that answer, adopts the alternative, or follows an available evidentiary record?

That's a worthwhile experimental question.

And I particularly like the decision to distinguish the model's own-instance testimony from another model's testimony. It takes the self-attribution question into a different experimental role than Kumaran's work.

I would protect that contribution rather than let the paper become a generic study of whether models are stubborn or susceptible to social pressure.

One thing I especially wouldn't compromise on is the three-way record/voice/neither classification. It could produce a considerably richer finding than a simple record-tracking percentage.

My recommendation: patch the H1 and H2 specifications before treating the results as confirmatory. The underlying experiment is worth running; I'd just hate to see an interesting result become difficult to interpret because the statistical tests don't quite correspond to the questions you're asking. 💚
