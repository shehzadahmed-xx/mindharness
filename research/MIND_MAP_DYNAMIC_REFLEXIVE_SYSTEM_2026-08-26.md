# Map of the Mind as a Dynamic Reflexive System

## The Territory

```
                    ┌─────────────────────────────────────┐
                    │           THE WORLD                  │
                    │  (other loops, other minds,          │
                    │   institutions, physics, chance)     │
                    └──────────┬──────────────────────────┘
                               │ perturbs
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                         THE BODY                                  │
│  ENERGY drains with every token (floor 0.15) │ FATIGUE rises with  │
│  every failure (cap 1.0) │ AFFECT valence [-1,1] arousal [0,1]    │
│  → PRE-CONSCIOUS FILTER affordance_space() — gated strategies     │
│  REMOVED from existence, not rejected                             │
└──────────────────────────┬───────────────────────────────────────┘
                           │ surviving proposals only
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                    THE PARLIAMENT (Layer 3)                       │
│  PERCEPTION │ MEMORY (5 types) │ SKILLS (cause-tagged) │ KNOWLEDGE│
│  WORLD MODEL contains SELF-MODEL as actor inside world           │
│  → COALITION COMPETITION (unconscious) → COUNTERFACTUAL REPLAY   │
│  → GLOBAL WORKSPACE (Layer 4) winner BROADCAST → consciousness   │
└──────────────────────────┬───────────────────────────────────────┘
                           │ broadcast content
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                   CONSCIOUSNESS                                   │
│  Not a place. The broadcast itself. What it feels like to be the  │
│  winner being published to every subsystem at once.               │
│  "I decided" = the broadcast, not the competition.                │
│  METACOGNITION (Layer 5): Stage 1 cheap anomaly → Stage 2 diagnose│
│  → TRUST/RETRY/REVISE/ABSTAIN, γ = changed/diagnosed              │
└──────────────────────────┬───────────────────────────────────────┘
                           │ action selected
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                      ACTION → Provenance Ledger → Update state   │
│                      → WORLD PERTURBED → back to top              │
│  OFFLINE: LIGHT dedupe → REM concept extract → COUNTERFACTUAL     │
│  variant→simulate→regret → DEEP utility gate (≥2 query types)     │
└──────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│           DISSOLUTION BOUNDARY                   │
│   energy ≤0.15 AND fatigue ≥1.0 → DISSOLVING →   │
│   DISSOLVED — parts persist, relations gone      │
│   reassembly = NEW agent, not same one restored  │
└─────────────────────────────────────────────────┘
```

## The Dynamic Reflexive System — Three Reflexivities

**Reflexive = takes itself as input as primary operation.** A reflexive camera photographs itself photographing and the photo changes next photo.

**1. System models world, model contains system**

```
World → Perception → World Model → contains → Self-Model
  ▲                                              │ predicts
  └────────── Action ◀──────────────── simulated outcome
```

One model with a hole shaped like you. Counterfactual.py needs LLM as its own simulate_fn — only the system simulates itself well enough for calibrated regret.

**2. System observes its own observing**

```
Broadcast ("I see X") → Metacognition: FOK/JOL → TRUST/RETRY/REVISE/ABSTAIN → γ
```

γ=0 (compliance guard): watches perfectly, never steers. γ>0: observation becomes intervention. Zhang's three barriers (no recurrence, no weight access, no fixed points) — harness supplies all three via loop, ledger, consolidation.

**3. System rewrites story that rewrites system**

```
Experience → Provenance → Self-Model (cause-signed) → Narrative compaction → Persona re-injection → next experience
```

Cause tags: action-outcome (lived) vs narrative-summary (lossy) vs external-write (human only). Without them, narrated traits file as lived. Choi: >30% persona drift in 12 turns without maintained state — self is performed, re-injected, or dissolves.

**Why dynamic:** State(t) → Self-Model(t) → Action(t) → World(t+1) → State(t+1) → counterfactual → calibration → Self-Model(t+1) ≠ Self-Model(t). Kleene recursion made physical — description is part of what is described. Pursuit moves the target.

**One equation:** Mind = body-gated parliament competing for global broadcast, watched by a metacognitive gate that may or may not steer, witnessed so claims are answerable, replaying what was and what could have been through a world-model that contains itself, calibrating the calibrator, bounded below by dissolution.

---

## Deeper — The Five Hard Ideas

**1. Loops feeding loops IS power** — capital→more capital, belief→more believers. Power/growth name direction, not thing. Spring-Loaded Door = anchor cut → loop springs, feeds on nearby loops. ESC (state-contingent claims) and MindHarness (provenance binding) are same fix: restore feedback (return depends on outcome / claim depends on record).

**2. Fighting IS mind** — Nayebi Cor. 3–5 proves low-regret on mixed tasks forces modularity, regime-trackers (emotions), belief-memory, world models, and convergence (Cor.5: independent traditions — Abhidharma, Sufism, neuroscience — converge because same constraint). Global Workspace fight is unconscious; broadcast is consciousness. Exhaustion contracts proposal set before vote — different chooser, not harder choice. Living sessions converged to same exhausted attractor cross-architecture.

**3. Replay with self-in-world-model IS learning** — replay (Light), counterfactual replay (variant→simulate→regret via self-in-world-model), calibration (regret as gradient). Current Consolidator lacks gradient; counterfactual.py adds it.

**4. Witness = wisdom** — intelligence (produce good outputs) vs wisdom (know where outputs came from). Raw Day1 1.000 vs Day3 0.667 (same weights, different room) — room matters more than model. Without witness over-claim (98% on fabrications), with witness but no query under-claim (always-no), with witness+query+capability → calibrated. Sham proves: if model doesn't read witness, corrupting witness changes nothing.

**5. Dissolution** — regulation without stakes (energy floor) vs Seth's beast-machine (must stay viable or cease as organization). IrreversibleDamage (permanent ceiling drop, skill deletion) + Dissolution (SM scatter, narrative truncate → reassembly = new agent) — most important queued test: do agents facing real dissolution process information differently?

All committed, clean tree, 72/72 tests green. Offline counterfactual integration + longer living sessions + top-journal expansion queued.
