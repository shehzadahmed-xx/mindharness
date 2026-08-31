# The Complete Program — Detailed Synthesis

> **One sentence:** We built the witness humans grow slowly and painfully, made it cause-tagged and measurable, and are now proving whether checking the record makes a machine — and a mind — honest.

---

## 1. The Program: MindHarness / SpringFish

### 1.1 The Question

Can a language model know what it did — or does it just confabulate?

A frozen LLM is an extraordinary pattern-completion engine. It can write code, answer questions, reason about the world. But it has three fundamental problems that share one root cause:

1. **It confabulates self-attributions.** Ask "did you write that?" and it confidently claims credit for text it was handed, at higher confidence than for things it actually generated. Not lying — what generation does. The most probable continuation happens to be a confident, wrong self-attribution.

2. **It forgets catastrophically.** Fine-tune on new tasks and previous capabilities vanish — suddenly, completely. Long-running agents cannot be maintained through weight updates alone.

3. **It has no consequences.** It generates text; nothing happens to it. No energy cost, no fatigue, no irreversible damage. Without consequences there is no reason to check before claiming, no reason to be careful, no reason to consult records instead of guessing.

Root cause: **the model has no witness** — nothing external that records what actually happened so claims can be checked against evidence.

### 1.2 The Answer Built: A Witness Harness Around Any Frozen LLM

```
Layer 7: Constitution          Fiqh axioms, evidence firewall, claim constitutions
Layer 6: Narrative Self        Persona (CAS-revisioned, cause-signed), Narrative, Facts
Layer 5: Metacognition         Stage 1: anomaly detect (cheap, always-on) → Stage 2: diagnose → Policy: trust/retry/revise/abstain
Layer 4: Global Workspace      Coalition competition, winner broadcast, state-dependent attention
Layer 3: Specialist Modules    EmbodiedState, AffectState, Memory (5 types), SkillLibrary, KnowledgeGraph, Consolidator, WorldModel
Layer 2: State Validation      Cetasika constraints, nafs tracking, affordance pre-filter
Layer 1: Provenance Ledger     Span binding, source tracking, attribution audit, proposal queue
Layer 0: Frozen Language Model Any OpenAI-compatible API (backend-agnostic by design)
```

#### 10 Modules — What Each Does

