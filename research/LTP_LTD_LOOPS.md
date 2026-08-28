# LTP and LTD as Loops

**The part usually missed: LTP and LTD are not a loop and its brake. They are
two loops that both run away, and the brake is a third, slower one.**

---

## The two fast loops

```
LTP — strengthening                    LTD — weakening
───────────────────                    ───────────────
pre + post fire together               weak, unpaired activity
        ↓                                      ↓
Mg²⁺ ejected, NMDA opens               NMDA flickers open
        ↓                                      ↓
big brief Ca²⁺ SPIKE                   slow Ca²⁺ TRICKLE
        ↓                                      ↓
CaMKII (kinase)                        calcineurin → PP1 (phosphatase)
        ↓                                      ↓
AMPA receptors phosphorylated          AMPA dephosphorylated,
and inserted                           pulled out by clathrin endocytosis
        ↓                                      ↓
synapse stronger                       synapse weaker
        ↓                                      ↓
MORE likely to fire with partner       LESS likely to participate
        ↓                                      ↓
    ┌───┘                                  ┌───┘
    └──► back to the top                   └──► back to the top
```

Both are **positive feedback in their own direction.** Strengthening makes
future strengthening more likely. Weakening makes future weakening more likely —
use it or lose it, and losing it means using it even less.

So neither one restrains the other. Left alone, a synapse either saturates or
vanishes.

---

## The switch between them is a shape, not a substance

The same ion decides both fates. What differs is its profile.

| | Calcium signal | Enzyme recruited | Outcome |
|---|---|---|---|
| **LTP** | High amplitude, brief | Kinases (CaMKII, PKC) | Receptors in, spine grows |
| **LTD** | Low amplitude, prolonged | Phosphatases (calcineurin, PP1) | Receptors out, spine shrinks |

**Why low calcium picks phosphatases:** they have higher affinity for Ca²⁺ than
the kinases do. At a trickle, only the high-affinity enzymes activate. At a
spike, the kinases engage and dominate.

That is the entire switch. Not two pathways with a selector — one pathway whose
downstream outcome inverts depending on the *shape* of the input.

### Why the coincidence requirement exists at all

The NMDA receptor is plugged by a magnesium ion that is only electrostatically
repelled when the postsynaptic cell is *already* depolarised. So the channel
opens only when presynaptic glutamate and postsynaptic activity arrive
**together**.

Hebb's rule, implemented in protein. Fire together, wire together — but the
"together" is enforced by a physical plug, not by a rule written somewhere.

---

## CaMKII is why the loop outlives its cause

Worth isolating, because it is the strangest piece.

CaMKII autophosphorylates at Thr286 — **each subunit phosphorylates its
neighbour** — so once the switch flips it stays on after the calcium has
cleared.

A molecular latch holding the memory of an event that has already ended. The
loop persists without its trigger, which is the minimum requirement for anything
to count as **memory** rather than **reaction**.

---

## The third loop — the one that actually brakes

Since both fast loops self-amplify, stability has to come from somewhere slower.
That is **metaplasticity**: the BCM sliding threshold θₘ.

```
        ┌──────────── watches the neuron's own recent history ────────────┐
        ▼                                                                 │
neuron has been quiet ──► θₘ slides DOWN ──► easier to potentiate ────────┤
                                                                          │
neuron has been hyperactive ──► θₘ slides UP ──► harder to potentiate ────┘
```

The threshold separating "this counts as LTP" from "this counts as LTD"
**moves, based on what the neuron has been doing.** A quiet synapse becomes
eager; a saturated one becomes resistant.

**Oja's rule** does the complementary job across synapses — normalising weights
so no single input takes all the strength, which turns Hebbian growth into
something closer to principal-component extraction rather than winner-take-all.

**Synaptic scaling** and sleep's global downscaling operate on the same
principle at longer timescales: multiply everything by a factor below one, keep
the relative strengths, delete the noise.

---

## The two commit speeds

| | Early LTP | Late LTP |
|---|---|---|
| Duration | 1–3 hours | Days to lifetimes |
| Requires | Local protein modification only | Gene transcription, new protein |
| Mechanism | CaMKII phosphorylates existing AMPA receptors, drives insertion from intracellular stores | Ca²⁺ → adenylyl cyclase → cAMP → PKA → nucleus → CREB → BDNF → actin remodelling, spine enlargement |
| Reversible? | Largely | Structural — a new spine exists |

**Synaptic tagging and capture** decides which synapses get the scarce
newly-synthesised proteins: weak activity sets a local tag, strong activity
elsewhere triggers protein synthesis, and the proteins are captured by whatever
is tagged.

**Salience decides what becomes permanent.** Not recency, not repetition alone —
salience.

---

## Why this is the same architecture as everything else

Map it onto the five organs and it is exact:

| Organ | At the synapse |
|---|---|
| Boundary | The cleft — which side fired is attributable |
| Two-speed memory | Early LTP (hours, local) vs late LTP (days, transcription, new spine) |
| Salience gate | Tag-and-capture — which tagged synapse captures the scarce proteins |
| **Damping** | **LTD, synaptic scaling, Oja normalisation** |
| **Internal observer** | **BCM θₘ — a slower loop watching a faster one and changing its rules** |

**The synapse has a metacognition layer.** It watches its own recent activity and
adjusts what will count as significant next time. That is the same speed-ratio
move as prefrontal cortex over amygdala, or a journal over a day — just at
milliseconds against minutes.

---

## What it means one level up

Three consequences follow directly.

### There is no neutral

Plasticity is always running. Not practising something is practising the
default. Whatever you repeat gets myelinated, up to roughly 100× conduction
speed — so the highway gets paved whether or not you chose its direction.

### Forgetting is a feature, and it is active

Without LTD every synapse saturates and nothing is distinguishable. Erasure is
not decay — it is machinery: clathrin coats the membrane, dynamin pinches the
vesicle off, and the receptors are carried inside to be stored or destroyed.

A brain that could only strengthen would learn everything once and then be
unable to distinguish anything.

### Rumination is the LTP recipe

High-frequency, emotionally intense, repeated. Which means a depressive loop is
not *failing* to break itself — it is **succeeding at exactly what the mechanism
does**. The circuit gets easier to run tomorrow because it ran today.

And the corollary, which is the entire mechanical basis of cognitive defusion:

> **Observing a thought without engaging it produces the low-frequency
> trickle.** That is the phosphatase condition. Not passivity — the specific
> input pattern that weakens the circuit.

"I am anxious" is identity-level and drives continuous engagement: kinases,
strengthening. "I notice I am having the thought that I am anxious" drops the
charge, and the dropped charge drops the firing frequency into the regime where
phosphatases dominate.

---

## The whole thing in one picture

```
   FAST                          FAST                       SLOW
   ────                          ────                       ────
   LTP loop                      LTD loop                   BCM / scaling
   (self-amplifying)             (self-amplifying)          (watches both)
        │                             │                          │
        └──────────► both run away ◄──┘                          │
                          ▲                                      │
                          │                                      │
                          └────── threshold moved by ────────────┘
```

Two fast loops that would each destroy the system alone, arbitrated by a slower
loop that changes the rules based on history.

That is not a synapse-specific design. It is the minimum viable architecture for
anything that has to keep learning without either saturating or forgetting
itself out of existence.

---

*Related: `SEVEN_LOOPS.md` for the same cycle at seven scales ·
`REFLEXIVE_SYSTEMS_AND_THE_CLINICAL_LOOP.md` for what this implies for
depression, CBT and medication · `WHAT_IT_ALL_MEANS_FULL.md` for the full
synthesis.*
