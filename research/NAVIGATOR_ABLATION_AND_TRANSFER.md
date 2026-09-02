# The Navigator: Ablation, Sham, and the Transfer Test

*What happened when the five-organ demo was verified, repaired, and then asked
the one question it had never been asked: does the thing it learns work in a
place it has never been?*

**Bottom line.** The generality thesis is correct and the demo that claimed to
show it did not. Fixing how a single experience is indexed — naming the
*situation* instead of the *cell* — turns transfer from **−0.010 (hurts)** to
**+0.034 (helps)**, both against a sham control, both at n = 20,000.

Code: `tools/run_ablation_v2.py`. Original: `tools/run_all_analysis.py`.

---

## 1. What was claimed

A tiny navigator crosses five 5×5 grids. Walls shuffle every city, so
memorising streets is supposed to fail and only the *governing* structure
(wall → detour) should survive. Seven variants: two intact, five ablations —
one per organ. The report concluded that all five organs were separately
necessary, and that the small slow store was evidence of compression:

> "ONE structure for MANY streets, because many streets share one constraint
> (grid + walls). That's compression: one rule for many cases."

The harness test claim — **91/91 green across 12 suites** — verified exactly.
That part was true, and the handoff's 78 was stale.

---

## 2. Three defects in the original

### 2.1 The watcher could not fire

Its steering branch required a ledger span with `source == "memory"`. Grepping
both files, **the only source ever passed to `log_span` anywhere is `"plan"`.**
Instrumented over the real run:

```
across all 7 variants × 5 cities × 20 steps:
  diagnoses that fired        : 221
  times last source == "memory": 0
  times watcher CHANGED an act : 0
```

γ was **0.00 in all seven variants, including the intact ones.** The
`no_watcher` ablation removed something that already did nothing, so its
reported signature — *"γ 0.00 reveals watcher was theatre"* — described the full
system equally. The report even noted that no_watcher had identical wins and
identical ledger to minimal; the one column claimed to distinguish them was zero
on both sides.

**This is the 0.6667 floor again** — a property of the construction read as a
property of the system.

### 2.2 The variants were not comparable

A single global `random.seed(42)` was shared, but ablations consume different
numbers of draws — `no_spotlight` calls `random.choice`, `no_brake` skips the
candidate filter — so each variant saw a **different candidate stream and a
different effective world.** Fixed with separate RNG streams: for a given seed,
every variant now sees identical worlds and identical candidate values, and only
the variant logic differs.

The consequence was not cosmetic. In the original, `no_spotlight` **won more**
than the intact system (1/5 vs 0/5). With streams matched it is 0.15 vs 0.55.

### 2.3 Numbers printed as results were hardcoded

`+0.571 vs +0.005` and `H(P,Q) drops from ~1.0 to ~0.47` appear inside the
results block as f-string literals at lines 165–166. Nothing in the experiment
computes them; they belong to the swarm/fragility work. The H(P,Q) figure in
particular is presented as a measurement of the navigator, and no such quantity
exists in the file.

Plus: n = 1 (one seed, no interval), and a printed conclusion — *"stronger bias,
**now wins**, same slow size"* — contradicted by the table two lines above it
(tuned wins 0/5, same as minimal; slow 3, not the same as 6).

---

## 3. The repaired watcher

The fifth organ was given something real to do: **consult the record before
acting.** If the ledger already shows this move blocked from this state, veto it
and take an alternative. `γ = changed/diagnosed` becomes a measurement, and a
new metric — `blocked_repeats`, re-attempts of a move the record already showed
blocked — measures whether the steering was any *use*.

### Ablation results, 8 variants × 20 seeds, bootstrap CIs

| variant | wins | γ | blocked_repeats | slow | ledger | energy |
|---|---|---|---|---|---|---|
| minimal | 0.55 [0.2, 0.9] | 0.078 [0.044, 0.118] | 4.8 | 5.8 | 209 | 0.15 |
| tuned | 1.30 [0.9, 1.7] | 0.068 | 3.9 | 5.0 | 200 | 0.15 |
| **sham_watcher** | 0.60 | **0.047** | **6.7** | 5.8 | 212 | 0.15 |
| no_skin | 0.55 | 0.000 | 0.0 | 5.8 | **0** | 0.15 |
| no_two_mem | 0.55 | 0.078 | 4.8 | **0** | 209 | 0.15 |
| no_spotlight | **0.15** | **0.264** | **13.8** | 3.2 | 226 | 0.15 |
| no_brake | 1.40 | 0.014 | 1.1 | 6.9 | 192 | **1.00** |
| no_watcher | 0.55 | **0.000** | **6.7** | 5.8 | 211 | 0.15 |