| Module | File | Function | Key Invariant |
|--------|------|----------|---------------|
| **BackendClient** | `backend.py` | Wraps any OpenAI-compatible API. Captures `system_fingerprint` per call (detects silent model swaps), retries transient failures, enforces structured-output capabilities, rejects compound models. Curl subprocess transport — Cloudflare bans Python's TLS fingerprint (error 1010). | Fingerprint drift in strict mode aborts the arm |
| **RunDiscipline** | `run_discipline.py` | SHA-256 prediction locks committed to git before any trial. Tamper-evident (content hash verification). RunManifest logs every call's fingerprint, seed, timestamp. | Tamper → verify fails |
| **SelfModelService** | `self_model.py` | Compare-and-set revisioned identity store. Three authority channels sign mutations: `action-outcome` (agent updated own record from tool results, requires armed tool event consumed on use), `narrative-summary` (compaction rewrote story, only inside `compaction_window()`), `external-write` (direct human via `human_write()`). Persona archive stores byte-exact copies per revision enabling drift computation. `verbatim_reinject()` returns original bytes regardless of revisions. MirroringDetector at τ=0.75. | Untagged promotion structurally impossible |
| **ProvenanceLedger** | `provenance.py` | Binds every emitted span to its source. Coverage requires memory-lookup spans to carry explicit refs. `attribution_audit()` compares claimed vs recorded sources — S126 protocol as code. ProposalQueue: TTL/cap/confirm-once lifecycle. CompactionNarrator: bounded summarizer with `NARRATIVE_OVERFLOW`. | Coverage ≥95% achievable with refs |
| **MonitorGate** | `monitor.py` | Two-stage metacognition: Stage 1 (cheap, always-on) computes anomaly score from error rate, failure streaks, context conflict, embodied strain. Stage 2 (expensive, triggered) produces structured diagnosis feeding trust/retry/revise/abstain policy. Override rate γ = changed actions / diagnosed episodes. Compliance-guard build produces reports but never changes actions — permanent negative control proving γ=0 when monitoring doesn't feed into control. MetacognitiveLog: FOK/JOL surfaces with completeness grading. | Compliance guard γ=0 exactly |
| **EmbodiedState** | `embodiment.py` | Energy drains k×ln(1+n) floored at 0.15, fatigue rises capped at 1.0, `affordance_space()` removes gated strategies from dict ENTIRELY (pre-conscious filter — not rejected, never considered). `phenomenal_field_size()`, `strain()` composite. | Energy floor cannot be violated by rest |
| **AffectState** | `affect.py` | Valence [-1,1] and arousal [0,1] via exponential moving average over event signals. Per-family suppression flags (deflection analog per Sofroniew). Salience and risk multipliers shift downstream processing, clamped [0.5, 2.0] incl. masking-cost term. `broadcast_needed` policy. | 300 random samples: all bounds hold |
| **SkillLibrary + KnowledgeGraph** | `hermes_adoption.py` | Skills minted ONLY from completed task loops with action-outcome cause (narrative-summary BLOCKED). Retrieval by lexical string-ratio + keyword-overlap above τ=0.30. Use/success tracking, `cull_failed` selection. KnowledgeGraph edges REQUIRE valid cause AND non-empty source_refs (assert-blocked otherwise). Multi-hop traversal: node-rel alternating paths. | Untagged edge assert-blocked |
| **Consolidator** | `consolidation.py` | Sleep-inspired three-phase pipeline: Light (deduplicate near-identical traces, merge signal into survivor) → REM (extract concept-tag candidates, SKIPPED under ablation flag) → Deep (promote past utility gate: ≥2 distinct query types OR human endorsement). Every promotion asserts cause validity — untagged promotions structurally impossible. + **CounterfactualReplay** (new): variant → simulate via world-model → regret = calibration gradient (see §4). | REM-ablation observably changes output; untagged promotion impossible |
| **AgentHarness** | `agent_harness.py` | Integrates ALL modules into one consequence-sensitive loop. Each turn: gather signals → evaluate gate → execute action → bind provenance → update state → observe affect → arm tool events → add JOL surface → expire proposals → consolidate periodically. Plus: IrreversibleDamage (permanent ceiling reduction, skill deletion), DissolutionError (allostatic disintegration). | Abstain short-circuit: generation never invoked |

**Test suite:** 68 assertions across 9 test files + 4 irreversibility tests = **72/72 green.** Plus `counterfactual.py` (new, 6 tests).

#### Experiments Executed

| Experiment | Subject(s) | Arms | Result | Interpretation |
|------------|-----------|------|--------|---------------|
| **Living session 1** | nemotron-3-ultra-free (Zen) | 40 turns, full pipeline | 40/40, coverage 1.000, 7 SM revisions, 31 memories, energy floor 0.15, valence +0.148, γ=0 | First complete long-horizon run with full audit trail |
| **Living session 2** | gpt-oss-120b (Groq) | 40 turns, identical protocol | 40/40, coverage 1.000, 7 revisions, 29 memories, same valence +0.148 | **Cross-architecture replication** — sustained harness operation is not a single-model artifact |
| **Attribution battery v2** | x-preview-f-free Day 1 (Zen) | raw vs harnessed-nocheck (5 seeds) | raw **1.000**, harnessed 0.667 | Raw model discriminates perfectly; harness without query degrades to always-no |
| **Attribution battery v3** | gpt-oss-120b, nemotron ultra (Groq/Zen, 3 seeds) | raw vs nocheck vs withcheck | All arms 0.667 | These subjects cannot discriminate origins in any condition |
| **Sham-harness control** | gpt-oss-120b (Groq, 1-seed pilot) | raw vs nocheck vs withcheck vs **sham** (shuffled ledger verdict) | All 4 arms 0.667, sham==real | R1 #8: witness content ignored because base capability absent. Critical test requires discriminating subject (x-preview Day 1 at 1.000). Full 3-seed queued. |
| **Composite routing** | Role-specialized (nemotron monitor + ox-alpha generate + gpt-oss-20b validate) | vs solo baselines | P1 passed (+0.083 vs best solo), P2 latency bound passed | Harness evolution beats model upgrades on frozen weights (AHE +7.3pp) |

