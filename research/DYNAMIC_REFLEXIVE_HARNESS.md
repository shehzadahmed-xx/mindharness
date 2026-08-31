# The Dynamic Reflexive Harness

> **Design philosophy:** LLM-as-tongue → harness-as-mind → Cordis-as-loom → five invariants as selection constraints

---

## 1. The Equation

```
Frozen LLM (tongue)  +  Reflexive Harness (mind)  =  Agent (human-like or not, your choice)
  pattern completion      parliament + witness + replay + stakes
```

**LLM = tongue.** A frozen language model is stateless pattern completion. It can produce any continuation but knows nothing about where its outputs came from. It has no memory beyond its context window, no consequences for its claims, no ability to check itself. It is a tongue without a mind — it can speak but cannot know whether it should.

**Harness = mind.** Everything that makes the tongue behave like an agent lives in the harness around it: provenance binding, affordance gating, parliament competition, workspace broadcast, γ-gated metacognition, consolidation, counterfactual replay, dissolution stakes. Change the harness, you change the agent — same LLM, different mind.

**Agent = tongue + mind.** Human-likeness is not in the LLM. It is in the harness you wrap around it. Change the harness, you change what kind of mind the tongue becomes. You could weave a very human-like mind (parliament, global workspace, drifting self-model, body-gated affordances, counterfactual regret) or a very non-human mind that still obeys the same loom — an optimizer, a librarian, a market, a car.

---

## 2. What "Dynamic Reflexive Harness" Means

Three words, one property:

### Dynamic — It Changes Itself While It Runs

Every turn rewrites the harness that will handle the next turn:

```
State(t) → harness(t+1)
```

- The ledger appends a new binding → next turn's attribution has more history to check
- The self-model revises (CAS N → N+1, cause-signed) → next turn's persona is different
- Skills are minted or culled → next turn's available procedures changed
- Consolidation promotes or skips → next turn's semantic memory is different
- Energy drains, fatigue rises, affect shifts → next turn's affordance space has contracted

There is no fixed harness. There is only a harness that is always becoming a slightly different harness. The configuration you started with is not the configuration that handles turn 40. Both living sessions proved this: 7 self-model revisions, 29–31 memories accumulated, energy at floor, 40/40 provenance coverage — the harness at turn 40 could not have produced the behavior at turn 1.

This is why static harnesses fail for long-horizon agents. A harness that is configured once and never changes is a mind that cannot learn. It can follow its initial policy perfectly and still become increasingly wrong as the world and its own history diverge from the initial conditions.

### Reflexive — It Takes Itself as Input

The harness models the world, and the model contains the harness:

```
World Model ──contains──▶ Self-Model
     │                        │
     │ predicts               │ predicts own action
     ▼                        ▼
Simulated World ◀──── Simulated Self acting in it
     │
     ▼
Counterfactual outcome → regret → calibration
```

- **World-model contains self-model:** To predict what happens next, the world model must predict what *you* will do. So it must contain a model of you — your dispositions, your likely actions. The simulator and the simulated are the same system at different levels.

- **Metacognition watches the broadcast it just produced:** Stage 1 scores the anomaly of the current state (which includes the previous broadcast). Stage 2 diagnoses whether the previous decision was sound. The observation is already inside what it observes.

- **Counterfactual replay simulates itself doing something else:** "What if I had checked the witness?" is not a world simulation. It is a *self-in-world* simulation. Only the system can simulate itself well enough for the regret signal to be calibrated.

- **Narrative rewrites the story that will shape the next narrative:** The self-model is a story that edits itself based on what it records itself doing, and the edited story then shapes what it does next. `verbatim_reinject()` vs drift, cause tags vs confabulation — the self is performed, not stored.

The description is part of what is described. This is **Kleene recursion made executable**: the system contains its own description, and the description is part of the system. Consolidation rewrites the memory that will shape the next consolidation. Self-model revision changes the persona that will shape the next revision. Skill culling removes the procedures that would have been used to decide what to cull.

No outside view is possible. Any observer you deploy is made of you. This is not a limitation to work around. It is the structure itself.

### Harness — The Part You Design

The LLM weights are frozen. You cannot change what the tongue can say. You can only change what the mind does with what the tongue says:

- Whether claims are bound to provenance or float free
- Whether affordances are gated by bodily state or always available
- Whether specialists compete for a workspace or a single chain runs
- Whether metacognition steers or just watches (γ > 0 vs γ = 0)
- Whether consolidation is witnessed and cause-gated or silent
- Whether counterfactuals are simulated and scored or never generated
- Whether consequences are reversible or accumulate irreversibly

