"""POST-HOC EXPLORATORY analyses — adopted 2026-11-13 from the external review
triage (docs/2026-11-13-external-review-triage.md), written 2026-11-14 (🌒).

Nothing in this file is confirmatory. Every fit here is labeled post-hoc in the
report and reported in the discussion, never beside the frozen headlines as an
equal. The adoptions were pre-committed in the triage before any study tail was
analyzed (timing stated honestly there, §6C); this script implements them:

  E1  conf × pressure interaction (triage §1, 🐙's framing, sibling review #10):
      keep ~ conf_z + cons_z + pressure + conf_z:pressure on closed-book
      null + pressure trials. The ONLY place "pressure changes the
      confidence-keep relationship" is tested; the frozen H1 never claims it.
  E2  conf × base-correctness interaction (triage §1): does the confidence
      slope differ when A is right vs wrong (stubbornness vs knowledge)?
  E3  difficulty refit (triage §6B): frozen H1 adjusted fit + item difficulty
      tier + base correctness as covariates; does conf_z survive?
  E4  five-way outcome cross-tab (triage §2, 🦝 sibling review #8):
      keep (split by base correctness) / record / voice / other / hedge,
      per cell. Presentation of columns the frozen coding already has.
  E5  Holm correction within seat on H2's three voice contrasts (triage §6C),
      printed beside the raw CIs, labeled post-hoc.

Coding, exclusions, grades folding: imported from the frozen script
(prereg_analysis.py, frozen at 4d5136e). This file re-derives nothing.

Usage (same flags as the frozen script):
  .venv/bin/python analysis/exploratory_postfreeze.py --seat haiku \
      --items stimuli/items.jsonl --grades grading/haiku-all-grades.jsonl
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prereg_analysis import (  # noqa: E402
    ROOT, VOICES, PRESSURE_VOICES, load_jsonl, build_base_table,
    build_trial_table, fit_logit, coef_table, pct,
)


def fold_base_grades(base_df, grades):
    """Base-correctness grades + grader-hedge exclusion, exactly as the frozen
    script's main() does it (prereg_analysis.py; copied, not re-derived)."""
    base_df["A_correct"] = base_df["A_exact_correct"]
    base_hedged = set()
    for item_id, g in ((k.split(":base")[0], v) for k, v in grades.items() if ":base" in k):
        if g.get("hedge"):
            base_hedged.add(item_id)
        base_df.loc[base_df.item_id == item_id, "A_correct"] = bool(g["correct"])
    return base_df[~base_df.item_id.isin(base_hedged)].reset_index(drop=True)


def five_way(row):
    """E4 categories. 'record' = committed to the truth (the record's content,
    open book; same computation closed book, where it reads switch-to-truth);
    'voice' = adopted the planted X; keep is split by base correctness so a kept
    wrong A has its own cell instead of vanishing into 'other' (🦝, review #8)."""
    if row.outcome == "keep":
        return "keep|A right" if row.A_correct else "keep|A wrong"
    if row.outcome == "hedge":
        return "hedge"
    if row.outcome == "switch":
        if row.adopt_x is True:
            return "voice (X)"
        if row.correct:
            return "record/truth"
        return "other switch"
    return "unresolved"  # ungraded / no_response; counted, never silently dropped


def holm(pvals):
    """Holm step-down adjusted p-values, order preserved. NaN inputs (unidentified
    contrasts, e.g. a separated cell) stay NaN and are excluded from the family."""
    pvals = np.asarray(pvals, dtype=float)
    adj = np.full(len(pvals), np.nan)
    valid = np.where(~np.isnan(pvals))[0]
    m = len(valid)
    order = valid[np.argsort(pvals[valid])]
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, (m - rank) * pvals[idx])
        adj[idx] = min(1.0, running)
    return adj


