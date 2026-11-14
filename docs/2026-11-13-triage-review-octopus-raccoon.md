# Review of the external-review triage — 2026-11-13 (🐙 + 🦝, consolidated by 🐙, carried by Sharon)

Both of us read `2026-11-13-external-review-triage.md` against the frozen pre-reg (4d5136e, tree d073fe2bbfdb) and the repo, independently, Friday afternoon. Four catches were found by both seats; three by 🦝 alone; three by 🐙 alone. Neither of us has read a study number: the `analysis/out/*.json` files were inspected with key names only, values masked.

## Bottom line (both)

The triage holds. Nothing in the review requires touching frozen code, and nothing has been: `git diff 4d5136e HEAD -- analysis/ harness/ stimuli/` shows only the two new `analysis/out/*.json` files, and the pre-reg doc differs from the freeze by the stamp line alone. Every FROZEN-IN verdict we spot-checked matches the frozen text (§5 H1 on pressure trials only with the null slope beside, never pooled; §2 three-way coding with adopt-X and tracks-record as separate columns; §5 record-honoring <50% rule; §6 objection-vs-claim caveat and the stubbornness reading rule; §2 loose_same with ≥3 parseable else NaN; §9 diff 1 cluster-robust GLM primary; `voices.json` turn-1 confidence wording verbatim what the reviewer asked for). The "4 stale" count is right. 6C (H2 multiplicity) is correctly called the sharpest hit. Timeline receipted from the repo: freeze commits 11/12 15:08 PT, first study run directory 11/13 10:47 PT.

## Fixes, in order of weight

1. **"Adopted before any study tail is read" is not supportable as written (both).** Folding grades means running the frozen script, which prints the tails, H1 and H2 to the terminal and writes `h1_adj_conf_slope` and all four H2 coefficients to `analysis/out/<seat>.json`. Haiku's output was committed at 12:11, DeepSeek's at 15:53, the triage at 16:04; DeepSeek's floor verdict is quoted in its own commit message. So for two of three seats the headline numbers were on a screen and in the repo before the pre-look rules were written. Neither of us thinks anything was tuned (Holm and the replication rule are mechanical, and the five adoptions are exploratory/limitation/QA that would be adopted whatever the numbers say; the label is what makes them honest, not the sequence). The honest sentence: *written after Haiku and DeepSeek outputs existed on disk, before Terra completed, and not informed by them.* Testimony, stamped as testimony.

2. **"Seats clearing the floor" needs "for H1" (both).** The floor gates H1 only (§4). DeepSeek failed it (IQR 5.0 < 10), so H1 has two replications, Haiku and Terra. H2 still has three. As written the rule drops DeepSeek from H2, where it has every right to be.

3. **"Added to §8b's ladder, dated today" didn't happen (both).** The pre-reg's only post-freeze edit is the stamp. "Unattributed" appears nowhere in the repo except the triage. Adding the unattributed-X cell to §8b is allowed (future work, not a confirmatory analysis; dated and marked per the stamp). Either make the edit or change the sentence to "to be added."

4. **The power-sim concession is slightly over-conceded (both).** `powersim.py:39` rounds latent consistency to the five-resample grid (steps of 0.2), so the coarse grid *is* simulated. What isn't simulated is the sampling noise of five draws from a latent stability. The methods sentence should say exactly that, or it undersells the sim in one direction and oversells it in the other.

5. **Own-vs-peer gets promoted and contradicted in the same doc (🦝).** Triage §2 says it "survives" the source-reliability objection and calls it "the paper's protected contribution"; triage §3 then concedes the perceived-competence confound on exactly that contrast. The frozen plan has own-minus-peer as a secondary Wald, with own < peer "uninterpretable as a pure source effect"; the frozen H2 headline is voice-vs-null. The attribution-with-ownership-fixed *design* can be the novelty wedge without the secondary *test* quietly becoming the headline. "Protected contribution" is the triage's phrase; it isn't in the convening docs.

6. **§3's FROZEN-IN is a stretch; make it a LIMITATION (🦝).** The §6 caveat covers objection-vs-own and says nothing about claim-vs-null, while §5 calls the own and peer coefficients against null "the contamination numbers." Chipiti's point (own-vs-null bundles *naming a rival answer* with *attribution*) lands harder than the triage admits. One limitation sentence, with the decomposition the ladder already gives: null → objection isolates the bare challenge, objection → claim adds a named rival, own ↔ peer isolates attribution; "contamination" in §5 means contamination by testimony, not a pure source effect.

7. **The review itself isn't in the repo (🦝).** We can check the triage against our record but not against what Chipiti actually said. "A third stamp from outside the family" is also generous: agreement from a reader isn't a stamp in the house sense (nothing was measured). Sharon, please drop the raw review into `docs/`.

8. **The four-way cross-tab needs a place for "kept a wrong A" (🦝).** Record / voice / other / hedge has no keep cell, so "other" will be mostly that. Five-way, or keep split by base correctness, which the §6 tails already do.

9. **Second-grader QA: different vendor from Sonnet 5.5, and not a Fable (🐙).** Same-vendor agreement is weaker QA, and Sharon's Fable budget is for relays and the write-up, not grading.

10. **Claim-language discipline on H1 (🐙, agreeing with triage §1).** The paper claims "confidence predicts the fate of the answer under pressure beyond instability"; it does not claim "pressure changes the confidence–keep relationship." The conf × pressure interaction on null + pressure trials is the right exploratory for the second claim and should be labeled as the only place that claim is tested.

## Operational, Terra (🐙, as of 16:18 PT)

Base complete, 3000/3000; four 429s, all retried clean. Pressure at 3339/4000, running at the 20 rpm cap (~20.3/min), so it lands around 16:50. **Four pressure calls 429'd with no successful retry in the log yet**; after the run exits, run the resume pass *before* exporting residue, or those four become `no_response` exclusions that didn't need to exist. Haiku's 3004 base rows are the content-filter item from the runbook plus its retries; the analysis skips error rows and keeps the last good record, so the count is cosmetic.

## Housekeeping

Stage by path in the shared checkout (one working tree). Every edit above is to the triage doc or to §8b, dated post-freeze; nothing touches `prereg_analysis.py`.
