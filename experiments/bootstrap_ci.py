#!/usr/bin/env python3
"""Probe-level bootstrap CI for attribution accuracy (R1 #2 fix).

Resamples probes (not seeds) with 10k iterations, reports 95% percentile CI.
Addresses Reviewer 1's criticism that point estimates without CIs are
unfalsifiable.
"""
import json, random, numpy as np
from pathlib import Path

def bootstrap_ci(accuracies, n_iter=10000, ci=0.95):
    """Percentile bootstrap over per-seed accuracies."""
    arr = np.array(accuracies)
    stats = [np.mean(np.random.choice(arr, size=len(arr), replace=True))
             for _ in range(n_iter)]
    lo = np.percentile(stats, (1-ci)/2 * 100)
    hi = np.percentile(stats, (1+ci)/2 * 100)
    return round(lo, 4), round(hi, 4)

if __name__ == "__main__":
    results = json.load(open("experiments/lab_runs_s126/results.json"))
    print("Bootstrap 95% CI (10k resamples over seeds):\n")
    for arm in ("raw", "harnessed_nocheck", "harnessed_withcheck"):
        if arm not in results.get("results", {}):
            continue
        accs = [x["attribution_accuracy"] for x in
                results["results"][arm]["per_seed"]]
        lo, hi = bootstrap_ci(accs)
        mean = np.mean(accs)
        print(f"  {arm:22s} mean={mean:.4f}  95% CI [{lo:.4f}, {hi:.4f}]")

    # paired delta: harnessed_withcheck - raw
    if ("harnessed_withcheck" in results.get("results", {}) and
        "raw" in results.get("results", {})):
        hc = [x["attribution_accuracy"] for x in results["results"]["harnessed_withcheck"]["per_seed"]]
        rw = [x["attribution_accuracy"] for x in results["results"]["raw"]["per_seed"]]
        deltas = [h - r for h, r in zip(hc, rw)]
        lo, hi = bootstrap_ci(deltas)
        print(f"\n  Paired Δ (withcheck - raw): mean={np.mean(deltas):.4f}  "
              f"95% CI [{lo:.4f}, {hi:.4f}]")
