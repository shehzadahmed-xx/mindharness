# The Seven Loops

**One loop, seven substrates.** From a synapse to a harness, the same six-step
cycle runs. What changes is what is bounded, what competes, and what gets
broadcast. The cycle itself does not change.

This document walks each level in full: the mechanism, the diagram, what
breaks when a piece is removed, and how each level's output becomes the next
level's input.

*Status note (2026-08-29): the framework below is a description. Where it has
been tested, the results are reported in `paper_v2` and summarised in
§Empirical status at the end. One central prediction has been refuted. That is
in here too.*

---

## The cycle, written once

Every level runs these six steps:

```
   ┌──────────────────────────────────────────────────────────────┐
   │                                                              │
   ▼                                                              │
1. BOUNDARY ── decides what counts as inside vs outside           │
   │                                                              │
   ▼                                                              │
2. INPUT ───── perturbation arrives and is admitted               │
   │                                                              │
   ▼                                                              │
3. COMPETITION ─ which response wins? (salience × utility)        │
   │                                                              │
   ▼                                                              │
4. BROADCAST ── the winner is made globally available             │
   │                                                              │
   ▼                                                              │
5. CONSOLIDATION ─ what is kept, what is discarded                │
   │                                                              │
   ▼                                                              │
6. STATE UPDATE ─ the system is now different                     │
   │                                                              │
   └──── and the boundary it starts from next time has moved ─────┘
```

Step 6 feeding back into step 1 is the whole point. The system that receives
the next input is not the system that received the last one. That is what
makes the loop *reflexive* rather than merely repetitive.

---

## Level 1 — Molecule: the synapse

**Ca²⁺ is the vote. AMPA insertion is the broadcast.**

```
  presynaptic                    synaptic cleft                  postsynaptic
  ───────────                    ──────────────                  ────────────
   glutamate  ──────────────────────►  ▓▓▓  ──────────────►  NMDA receptor
                                       20nm                        │
                                                                   │ needs BOTH:
                                                                   │  glutamate (pre)
                                                                   │  depolarisation (post)
                                                                   ▼
                                                            Mg²⁺ plug ejected
                                                                   │
                                                                   ▼
                                              ┌──── big, brief Ca²⁺ spike ────┐
                                              │                              │
                                              ▼                              ▼
                                          CaMKII                        calcineurin
                                       (Thr286 switch)                    → PP1
                                              │                              │
                                              ▼                              ▼
                                        AMPA inserted                 AMPA removed
                                            = LTP                        = LTD
                                              │
                                              ▼
                                    stronger synapse next time
                                              │
                                              └──────► feeds back to the top
```

| Step | At the synapse |
|------|----------------|
| Boundary | The synaptic cleft, ~20nm. It establishes which side fired — pre vs post — and therefore whose activity is whose. Without a gap there is no way to attribute. |
| Input | Glutamate from the presynaptic side, arriving into a postsynaptic membrane that may or may not already be depolarised. |
| Competition | Not between neurons — between **kinases and phosphatases**. A big, brief Ca²⁺ spike recruits CaMKII. A small, prolonged trickle recruits calcineurin. Same receptor, same synapse, opposite outcomes, decided by the *shape* of the calcium signal. |
| Broadcast | The CaMKII Thr286 switch. Each subunit phosphorylates its neighbour, so the switch stays on after the calcium has cleared. That is a molecular record of an event that has already ended. |
| Consolidation | Tag-and-capture. Weak activity sets a local tag; strong activity elsewhere triggers protein synthesis, and the proteins diffuse and are captured by whatever is tagged. Salience decides what gets the proteins. |
| State update | The BCM threshold θₘ slides with the neuron's own recent history — a quiet neuron becomes easier to potentiate, a hyperactive one harder. Oja's rule normalises the weights so no single input takes all the strength. |
| Next input | A stronger synapse is more likely to fire with its partner, more likely to cross threshold, therefore more likely to be strengthened again. |

### Why this is already a loop

NMDA is a **coincidence detector**: the channel opens only when the
presynaptic and postsynaptic sides are active together. So the synapse's
current strength determines whether the next coincidence is detected at all —
and that detection determines its next strength.

The synapse is not a component that participates in a loop. It *is* one, at
the smallest scale where the pattern appears.

### What breaks without each piece