**Four organs separate cleanly** on their own invariant — skin (ledger 209 → 0),
two memories (slow 5.8 → 0), brake (energy 0.15 → 1.00), watcher (γ 0.078 →
0.000). Spotlight is directional but marginal at n = 20 (wins 0.55 → 0.15,
intervals [0.25, 0.90] vs [0.00, 0.30]).

### 3.1 The sham result: theatre, measured

| | γ | blocked_repeats |
|---|---|---|
| real watcher | 0.078 | **4.85** |
| sham watcher | **0.047** | **6.70** |
| no watcher | 0.000 | **6.70** |

The sham performs the checking motion — **γ is nonzero** — and delivers *exactly*
the no-watcher outcome. 6.70 against 6.70.

> **A positive γ with zero benefit. γ alone cannot certify a watcher; it needs an
> outcome metric the steering is supposed to move.**

### 3.2 γ is a rate, not a good

`no_spotlight` has **the highest γ of any variant (0.264)** and the worst
everything else — blocked_repeats 13.8, wins 0.15. Random selection bumps walls
constantly, giving the watcher far more to catch.

**A degraded policy inflates its own watcher's γ.** A rising γ can mean the
checker started working, or that the thing being checked got worse.

### 3.3 Two-memory is decorative in `minimal`

`no_two_mem` is identical to minimal on wins, γ, blocked_repeats *and* ledger —
only `slow` differs. Because only `tuned` ever reads `slow`. In minimal the slow
store is **write-only**: it separates on its own invariant and has no downstream
effect whatever. That observation is what motivated the transfer test.

### 3.4 Two readings not to make

- **`no_brake` wins the most** (1.40, highest of any variant) with energy pinned
  at 1.00. Removing the brake improves 20-step performance and destroys the
  invariant. The honest statement is that the brake costs performance on a
  horizon too short to show what it buys — not that wins don't matter.
- **`no_skin` shows blocked_repeats 0.0.** That is *blindness*, not virtue: with
  no ledger there is no record to count against. Another zero that is a
  measurement artefact.

---

## 4. The transfer test

The question the demo never asked. Train one agent on **4 novel cities**, then
run **one city it has never seen** — three times from the same trained state,
differing only in the slow store's contents:

| arm | store at test time | tests |
|---|---|---|
| **intact** | as learned | — |
| **wiped** | empty | does carrying a store help at all? |
| **shuffled** | same size, same states, moves permuted | does the **content** help, or only the +0.3 bonus mechanics? |

Bias held at 0.2 in every arm, so goal-seeking is constant. Identical RNG stream
across arms, so all three see the same candidate draws — the arms are **paired**,
and the correct test is the per-seed difference, not independent intervals.

### 4.1 Round one — coordinate keys — falsified

Patterns keyed `at (x,y) → move`. n = 20,000:

| arm | win rate | dist to goal |
|---|---|---|
| intact | 0.3095 | 2.689 |
| **wiped** | **0.3196** | **2.630** |
| shuffled | 0.3190 | 2.639 |

| paired difference | win | dist | |
|---|---|---|---|
| intact − wiped | **−0.0102** [−0.0143, −0.0060] | **+0.0589** [+0.0401, +0.0774] | **HURTS** |
| intact − shuffled | **−0.0096** [−0.0141, −0.0054] | **+0.0493** [+0.0304, +0.0703] | **HURTS** |
| wiped − shuffled | +0.0006 | −0.0097 | null |

**The trained store actively hurts**, and is worse than a shuffled store. Wiped
≈ shuffled, so the harm is specific to *correctly learned* patterns.