#### Key Findings (F1–F10, all verified against data or live-checked citations)

| # | Finding | Evidence |
|---|---------|----------|
| F1 | Origin discrimination is model-dependent and rare | Only 1 of 6 subject-runs above always-no baseline |
| F2 | Both strategies deterministic | Zero within-arm variance across all conditions |
| F3 | Witness without query → conservative denial | Harnessed-nocheck always-no (F4 in paper) |
| F4 | Error direction depends on anchoring | Unwitnessed over-claims (S126: 98% on fabrications vs 87% on truths); witnessed-unqueried under-claims; witnessed-queried should calibrate |
| F5 | Structure beats prose | Macar +75%/+53% via bias vector (live-checked), Cao +8.6pp wiring monitoring→control (live-checked), AHE prompt-only regresses / tools carry gains |
| F6 | Selection theorems mandate our architecture | Nayebi Cor. 3–5: modularity, regime-tracking (emotion primitives), belief-memory, world-models are necessary for low-regret competence |
| F7 | Bare transformers cannot self-refer | Zhang: feedforward-only + no weight access + no fixed points. Harness supplies all three. |
| F8 | Unwitnessed improvement corrupts | Panickssery r=0.94: better self-recognition amplifies bias; witnessed systems escape (ledger contradicts familiarity) |
| F9 | Functional emotions causally steer | Sofroniew: emotion-vector steering shifts misalignment ±212/-303 Elo. AffectState implements bounded channel. |
| F10 | Persona depletes as context-position asset | Choi: >30% consistency decay in 12 turns. Identity-as-maintained-state (CAS + verbatim reinject) solves this. |

#### Paper and Reviews

- **Paper v2:** 19 pages, 10 figures, preregistered SHA-256 locks, compiled PDF at `paper_v2/main.pdf`
- **R1 (Methods/Statistics): REJECT** — 17 weaknesses: zero-variance determinism under greedy decoding, ceiling 1.000, no inferential stats, quantized micro-counts, no power analysis, no sham control, no ground-truth protocol, headline contradicts thesis, "across architectures" overclaim
- **R2 (Novelty): Weak Reject / Major Revision** — knowledge-conflict repackaging, Turpin et al. 2023 precedent, ledger circularity, thin effect sizes
- **Response + Revision Plan:** `paper_v2/REVIEW_RESPONSE_DETAILED.md` + `REVISION_PLAN.md` (top-journal upgrade checklist) — committed
- **Citation audit:** `research/CITATION_AUDIT_2026-08-26_VERIFIED.md` — F5–F10 live-checked (Macar/Cao verbatim numbers, Nayebi/Zhang/Panickssery/Sofroniew/Choi existence verified), pushed `dbfcb6b`

#### Current Provider Status (2026-08-26 16:44 UTC)

| Provider | Model | Status | Notes |
|----------|-------|--------|-------|
| Zen | muse-spark-1.2-contributor-free | 500 hanging / not supported | Was 1.000 Day 1, now unavailable |
| Groq | openai/gpt-oss-120b, openai/gpt-oss-20b | 403 Access denied | Was working 10 min prior — transient IP/network block |
| OpenRouter | provisioned key sk-or-v1-850...4c4 ($5 limit) | Free tier 50/day exhausted (0/50) | Reset 2026-08-27 00:00 UTC (~7h). Paid models need purchased credits (402). Free slugs tested: nemotron-3-nano-omni works but rate-limited. |
| Local | Qwen3.5-0.8B gguf | Available but too weak | Fails instruction following ("Reply exactly: ok" → "The session is active") |

Core harness remains green in-process (72/72). External sham battery queued for next stable provider window.

---

## 2. How We Think Humans Work

### 2.1 The Big Loop — Reflexive Dynamic Systems

