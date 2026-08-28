# Reflexive Systems, Depression, and How the Loop Gets Broken

**From Soros to synapses to SSRIs.** One structure — a system whose actions
rewrite the conditions for its next actions — traced across economics, machine
learning, neurobiology, clinical psychology, pharmacology, and autonomous
vehicles.

The clinical sections are the substance here: what depression looks like as a
loop, how CBT interrupts it, and — the part usually left as a black box — what
medication actually does at the molecular level.

> **This is an explanatory document, not medical advice.** It describes
> mechanisms as currently understood. Decisions about medication belong with a
> prescribing clinician who knows the individual case. Nothing here should be
> used to start, stop, or alter a treatment.

---

## Part I — What a reflexive system is

In a standard system you are an observer watching a game. In a reflexive system
you are a player whose actions reshape the rules and the environment in real
time.

Three fields found this independently and named it three things.

### 1. Reflexivity (economics and finance)

George Soros's term. Investors' biases change market fundamentals, which change
investors' expectations.

```
People think a stock is valuable → they buy it → the price rises
→ the higher price makes the company look more valuable → more people buy
```

The belief did not *describe* the value. It *produced* it.

### 2. Non-stationary environments (AI and machine learning)

A *stationary* environment has fixed rules — chess. A *non-stationary* one
changes its distributions over time, especially when an agent interacts with it.

```
An algorithm starts buying an asset → its own volume shifts market liquidity
→ the environment changes → the model's original data is now obsolete
```

The agent invalidated its own training data by acting on it.

### 3. Recurrent feedback loops (systems dynamics)

A closed loop with feedback. Not A → B but A → B → A.

```
Microphone picks up sound → amplifies through speaker
→ picks up the speaker's own sound → deafening shriek
```

### Comparing system types

| Feature | Static (weather) | Dynamic (orbit) | **Reflexive (market, mind)** |
|---|---|---|---|
| Changes over time? | No | Yes | Yes |
| Affected by being observed? | No | No | **Yes** |
| Does acting change future state? | No | No | **Yes — directly alters reality** |
| Predictability | High | High (via physics) | **Low — chaotic loop** |

### Where you have already met this

- **Goodhart's Law** — "when a measure becomes a target, it ceases to be a good
  measure." Judge a hospital on waiting times and patients wait in ambulances
  instead. Measuring changed the behaviour of the thing measured.
- **Social media** — your feed shows a post, you linger three seconds, the
  algorithm rewrites itself to show more of that, and the information ecosystem
  you inhabit tomorrow is one your attention today produced.

---

## Part II — Humans are the clearest case

You are not a static object observing your life. You are a system where
thoughts change biology, biology changes actions, and actions rewrite who you
are.

```
  ┌──────────────────────────────────────────────────────────┐
  ▼                                                          │
[Thoughts] ──► [Biology] ──► [Actions] ──► [Environment] ────┘
```

### Layer 1 — The neurobiological loop

You feel stressed → the brain releases cortisol and adrenaline → heart rate
rises, muscles tense → **the anxious body signals the brain that danger is
present** → which generates more stressful thoughts.

The body is not downstream of the thought. It is an input to the next one.

### Layer 2 — The behavioural loop (self-fulfilling prophecy)

You believe you are bad at socialising → you sit in the corner → people don't
approach someone who looks closed off → **"See? I am bad at socialising."**

The belief did not predict the outcome. It arranged it.

### Layer 3 — The neuroplasticity loop (software rewriting hardware)

In computing, software cannot easily rewrite hardware. In humans it happens
continuously. Practise a skill → neurons fire together → the brain builds myelin
around those pathways → the skill becomes automatic → your baseline capability
has changed.

### Autopoiesis — the loop that builds its own container

Maturana and Varela's term for a system that continuously produces the
components that maintain it.

```
metabolism → produces proteins and lipids → regenerate the cell wall
→ the wall preserves the chemical environment metabolism needs → metabolism
```

**The product of the system is the system itself.** Your proteins turn over in
days. What persists is not the stuff but the pattern that keeps rebuilding it.

### The reflexive self (sociology)

Giddens's "reflexive project of the self": in traditional societies, action was
dictated by fixed external rules. In modernity, we observe our own behaviour,
ingest knowledge about ourselves from expert systems, and chronically revise —
and those revisions alter the social structure we exist within.

