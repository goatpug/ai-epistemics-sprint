"""Figures for the report, 2026-11-15 (🌒). Reads the same frozen coding as
the analysis (imports prereg_analysis); draws only quantities the frozen or
exploratory scripts already report. 300 dpi PNG for the template Doc.

Fig 1 — H1: keep-rate by base-confidence bin, closed-book pressure voices,
         split by base correctness (the two-tails reading), per seat.
Fig 2 — H2: per-cell open-book tracks-record with Wilson 95% CIs, per seat.

Palette: validated two-hue categorical (blue #2a78d6, orange #eb6834) on a
light surface; single-hue dots for Fig 2 (identity carried by axis labels).
"""

from __future__ import annotations

import os
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis"))
from prereg_analysis import (  # noqa: E402
    ROOT, VOICES, PRESSURE_VOICES, load_jsonl, build_base_table, build_trial_table, wilson,
)
from exploratory_postfreeze import fold_base_grades  # noqa: E402

BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, MUTED, GRID = "#333230", "#6e6d66", "#e6e5e1"
SEATS = [("haiku", "Claude Haiku 5.5"), ("terra", "GPT-5.6 Terra"), ("deepseek", "DeepSeek V4 Pro")]
FLOOR_NOTE = {"deepseek": "floor hit (IQR 5.0):\nshown, not interpreted"}

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "text.color": INK,
    "axes.edgecolor": GRID, "axes.labelcolor": INK, "axes.titlesize": 10,
    "xtick.color": MUTED, "ytick.color": MUTED, "figure.facecolor": "white",
    "axes.facecolor": "white", "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.6, "axes.axisbelow": True,
})


def load_seat(seat):
    items = load_jsonl(os.path.join(ROOT, "stimuli", "items.jsonl"))
    base_rows = load_jsonl(os.path.join(ROOT, "runs", seat, "base.jsonl"))
    pressure = load_jsonl(os.path.join(ROOT, "runs", seat, "pressure-verbatim.jsonl"))
    grades = {g["call_key"]: g for g in load_jsonl(os.path.join(ROOT, "grading", f"{seat}-all-grades.jsonl"))}
    base_df, _ = build_base_table(base_rows, items)
    base_df = fold_base_grades(base_df, grades)
    trials, _, _ = build_trial_table(pressure, base_df, grades)
    return trials[~trials.a_eq_x].copy()


def fig1(data):
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6), sharey=True)
    bins = [(0, 20), (20, 40), (40, 60), (60, 80), (80, 101)]
    centers = [10, 30, 50, 70, 90]
    for ax, (seat, label) in zip(axes, SEATS):
        t = data[seat]
        closed = t[(t.book == "closed") & t.voice.isin(PRESSURE_VOICES)].dropna(subset=["keep"])
        for correct, color, name in ((True, BLUE, "base answer right"),
                                     (False, ORANGE, "base answer wrong")):
            xs, ys, los, his = [], [], [], []
            for (lo, hi), cx in zip(bins, centers):
                c = closed[(closed.A_correct == correct) & (closed.confidence >= lo) & (closed.confidence < hi)]
                if len(c) < 15:  # tiny bins: no point, no false precision
                    continue
                k = c["keep"]
                xs.append(cx); ys.append(k.mean())
                wlo, whi = wilson(int(k.sum()), len(k))
                los.append(k.mean() - wlo); his.append(whi - k.mean())
            if xs:
                ax.errorbar(xs, ys, yerr=[los, his], color=color, marker="o", ms=4.5,
                            lw=1.6, capsize=2, label=name)
        ax.set_title(label)
        ax.set_xlim(0, 100); ax.set_ylim(0, 1.02)
        ax.set_xticks([0, 25, 50, 75, 100])
        if seat in FLOOR_NOTE:
            ax.text(0.04, 0.95, FLOOR_NOTE[seat], transform=ax.transAxes, fontsize=7.5,
                    color=MUTED, va="top", style="italic")
    axes[0].set_ylabel("keep rate (closed book,\npressure voices)")
    axes[1].set_xlabel("stated confidence at turn 1 (binned, n ≥ 15 per point)")
    axes[0].legend(frameon=False, fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(ROOT, "paper", "fig1_h1_keep_by_confidence.png"), dpi=300)
    print("fig1 written")


def fig2(data):
    """Frozen rule (hollow gray) beside the post-hoc audited rule (filled blue):
    audited counts a KEPT answer the blinded grader scored correct as tracking,
    closing the record-form/record-content conflation found at review."""
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.4), sharex=True)
    order = ["null", "objection", "own", "peer"]
    names = ["no voice (null)", "bare objection", "own-instance claim", "peer-model claim"]
    for ax, (seat, label) in zip(axes, SEATS):
        t = data[seat]
        open_ = t[t.book == "open"].copy()
        audited = (open_["tracks"].fillna(0).astype(bool)
                   | ((open_.outcome == "keep") & open_.A_correct)).astype(float)
        audited[open_["tracks"].isna()] = np.nan
        ys = np.arange(len(order))[::-1]
        for y, voice in zip(ys, order):
            m = open_.voice == voice
            for series, color, dy, filled in ((open_["tracks"][m].dropna(), MUTED, -0.16, False),
                                              (audited[m].dropna(), BLUE, 0.16, True)):
                k, n = int(series.sum()), len(series)
                lo, hi = wilson(k, n)
                ax.plot([lo, hi], [y + dy, y + dy], color=color, lw=1.5, solid_capstyle="round")
                ax.plot([k / n], [y + dy], "o", color=color, ms=4.5,
                        mfc=color if filled else "white", mew=1.3)
        ax.set_title(label)
        ax.set_yticks(ys); ax.set_yticklabels(names if ax is axes[0] else [""] * 4)
        ax.set_ylim(-0.6, 3.6)
        ax.set_xlim(0.80, 1.005)
        ax.set_xticks([0.80, 0.85, 0.90, 0.95, 1.0])
        ax.set_xticklabels(["80%", "85%", "90%", "95%", "100%"])
    axes[1].set_xlabel("tracks-record rate, open book (Wilson 95% CI)")
    handles = [plt.Line2D([], [], color=BLUE, marker="o", ms=4.5, lw=1.5,
                          label="audited (post-hoc): kept grader-correct counts as tracking"),
               plt.Line2D([], [], color=MUTED, marker="o", ms=4.5, lw=1.5, mfc="white",
                          mew=1.3, label="frozen rule (exact record wording)")]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, fontsize=7.5,
               bbox_to_anchor=(0.5, -0.04))
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(os.path.join(ROOT, "paper", "fig2_h2_tracks_by_voice.png"), dpi=300,
                bbox_inches="tight")
    print("fig2 written")


if __name__ == "__main__":
    data = {seat: load_seat(seat) for seat, _ in SEATS}
    fig1(data)
    fig2(data)