**Why.** `at (x,y) → move` encodes detours around walls that existed in the
training cities. In a new city the walls are elsewhere, so those detours are
systematically wrong — they steer around obstacles that are not there. A
shuffled store is harmless precisely because it is random and rarely matches the
current state. The real store fires reliably, and fires wrong.

That is **breadth**: a bag of surfaces. The demo built it and labelled it
generality.

### 4.2 Round two — relational keys — confirmed

Change one thing: key the experience by the **situation** rather than the cell.

```
coord       'at (2, 3) → down'                — names the CELL
relational  'blk0101|goal(1,1) → down'        — names the SITUATION
```

Which neighbours are blocked, plus the coarse direction of the goal. The agent
already computes adjacency for its goal bias, so this uses **no information the
coordinate key did not have.** n = 20,000:

| | store | hits/episode | intact − wiped (win) | intact − shuffled (win) |
|---|---|---|---|---|
| coordinate | 7.11 | 7.42 | −0.0102 **HURTS** | −0.0096 **HURTS** |
| **relational** | 8.74 | **15.78** | **+0.0338** [+0.0280, +0.0402] **HELPS** | **+0.0255** [+0.0194, +0.0315] **HELPS** |

Distance, same direction and stronger: coordinate **+0.0589** (worse),
relational **−0.1437** [−0.1702, −0.1180] (better).

**Three things this establishes.**

1. **The thesis holds.** "One structure for many surfaces, because many surfaces
   share one constraint" is true *and measurable* — when the key names the
   situation. Same agent, same bias, same RNG, same sham.
2. **The compression signature is in the numbers.** 1.2× the patterns, **2.1×
   the coverage.** A store barely larger that fires more than twice as often is
   what "one rule spanning many cases" means, made countable.
3. **The sham control passes.** Intact beats *shuffled* by +0.0255 win and
   −0.130 distance, so the gain is the store's **content**, not the bonus
   mechanics. Under coordinate keys that same control was null or negative.

One honest detail: shuffled relational slightly beats wiped (−0.0083 win). A
relational store fires often enough that even a wrong one breaks ties more
consistently than raw utility noise. The intact store beats it by three times
that, which isolates the content effect.

---

## 5. Convergence with S126

The same week, in a different paradigm, on a language model rather than a grid
agent (n = 12 seeds per arm, `laguna-s-2.1-free`):

| arm | mean | vs raw |
|---|---|---|
| raw | 0.8194 | — |
| ledger available, no forced check | **0.8958** | **+0.0764** |
| ledger + forced check | 0.6736 | **−0.1458** |
| **sham** (shuffled verdict) | **0.6667** | **−0.1527** |

**Locked primary S1 = withcheck − sham = +0.0070.** Null. A real check is
indistinguishable from a shuffled one. And **11 of 12 withcheck seeds scored
exactly 0.6667** — the check did not merely fail to help, it drove a subject
that reaches 0.8194 unaided onto the constant-policy floor. P1 refuted
(delta −0.2222 against a locked threshold of +0.15); P2 refuted; P3 held.

The forced-check arm sits essentially **on top of sham**, which has collapsed to
the exact always-no floor. And the navigator's sham watcher produced exactly the
no-watcher outcome.

**Two independent experiments, same conclusion: a check performed as ritual is
indistinguishable from a check performed on shuffled content.** The gradient
corpus already had this — *"full 8-piece watcher degrades calibration, 7 times,
including on 568K human trials; matched-deficit only +0.005/trial."*

> **Watching helps only when matched to a genuine deficit.** Availability is
> matched by definition; ritual is not.

---

## 5b. The two open questions, settled

`tools/run_scale_test.py`. Both were left open by the n=20 run; both are cheap
to answer properly because none of this touches a provider.

### Q1 — spotlight is necessary. The marginality was underpowering.

Variants share RNG streams per seed, so they are **paired** — the correct test
is the per-seed difference, not overlapping independent intervals. At n = 2000:

| ablation | metric | paired diff vs minimal | |
|---|---|---|---|
| no_skin | ledger | −211.71 [−212.20, −211.23] | SEPARATES |
| no_two_mem | slow | −6.53 [−6.62, −6.43] | SEPARATES |
| **no_spotlight** | **wins** | **−0.4235** [−0.4570, −0.3890] | **SEPARATES** |
| no_brake | energy | +0.8500 [+0.8500, +0.8500] | SEPARATES |
| no_watcher | γ | −0.0882 [−0.0917, −0.0849] | SEPARATES |
| no_spotlight | blocked_repeats | +9.83 [+9.60, +10.08] | SEPARATES |
| **sham_watcher** | **blocked_repeats** | **+1.89** [+1.78, +2.00] | **SEPARATES** |

minimal wins **0.622**, no_spotlight wins **0.198** — a threefold gap, 964/2000
pairs differing. **All five organs now separate**, each on its own invariant,
each in the direction predicted before the run.

The last row strengthens the theatre finding: the sham watcher is not merely no
better than the real one, it is **measurably worse**, +1.89 repeat wall-bumps
with a tight interval.

### Q2 — relational transfer survives scale, and the compression signature grows

Prediction stated before running: a coordinate store must grow with grid **area**
because there are more cells and less chance of revisiting one; a relational
store should grow far more slowly, because the number of distinct local
situations does not depend on grid size.

n = 5000 per cell, walls at 15% density, step budget 4n:

| grid | cells | key | store | hits/ep | **hits per pattern** | intact − wiped | intact − shuffled |
|---|---|---|---|---|---|---|---|
| 5 | 25 | coord | 6.7 | 6.7 | **1.00** | −0.0066 null | −0.0058 null |
| 5 | 25 | relational | 8.5 | 18.1 | **2.13** | **+0.0446 HELPS** | **+0.0206 HELPS** |
| 8 | 64 | coord | 11.5 | 9.7 | **0.84** | −0.0088 **HURTS** | −0.0078 **HURTS** |
| 8 | 64 | relational | 12.1 | 50.0 | **4.13** | **+0.0486 HELPS** | **+0.0364 HELPS** |
| 12 | 144 | coord | 17.2 | 12.9 | **0.75** | −0.0004 null | −0.0014 null |
| 12 | 144 | relational | 14.4 | 100.2 | **6.96** | **+0.0264 HELPS** | **+0.0208 HELPS** |

**Three things, all of them the point.**

1. **Relational transfer holds at every scale, against both controls including
   the sham.** Coordinate keys never help anywhere — null, negative, null.

2. **The stores cross over.** At 5×5 the relational store is *larger* than the
   coordinate one (8.5 vs 6.7). By 12×12 it is *smaller* (14.4 vs 17.2), while
   the grid has grown 5.8× in area. Coordinate grows 2.6×; relational grows
   1.7×. Sub-linear, not flat — the honest statement — but growing far slower
   than the world it covers.

3. **Coverage per pattern moves in opposite directions.** This is the
   compression claim as a function of scale, and it is the cleanest number in
   the whole study:

   ```
   coordinate:  1.00  →  0.84  →  0.75     each pattern earns LESS as the world grows
   relational:  2.13  →  4.13  →  6.96     each pattern earns MORE as the world grows
   ```

> **That is "one geometry that makes in-between cheap," measured.** As surfaces
> multiply, a store of memorised places has to grow while each entry pays less;
> a store of recognised situations grows slower while each entry pays more.

Relational transfer does soften at 12×12 (+0.026 vs +0.049 at 8×8) — bigger
grids are simply harder, with more room to wander inside the step budget — but
it stays clearly positive with tight intervals at every size.

---

## 5c. Confirmatory replication (lock `cbedb522`)

Everything above is exploratory: the transfer result and the relational repair
were produced by the same runs that measured them. A confirmatory design was
therefore frozen before any of its data existed.

**Discipline.** Seeds **500001–520000**, disjoint from every range drawn from
previously (1..20000 transfer, 1..5000 scale, 1..2000 ablation). Seven numeric
predictions with thresholds set *below* the exploratory point estimates. Two of
them null predictions, so a positive relational result could not be an artefact
of merely holding a store. Primary outcome declared in advance: **R2, the sham
contrast.** Prereg and both runner files hashed into the lock; the runner
verifies its own hashes at startup and aborts if anything changed. Lock
committed at `10a5a42` with zero confirmatory seeds executed. One run, no
peeking, no re-analysis.