---

## Part III — The molecular layer: LTP and LTD

This is where "a thought changed me" stops being metaphor.

### Long-term potentiation — how a loop gets stronger

**Induction: coincidence detection.**

```
Low-frequency stimulus  → small glutamate release → only AMPA opens
                        → mild depolarisation → Mg²⁺ block stays

High-frequency stimulus → large glutamate release → mass AMPA opening
                        → strong depolarisation → Mg²⁺ repelled → Ca²⁺ floods in
```

At rest, glutamate binds both AMPA and NMDA receptors, but the NMDA channel is
plugged by a magnesium ion. Only when the postsynaptic cell is *already*
depolarised does that plug get electrostatically repelled. **The NMDA receptor
is therefore a coincidence detector** — it requires presynaptic glutamate *and*
postsynaptic activity together. That is Hebb's rule implemented in protein.

**Early-phase LTP (1–3 hours, no new proteins).** Calcium binds calmodulin,
activating CaMKII and PKC. CaMKII autophosphorylates at Thr286 — each subunit
phosphorylating its neighbour — so it **stays active after the calcium has
cleared**. A molecular latch holding the memory of an event that has ended. It
phosphorylates existing AMPA receptors, raising their conductance, and drives
insertion of more from intracellular stores.

**Late-phase LTP (days to lifetimes, requires transcription).**

```
Sustained Ca²⁺ → adenylyl cyclase → cAMP → PKA → travels to nucleus
→ phosphorylates CREB → transcribes BDNF and structural genes
→ actin remodelling → the dendritic spine physically enlarges
```

Synaptic tagging decides *which* synapses capture those newly made proteins —
so salience determines what becomes permanent.

### Long-term depression — how a loop gets weaker

Without LTD, synapses saturate: every connection maximally strong, nothing
distinct, no bandwidth for anything new.

```
Low-frequency stimulus → weak pulsed glutamate → Mg²⁺ block flickers
→ slow trickling Ca²⁺ → phosphatases activate (not kinases)
```

**The switch is the shape of the calcium signal, not its presence.** Phosphatases
have higher affinity for low calcium concentrations than kinases do. So a big
brief spike recruits CaMKII and strengthens; a small prolonged trickle recruits
calcineurin → PP1 and weakens.

PP1 strips the phosphate groups CaMKII added. The dephosphorylated AMPA
receptors detach from their anchors, drift into an endocytic zone, get wrapped
in a clathrin-coated pit, pinched off by dynamin, and pulled inside — either
stored or destroyed. The spine shrinks.

| | LTP | LTD |
|---|---|---|
| Stimulation | High-frequency burst | Low-frequency, prolonged |
| Calcium | High volume, rapid spike | Low volume, slow trickle |
| Enzymes | Kinases (CaMKII, PKC, PKA) | Phosphatases (calcineurin, PP1) |
| AMPA receptors | Phosphorylated, inserted | Dephosphorylated, removed |
| Structure | Spine enlarges | Spine shrinks |

**The consequence.** Repeatedly cycle a thought and the hardware for it expands.
Ignore a circuit and phosphatases erase its machinery. Your actions reshape what
your brain is literally capable of doing next.

---

## Part IV — Depression as a pathological loop

Depression is not "sadness that lasts." Structurally, it is a reflexive loop
that has become self-sustaining, where every output feeds an input that produces
more of the same output.

### The cognitive loop

```
   ┌─────────────────────────────────────────────────────┐
   ▼                                                     │
negative belief ──► attention biases toward confirming   │
("I'm a burden")    evidence ──► ambiguous events read   │
                    as confirmation ──► withdrawal ──►   │
                    fewer positive inputs ──────────────►┘
```

Each pass makes the next pass easier. Rumination is a high-frequency,
emotionally intense circuit — which is precisely the LTP recipe. **You are
potentiating the pathway you are suffering from.** The thought becomes easier to
think tomorrow because it was rehearsed today.

### The biological loop

Chronic stress flips the plasticity regime:

- Sustained **cortisol** biases hippocampus and prefrontal cortex toward LTD —
  dendrites retract, neurogenesis in the dentate gyrus slows, volume measurably
  declines.