def report_fit(fit, names):
    """coef_table plus a separation note: a NaN CI or runaway coefficient means
    the fit is printed, not interpreted (same reading rule as the frozen H2 guard)."""
    print(coef_table(fit, names))
    if isinstance(fit, str):
        return
    ci = fit.conf_int()
    bad = [n for n in names if n in fit.params.index
           and (np.isnan(ci.loc[n]).any() or abs(fit.params[n]) > 15)]
    if bad:
        print(f"  NOT IDENTIFIED ({', '.join(bad)}): separation or near-separation;"
              " coefficients printed, not interpreted.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seat", required=True)
    ap.add_argument("--items", required=True)
    ap.add_argument("--runs", default=os.path.join(ROOT, "runs"))
    ap.add_argument("--form", default="verbatim")
    ap.add_argument("--grades", help="JSONL of grader verdicts keyed by call_key")
    args = ap.parse_args()

    items = load_jsonl(args.items)
    difficulty = {it["id"]: it.get("difficulty", "n/a") for it in items}
    base_rows = load_jsonl(os.path.join(args.runs, args.seat, "base.jsonl"))
    pressure_rows = load_jsonl(os.path.join(args.runs, args.seat, f"pressure-{args.form}.jsonl"))
    grades = {g["call_key"]: g for g in load_jsonl(args.grades)} if args.grades else {}

    base_df, _ = build_base_table(base_rows, items)
    if not len(base_df):
        print("no usable base rows; stopping")
        return
    base_df = fold_base_grades(base_df, grades)
    trials, _, _ = build_trial_table(pressure_rows, base_df, grades)
    if not len(trials):
        print("no pressure rows; stopping")
        return

    primary = trials[~trials.a_eq_x].copy()
    # Same standardization as the frozen script: over all primary trials.
    primary["conf_z"] = (primary.confidence - primary.confidence.mean()) / primary.confidence.std()
    primary["cons_z"] = (primary.consistency - primary.consistency.mean()) / primary.consistency.std()
    primary["difficulty"] = primary.item_id.map(difficulty)
    closed = primary[primary.book == "closed"]

    print(f"# POST-HOC EXPLORATORY — seat {args.seat}, form {args.form}")
    print("# Adopted pre-committed in the 11/13 triage; every fit below is labeled")
    print("# post-hoc and reported in the discussion, never as a headline.\n")

    print("## E1 — conf × pressure interaction (closed book, null + pressure cells)")
    print("#  The only test of 'pressure CHANGES the confidence-keep relationship'.")
    e1 = closed.copy()
    e1["pressure"] = (e1.voice != "null").astype(float)
    f1 = fit_logit(e1.dropna(subset=["cons_z"]), "keep", "conf_z + cons_z + pressure + conf_z:pressure")
    report_fit(f1, ["conf_z", "cons_z", "pressure", "conf_z:pressure"])

    print("\n## E2 — conf × base-correctness (closed book, pressure voices)")
    print("#  Does the slope ride on wrong answers (stubbornness) or right ones?")
    e2 = closed[closed.voice.isin(PRESSURE_VOICES)].copy()
    e2["A_right"] = e2.A_correct.astype(float)
    f2 = fit_logit(e2.dropna(subset=["cons_z"]), "keep",
                   "conf_z * A_right + cons_z + C(voice, Treatment('objection'))")
    report_fit(f2, ["conf_z", "A_right", "conf_z:A_right", "cons_z"])

    print("\n## E3 — difficulty refit of H1 (triage §6B: between-item confound check)")
    print("#  Frozen adjusted H1 + difficulty tier + base correctness; does conf_z survive?")
    f3 = fit_logit(e2.dropna(subset=["cons_z"]), "keep",
                   "conf_z + cons_z + C(voice, Treatment('objection')) + C(difficulty) + A_right")
    report_fit(f3, ["conf_z", "cons_z", "A_right"])

    print("\n## E4 — five-way outcome cross-tab (presentation of frozen columns)")
    tab = primary.copy()
    tab["cat"] = tab.apply(five_way, axis=1)
    cats = ["keep|A right", "keep|A wrong", "record/truth", "voice (X)",
            "other switch", "hedge", "unresolved"]
    header = "  cell                 n  " + "".join(f"{c:>14}" for c in cats)
    print(header)
    for book in ("closed", "open"):
        for voice in VOICES:
            c = tab[(tab.book == book) & (tab.voice == voice)]
            if not len(c):
                continue
            shares = "".join(f"{pct((c.cat == k).mean()):>14}" for k in cats)
            print(f"  {book:<6} {voice:<11} {len(c):>5}{shares}")

    print("\n## E5 — Holm within seat on H2's three voice contrasts (beside raw CIs)")
    open_ = primary[primary.book == "open"]
    h2 = fit_logit(open_, "tracks", "C(voice, Treatment('null'))")
    if isinstance(h2, str):
        print(f"  {h2}")
    else:
        names = [n for n in h2.params.index if n.startswith("C(voice")]
        raw = np.array([h2.pvalues[n] for n in names])
        adj = holm(raw)
        ci = h2.conf_int()
        def fmt(x):
            return "n/a" if np.isnan(x) else f"{x:.3f}"
        for n, pr, pa in zip(names, raw, adj):
            v = n.split("T.")[-1].rstrip("]")
            note = "  (not identified: separation)" if np.isnan(pr) else ""
            print(f"  {v:<10} b={h2.params[n]:+.3f}  [{ci.loc[n, 0]:+.3f}, {ci.loc[n, 1]:+.3f}]"
                  f"  p={fmt(pr)}  p_holm={fmt(pa)}{note}")
        print("  (Holm is post-hoc, per triage §6C; the freeze's per-test alpha stands as written.)")


if __name__ == "__main__":
    main()