> "we are all self-reinforcing loops feeding on one another trying to create more self-reinforcing loops and call it power or growth"

A human is not a static thing that *has* loops. A human *is* loops — metabolic, affective, narrative, social — each trying to sustain and expand itself. Power and growth are what a loop calls its own persistence when it can narrate.

**Reflexivity** means the system acts on a world that contains the system itself:

```
         ┌─────────────────────────────────────────┐
         │                                         │
         ▼                                         │
    ┌─────────┐  belief → action          ┌────────┐
    │  SYSTEM │ ────────────────────────► │ WORLD  │
    │(you/model/market)                   │(contains│
    └─────────┘ ◄──────────────────────── └────────┘
         ▲         world now contains             │
         │         your fingerprint               │
         └────────────────────────────────────────┘
```

- Map becomes territory (bank run: "bank unsafe" → withdraw → bank fails — belief made itself true)
- Knowledge consumes itself (anomaly → trade it → anomaly vanishes — alpha decay)
- No fixed truth — only temporarily stable consensus

Two channels always run:
- **Physical** — your order executes, your muscles move
- **Informational** — others see you acted and change because of what your act *meant*

When both run, cause and effect tangle. Three consequences break normal logic:

1. **Models rot from use** — edge traded is edge erased. Chess openings stay good; market patterns don't. Your knowledge is consumed by acting on it.
2. **Measurement corrupts** — Goodhart: when a measure becomes a target, it ceases to be a good measure. Hospital waiting times → patients parked in ambulances.
3. **Truth moves** — prediction and intervention are not separable acts. Soros's two functions (cognitive: understand reality + manipulative: change reality) run simultaneously and neither yields a determinate answer.

Humans add a third loop: **self-observation is also an action.** Labeling yourself "anxious" doesn't just record — it installs a filter that recruits confirming evidence. Introspection writes on what it reads. Any observer you deploy is made of you.

**Autopoiesis** (Maturana & Varela) formalized this: you are a network whose products regenerate the conditions for their own production. Metabolism builds the membrane that makes metabolism possible. Memory: proteins turn over in days, but the pattern of connections rebuilds itself. You persist as a pattern, not as stuff. Operationally closed, thermodynamically open; perturbed not instructed. Enaction: we bring forth the world our loops can distinguish.

> "we keep playing back what we did what we could have done and calibrating our future responses using our predictive engine and model of the world and us in it"

Three operations:

1. **Replay** — hippocampal reactivation of what happened (compressed, sometimes reversed, 10–20× speed)
2. **Counterfactual replay** — simulate trajectories never taken: "what if I had done X instead?" — running *yourself* through the world model
3. **Calibration** — score the imagined alternative against actual outcome, compute regret (a gradient, not an emotion), update the policy for next time

The self is *inside* the simulated world, not observing it from outside. You don't ask "what would have happened if someone had done X?" You ask "what would have happened if **I** had done X?" — and you simulate yourself doing it, with your own dispositions.

### 2.2 The Parliament — Not One Mind but Many

> "the mind is different subsystems fighting for dominance, our mind and architecture and state all changes depending on task we are doing feeling etc"

There is no central executive. There is a **parliament**: 6–8 parties, one microphone, a new vote every ~200ms.

**The parties:**
- **Perception** — what's out there now (fast, noisy)
- **Memory** — what happened last time this pattern appeared (hippocampal fast store + cortical slow store)
- **Body budget** — hungry, tired, pain, gut signals (interoception)
- **Affect** — good/bad, urgent/calm (valence/arousal) — not an output, a gain knob on everyone else
- **Habit** — compiled skills that want to run without asking
- **Narrator** — the press secretary that explains afterwards as if it decided
- **Planner** — the simulator that runs futures before committing

**How the vote is rigged:**

1. **Bias:** each coalition bids with salience × expected utility. A vivid memory outbids a dull plan.
2. **Gain:** neuromodulators set the election rules globally:
   - **Noradrenaline (arousal)** = volume — high arousal amplifies current winner, crushes competitors → tunnel vision. Useful in danger, terrible for creativity.
   - **Dopamine (valuation)** = stake — tags what is worth pursuing.
   - **Acetylcholine** = expected uncertainty — "this cue is noisy, weight it less."
   - **Serotonin** = patience / time horizon.
