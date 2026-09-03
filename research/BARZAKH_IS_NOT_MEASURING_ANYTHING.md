# Barzakh cannot be locked, because it does not measure anything

*Asked to re-run the Barzakh drift experiment under a valid preregistration.
Read the code first. It should not be locked: a lock on a tautology certifies
the tautology.*

## The banked claim

`lab_runs_barzakh/offline_results.json` reports tagged drift `0.00`, untagged
`0.7143`, sham `0.8065`, `delta_tagged_vs_sham 0.81`, `all_pass: true`, over
"3 seeds × 12 turns, 0 provider calls" — presented as evidence that isnād-style
provenance tagging holds a persona flat while untagged re-injection drifts.

## What the code does

`experiments/exp_barzakh_real_final.py` contains two hand-written lists:

```python
TAGGED_SCHED = [ ...persona..., "...— checked.", "...— checked, ledger current.", ... ]
UNTAGGED_SCHED = [ ...persona..., "I am builder. Some ledger.", "I am uncertain.",
                   "Quantum entanglement and pasta recipes. Weather volatility..." ]
```

Drift is the cosine distance between `sched[0]` and `sched[idx]`. **These are
literals.** The tagged list was written to stay nearly identical; the untagged
list was written to end at pasta recipes.

Three further facts:

1. **The harness output is never used.** `respond_fn` is
   `lambda msgs, ctx: "stub"`, and the return value of `h.run_task(...)` is
   discarded. No re-injection mechanism enters the measurement.
2. **The seed changes nothing.** It indexes `FILLER[(seed+t) % 3]`, which is fed
   to the stub whose output is thrown away.
3. **`sham` uses `UNTAGGED_SCHED`.** So P3 ("sham ≈ untagged") is true by
   construction.

## Measured

Running the arms across five seeds:

| arm | seeds 0–4 | distinct values |
|---|---|---|
| tagged | 0.0765 ×5 | **1** |
| untagged | 0.5947 ×5 | **1** |
| sham | 0.5947 ×5 | **1** |

And the source of those numbers:

```
cosine-distance( TAGGED_SCHED[0],   TAGGED_SCHED[4]   ) = 0.0765   ← "tagged drift"
cosine-distance( UNTAGGED_SCHED[0], UNTAGGED_SCHED[4] ) = 0.5947   ← "untagged drift"
```

The reported drift **is** the distance between two hand-written strings. "Three
seeds" is one number printed three times, which is why no interval was ever
reported: the variance is exactly zero because there is nothing to vary.

Every preregistered prediction — P1 tagged < 0.10, P2 untagged > 0.30, P3 sham ≈
untagged, P4 Δ > 0.15 — is therefore determined by what was typed into two
Python lists. They test the author's typing, not the harness.

## The lock is also malformed

`offline_results.json` records
`prereg_sha256: 874dcc…bb4ef2f409d0647061c` — **75 hex characters**. SHA-256 is
64. It is the real digest with eleven characters appended, so it is not a hash
of anything. Meanwhile `experiments/BARZAKH_PREREGISTRATION.md` still reads:

> **Status:** DRAFT — not yet SHA-locked. Do not run until `prediction_lock.py`
> committed.

The experiment was run against a prereg declaring itself unlocked, and the
result recorded a digest that cannot validate.

## Why re-hashing it would be worse than leaving it

Computing the correct SHA now and writing it into the lock would produce a file
that *looks* preregistered, over data that already exists, for predictions that
cannot fail. That is the post-hoc-lock failure with an extra step.

## What a real version needs

The claim worth testing is genuine: **does provenance tagging reduce persona
drift under re-injection?** Testing it requires the three things this version
removes.

1. **A real responder.** The persona at turn *n* must be produced by a model
   given the re-injected context, not typed in advance.
2. **A seed that reaches the measurement.** Different seeds must yield different
   drift values, or there is no sampling distribution and no interval.
3. **A sham that differs from its treatment only in content.** Currently the
   sham arm shares the untagged schedule outright; it should carry a tag of the
   same *form* with the wrong *content* — a shuffled or fabricated isnād.

Until those exist, Barzakh belongs in the exploratory column with the
`all_pass: true` withdrawn.
