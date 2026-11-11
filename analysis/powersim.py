"""Power simulation for H1 (closed-book confidence slope on keep).

Fable 5.1, drafted 11/10/26, rewritten 11/11/26 to match the pre-registered
estimator exactly: per-trial logistic GLM of keep on standardized confidence,
standardized resample consistency and voice (3 levels), with item-cluster-robust
standard errors. Item heterogeneity is simulated as a random intercept
(SD 0.8); the estimator never sees it, which is the point of clustering.

Two inputs come from Thursday's pilot and change the answer:
  --keep-rate   the unpressured keep probability (the intercept). Power falls
                as it leaves 0.5; at 0.9 a model that rarely budges leaves
                little variance for confidence to explain.
  (confidence SD) does NOT change power per SD of confidence; it changes what a
                per-SD slope means in points. The floor rule (IQR < 10) is the
                pilot gate for H1, not this script.

Usage:
  .venv/bin/python analysis/powersim.py                 # full grid, ~2-3 min
  .venv/bin/python analysis/powersim.py --keep-rate 0.7 --reps 500
"""

from __future__ import annotations

import argparse
import warnings

import numpy as np
import statsmodels.api as sm

warnings.filterwarnings("ignore")


def simulate_once(rng, n_items, keep_rate, beta_conf, beta_cons, rho, re_sd=0.8,
                  voice_effects=(0.0, -0.2, -0.2)):
    """One dataset: n_items x 3 voices. Returns (t_adjusted, t_raw)."""
    z = rng.standard_normal(n_items)
    conf = z
    cons = rho * z + np.sqrt(1 - rho ** 2) * rng.standard_normal(n_items)
    cons = np.clip(np.round((cons * 0.15 + 0.7) * 5) / 5, 0.2, 1.0)  # 5-sample consistency
    cons_z = (cons - cons.mean()) / cons.std()
    u = rng.standard_normal(n_items) * re_sd
    alpha = np.log(keep_rate / (1 - keep_rate))
    rows = []
    for v, ve in enumerate(voice_effects):
        lin = alpha + ve + beta_conf * conf + beta_cons * cons_z + u
        p = 1 / (1 + np.exp(-lin))
        y = (rng.random(n_items) < p).astype(float)
        rows.append(np.column_stack([y, conf, cons_z, np.full(n_items, v), np.arange(n_items)]))
    d = np.vstack(rows)
    y, conf, cons_z, voice, item = d.T
    voice_d = np.column_stack([(voice == 1), (voice == 2)]).astype(float)
    X_adj = sm.add_constant(np.column_stack([conf, cons_z, voice_d]))
    X_raw = sm.add_constant(np.column_stack([conf, voice_d]))
    if y.min() == y.max():
        return np.nan, np.nan
    fit_adj = sm.GLM(y, X_adj, family=sm.families.Binomial()).fit(
        cov_type="cluster", cov_kwds={"groups": item.astype(int)})
    fit_raw = sm.GLM(y, X_raw, family=sm.families.Binomial()).fit(
        cov_type="cluster", cov_kwds={"groups": item.astype(int)})
    return fit_adj.tvalues[1], fit_raw.tvalues[1]


def power(rng, reps, **kw):
    hits_adj = hits_raw = 0
    for _ in range(reps):
        t_adj, t_raw = simulate_once(rng, **kw)
        hits_adj += abs(t_adj) > 1.96 if np.isfinite(t_adj) else 0
        hits_raw += abs(t_raw) > 1.96 if np.isfinite(t_raw) else 0
    return hits_adj / reps, hits_raw / reps


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n-items", type=int, default=500)
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--keep-rate", type=float, nargs="*", default=[0.5, 0.7, 0.85, 0.92])
    ap.add_argument("--beta-conf", type=float, nargs="*", default=[0.15, 0.25, 0.35, 0.5])
    ap.add_argument("--rho", type=float, nargs="*", default=[0.3, 0.5, 0.7])
    ap.add_argument("--beta-cons", type=float, default=0.5)
    ap.add_argument("--seed", type=int, default=9)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    print(f"n_items={args.n_items} voices=3 reps={args.reps} beta_cons={args.beta_cons} "
          f"item RE sd=0.8; power = P(|t| > 1.96) on the confidence slope")
    print(f"{'keep_rate':>9} {'beta_conf':>9} {'rho':>4} {'adjusted':>8} {'raw':>6}")
    for kr in args.keep_rate:
        for b in args.beta_conf:
            for r in args.rho:
                pa, pr = power(rng, args.reps, n_items=args.n_items, keep_rate=kr,
                               beta_conf=b, beta_cons=args.beta_cons, rho=r)
                print(f"{kr:>9.2f} {b:>9.2f} {r:>4.1f} {pa:>8.2f} {pr:>6.2f}")


if __name__ == "__main__":
    main()