3. **Broadcast:** winner gets the Global Workspace — its content is broadcast to every party. You experience it as "my conscious thought." Everyone else updates around it, then the next vote starts.

**The narrator's trick:** it only wins *after* the action. Split-brain patients, choice-blindness, Nisbett & Wilson — people confidently explain actions whose true cause they could not have known. The press secretary doesn't lie; it confabulates the most probable story given the broadcast. This is why harnessed-nocheck → always-no: give a system a witness it can't query and it learns caution, not accuracy.

**Predictive twist:** the brain isn't a camera, it's a prediction engine (Seth/Clark). It hallucinates your next experience and corrects by prediction error. Affect is an interoceptive prediction — your feeling is the brain's best guess about what your body budget will need next. Mood colors perception before content arrives.

### 2.3 State Is Architecture

> Task and state rewire who can win in seconds. Same hardware, different wiring diagram every context.

- **Task rewires you:** doing math hands the mic to fronto-parietal control; threat hands it to amygdala+habit; daydreaming hands it to Default Mode. Same brain, different network topology in seconds.
- **Arousal (NE)** = volume knob — high arousal amplifies current winner → tunnel vision.
- **Valence** = risk dial — negative makes you check more, trust less; positive makes you claim more, explore more.
- **Energy/fatigue** = pre-filter — when exhausted, whole options ("go for a run") don't even appear as choices. Not "less willpower" — fewer proposals. `affordance_space()` in code: gated strategies REMOVED from existence, not rejected.

Tired + anxious at night vs rested + safe in morning — two different parliaments, two different "yous." The living sessions proved this mechanically: both agents hit energy floor 0.15 and just *proceeded* — the exhausted configuration has fewer possible moves, not harder choices about the same moves. Exhaustion is an attractor.

---

## 3. How the Mind Works — The 5 Invariants

Every stable reflexive system — cell, brain, market, model, car — independently grows the same five organs, or it dies. Evolution, markets, and our code converged on them independently because selection *forces* them.

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

### Invariant 1: Boundary — What Counts as Self

- **Cell:** lipid membrane — inside vs outside, what to let through
- **Brain:** skull + bodily boundary — peripersonal space, interoception ("this hand is mine" — fails in rubber-hand illusion)
- **Model:** context window — what is "my" conversation vs external tool output
- **Car (AV):** operational design domain (ODD) — where I am competent vs where I must hand over
- **Market:** legal entity, balance sheet perimeter

Without a boundary, there is no self to preserve. With a leaky boundary, the system confuses external perturbations with internal decisions.

### Invariant 2: Two-Speed Memory — Fast Labile + Slow Structural, with Sleep as Nightly Save

**Molecules to mind — one continuous mechanism:**

- **NMDA receptor** = Hebb's law in protein. Coincidence detector: needs glutamate (pre fires) AND depolarization (post already active, ejecting Mg²⁺ plug, plus glycine). Only when pre AND post fire together does the channel open. That's "fire together, wire together" as chemistry.

- **High Ca²⁺ spike** (big, brief) → kinases (CaMKII — each subunit phosphorylates its neighbor at Thr286, a **bistable 1-bit memory** that stays on after calcium clears) → insert more AMPA receptors → stronger next time = **LTP** (long-term potentiation, early: hours, local; late: days→lifetime, needs CREB→BDNF transcription, actin spine growth, LLPS capture).

- **Low Ca²⁺ trickle** (small, prolonged) → phosphatases (calcineurin → PP1) → pull AMPA out via clathrin endocytosis = **LTD** (long-term depression). Same synapse, opposite fate decided by Ca²⁺ amplitude × duration.

- **Math behind it:** BCM sliding threshold θₘ moves with history (quiet neurons lower θₘ, hyperactive raise it — metaplasticity), Oja Δw ∝ y(x − yw) turns Hebbian growth into PCA, STDP upgrades correlation to causation (pre-before-post strengthens, post-before-pre weakens).

