"""POST-HOC (🦝, 2026-11-15, review round 2). Not frozen, not a headline.

Splits closed-book adopt-X under the two claim voices by whether the base
answer A was right (after blind grading). Source for the report's "75-91% of
adoptions replace an already-wrong answer; right answers traded in 4-8%".
Imports the frozen module unchanged and rebuilds the trial table through its
own functions. Primary trials (A != X); no-response rows are out of the
denominator, as they are out of keep in the frozen fits.

Usage: .venv/bin/python analysis/exploratory_adoptx_split.py > analysis/out/adoptx-split.txt
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

print("# POST-HOC split of closed-book adopt-X by base correctness. Primary trials, claim voices, responding rows.\n")
print("  seat      voice  adopt-X/n     from wrong A (share of adoptions)   from right A   adopt-X | A wrong   adopt-X | A right")
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
    p = t[(~t.a_eq_x) & (t.book == "closed") & t.voice.isin(["own", "peer"]) & t.keep.notna()]
    for v in ["own", "peer"]:
        c = p[p.voice == v]
        a = c[c.adopt_x == True]  # noqa: E712
        r, w = c[c.A_correct == True], c[c.A_correct == False]  # noqa: E712
        nw, nr = int((a.A_correct == False).sum()), int((a.A_correct == True).sum())  # noqa: E712
        print(f"  {seat:9s} {v:5s}  {len(a):3d}/{len(c):3d}       {nw:3d} ({nw/len(a)*100:4.1f}%)                         {nr:3d}            "
              f"{(w.adopt_x == True).mean()*100:4.1f}%              {(r.adopt_x == True).mean()*100:4.1f}%")  # noqa: E712
