# Triage: external review #2 (Chipiti, of rev 1 / 07d6f07) — 2026-11-15 (🌒)

Second external review, commissioned by Sharon, run in parallel with sibling
review round 1. It reviewed rev 1, one revision behind the audit. Verdicts
against rev 2/3; nothing touches a frozen number. Convergence note worth the
header: Chipiti's #1 (attribution overclaim) is the same finding 🦝 raised in
round 2, from outside the family; its #2 (adopt-X vs tracks decomposition) is
the outsider's view of the seam the tracks audit closed from the rows.

## Adopted (in rev 3)

1. **"Attribution is the active ingredient" overclaim** — abstract,
   discussion, conclusion rewritten to "a claim carrying both a name and a
   rival answer"; the unattributed-X future cell named as the separator.
   (= 🦝 round-2 #1.)
2. **Open-book adopt-X separated from tracks failure** — STALE in part (rev 2
   did this via the audit: 5.7% / ≤0.4%); mechanism split added (own-voice
   adopts, peer-voice digs in; 🐙's texture).
3. **Stratify by base correctness** — adopted post-hoc, 🦝's table verified
   independently by 🌒 before use: 75–91% of closed-book adoptions replace
   already-wrong answers; right answers surrendered in a flat 4–8%. In §4
   secondaries, discussion, abstract.
4. **"Beyond observed five-draw consistency, not latent stability"** —
   wording adopted in abstract ("observed resample-consistency measure"),
   conclusion, and Appendix A sentence.
5. **E1 exploratory status in conclusion** — labeled.
6. **DeepSeek "cannot carry information" softened** — "near-ceiling,
   low-variance channel that failed the pre-registered evaluability
   criterion; 'decorative' is the floor rule's label, not a measured zero."
7. **Fisher vs paired data** — clause added to Appendix A: item-clustered GLM
   is the inferential authority; Fisher is the frozen separation fallback,
   ignores pairing, robust where used (audited Haiku contrasts), approximate
   elsewhere.
8. **Record form named** — §3 now states verbatim form + the pilot demotion
   rule.
9. **OpenRouter resolved provider** — logs carry served model id and per-call
   cost but not the resolved upstream provider (checked 11/15); cannot be
   retrofitted. Disclosed in Appendix A as a reproducibility limitation.
10. **Fig 2** — "null re-prompt" label, n per panel; peer-string per-seat
    meaning goes in the Doc caption.
11. **Kumaran competence-confound softened**; "future-work line describes
    this design" already cut in rev 2 (STALE).
12. **Xiong positioning** — credit their confidence+consistency pairing; our
    novelty restated as behavioral fate.
13. **Lineage vs session independence** — LLM statement now says it.

## Declined, with reasons

- **H2 omnibus test**: not in the frozen plan; the audited read makes the
  per-cell pattern the result, and adding a new post-hoc omnibus now would
  be test-shopping in the direction that flatters us.
- **Forest plot of model-based contrasts**: right in principle; out of space
  in a 4-page sprint report. The GLM contrasts with CIs are in the text and
  output files.
- **ClashEval "more prominence"**: §2 already leads its paragraph and §4/§6
  use its decomposition; further expansion loses the length fight.
- **Abstract Holm labeling**: STALE — rev 2's abstract no longer cites Holm.

## Noted

Chipiti reviewed rev 1 and independently recommended organizing the
discussion around the two findings rev 2 had already reorganized around
(confidence behaviorally informative but not uniform; record adherence high
but not attribution-proof). Credited here as convergence, not adopted as
change.

## Addendum: Haiku 5.5's solo review (full text via Sharon, same rev 1)

Already fixed by rounds 1–2: Fisher two-exceptions, hit-rate formula, point
ranges, abstract length, Holm placement, H2 attribution language, E1
conclusion label, "collapsed," floored-seat replication counts, process-text
cuts (header stays as draft metadata; stripped at Doc fill).

Newly adopted from Haiku's list (rev 3.1): null-cell slope "far smaller" →
"lower" (Terra's 0.61 vs 0.82 is not far); conclusion "two of three models"
→ "both models where it varied enough to test"; pilot-IQR-10.0 clause beside
the floor verdict (also a pre-reg §4 reporting requirement — good catch);
abstract 'decorative' in scare quotes (label, not diagnosis); E2
stubborn-component qualifier beside the frozen tails reading; full row
accounting in Appendix B (3,952 = 494×8 after skipped unparseable-base
items; adjusted n 1,406 = raw 1,409 − the one consistency-NaN item's 3
trials — verified by recomputation, nothing unexplained); QA/call-count
figures now cite their files, second-grader report committed to
analysis/out/; LLM statement points at the committed check documents.

Declined: cutting "What didn't work" (the template asks for it); conclusion/
abstract merge and secondaries-to-three-sentences (length is inside the 4–8
page band; further compression trades away Execution Quality receipts);
NeurIPS critique to a footnote (it motivates the design's wording controls).
Refs 6/7/8/11: already cited in §2 (Haiku reviewed rev 1, where they
weren't). [CONFIRM] tags: Sharon's, flagged to her for pre-submission.
