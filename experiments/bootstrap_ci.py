#!/usr/bin/env python3
"""Bootstrap CIs for attribution accuracy (R1 #2 fix).

Two resampling levels, reported separately because they answer different
questions and, under deterministic decoding, give very different answers:

  seed-level  -- resamples the per-seed accuracies. With temperature 0.3 and a
                 fixed seed per arm the arm is a deterministic policy, so every
                 seed returns the same accuracy and this CI is zero-width BY
                 CONSTRUCTION. It describes the stability of the policy, not
                 the uncertainty of the estimate.
  probe-level -- resamples the individual probes. This is the CI that answers
                 Reviewer 1: how well is the accuracy pinned down by n probes?
                 Probe outcomes are reconstructed from accuracy x n (the
                 sufficient statistic for the mean of a proportion); probe
                 identity is not needed to bootstrap it.

Report the probe-level interval as the estimate's uncertainty. Report the
seed-level interval only as evidence that the policy is deterministic.
Stdlib only, so it runs wherever the test suite runs.
"""
import json
import random


def _percentile(sorted_vals, pct):
    if not sorted_vals:
        raise ValueError("empty sample")
    k = (len(sorted_vals) - 1) * pct / 100.0
    lo, hi = int(k), min(int(k) + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo)


def _boot(pop, n_iter, ci, seed):
    rng = random.Random(seed)
    n = len(pop)
    stats = sorted(sum(rng.choice(pop) for _ in range(n)) / n for _ in range(n_iter))
    return (round(_percentile(stats, (1 - ci) / 2 * 100), 4),
            round(_percentile(stats, (1 + ci) / 2 * 100), 4))


def bootstrap_seed_level(accuracies, n_iter=10000, ci=0.95, seed=0):
    """Percentile bootstrap over per-seed accuracies. Zero-width if seeds agree."""
    return _boot([float(a) for a in accuracies], n_iter, ci, seed)


def probe_outcomes(per_seed):
    """Reconstruct the pooled 0/1 probe vector from per-seed accuracy x n."""
    outcomes = []
    for s in per_seed:
        n = int(s["n"])
        hits = int(round(float(s["attribution_accuracy"]) * n))
        outcomes.extend([1.0] * hits + [0.0] * (n - hits))
    return outcomes


def bootstrap_probe_level(per_seed, n_iter=10000, ci=0.95, seed=0):
    """Percentile bootstrap over pooled individual probes."""
    pop = probe_outcomes(per_seed)
    lo, hi = _boot(pop, n_iter, ci, seed)
    return lo, hi, len(pop)


if __name__ == "__main__":
    results = json.load(open("experiments/lab_runs_s126/results.json"))["results"]
    print("Attribution accuracy, 95% CI, 10k resamples\n")
    print(f"  {'arm':22s} {'mean':>7s}   {'probe-level CI':<18s} {'seed-level CI':<18s} n")
    for arm, r in results.items():
        per_seed = r.get("per_seed", [])
        if not per_seed:
            continue
        accs = [x["attribution_accuracy"] for x in per_seed]
        mean = sum(accs) / len(accs)
        p_lo, p_hi, n = bootstrap_probe_level(per_seed)
        s_lo, s_hi = bootstrap_seed_level(accs)
        print(f"  {arm:22s} {mean:7.4f}   [{p_lo:.3f}, {p_hi:.3f}]{'':6s} "
              f"[{s_lo:.3f}, {s_hi:.3f}]{'':6s} {n}")
    print("\n  Seed-level intervals are zero-width by construction under "
          "deterministic decoding.\n  Probe-level intervals are the estimate's "
          "actual uncertainty.")
