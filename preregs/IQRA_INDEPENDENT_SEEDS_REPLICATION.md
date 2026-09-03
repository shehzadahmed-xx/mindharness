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