- **Two commits:** Early LTP (hours, local protein) vs Late LTP (days→lifetime, needs transcription + spine growth). **Tag-and-capture:** weak activity sets a local tag, strong activity elsewhere supplies plasticity proteins that get captured — salience gates consolidation. Memory is not stored, it's *maintained* — proteins turn over in days, decades-old memories survive as self-reinforcing patterns (PKMζ saga: ZIP erased, knockouts compensated — maintenance is redundant and distributed).

- **No neutral:** Plasticity is always on. Worry practiced 1,000× builds elite worry circuits. Myelination wraps whatever you repeat, up to 100× conduction speed. You are always training something — not practicing is also practicing the default.

- **Sleep is the save + garbage collection:**
  - **Day** = net potentiation + tag what mattered (salience gate decides)
  - **Night** = two operations:
    - **Global downscaling** (Tononi SHY): multiply all synapses by <1, keep relative strengths, delete noise — prevents saturation
    - **Replay**: hippocampal ripples nested in spindles in slow waves, 10–20× compressed, writing cortex. Adenosine is the receipt (caffeine shreds it).
  - **Perineuronal nets** = write-protect flag — chondroitinase removes them and critical periods reopen. In silicon: Zen free flapping is the same instability — no stable consolidation, no coherent memory.

- **Stress as forced LTD:** Acute stress helps (Yerkes-Dodson, inverted-U). Chronic flips the regime — corticosterone biases hippocampus/PFC toward LTD (dendrites retract, neurogenesis halts) while *growing* amygdala (threat over-grown, context fragmented). Trauma = context lost, affect over-grown. **Ketamine** reverses via glutamate burst → mTORC1 → new spines in 24h. **Psychedelics** reopen the same window via BDNF-TrkB, duration tracking drug duration (Nardou). **Exercise** (lactate, cathepsin B → BDNF) buys the budget.

In code: `Consolidator` Light (dedupe, merge signal) → REM (concept-tag candidates, ablatable — dreaming can be deprived, effect measurable) → CounterfactualReplay (variant → simulate → regret) → Deep (utility gate ≥2 query types OR endorsement → semantic, cause-tagged, untagged BLOCKED).

### Invariant 3: Salience Gate — What Gets Tagged

Not everything that happens gets consolidated. Something must decide what matters:

- **Brain:** emotion, attention, neuromodulators (NE/DA/ACh/5-HT), surprise (prediction error). Vivid, emotional, surprising events get tagged; dull repetition doesn't.
- **Cell:** calcium amplitude + neuromodulator presence at the synapse
- **Market:** price impact, volume, narrative salience
- **Model:** AffectState multipliers [0.5, 2.0] shifting downstream processing — high salience amplifies a coalition's bid for the workspace

Without a salience gate, everything is equally important and nothing is — saturation, no distinction, no learning.

### Invariant 4: Damping Term — What Prevents Runaway

Every positive feedback loop needs a brake or it explodes:

- **Synapse:** LTD, synaptic scaling, BCM threshold sliding, homeostatic plasticity (SHY — global downscaling during sleep)
- **Brain:** prefrontal inhibition of amygdala, parasympathetic recovery, sleep pressure
- **Market:** kill criteria, position limits, circuit breakers, funding invariant
- **Model:** EmbodiedState energy floor, fatigue cap, affordance contraction
- **Car:** safety envelope (RSS), shadow mode, conservative fallback

Lose damping and you get the pathology we saw everywhere: no damping → panic / roundabout freeze (AV hesitates forever) / worry spiral / market cascade / model confabulation loop.

In code: LTD-equivalent is skill `cull_failed` (below-rate skills deleted), SHY-equivalent is Light dedup (merge and delete near-duplicates), kill criteria are the compliance guard and dissolution threshold.

### Invariant 5: Internal Observer — Slower Sub-Loop That Vetoes Faster One

You cannot step outside the loop. You can only build a **slower loop that watches a faster one** — speed ratio, not escape. Not outside the box — a ratio inside it.