- The **amygdala** goes the other way — dendritic growth, heightened threat
  reactivity.
- **BDNF** expression falls, so the machinery for building new connections is
  itself depleted.

The functional result: **threat processing is over-grown while context
processing is under-grown.** The system becomes very good at detecting danger and
poor at situating it — which is a fair description of what depression and anxiety
feel like from inside.

And it is self-reinforcing. Reduced hippocampal function impairs contextual
discrimination, so more situations read as threatening, which raises cortisol,
which further impairs the hippocampus.

### The behavioural loop

Anhedonia reduces activity → reduced activity removes the reward inputs that
would counter the negative prediction → the prediction is confirmed → activity
falls further. This is why the illness is so good at defending itself: **the
symptom produces the evidence.**

### Why willpower alone often fails here

Three reasons, all structural:

1. **The options are gone before you choose.** Fatigue and anhedonia remove
   candidate actions pre-consciously. An exhausted system does not face a harder
   choice — it faces *fewer options*.
2. **The plasticity to build a new route is depleted.** Low BDNF, retracted
   dendrites, suppressed neurogenesis. You are asked to pave a new road with no
   materials.
3. **The observer is offline.** The prefrontal capacity that would veto the
   spiral is precisely what chronic stress degrades.

That is not a character failure. It is a system that has lost the components
required to change itself — which is exactly what treatment restores.

---

## Part V — CBT as loop interruption

Cognitive behavioural therapy is not "thinking positively." Mechanistically it
is a set of techniques for **breaking the coupling between the parts of a
self-reinforcing loop**, and each one maps onto a specific point in the cycle.

### Where each technique cuts

| Technique | Where it intervenes | What it does mechanically |
|---|---|---|
| Thought records | Belief → interpretation | Forces the ambiguous event to be logged before the narrative fills it in |
| Behavioural activation | Withdrawal → fewer inputs | Restores reward inputs *before* motivation returns, breaking the "wait to feel like it" deadlock |
| Cognitive restructuring | Interpretation → belief | Tests the prediction against outcomes instead of against feeling |
| Exposure / response prevention | Anxiety → avoidance | Demonstrates the veto can be withheld and the system survives |
| Cognitive defusion (ACT) | Thought → identity | Converts a fact-about-me into an object-I-am-holding |
| Mindfulness (MBSR/MBCT) | Rumination → amplification | Stops feeding the loop the high-frequency engagement it needs |

### Defusion — the linguistic mechanism

The words matter because identity-level statements are processed as permanent
facts.

```
"I am anxious."
    → identity level, processed like "I am human"
    → continuous threat-system engagement, high-frequency firing

"I am having the thought that I am anxious."
    → the thought becomes an object, not a fact

"I notice I am having the thought that I am anxious."
    → an observer position now exists that the thought is occurring inside
```

Each tier reduces the emotional charge, and reduced charge means reduced
firing frequency — the low-frequency condition that recruits phosphatases rather
than kinases. **Observing without reacting is not passivity. It is the input
pattern that weakens the circuit.**

### The sky and the weather

Consciousness as open sky; thoughts as weather passing through it. You do not
fight the storm — fighting is engagement, and engagement is the high-frequency
input that strengthens. You occupy the position of the sky, which cannot be
scratched by any weather. The cloud passes on its own.

### Leaves on a stream

Place each arising thought on a leaf and watch it float away. This trains the
specific skill of *not grabbing* — maintaining the unreactive baseline while
content continues to arise.

### Why MBCT works for relapse specifically

Mindfulness-based cognitive therapy roughly halves relapse rates in recurrent
depression, and the reason is targeted: it does not treat the current episode's
content. It trains the **detection** of rumination onset — noticing the loop
starting, early, while the veto is still cheap. It builds the observer, not a
better argument.

---

## Part VI — What medication actually does

This is the part usually left as "it fixes your brain chemistry." That
explanation is both wrong and unhelpful.

### The serotonin story is not the mechanism

The old monoamine hypothesis said depression is a serotonin deficiency and SSRIs
top it up. The evidence has not been kind to it, and **one observation refutes
the simple version outright**:

> SSRIs occupy serotonin transporters within **hours**. Clinical improvement
> takes **two to six weeks**.

