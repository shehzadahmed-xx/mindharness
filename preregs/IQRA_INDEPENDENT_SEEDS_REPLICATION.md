# Iqra skin-threshold — independent-seed replication

**Status:** CONFIRMATORY replication of an exploratory result. Frozen before the
first replication seed is drawn.

## What is being replicated

`tools/tiny_agent_iqra.py` banked `learned 0.8767` vs `fixed 0.6725`,
`delta +0.2042`, CI `[0.1758, 0.2325]`, reported as `n=100`.

**The n is misleading.** `run_experiment(n_episodes=100, seed=42)` draws every
episode from **one** master RNG stream. The interval is over episodes inside a
single stream, not over independent replications, so it cannot speak to
between-run variability.

## What this replication changes

**Independent master seeds `9001..9200`**, disjoint from the original `42`. Each
seed is a full independent experiment; the statistic is the distribution of
per-seed deltas.

## Predictions

**I1 — the effect replicates.** Mean delta across 200 independent seeds
**≥ +0.15**, with the 95% percentile interval over seeds excluding 0.

**I2 — the honest interval is wider.** The between-seed 95% interval will be
**wider** than the original within-seed episode bootstrap `[0.1758, 0.2325]`
(width 0.057). Predicted width **> 0.057**. If it is not wider, the original
interval was not obviously understating uncertainty and I was wrong to say so.

**I3 — the effect is a design parameter, not a discovery.** The source comment
reads *"distributions — calibrated for +0.15 delta"*, and `FIXED_THR = 0.5` sits
well above `OPTIMAL_THR = 0.31`. Sensitivity test: re-run with the fixed
threshold set to the optimal value (0.31). **Predicted delta collapses to
< +0.05.** If it does, the banked +0.204 measures the distance between an
arbitrary constant and the optimum, not the value of learning.

I3 is the load-bearing prediction. I1 and I2 concern precision; I3 concerns what
the number means.

## Fixed parameters

`PROBES_PER_EPISODE=12`, `CITIES=5`, `GRID=5`, `EXT ~ N(0.16, 0.12)`,
`SELF ~ N(0.46, 0.12)` (the values in code, which differ from the docstring's
0.25/0.55 — the docstring is stale), clipped to [0,1]. 200 seeds, percentile
bootstrap over seeds, 5000 resamples, α=0.05.

## Stopping rule

One run at n=200 seeds plus one sensitivity run. No peeking, no extension.

---

## Outcome (recorded 2026-09-03, seeds 9001–9200)

| | prediction | observed | verdict |
|---|---|---|---|
| **I1** | mean delta ≥ +0.15, CI excludes 0 | **+0.1898** [+0.1882, +0.1914], range +0.1616…+0.2267 | **PASS** |
| **I2** | between-seed interval wider than 0.0570 | width **0.0032** — *narrower* | **FAILED (mine)** |
| **I3** | with fixed = optimal (0.31), delta < +0.05 | **−0.0218** [−0.0228, −0.0208] | **PASS, past prediction** |

### I1 — the effect replicates

+0.1898 across 200 independent master seeds, against +0.2042 from the single
original stream. The effect is real and stable.

### I2 — my prediction was wrong, and wrong for an instructive reason

I predicted the honest between-seed interval would be *wider* than the original.
It is 18× **narrower**. The two intervals are not intervals on the same
quantity: the original bootstraps over **episodes** (noisy single units), this
one bootstraps over **seed-means** (each already an average of 100 episodes).
Averaging first collapses the variance, so a tighter interval is arithmetic, not
better evidence.

My criticism that the original CI "understated uncertainty" was therefore
misplaced. The correct criticism is narrower: the original interval answers
*"how variable is one episode?"* and was being read as *"how variable is the
result?"* Those differ, but not in the direction I predicted.

### I3 — the primary, and the finding

Set the fixed comparator to the **optimal** threshold (0.31) instead of the
arbitrary 0.5, and the learned threshold does not merely stop winning — it
**loses**, by −0.0218.

The learned threshold converges to ≈0.285–0.31, i.e. approximately the optimum.
So the banked **+0.204 is a measure of how bad 0.5 is** for distributions the
source comment says were *"calibrated for +0.15 delta"*. It is the distance
between an arbitrary constant and the optimum, not the value of learning.

**What the experiment actually demonstrates:** a threshold learned from
two-speed memory converges to roughly the right value. That is a real and
respectable result. **What it does not demonstrate** is a +0.204 advantage from
having a skin, because the comparator was chosen to be far from optimal.

A fair version reports the delta against a *reasonable* baseline, or reports
convergence directly (distance from optimum over episodes) rather than an
advantage over a strawman constant.