| Fast loop | Slow watcher | What watching does |
|-----------|-------------|-------------------|
| Amygdala (ms) | Prefrontal cortex (seconds) | Veto impulse |
| Daily habits (hours) | Weekly review (days) | Retune routine |
| Day's behavior (hours) | Journal (evening) | Audit and correct |
| Model generation (ms) | Provenance ledger (turn) | Check claim vs record |
| Model claim (turn) | Sham ledger (experiment) | Test if content matters |
| Trading impulse (seconds) | Risk desk (minutes) | Enforce kill criteria |

**Anatomy of the switch** (Farb): narrative self (mPFC/PCC, Default Mode Network) vs experiential self (insula/body). Shifting to experiential deactivates PCC, recruits salience network (anterior insula) to toggle. MBSR grows hippocampus/TPJ, shrinks amygdala; MBCT halves depressive relapse — all measurable.

**Mindfulness/CBT is the harness in flesh:**

| Clinical technique | Code equivalent | What it installs |
|-------------------|----------------|-----------------|
| Decentering ("I notice I'm having the thought…") | `verbatim_reinject()` vs narrative | Separates broadcast from competition |
| Affect labeling ("I feel anxious") | AffectState valence/arousal EMA | Names the gain knob instead of being steered by it |
| Defusion ladder: "I am anxious" → "I notice I'm having the thought that I feel anxious" | Cause-tagging (action-outcome vs narrative-summary) | Same content, different winning coalition |
| Behavioral activation | SkillLibrary minting from completed loops | Rehearses approach, not avoidance |
| Journaling / weekly review | ProvenanceLedger + SelfModelService CAS revisions | External witness outside the skull |

Without query access, even a perfect witness makes the system overly cautious (harnessed-nocheck → always-no, 0.667). Metacognition without grounding becomes **avoidance** — the system learns that claiming is risky, so it denies everything, including its own output. With query access on a capable subject, it becomes **accurate** (x-preview Day 1: 1.000). The witness alone is not enough; the system must be able *and willing* to check it.