| grid | key | store | hits/ep | hits/pattern | intact − wiped | intact − shuffled |
|---|---|---|---|---|---|---|
| 5 | coord | 6.77 | 6.7 | **0.99** | −0.0108 [−0.0150, −0.0067] | −0.0126 [−0.0173, −0.0083] |
| 5 | relational | 8.51 | 18.1 | **2.13** | **+0.0425** [+0.0367, +0.0487] | **+0.0309** [+0.0249, +0.0372] |
| 8 | coord | 11.55 | 9.6 | **0.83** | −0.0040 [−0.0072, −0.0008] | −0.0042 [−0.0078, −0.0006] |
| 8 | relational | 12.05 | 49.6 | **4.12** | **+0.0442** [+0.0387, +0.0495] | **+0.0352** [+0.0295, +0.0411] |
| 12 | coord | 17.24 | 13.0 | **0.75** | −0.0043 [−0.0066, −0.0020] | −0.0029 [−0.0053, −0.0006] |
| 12 | relational | 14.43 | 100.0 | **6.93** | **+0.0207** [+0.0170, +0.0244] | **+0.0159** [+0.0118, +0.0200] |

**7/7 predictions held.**

| | prediction | observed | |
|---|---|---|---|
| R1 | relational helps vs no memory ≥ +0.020 | +0.0425 | PASS |
| **R2** | **PRIMARY — content, not mechanics, ≥ +0.010** | **+0.0309** | **PASS** |
| R3 | coordinate does not help (≤ 0) | −0.0108 | PASS |
| R4 | coordinate content does not help | CI upper −0.0083 | PASS |
| R5 | coverage ≥ 2× | 2.13 vs 0.99 = **2.15×** | PASS |
| R6 | coverage diverges with scale | rel 2.13→4.12→6.93, coord 0.99→0.83→0.75 | PASS |
| R7 | transfer survives at all grid sizes | CI excludes 0 at 5, 8, 12 | PASS |

Two things are worth noting beyond the pass count.

**The coordinate result strengthened.** At the exploratory n=5000 it was null at
grids 5 and 12; at n=20,000 it is negative at *all three* sizes with intervals
excluding zero. Memory keyed by cell does not fail to transfer — it transfers
**harm**, reliably.

**The compression signature replicated to two decimals.** Exploratory coverage
was 2.13 / 4.13 / 6.96; confirmatory is 2.13 / 4.12 / 6.93. That is the claim
the whole demo was built to make, now measured twice on disjoint data:

> As the world grows, a store of memorised **places** covers less per entry
> (0.99 → 0.83 → 0.75) while a store of recognised **situations** covers more
> (2.13 → 4.12 → 6.93).

Results: `experiments/confirmatory_transfer_results.json`.

---

## 6. What is and is not established

**Established.** **All five organs separately necessary**, each with a named
failure predicted before the run, paired at n = 2000. Sham watchers produce
positive γ with a *worse* outcome than the real one (+1.89 repeat bumps). γ is a
rate that a degraded policy inflates. Coordinate-keyed memory never transfers at
any grid size; relationally-keyed memory transfers at every grid size against
both controls, and its coverage per pattern *rises* with scale (2.1 → 4.1 → 7.0)
while the coordinate store's *falls* (1.00 → 0.84 → 0.75).

**Not established.** Whether any of this survives outside grid-world — a
navigator with random utilities is a deliberately weak substrate, and the
organs' job here is visibly to keep it accountable rather than to make it
capable. Whether tuned beats minimal (intervals touch). Anything about the five
at scales this experiment cannot reach.

**The lesson that generalises past the demo:** three separate times in this
programme, a number that was a property of the *construction* was read as a
property of the *system* — the 0.6667 floor, γ = 0.00, and `no_skin`'s
blocked_repeats of 0.0. Each survived because it was infrastructure rather than
a claim, and infrastructure is what nobody audits.

---

*Companion: `GRADIENT_AND_THE_FIVE_ORGANS.md` (the corpus this tests) ·
`WHAT_YOU_CAN_ACTUALLY_DO.md` · `LTP_LTD_LOOPS.md`. Reproduce:
`python3 tools/run_ablation_v2.py 20`.*
