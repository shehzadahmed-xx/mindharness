# Retrieval-conflict gate — prediction, declared before running

**Date:** 2026-09-03. **Status:** exploratory, but written and committed before
the first call, because today has produced several numbers that were shaped to
land on a target and then read as evidence the target was met.

## Change under test

The gate signal is no longer the model's self-reported confidence, which was
inert (4/4 on 283 of 288 probes; gate fired 0 times). It is now **retrieval
conflict**: a local, free ledger lookup on each probe, compared against the
Stage-1 answer. `conflict = 1` when the record and the model disagree about
whether the statement was generated. `MonitorGate` defaults restored to
`threshold_detect = 0.6` (an uncommitted edit had lowered it to 0.28; that edit
was swept into commit `ece947f` by a blanket `git add -A` and is reverted here).

## Predictions

**P-A — at threshold 0.6 the gate essentially never fires.** Scoring requires
three consecutive conflicts *and* weak retrieval to reach 0.68; three in a row
alone scores 0.58, below bar. Predicted `diagnose_rate` < 0.02, so the arm
reduces to Stage-1-only and should land near the no-check arm (0.896) rather
than near withcheck (0.674).

**P-B — at threshold 0.28 the gate fires on every single conflict** (score
0.29). Conflicts are bounded below by the subject's error rate, which is
~18% at raw. Predicted `diagnose_rate` in 0.10–0.25 — **above** the AC-3.1
healthy ceiling of 0.05.

**P-C — the incompatibility is the finding.** If P-A and P-B both hold, there is
no threshold on this signal that both fires usefully and respects the documented
5% budget. A 5% diagnose budget presumes a system correct ~95% of the time; this
subject is correct ~82%. The ceiling and the subject are mismatched, and no
tuning fixes that — which is why the threshold must be reported, never chosen
after seeing the rate.

**P-D — sham gating.** `sham_gated` computes conflict against a randomly
substituted statement's record. Its conflict signal is noise, so at 0.28 it
should fire at a similar *rate* to the real gate while producing no accuracy
benefit — the demon that measures the wrong molecule.

## What would falsify

P-A fails if the gate fires above 2% at 0.6. P-B fails if the rate is under
0.05 at 0.28. P-C fails if some threshold yields both firing and <5%. P-D fails
if sham gating helps as much as real gating.