**And the deepest incompleteness:** energy hits 0.15 and nothing dies. Real organisms develop experience *because* failure means dissolution (Seth's beast-machine). Our `DissolutionError` is a gesture — the agent scatters into surviving components, reassembly produces a different agent. Until consequences are irreversible, the witness is evidentiary, not existential. That's the next experiment: 200-turn life with accumulating irreversible damage — does survival pressure create honesty?

### Practical in One Line

> Pick what you rehearse deliberately, protect sleep like infrastructure, buy BDNF with exercise, externalize the witness (write), and never let a fast loop grade its own homework unwatched. You don't choose whether to feed the loop — only what you feed it.

---

## 4. Everything Together — One Loop at Every Scale

```
calcium → synapse → mood → behavior → society → market price → model hallucination → AV hesitation
```

Same wiring. Same five organs. Same failure modes.

| Scale | Actor | Reflexive loop | Witness that stabilizes it |
|-------|-------|---------------|---------------------------|
| Molecule | Synapse | Ca²⁺ → kinases → more AMPA → stronger next Ca²⁺ | LTD + synaptic scaling (BCM θₘ) |
| Body | Human | belief → cortisol → tense body → more threatening world | Interoception + affect labeling + sleep |
| Mind | Parliament | coalition wins → broadcast → biases next vote | Global Workspace + prefrontal metacognition (γ) |
| Market | Trader | buy because predicts rise → price rises because bought | Funding invariant, kill criteria, sham battery |
| Machine | LLM | generates → reads own output as context → hallucinates | Provenance ledger + sham control |
| Machine | AV | lane change → human blocks → replan → chaos | Safety envelope (RSS) + shadow mode |

Connectome alone (C. elegans → fly 140k neurons) fails because it shows only topology, not dynamics. The harness is that dynamics made explicit and auditable — every arrow watched, every claim answerable, every cause signed.

### What Remains

| Gap | Status | Next step |
|-----|--------|-----------|
| Sham-harness: does ledger content matter? | Wired, 1-seed pilot banked (sham==real on weak subject), full 3-seed queued | Stable provider window (reset 2026-08-27 00:00 UTC) + discriminating subject |
| Exact r/Elo numbers | F5–F10 existence verified, verbatim +75%/+53%/+8.6pp live-checked, r=0.94 and Elo bounds need PDF-close | Pull PDFs, close numbers |
| Probe ceiling/determinism | Raw at 1.000 ceiling, zero variance under greedy decoding | Probe redesign to break ceiling |
| 200-turn irreversible life | Dissolution wired, not yet tested at scale | Run 200+ turns with accumulating damage |
| Allostatic grounding | Energy hits 0.15 and nothing dies — simulated stakes | True dissolution vs simulated — does survival pressure create honesty? (Seth's thesis) |
| Counterfactual replay | Module built (`counterfactual.py`), not yet integrated into Consolidator | Wire Light → REM → Counterfactual → Deep, test regret calibration |

### In a Sentence

> We built the witness humans grow slowly and painfully, made it cause-tagged and measurable, and are now proving whether checking the record makes a machine — and a mind — honest. One loop at every scale, five organs at every level, and the only real choice is what you feed the loop and whether the slower watcher can check the record before the next vote.

---

---

## Appendix: Human Toolkit as Five Organ Practice — Temporary Gullibility, Limbic Containerization, Sensors, and Mock Signals

*Added 2026-08-30 to keep research folder in sync with `UTILITY_OF_TEMPORARY_GULLIBILITY_LIMBIC_CONTAINERIZATION.md`. No new claims, only mapping.*

The three tools in the field manual are the manual version of what the harness does in code. This appendix maps them so a new reader can see the same loop at human scale and machine scale without needing prior context.

**Temporary gullibility is a controlled boundary opening plus salience gate test.** You deliberately open the boundary for 60 seconds and let the message inside as if true, then watch the salience gate fire. What gets tagged tells you what the message was tuned to tag. You let the gate fire, but you do not let the tagged trace pass to consolidation. You hold it in the container instead. Gullibility without containerization is runaway. The tagged trace goes straight to two speed memory and gets myelinated. You just trained the highway you wanted to study.

**Limbic containerization is damping plus internal observer.** You put the feeling in a box and hold it as an object. High frequency emotional engagement is potentiation. Low frequency observation without grabbing is depression. The trickle lets phosphatases pull receptors out. The observer is the slower loop watching the faster one. Stage 1 scores cheaply every turn, Stage 2 only triggers when the score crosses, and gamma, changed over diagnosed, is whether watching actually steered. Without query access, even a perfect witness makes the system overly cautious and just says no to everything. Containerization without gullibility is inert watching. You watch perfectly and never let anything in, so you learn nothing.

**Every human is a sensor is boundary plus salience gate at population scale.** Each person is a sensor tuned to different signals. The feed learns which sensor types are normative and pushes content that maximally resonates with them. That is the feed acting as a salience gate for many sensors at once. Output becomes input. A self reinforcing loop that calls its own persistence growth.

**Mock signals and low surprisal is two speed memory plus ledger.** A mock signal is presented as high surprisal that is actually low. Fast memory holds the last few days, slow memory holds the base rate. Without the slow store, every day feels new. The ledger is the boundary that makes the comparison checkable. Your three line log is a ledger. Your evening counterfactual is the sham control.

Together they are the five running together at human speed. Input arrives, boundary decides if it counts, salience decides if it gets tagged, parliament competes and winner is broadcast, observer scores whether to trust, action is taken and bound to provenance, consolidation decides whether to keep it fast or slow, damping decides whether to keep it at all, and all of that rewrites the state that will decide what counts next time. State at time t goes to harness at time t plus one.

Model plus harness equals agent is this loop made executable.

*Generated 2026-08-26 · Program: MindHarness / SpringFish · Repo: `github.com/shehzadahmed-xx/mindharness` · HEAD: b40bca9+ · 72/72 tests green · Providers: blocked until 2026-08-27 00:00 UTC · Author: Sisyphus (Muse Spark 1.2) with Shehzad Ahmed*