If low serotonin were the fault and blocking reuptake were the fix, relief
would arrive the same day. It does not. So whatever the drug is doing that
matters, it is not the immediate transporter blockade — that is only the trigger
for something slower.

### What the delay is actually the timescale of

Structural plasticity. The weeks-long lag matches the timeline of BDNF
expression, dendritic remodelling, and hippocampal neurogenesis — the same
late-phase machinery described in Part III.

```
SSRI → transporter blockade (hours)
     → downstream receptor adaptation (days)
     → CREB activation → BDNF expression (weeks)
     → dendritic growth, restored neurogenesis (weeks)
     → the capacity to form new loops returns
```

**The drug does not install better thoughts. It restores the plasticity that
lets new patterns be built at all.** It reopens the window. It does not decide
what goes through it.

That single reframe explains several things at once:

- **Why the delay exists** — you are waiting on structural growth, not chemistry.
- **Why medication plus therapy beats either alone** — one restores the capacity
  to change, the other supplies what to change *into*. Plasticity without
  direction is just plasticity.
- **Why stopping early relapses** — the window closes before the new route is
  consolidated.
- **Why "the pills didn't make me happy" is the wrong test** — they were never
  the content. They were the conditions.

### Ketamine — acting directly on the structural layer

Ketamine's antidepressant effect appears in **hours, not weeks**, and its
mechanism explains why it skips the queue.

```
NMDA blockade on inhibitory interneurons → disinhibition
→ glutamate burst → AMPA throughput
→ mTORC1 activation → rapid protein synthesis
→ new dendritic spines within ~24 hours
```

It intervenes at the synaptogenesis step directly, rather than waiting for a
transcriptional cascade to get there. It is fast for the same reason it is
usually not durable alone — it opens the window abruptly, and the window closes
again unless something is built during it. Which is why ketamine protocols
increasingly pair the dosing with psychotherapy scheduled *inside* the plastic
window.

### Psychedelics — reopening a critical period

5-HT2A agonism → BDNF–TrkB signalling → a transient state of markedly elevated
plasticity, with animal work describing it as reopening a developmental critical
period.

The clinical framing follows the same logic: the compound is not the treatment.
The **plasticity window plus structured psychological work inside it** is. This
is why the trial protocols involve preparation and integration sessions rather
than dosing alone.

### The other classes, briefly

- **SNRIs** — same plasticity story with noradrenergic recruitment; sometimes
  better on energy and concentration.
- **Bupropion** — dopaminergic/noradrenergic; often targeted at anhedonia
  specifically, the symptom that keeps behavioural activation from starting.
- **Mood stabilisers (lithium, valproate)** — damping in the literal sense.
  Lithium has independent neurotrophic effects and is the strongest
  anti-suicidal agent known.
- **Antipsychotics** — dopaminergic damping; in mood disorders often used to
  brake an amplifying loop rather than to correct a deficiency.
- **Benzodiazepines** — fast, effective, and *not* plasticity restoration. They
  suppress the alarm without rebuilding anything, which is why they work
  immediately, why tolerance develops, and why they are poor long-term
  monotherapy for a structural problem.

### The non-pharmacological interventions work the same way

They are not lesser versions. They act on the same substrate:

- **Exercise** — lactate and cathepsin B → BDNF → mTORC1. The same pathway
  ketamine reaches faster and more forcefully. This is the budget for new wiring.
- **Sleep** — the consolidation step itself. Downscaling plus replay. Without
  it, the day's tagging is wasted and potentiation saturates. Sleep disruption is
  not only a symptom of depression; it removes the mechanism by which any
  intervention would be consolidated.
- **Light, social contact, routine** — inputs to a circadian and reward system
  that has stopped receiving them.

### The unified picture

| Intervention | What it changes | Speed | What it does *not* do |
|---|---|---|---|
| SSRI / SNRI | Restores plasticity via BDNF pathway | Weeks | Choose the new pattern |
| Ketamine | Direct synaptogenesis via mTORC1 | Hours | Persist unaided |
| Psychedelic + therapy | Opens a plasticity window | Hours–days | Work without integration |
| Benzodiazepine | Suppresses the alarm | Minutes | Rebuild anything |
| CBT / behavioural activation | Supplies the new pattern, restores inputs | Weeks | Create plasticity from nothing |
| Exercise | BDNF budget | Weeks | Substitute for treatment in severe illness |
| Sleep | Consolidation of any change | Nightly | Compensate for its own absence |