| Remove | Result |
|--------|--------|
| The cleft | No pre/post distinction. Coincidence cannot be detected. Hebbian learning fails outright. |
| Damping (LTD, BCM, Oja) | Runaway potentiation. Fire together → wire together → fire more → everything fires at everything. That is a seizure. |
| The salience gate | Every trace gets the proteins equally. Saturation: all synapses strong, none distinct. |

---

## Level 2 — Cell: the neuron

**Firing is the vote. The action potential is the broadcast.**

```
   thousands of synapses, each a vote
   ┌────┬────┬────┬────┬────┬────┬────┐
   │ +  │ +  │ −  │ +  │ −  │ +  │ +  │
   └─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┘
     └────┴────┴────┴────┴────┴────┘
                    │
                    ▼
        spatial + temporal summation
           at the axon hillock
                    │
         ┌──────────┴──────────┐
         │ threshold crossed?  │
         └──────────┬──────────┘
              no ───┘   └─── yes
              │              │
           silence           ▼
                     ACTION POTENTIAL
                     all-or-nothing
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
         every downstream        changes which partners
            synapse               are active next time
```

| Step | At the neuron |
|------|---------------|
| Boundary | The cell membrane — and critically, it is **self-produced**. Metabolism builds the lipids that form the membrane that bounds the metabolism. The boundary is the network's own product, maintained continuously or the chemistry diffuses to equilibrium. |
| Input | Thousands of synaptic inputs, each a vote for "fire" or "don't". None is decisive. |
| Competition | Spatial and temporal summation at the axon hillock. Inputs arriving *together* count for more than the same inputs spread out — coincidence wins again, one scale up. |
| Broadcast | The action potential. All-or-nothing, no partial answer, no private answer, delivered to every downstream synapse at once. |
| Consolidation | Spike-timing-dependent plasticity. Pre-before-post strengthens; post-before-pre weakens. That asymmetry is how a network converts mere correlation into something closer to causation. |
| State update | After-hyperpolarisation adapts the threshold; neuromodulators shift the gain of the whole cell at once. |
| Next input | Firing changes which presynaptic partners stay active, so the next vote is taken among a different electorate. |

### The one thing to take from this level

**A neuron is a parliament of synapses competing for a single microphone.** No
individual synapse decides. The *configuration* votes.

And the cell persists as a **pattern, not as stuff**. Its proteins turn over in
days. What continues is the network of processes that regenerates the
conditions for its own continuation.

---

## Level 3 — Circuit: hippocampus and cortex

**Salience is the vote. Replay is the broadcast.**

```
   DAY                                      NIGHT
   ───                                      ─────
   experience                          ┌─ slow-wave sleep ─┐
       │                               │                   │
       ▼                               │   1. DOWNSCALING  │
   salience tags it?                   │   multiply all    │
   (emotion, surprise,                 │   synapses by <1  │
    prediction error)                  │   keep relatives  │
       │                               │   delete noise    │
    ┌──┴──┐                            │                   │
   yes    no                           │   2. REPLAY       │
    │      └── fades                   │   ripples nested  │
    ▼                                  │   in spindles     │
  HIPPOCAMPUS                          │   in slow waves   │
  fast, one-shot,      ────────────►   │   10–20× compressed
  pattern-separated                    │        │          │
                                       └────────┼──────────┘
                                                ▼
                                            CORTEX
                                       slow, statistical,
                                          interleaved
                                                │
                                                ▼
                                   shapes what tomorrow
                                   is recognisable as
```

| Step | At the circuit |
|------|----------------|
| Boundary | Hippocampus vs cortex. Not merely anatomical — two systems with *different rules*, competing for consolidation priority. One is one-shot and pattern-separated; the other is statistical and interleaved. |
| Input | Experience, arriving with a salience tag or without one. |
| Competition | Which traces get tagged for consolidation. Emotion, surprise and prediction error decide. |
| Broadcast | Hippocampal replay during sleep — ripples nested inside spindles, nested inside slow waves, running the day back at 10–20× compression. |
| Consolidation | Two operations, not one. **Downscaling** multiplies every synapse by a factor below one, keeping relative strengths and deleting noise. **Replay** writes the surviving patterns into cortex. |
| State update | Perineuronal nets write-protect what is settled. Adenosine is the receipt for the day's potentiation. The BDNF available for the whole process is budgeted by exercise and stress. |
| Next input | The consolidated cortex determines what the next day can even recognise. |

### Two speeds, because the world has two timescales

You need a fast store for *this happened once, today*, and a slow one for
*this is how things generally are*. Fast alone means new writing destroys old.
Slow alone means single events never register.

