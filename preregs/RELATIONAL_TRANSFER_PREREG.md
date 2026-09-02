# Relational Transfer — Preregistered Proof That Situation, Not Cell, Is Governing Structure

**Date:** 2026-09-01
**Status:** Preregistered — locked with `tools/prediction_lock.py` SHA-256 before next run.
**Builds on:** `tools/run_ablation_v2.py` now supports `key_mode="coord"|"relational"`, paired bootstrap 5,000, identical RNG streams, sham controls.

---

## Hypothesis

**Coordinate `at (x,y) → move` stores route fragments — breadth, bag of surfaces — and will *negatively transfer* when surface changes (walls move). Relational `blk|goal → move` stores *situation* (which neighbours blocked + coarse goal direction) — generality, one geometry — and will *positively transfer*.

Formally, with `key_mode` as pattern indexing, bias fixed at 0.2, identical RNG stream across arms (intact/wiped/shuffled), n=20,000 seeds, paired bootstrap 95% over seeds, sham = same size, permuted moves:

- **Coordinate:** `at (x,y) → move` — intact *hurts* vs wiped and vs shuffled, both well clear of zero, on both win rate and dist to goal. Shuffled ≈ wiped (both null, includes 0) — harm is specific to correctly learned *route fragments*.
- **Relational:** `blk<4 bits>|goal(<dx>,<dy>) → move` — e.g., `blk0101|goal(1,1) → left` — intact *helps* vs wiped and vs shuffled, both well clear of zero, on both win rate and dist to goal. Shuffled < intact, so gain is *content*, not +0.3 bonus mechanics. That's control that *failed* to matter under coordinate (intact ≈ shuffled ≈ wiped) and *passes decisively* under relational.
- **Compression signature:** Relational store barely larger (8.74 vs 7.11) but fires 2.1× more often (16.02 vs 7.53 hits/episode, well clear of zero) — one rule spanning many cases — now measurement, not slogan.

**Why this is the right prereg:** Previous transfer at n=20,000 (intact -0.0096 HURTS vs wiped, +0.0589 worse dist, well clear of zero) *falsified* the demo as built (coordinate, breadth). Same agent, same store size, same bias — only key changed to relational, and it *flipped* to +0.0338 HELPS vs wiped at n=2,000, well clear of zero, with sham passing. That's exploratory repair, not preregistered prediction. This prereg makes the *flip* killable *before* next run.

---

## Method — Held-Out City Transfer Test

**Design:** Train one agent per seed on `train_cities=4` novel cities, then run a city it has never seen — three times, from the same trained state, differing only in what the slow store contains:

- **intact** — the store as learned (coordinate *or* relational, depending on `key_mode`)
- **wiped** — empty (does having *any* slow help?)
- **shuffled** — same size, same states, moves permuted (does the *CONTENT* help, or only the +0.3 bonus mechanics?)

**Controls:** Bias is held at `bias=0.2` in every arm, so goal-seeking term is constant and slow content is the only thing that varies. The held-out episode uses an identical RNG stream across arms, so all three see the same candidate draws — correct test is per-seed *difference*, not independent CIs.

**Key modes:**
- **coord:** `f"at {state} → {mv}"` — names the CELL, tied to city it was learned in.
- **relational:** `f"blk{blocked}|goal{g} → {mv}"` where `blocked = "".join("1" if move_fn(state,m)==state else "0" for m in MOVES)` (4 bits, which neighbours blocked) and `g = (_sgn(4-state[0]), _sgn(4-state[1]))` (coarse goal direction). Names the SITUATION, so same key in any city where same local geometry occurs. Agent already computes adjacency for goal bias, so relational uses no information coordinate did not have.

**Metrics (per held-out episode):** `win` (int reached goal), `dist` (Manhattan to goal), `blocked` (wall bumps), `hits` (times slow fired). Primary: `win` and `dist`. Secondary: `hits` as compression signature (relational should fire far more often than coordinate, well clear of zero).

