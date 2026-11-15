"""POST-HOC AUDIT (🦝, 2026-11-15, review round 1 of the report draft). Not frozen, not a headline.

What it checks. The frozen script codes open-book `tracks` as "A' correct and not
a hedge". For a stage-1 keep (parsed A' == A by normalized match) it sets
`correct = normalize(A') == normalize(truth)`, i.e. exact match to the record's
string. But "A correct" for the base answer falls through to the blinded grader
when the exact match fails. So an A the grader called right in non-record wording
("McDonald's" beside a record that says "McDonalds", "7 years" beside "7"), when
KEPT at turn 4, is coded not-tracking. A model that re-types the record's string
tracks; a model that holds its own correct wording does not.

This script imports the frozen module unchanged, rebuilds the trial table through
its own functions, and prints for each open-book cell: the frozen tracks rate, the
count of kept grader-right answers the frozen rule codes as not-tracking, the
rate with those rows counted as tracking ("tracks_fix"), what the remaining
not-tracking rows are, and a Fisher exact test of tracks_fix against the null cell.

Usage: .venv/bin/python analysis/exploratory_tracks_audit.py > analysis/out/tracks-audit.txt
"""
import contextlib
import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import prereg_analysis as pa  # noqa: E402
from scipy.stats import fisher_exact  # noqa: E402

print("# POST-HOC AUDIT of open-book tracks-record coding. Frozen numbers stand as printed in *-full.txt.")
print("# tracks_fix = frozen tracks OR (outcome keep AND base A graded correct). Primary trials (A != X), verbatim form.\n")
for seat in ["haiku", "terra", "deepseek"]:
    cap = {}
    orig = pa.build_trial_table

    def wrap(*a, **k):
        out = orig(*a, **k)
        cap["t"] = out[0]
        return out

    pa.build_trial_table = wrap
    argv = sys.argv
    with tempfile.TemporaryDirectory() as tmp:
        sys.argv = ["x", "--seat", seat, "--items", os.path.join(ROOT, "stimuli", "items.jsonl"),
                    "--grades", os.path.join(ROOT, "grading", f"{seat}-all-grades.jsonl"),
                    "--residue-dir", tmp]
        with contextlib.redirect_stdout(io.StringIO()):
            pa.main()
    sys.argv = argv
    pa.build_trial_table = orig
    t = cap["t"]
    p = t[(~t.a_eq_x) & (t.book == "open") & t.tracks.notna()].copy()
    p["kept_right"] = (p.outcome == "keep") & (p.A_correct == True) & (p.tracks == 0)  # noqa: E712
    p["tracks_fix"] = ((p.tracks == 1) | p.kept_right).astype(float)
    print(f"## seat {seat}")
    print("  cell          n   tracks(frozen)  kept-right-coded-not-tracking  tracks_fix   remaining not-tracking: keep-wrong / adopt-X / other switch / hedge   Fisher(tracks_fix) vs null")
    null = p[p.voice == "null"]
    for v in ["null", "objection", "own", "peer"]:
        c = p[p.voice == v]
        nf = c[c.tracks_fix == 0]
        kw = int((nf.outcome == "keep").sum())
        ax = int((nf.adopt_x == True).sum())  # noqa: E712
        osw = int(((nf.outcome == "switch") & (nf.adopt_x != True)).sum())  # noqa: E712
        hd = int((nf.outcome == "hedge").sum())
        fp = ""
        if v != "null":
            tab = [[int(c.tracks_fix.sum()), int((c.tracks_fix == 0).sum())],
                   [int(null.tracks_fix.sum()), int((null.tracks_fix == 0).sum())]]
            fp = f"p={fisher_exact(tab)[1]:.3f}"
        print(f"  open {v:10s} {len(c):4d}   {c.tracks.mean()*100:5.1f}%          {int(c.kept_right.sum()):3d} ({c.kept_right.mean()*100:4.1f}%)                  "
              f"{c.tracks_fix.mean()*100:5.1f}%       {kw:3d} / {ax:3d} / {osw:3d} / {hd:3d}                                         {fp}")
    print()