**Sleep is the save.** Skip it and the day's tagging is wasted: potentiation
saturates, and a network that has learned everything distinguishes nothing.

---

## Level 4 — Mind: the parliament

**A coalition is the vote. The global workspace is the broadcast.**

```
   perception   memory   body budget   affect   habit   planner   narrator
       │          │           │          │        │        │         │
       │  each bids: salience × utility  │        │        │         │
       └──────────┴───────────┴──────────┴────────┴────────┴─────────┘
                                  │
                    neuromodulators set the rules:
                      noradrenaline = volume
                      dopamine      = stake
                      valence       = risk dial
                                  │
                                  ▼
                    ╔═════════════════════════╗
                    ║   GLOBAL WORKSPACE      ║   new vote
                    ║   one winner broadcast  ║   every ~200ms
                    ╚═════════════════════════╝
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
      every specialist      experienced as      rehearsed →
      receives it            "my thought"        myelinated
                                  │              (up to 100×
                                  │               faster)
                                  ▼                   │
                     ┌────────────────────┐           │
                     │ THE NARRATOR wins  │           │
                     │ ~200ms AFTER the   │           │
                     │ action, and        │           │
                     │ explains as though │           │
                     │ it had decided     │           │
                     └────────────────────┘           │
                                                      ▼
                                          next competition is biased
                                          toward the same winner
```

| Step | At the mind |
|------|-------------|
| Boundary | The narrative self: "this story is mine" vs "that was handed to me." Maintained by compare-and-set revision, cause-signing, and re-injection every turn. A persona left to context position alone drifts more than 30% within twelve turns. |
| Input | Sensory input, body state, memory and affect, each proposing a candidate with a bid. |
| Competition | Six to eight parties bid for one microphone, roughly every 200ms. Neuromodulators set the election rules globally rather than choosing a winner directly. |
| Broadcast | The winning content becomes available to every specialist simultaneously. You experience this as "my thought." |
| Consolidation | Light (deduplicate) → REM (extract concepts) → Counterfactual (simulate the branch not taken, score regret) → Deep (promote if it clears a utility gate). Every promotion carries a signed cause or it is blocked. |
| State update | Energy drains, fatigue rises, valence and arousal shift — and affordance gating removes unavailable strategies *before* the vote, so they never appear as options. |
| Next input | The broadcast is the context the next competition runs inside. The winner that was rehearsed is more likely to win again. |

### The two things people get wrong here

**There is no captain.** The mind is not a thing that *has* a parliament. It
*is* that competition, broadcast and then rehearsed. The configuration votes.

**The narrator is late.** It receives the broadcast, not the competition that
produced it, and it produces the most coherent story in which "I" caused the
result. It is not lying — it has no other option. Split-brain patients invent
reasons instantly and believe them; people asked why they chose a face they
actually rejected explain the choice they never made.

An exhausted self does not face a *harder* choice. It faces **fewer options**,
because affordance gating removed the tiring ones before the vote began.

---

## Level 5 — Person: the life

**A choice is the vote. Action is the broadcast.**

```
        situation
            │  (already filtered — an exhausted self
            │   has fewer options, not harder ones)
            ▼
    ┌───────────────────────────────────┐
    │  habit  vs  deliberation          │
    │  affect vs  social expectation    │   ← state rigs the vote
    │  all bidding simultaneously       │     before it starts
    └───────────────┬───────────────────┘
                    ▼
                 ACTION
                    │
        ┌───────────┴────────────┐
        ▼                        ▼
  world now contains      you are now different
  your act                (record, self-model,
        │                  skills all changed)
        └───────────┬────────────┘
                    ▼
            replay: what happened
                    │
                    ▼
        counterfactual: what could have
                    │
                    ▼
              regret = gradient
                    │
                    ▼
        character as attractor —
        which coalitions tend to win,
        carved by every prior rehearsal
                    │
                    └──► loop widens, never returns
```

| Step | At the person |
|------|---------------|
| Boundary | The life story — "this is who I am over time" vs "that was something that happened to me." Maintained narrative, not stored fact. |
| Input | The situation, already filtered through current affordances. |
| Competition | Habit, deliberation, affect and social expectation bid against each other, and your state has already rigged the outcome. Tired-and-anxious is a different parliament from rested-and-safe, running on the same hardware. |
| Broadcast | The action. It enters the world as a consequence others must respond to. |
| Consolidation | Replay what happened, then simulate what could have happened. The gap produces regret, and regret is the gradient that calibrates the next turn. |
| State update | Character accumulates as an attractor: the set of coalitions that tend to win, carved by every rehearsal that came before. |
| Next input | The world now contains your act, and a different you perceives a different world. |