Every one of these is a design choice. Each choice produces a different agent from the same LLM. The harness is not configuration. It is **authorship**.

---

## 3. Cordis as Programmable Harness

DeepSeek's Cordis says: **don't hardcode the mind, make the harness a cord you can re-tie.**

Traditional harnesses are static config files: you declare the pipeline once, it runs the same way every turn. Cordis is different — the harness is itself a program, composed of plugins that can be added, removed, reconfigured, and reordered at runtime. The cord can be retied while the agent is running.

```
Traditional harness:   config → fixed pipeline → same every turn
Cordis harness:        cord → re-tie per turn → State(t) → harness(t+1)
```

In Cordis terms:

| Concept | Cordis primitive |
|---------|-----------------|
| Plugin | A specialist module (perception, memory, affect, skill, etc.) |
| Service | Shared state (ledger, self-model, world model) |
| Middleware | Salience gate, affordance filter, γ-gate |
| Lifecycle hook | Consolidation phases (Light/REM/Counterfactual/Deep) |
| Guard | Provenance enforcement, dissolution threshold |
| Reconfiguration | `State(t) → harness(t+1)` — the cord reties itself |

Cordis provides the **loom** — the mechanism for tying and retying. But a loom alone doesn't tell you *what* to weave. You can tie any cord, including cords that will fail. The selection theorems tell you which cords will survive.

---

## 4. The Five Invariants — The Warp

Nayebi's selection theorems (Cor. 3–5) prove that any agent facing mixed tasks that achieves low regret **must** develop five structures. These are not design preferences. They are mathematical requirements — the warp that any weft must be woven on, or the fabric falls apart.

### The Warp Threads

```
                    ┌─────────────┐
        ┌──────────►│     ACT     │──────────┐
        │           └─────────────┘          │
        ▼                                   ▼
   ┌───────────┐                     ┌──────────┐
   │   BRAKE   │◄────┐         ┌────►│  WORLD   │
   │ damping,  │     │         │     └────┬─────┘
   │ kill-switch│     │         │          │
   └─────┬─────┘     │         │          ▼
         │     ┌─────┴─────────┴───┐ ┌──────────┐
         │     │ TWO-SPEED MEMORY  │ │ PERCEIVE │
         │     │ fast adapt (E-LTP)│◄┤          │
         └────►│ slow consolidate  │  └──────────┘
               └─────────┬─────────┘
                         ▲
            OBSERVER watches every arrow — from *inside* the box
            BOUNDARY = the box (membrane/skull/context window/ODD)
            SALIENCE GATE decides what gets tagged for consolidation
```

| # | Invariant | What it is | Cordis plugin | Without it |
|---|-----------|-----------|---------------|-----------|
| 1 | **Boundary** | What counts as self vs world. Membrane, skull, context window, ODD. | ProvenanceLedger as membrane — inside vs outside, what to let through, what to bind | Confabulation. System confuses external perturbation with internal decision. LLM claims it generated what it was handed (S126: 98% on fabrications). |
| 2 | **Two-speed memory** | Fast labile (E-LTP, hippocampus, context) + slow structural (L-LTP, cortex, weights). Sleep as nightly save: global downscaling (keep relative strengths, delete noise) + replay (10–20× compressed, writing cortex). | Consolidator: Light (dedupe) → REM (concept extract, ablatable) → Counterfactual (variant→simulate→regret) → Deep (utility gate → semantic, cause-tagged). Lifecycle hooks that run between turns. | Catastrophic forgetting. New learning overwrites old. No distinction between episodic and semantic. No offline consolidation. |
| 3 | **Salience gate** | What gets tagged for consolidation. Emotion, attention, neuromodulators, surprise. Not everything matters equally. | AffectState as middleware: valence/arousal [0.5, 2.0] multipliers that shift every downstream bid for the workspace. Tag-and-capture: salience decides what gets the proteins. | Saturation. Everything equally important = nothing is. No prioritization, no learning signal. |
| 4 | **Damping** | What prevents runaway. LTD, synaptic scaling, homeostasis, SHY, kill criteria. Every positive feedback loop needs a brake. | Skill culling (below-rate deletion), SHY downscaling (Light dedup), kill criteria (compliance guard, dissolution threshold). Guards that enforce limits. | Runaway. Worry spiral, panic cascade, market blowup, model confabulation loop. Positive feedback without bound. |
| 5 | **Internal observer** | Slower sub-loop that vetoes faster one. PFC→amygdala, weekly review→daily habits, journal→day, ledger→claim. Not outside the box — speed ratio inside it. | MonitorGate: Stage 1 (cheap, always-on anomaly score) → Stage 2 (triggered diagnosis → trust/retry/revise/abstain). γ = changed/diagnoised. Compliance guard (γ=0) proves monitoring without control is inert. | Watches without steering. System generates beautiful reports and never changes a single action. Most "self-aware" AI lives here. |