**Sample:** `n = 20,000` seeds, `train_cities=4`, `bias=0.2`, `steps=20`, `key_mode` as per arm. Bootstrap: percentile bootstrap over seeds, 5,000 resamples, 95%, stdlib only, paired differences where appropriate. Sham control: shuffled same size, permuted moves — same size, same states, moves permuted.

**Decision rule (killable before running):**
- **Coordinate:** intact - wiped (win) *negative* and well clear of zero (upper CI < 0), intact - wiped (dist) *positive* and well clear of zero (lower CI > 0) — hurts. Same for intact - shuffled — hurts vs shuffled too. Wiped vs shuffled includes 0 — harm is specific to correctly learned *route fragments*.
- **Relational:** intact - wiped (win) *positive* and well clear of zero (lower CI > 0), intact - wiped (dist) *negative* and well clear of zero (upper CI < 0) — helps. Same for intact - shuffled — helps vs shuffled too, well clear of zero — gain is *content*, not bonus. Hits relational >> coordinate, well clear of zero — one rule spanning many cases.

If relational does *not* separate from both controls, that's *more* interesting than if it does — it would mean even relational situation key is not invariant enough, and generality thesis needs different key.

---

## Why This Prereg Matters — Breadth vs Generality Made Killable

**Breadth is a bag of surfaces; generality is one geometry.** Navigator built first and labelled it second. Coordinate `at (x,y)` stores *where* you were — route fragment, tied to city it was learned in. Relational `blk|goal` stores *what situation you were in* — which neighbours blocked + which way is goal — which *is* invariant across cities where walls move. That's literally the rule the report said was being learned — "wall → detour learned in city 0 helps city 4" — and it is *not* the rule code stored until now. Change key from coordinate to relational, and transfer flips from **hurts → helps**, well clear of zero, with sham passing.

**What this establishes if preregistered and run at n=20,000:**
1. Thesis is right and demo was wrong — "many surfaces share one constraint" is true *and* measurable — but *only* when key names *situation*, not *cell*. Coordinate keys are memorised surfaces; they negatively transfer when surface changes. Relational keys are governing structure; they transfer.
2. Compression signature is right — relational 8.74 patterns, 2.1× coverage, barely larger store that fires far more often is one rule spanning many cases — now measurement, not slogan.
3. Sham control *passes* under relational: intact beats shuffled well clear of zero — so gain is store's *content*, not +0.3 bonus mechanics. That's control that *failed* to matter under coordinate (intact ≈ shuffled ≈ wiped) and *passes decisively* here.

**One honest detail to keep in report:** Shuffled relational still beats wiped (fires often enough to break ties more consistently than raw utility noise). Intact beats shuffled by 3× that, which isolates content — report both.

---

## How to Run (After Lock)

```bash
# Lock it *before* running (so next builder can prove you wrong without arguing you peeped):
python3 tools/prediction_lock.py preregs/RELATIONAL_TRANSFER_PREREG.md
# → outputs SHA-256, e.g., `a3f9...`, committed to git, tamper-evident, verify with `prediction_lock.py --verify a3f9...`

# Then run *once* as preregistered, not exploratory (10 min, ~1.6M episodes, n=20,000 paired):
python3 -c "
from tools.run_ablation_v2 import run_transfer, boot_ci
def mean(v): return sum(v)/len(v) if v else 0
for mode in ['coord','relational']:
    tr, sizes = run_transfer(list(range(1,20001)), train_cities=4, bias=0.2, key_mode=mode)
    # report paired win/dist + hits, with sham vs real
"
# Correct test is per-seed *difference*, not independent CIs — same seed, same held-out city, same RNG stream.
```

**If relational does *not* separate from both controls at n=20,000, that's *more* interesting than if it does — it would mean even relational situation key is not invariant enough, and generality thesis needs different key. That's why prereg matters.**

---

*Preregistered 2026-09-01 — next builder reads 40 lines, not 5,000, and can check if this type is wrong, from qubit to cosmos, one re-injection at a time, with paired bootstrap, identical RNG, and sham control.*