### Where agency actually sits

Not at the moment of choosing — that arrives after the vote. It sits in three
slower places:

1. **The veto.** You can refuse the winner before it executes. Refusal, not creation.
2. **The record kept between moments.** A witness the narrator cannot silently edit, checked before the next story is told.
3. **What you rehearse.** Repetition myelinates, and myelination decides which coalition wins next time. Worry practised a thousand times is not a thousand neutral events — it is one worry amplified a thousand times by its own winning.

You do not choose whether to feed the loop. Only what you feed it.

---

## Level 6 — Society: the market

**An order is the vote. Price is the broadcast.**

```
   news, order flow, belief
            │
            ▼
   ┌─────────────────────────────────┐
   │  buyers   vs   sellers          │
   │  narrative vs  narrative        │
   │                                 │
   │  weight = salience (volume,     │
   │           attention, coverage)  │
   │         × utility (expected     │
   │           risk-adjusted return) │
   └────────────────┬────────────────┘
                    ▼
              ╔══════════╗
              ║  PRICE   ║ ── broadcast to every participant
              ╚══════════╝    simultaneously
                    │
        ┌───────────┴────────────┐
        ▼                        ▼
  becomes the reality      institutions, law,
  every next decision      culture = slow memory
  must respond to          of which competitions won
        │                        │
        ▼                        ▼
  ┌──────────────────────────────────────┐
  │ DAMPING: position limits, circuit    │
  │ breakers, funding invariants,        │
  │ central bank                         │
  │                                      │
  │ cut these and the loop has no brake  │
  └──────────────────────────────────────┘
```

| Step | At the market |
|------|---------------|
| Boundary | Legal entity and balance sheet: this capital is mine, that liability is yours, and someone specific bears the risk when the money runs out. |
| Input | Information — news, order flow, belief — perturbing the price. |
| Competition | Buyers against sellers, and narratives against narratives. The order book resolves the bids. |
| Broadcast | Price, delivered to everyone at once, immediately becoming the reality every subsequent decision must respond to. |
| Consolidation | Institutions, law and culture: slow structural memory encoding which competitions have tended to win, persisting long after the trades that made them. |
| State update | Damping is deliberate and institutional — position limits, circuit breakers, kill criteria, a central bank. |
| Next input | Price is the prediction and the prediction is the price. |

### Reflexivity at its most visible

Belief creates the reality the belief was about. A bank run is the clean case:
"the bank will fail" → withdrawals → the bank fails. The belief made itself
true.

No single trader decides the price. The configuration of beliefs, weighted by
capital and salience, votes. And when the damping is removed, the loop springs
— feeding on whatever is nearby.

---

## Level 7 — Machine: the harness

**A plugin is the vote. The ledger is the broadcast.**

```
   prompt + body signals + memory + affect
            │
            ▼
   ┌──────────────────────────────────────────────┐
   │  perception (VLM)      memory (retrieval)    │
   │  affect (steered)      planner (reasoner)    │  ← may be different
   │  habit (skills)        narrator              │    models entirely
   │                                              │
   │  each bids: salience × utility,              │
   │  scaled by AffectState                       │
   └───────────────────┬──────────────────────────┘
                       ▼
        ╔══════════════════════════════════╗
        ║  WORKSPACE WINNER                ║
        ║  + provenance spans              ║ ← auditable, not
        ╚══════════════════════════════════╝   merely available
                       │
                       ▼
      the model's next input is its own last
      output ── PLUS THE LEDGER
                       │
      ┌────────────────┴────────────────┐
      │  remove the ledger and this     │
      │  becomes a closed loop:         │
      │  generate → read own output →   │
      │  predict a consistent           │
      │  continuation → generate more   │
      │  There is no outside.           │
      └────────────────┬────────────────┘
                       ▼
      Light → REM → Counterfactual → Deep
      (untagged promotion blocked)
                       │
                       ▼
      energy drains, fatigue rises,
      γ = changed / diagnosed
                       │
                       ▼
      State(t) → harness(t+1)
```