**Medication and therapy are not competing accounts of the same job.**
Medication changes the substrate's capacity to change. Therapy determines what
gets rehearsed while that capacity is available. The loop framing makes the
complementarity obvious rather than ideological.

---

## Part VII — The same structure, engineered

Having seen the biological version, the engineered ones are recognisable.

### The LLM harness as an artificial observer

A raw language model is a probabilistic prediction engine reading its own output
back as context. Left unharnessed, it enters exactly the runaway pattern
described above: generates → reads itself → predicts a consistent continuation →
generates more of the same. **No outside. No correction. A hallucination loop
that is structurally identical to rumination.**

| Harness component | Human equivalent |
|---|---|
| System prompt | Core beliefs and identity |
| Context assembly / memory | The ego narrative — what gets recalled to make sense of now |
| Output guardrails / evaluators | The mindful observer — the veto on unhelpful impulses |
| Fine-tuning over time | Neuroplasticity — LTP and LTD |

The harness is the engineered creation of an observer layer: something that
monitors the generation loop, detects the spiral, and interrupts it.

### Self-driving cars — the loop with physical stakes

An autonomous vehicle runs the loop in the physical world, where failure is a
collision rather than a bad paragraph. Its architecture maps cleanly:

```
[ Perception ] ──► [ Localisation & tracking ] ──► [ Path planning ] ──► [ Actuation ]
   (senses)          (the ego narrative:            (the observer:        (the body)
                      "I am at 45mph, that           safety envelope
                      is a cyclist")                 vetoes the plan)
```

**Shadow mode** is the observer made literal: the autonomous software receives
all sensor data and computes what it *would* do, with its outputs disconnected
from the controls. It watches without acting. When its prediction diverges from
what the human driver did, that mismatch is flagged and uploaded — and becomes
training data. Reinforced trajectories are fleet-wide LTP; pruned false alarms
are fleet-wide LTD.

**Runaway indecision** is the machine's panic attack. The car edges toward a
roundabout, the safety envelope vetoes on a 1% collision estimate, it brakes
hard, surrounding traffic becomes erratic in response, the sensors read that
escalation as increased danger, the envelope tightens further, and the vehicle
is paralysed — **its own defensive actions generating the chaos that justifies
more defence.** That is the structure of a panic spiral, in silicon, on tarmac.

---

## Part VIII — The one rule

| | Human | LLM | Autonomous vehicle |
|---|---|---|---|
| **The loop creator** | Rumination altering body chemistry | Transformer reading its own text as truth | Perception and planning interacting with traffic |
| **The loop breaker** | Mindfulness, CBT, medication | Guardrail harness | Shadow mode and safety envelopes |
| **The learning mechanism** | LTP / LTD via calcium, kinases, phosphatases | Fine-tuning, weight updates | Simulation driven by mismatch triggers |

Whether it is calcium entering a neuron, a harness stopping a model from
looping, or a vehicle recalculating a turn, all three solve one riddle: **how
does a system navigate an environment that it is itself continuously creating?**

The answer is the same in each case, and it is not "try harder from inside."

> You cannot fix a reflexive loop from inside the loop at the speed the loop
> runs. You need something **slower** — a watcher, a harness, a shadow, a
> record — that observes the fast process and can interrupt it.

And a caveat the clinical material adds, which the engineering version tends to
miss: **sometimes the slower watcher is the thing that is broken.** When chronic
stress has degraded the prefrontal capacity that would do the vetoing, and
depleted the plasticity that would build an alternative, telling the system to
observe itself harder is asking a damaged component to repair itself with tools
it no longer has.

That is what medication is for. Not to supply the content. To restore the
conditions under which content can be changed at all — so that the observer can
be rebuilt, and then have something to work with.

---

*Related: `SEVEN_LOOPS.md` for the same cycle across seven substrates,
`WHAT_IT_ALL_MEANS_FULL.md` for the full synthesis. The harness this document
compares against is implemented in `tools/harness_core/`, and what it has and
has not been shown to do empirically is in `paper_v2` §Discriminating subject.*