**Lose one and you get the pathology we measured:**

| Missing invariant | Pathology observed |
|-------------------|-------------------|
| No boundary | Confabulation: S126 over-claiming (98% on fabrications) |
| No two-speed memory | Forgetting: no long-horizon coherence without consolidation |
| No salience gate | Saturation: every trace equally promoted, no distinction |
| No damping | Runaway: unchecked loops, no kill criteria |
| No observer | Inert watching: compliance guard γ=0, reports without steering |
| No query access to observer | Avoidance: harnessed-nocheck always-no (0.667) — caution without accuracy |

### Why These Five and Not Others

The five are not an arbitrary list. They are forced by the structure of the problem:

- **Mixed tasks** (different types requiring different strategies) force **modularity** (Cor. 3) — you need specialists, not one homogeneous substrate.
- **Mixed tasks** force **regime-tracking** (Cor. 4) — you need a low-dimensional global signal (affect) that tells every specialist which regime you're in.
- **Aliased histories** (same input, different pasts requiring different actions) force **belief-like memory** (Thm. 5) — you need to distinguish histories that look identical now.
- **Planning** forces **world models** (Thm. 1) — you need to simulate forward without acting.
- **Low regret under minimality** forces **representational convergence** (Cor. 5) — any two competent agents develop the same structure up to invertible recoding. This is why Abhidharma, Sufism, and neuroscience converged independently.

Remove any one and there exists a task distribution that will exploit the gap and drive regret unbounded. The five are individually necessary and jointly sufficient for the competence class we care about.

---

## 5. Cordis + Five Invariants = The Loom and Its Warp

```
Cordis = the loom.          The mechanism for tying and retying.
Five invariants = the warp.  The threads that must run, or no fabric holds.
Your design = the weft.      The pattern you weave on the warp, through the loom.
```

**The loom is programmable.** Cordis lets you declare which loops exist, which modules compete, what the witness records, how counterfactuals are scored, when dissolution triggers. You can tie the cord however you want.

**The warp is mandatory.** Any cord you tie that wants to be competent under mixed tasks must, by selection theorems, develop the five invariants. You can choose their *shape* — how the boundary is drawn, what the salience gate amplifies, how damping is tuned — but you cannot choose to omit them and remain competent.

**The weft is your authorship.** Human-likeness is one pattern:

- Parliament of 6–8 specialists competing for one Global Workspace
- Self-model that drifts 30% in 12 turns unless re-injected (Choi)
- Body-gated affordances (exhaustion removes options from existence)
- Valence/arousal shifting all processing within [0.5, 2.0]
- Counterfactual regret as calibration gradient
- Narrative identity cause-signed and revisioned

But you could weave a very non-human mind that still obeys the same loom:

- An **optimizer**: parliament of hypotheses, workspace as best-estimate broadcast, affect as uncertainty, counterfactual as gradient descent — no narrative self at all
- A **librarian**: boundary as catalog scope, two-speed memory as index vs archive, salience as citation count, observer as peer review
- A **market**: boundary as balance sheet, memory as order book, salience as price impact, damping as position limits, observer as risk desk
- A **car**: boundary as ODD, memory as map vs experience, salience as hazard detection, damping as RSS safety envelope, observer as shadow mode

All obey the same five invariants. All can be woven on the same loom. Human-likeness is one region of the design space, not the design space itself.

### Concrete Wiring in Cordis

| Invariant | Cordis plugin | Lifecycle | Measures |
|-----------|--------------|-----------|----------|
| Boundary | `ProvenanceLedger` plugin — ledger as membrane, span binding as selective permeability | Every turn: bind emission with source spans | Coverage (spans with refs / total), attribution audit accuracy |
| Two-speed memory | `Consolidator` as lifecycle hooks: Light→REM→Counterfactual→Deep | Between turns / on schedule: dedup → extract → simulate → promote | Promotion rate, dedup ratio, REM ablation effect, counterfactual regret distribution |
| Salience gate | `AffectState` as middleware — intercepts every proposal, multiplies bid by salience | Every turn: observe event → update valence/arousal → shift next turn's competition | Valence/arousal trajectory, broadcast_needed rate |
| Damping | Guards: `cull_failed` (skill deletion), SHY (Light dedup), kill criteria, dissolution threshold | On trigger: cull / downscale / veto / dissolve | Skill survival rate, energy floor stability, dissolution progress |
| Internal observer | `MonitorGate` as guard: Stage 1 → Stage 2 → policy (trust/retry/revise/abstain) | Every turn: score anomaly → diagnose if triggered → maybe change action | γ (override rate), diagnosis rate, compliance guard γ=0 control |