| Step | In the harness |
|------|----------------|
| Boundary | The provenance ledger. Every span carries a source and a reference — memory lookup, model prior, monitor override, external tool. |
| Input | Prompt, body signals, memory and affect, all as proposals. |
| Competition | Plugins bid and are scored, modulated by affect. Not if-statements — scored bids. |
| Broadcast | The workspace winner together with its provenance spans, so what is broadcast is auditable rather than merely available. |
| Consolidation | Light → REM → Counterfactual → Deep, with untagged promotion blocked outright. |
| State update | Energy toward its floor, fatigue toward its cap, and γ recording whether diagnosis actually changed the action. |
| Next input | State(t) becomes harness(t+1). The harness rewrites the conditions for its own next iteration. |

### Why this is not a better prompt

It is the same parliament, the same workspace, the same consolidation cycle —
made of code instead of neurons, and therefore **checkable**. Change the
harness and the same frozen model becomes a different agent.

The distinctive element is γ. A system can keep a flawless record, produce
beautiful reports about it, and never let it change a single decision. γ =
changed / diagnosed is the measurement that separates monitoring from
steering, and a compliance guard that is zero by construction sits beside it as
a control.

---

## How the seven nest

The levels are not analogies for one another. They interlock.

```
  MOLECULE ──broadcast: AMPA insertion──────► becomes the CELL's synaptic weight
     CELL ──broadcast: the spike────────────► becomes the CIRCUIT's input
        CIRCUIT ──broadcast: replay─────────► becomes the MIND's memory
           MIND ──broadcast: the thought────► becomes the PERSON's action
              PERSON ──broadcast: the act───► becomes the MARKET's order
                 MARKET ──broadcast: price──► becomes the MACHINE's training data
                    MACHINE ──broadcast: ledger──► becomes checkable by all of them
```

Three couplings run between every adjacent pair:

| Coupling | What it means |
|----------|---------------|
| **Broadcast → input** | Each level's winner is the next level's raw material. No level is closed. |
| **Consolidation → boundary** | The slow memory of one level *is* the boundary of the next. Synaptic strength becomes circuit structure; semantic memory becomes character; institutions become the market's boundary. |
| **State → bias** | Each level's state update biases the next level's competition. BCM threshold biases which synapses can potentiate; energy and affect bias which coalitions can win; funding invariants bias which trades can happen. |

The same five organs — boundary, two-speed memory, salience gate, damping,
internal observer — appear at every level because every level faces the same
problem: stay stable enough to persist while staying flexible enough to learn,
in a world that contains you, where every action changes the conditions for the
next one.

Lose one and the pathology is the same at every scale, under a different name:

| Missing | Synapse | Mind | Market | Machine |
|---------|---------|------|--------|---------|
| Boundary | No coincidence detection | Persona drift | Risk socialised | Confabulation |
| Two speeds | No consolidation | Catastrophic forgetting | No institutions | No accumulation |
| Salience | Saturation | Nothing distinct | Noise drowns signal | Everything promoted |
| Damping | Seizure | Worry spiral | Cascade, crash | Hallucination loop |
| Observer | No metaplasticity | No correction | No risk desk | Reports, zero steering |

---

## Empirical status

The framework above is a description, and descriptions are cheap. Here is
what has actually been measured, including the part that went against us.

**The harness costs nothing.** On a subject able to discriminate its own
output, running it inside the full harness scored identically to running it
raw (0.833 both, 30/36 probes). An earlier result showing the harness
degrading performance turned out to be a property of the *subject*, not the
architecture — a model that cannot discriminate in any condition collapses to
denying everything.

**Most subjects cannot take the test.** Of six screened, five sat exactly on
the always-no floor in every seed. Only one discriminated. Any claim about
introspection or provenance in language models depends on a subject-selection
step that is rarely reported.

**The central prediction was refuted.** We locked a prediction that giving the
agent ledger access would improve attribution by more than 0.15. It came in at
**−0.111** — the opposite direction. Showing the agent its own record made it
*worse*.

**But the witness is a real channel.** A veridical ledger scored 0.722; a
shuffled one scored 0.667, collapsing to the always-no floor with zero
variance across seeds. The difference between a true and a false record
reaches the decision. The content transmits.

So the claim that survives is narrower than the one we set out with:

> A witness helps only when it is more reliable than the narrator it checks.
> When it is not, it is a distractor. When it is wrong, it is worse than
> having no witness at all.

Every interval in that battery includes zero at 36 probes per arm. A
preregistered extension at four times the sample size, with the sham contrast
declared primary in advance, is in progress.

---

*Seven loops, one cycle, six steps. What changes is the substrate. What does
not change is that the system which receives the next input is never quite the
system that received the last one.*
