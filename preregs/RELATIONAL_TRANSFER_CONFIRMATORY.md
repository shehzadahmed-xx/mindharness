# Relational vs Coordinate Memory Keys — Confirmatory Replication

**Status:** CONFIRMATORY. Hypotheses are derived from a prior exploratory run
and are therefore not novel; what is preregistered here is that they will hold
on **data that does not yet exist**.

**Disjoint seeds.** Every seed used to date lies in `1..20000` (transfer),
`1..5000` (scale sweep) and `1..2000` (ablation). This replication uses
**`500001..520000`**, which has never been drawn from. No result from the
exploratory range is admissible as evidence for the predictions below.

**Frozen before first trial.** This file and the runner are hashed into
`pilot/locks/relational_transfer_confirmatory.lock.json`, which is committed to
git before any confirmatory seed is executed. If the analysis code changes, the
hash breaks and the run is void.

---

## Background (exploratory, not evidence for what follows)

A grid navigator stores experiences in a slow memory and consults them on later
episodes. Walls are re-randomised every city, so route memorisation should fail
and only structure that is shared across cities should survive.

Exploratory runs on seeds `1..20000` found that memory keyed by **cell**
(`at (x,y) → move`) transfers *negatively* to a never-seen city, while memory
keyed by **situation** (`blk<4 bits>|goal(dx,dy) → move`) transfers positively,
and does so against a sham control. Those runs also produced the repair itself,
so they cannot test it. This document does.

---

## Design

Train one agent per seed on 4 novel cities; then run **one city never seen**,
three times from the same trained state, differing only in the slow store:

| arm | store at test | isolates |
|---|---|---|
| **intact** | as learned | — |
| **wiped** | empty | whether carrying a store helps at all |
| **shuffled** | same size, same states, moves permuted | whether the **content** helps, or only the +0.3 bonus mechanics |

Goal bias fixed at `0.2` in every arm. Identical RNG stream across arms, so the
three see the same candidate draws: arms are **paired**, and the analysis is the
per-seed difference, never independent intervals.

**Fixed parameters.** `train_cities=4`, `bias=0.2`, wall density `0.15`, step
budget `4n`, grids `n ∈ {5, 8, 12}`, `n_seeds=20000` per cell, percentile
bootstrap over seeds with 5000 resamples at α=0.05. Metrics: `win` (reached
goal), `dist` (Manhattan remaining), `hits` (times the store fired), and
`hits/pattern` (coverage).

---

## Predictions

Thresholds are set below the exploratory point estimates so the test is a
replication rather than a restatement. **All are evaluated at grid 5 unless
stated.**

| # | Prediction | Threshold | Fails if |
|---|---|---|---|
| **R1** | Relational memory helps against no memory | `intact − wiped` (win) **≥ +0.020**, 95% paired CI excludes 0 | point estimate < +0.020, or CI includes 0 |
| **R2** | **PRIMARY.** Relational memory's *content* does the work, not the bonus mechanics | `intact − shuffled` (win) **≥ +0.010**, 95% paired CI excludes 0 | point estimate < +0.010, or CI includes 0 |
| **R3** | Coordinate memory does not help | `intact − wiped` (win) **≤ 0.000** | point estimate > 0.000 |
| **R4** | Coordinate memory's content does not help | `intact − shuffled` (win) 95% CI **does not lie entirely above 0** | CI lower bound > 0 |
| **R5** | Compression signature | relational `hits/pattern` **≥ 2×** coordinate `hits/pattern` | ratio < 2 |
| **R6** | Compression *scales* | across grids 5→8→12, relational `hits/pattern` **strictly increases** and coordinate `hits/pattern` **strictly decreases** | either sequence is non-monotonic |
| **R7** | Relational transfer survives scale | `intact − shuffled` (win) CI excludes 0 at **all three** grid sizes | it includes 0 at any size |

**Primary outcome is R2.** It is the sham contrast: the one that distinguishes a
store whose contents carry usable structure from a store that merely fires. R2
failing while R1 passes would mean the benefit is mechanical, not informational,
and the generality claim would not be supported.

**R3 and R4 are the null predictions.** Predicting that a manipulation does
*nothing* is what makes R1/R2 interpretable; without them a positive relational
result could be an artefact of having any store at all.

## Stopping rule

One run at the stated `n`. No peeking, no extension, no re-analysis with
different bootstrap parameters. The verdict table is printed by the runner and
recorded verbatim.

## What would falsify the underlying claim

R2 null at grid 5, or R7 failing at grid 12, means situation-keyed memory does
not carry transferable structure and the exploratory flip was a small-world
artefact. R6 failing means the compression story is wrong even if transfer
holds — coverage would not be the mechanism.