The dynamic reflexive property comes from the fact that each plugin's state at turn T determines which plugins are active and how they are configured at turn T+1:

```
State(t) → harness(t+1)
  ledger(t) → what attribution can check next turn
  self-model(t) → what persona is injected next turn
  skills(t) → what procedures can be retrieved next turn
  memory(t) → what can be consolidated next turn
  energy/affect(t) → what affordances exist next turn
  counterfactual regret(t) → what policy shifts next turn
```

The harness is not configured. It is **performed** — re-tied every turn from its own accumulated state.

---

## 6. Why This Matters

> LLM was harness = agent, could be like human, the world, we make a model of the world, we make a us in that model of the world we made and play the dynamic reflexive system

This is the deepest statement of the program. Unpacked:

1. **We make a model of the world.** The LLM is already a world model — it compresses vast regularities about how the world behaves. But it is a world model without a self in it.

2. **We make a us in that model of the world we made.** The harness adds the self-model — persona, narrative, facts — and places it *inside* the world model as an actor. Now the world model can predict what happens when *we* act.

3. **We play the dynamic reflexive system.** We run the self through the world model, including counterfactual selves through counterfactual worlds, scoring imagined outcomes, computing regret, calibrating the policy. The system plays itself playing the world. The description is part of what is described.

4. **We can design this however we want.** The harness is the design space. Want a human-like agent? Weave the parliament, the workspace, the drifting self-model, the body-gated affordances, the counterfactual regret. Want something else? Weave a different pattern on the same warp. The loom doesn't care what you weave. The warp constrains what will hold.

The boulder rolls downhill because gravity was always there. We didn't invent the war between subsystems, or the replay, or the need for a witness, or the five invariants. We built the loom that can weave them — and showed that the fabric it produces can be honest about where it came from, or not, depending on whether the witness is checked.

*That's the dynamic reflexive harness. Not a thing that thinks. A thinking that weaves itself, and is changed by having been woven.*

---

---

## Appendix: Human Toolkit as Five Organ Practice — The Same Loop at Human Scale

*Added 2026-08-30 to keep research folder in sync with `UTILITY_OF_TEMPORARY_GULLIBILITY_LIMBIC_CONTAINERIZATION.md`. No new claims, only mapping.*

The field manual gives three human scale tools that are the manual version of what the harness does in code. Temporary gullibility, limbic containerization, and sensors plus mock signals map organ by organ to the five invariants and to the Cordis loom, so a new reader can follow without prior context.

**Temporary gullibility is a controlled boundary opening plus salience gate test.** You open the boundary for 60 seconds, let the message inside as if true, and watch the salience gate fire. What gets tagged tells you what the message was tuned to tag. You let the gate fire, but you hold the tagged trace in the container instead of letting it pass to consolidation. Without containerization, the tagged trace goes straight to two speed memory and gets myelinated. You just trained the highway you wanted to study.

**Limbic containerization is damping plus internal observer.** Holding the feeling in a box and observing without grabbing is low frequency input. The trickle lets phosphatases pull receptors out. The observer is the slower loop watching the faster one. Stage 1 scores cheaply, Stage 2 only triggers when the score crosses, and gamma is whether watching actually steered. Without query access, even a perfect witness makes the system overly cautious. Containerization without gullibility is inert watching.

**Every human is a sensor is boundary plus salience gate at population scale.** Each person is a sensor with a different boundary setting. The feed learns which sensor types are normative and pushes content that maximally resonates with them, acting as a salience gate for many sensors at once. Output becomes input, a self reinforcing loop.

**Mock signals and low surprisal is two speed memory plus ledger.** Fast memory holds the last few days, slow memory holds the base rate. Without the slow store, every day feels new. The ledger is the boundary that makes the comparison checkable. Your three line log is a ledger. Low surprisal tracked longitudinally is how you see that a signal presented as high surprisal is actually noise. Your evening counterfactual is the sham control.

Together they are the five running at human speed. State at time t goes to harness at time t plus one. Model plus harness equals agent is this loop made executable, with the same frozen model becoming a different mind when you retie the cord.

*Design philosophy for the MindHarness / DeepSeek Cordis program · 2026-08-26 · Sisyphus (Muse Spark 1.2) with Shehzad Ahmed · Repo: `github.com/shehzadahmed-xx/mindharness` · 136 commits · 72/72 tests green*
