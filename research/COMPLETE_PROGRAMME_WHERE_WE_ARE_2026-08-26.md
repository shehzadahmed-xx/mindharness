# The Complete Programme — Where We Are (2026-08-26)

> Captured verbatim from Sisyphus-Ultraworker synthesis — loops feeding loops, subsystems fighting, replay with self-in-world-model. Preserved as design requirements.

## 1. The Thesis in One Sentence

A mind is not a thing. It is a parliament of subsystems fighting for dominance inside a body that must stay alive, replaying what it did and what it could have done through a world-model that contains itself — and the fight matters only because some mistakes cannot be undone.

Everything we built is this sentence made executable.

## 2. The Three Research Threads

We work on three linked problems that are really one problem seen at three scales:

**Thread A: The Spring-Loaded Door (SLD)** — Crises decouple self-reinforcing loops from the institutional anchors that normally contain them. A banking panic, a currency collapse, a run on a fund — the loop that was held in place by rules and expectations suddenly springs free and feeds on itself. We mapped this as a network: 2,974 actors, 3,575 relationships, engine SpringFish V3.0 Beta3 (60/60 checks green). Every link is sourced and ranked. The question: who built doors that spring, and who bears the cost when they do?

**Thread B: Event-State-Contract (ESC)** — Financial claims are constitutional objects — their design determines who bears exhaustion risk (what happens when the money runs out). An interest-bearing loan says: return is stipulated regardless of outcome, severing action from survival consequence. A state-contingent claim says: return depends on what actually happened, restoring the feedback loop. Same principle as cognition — predictions without consequences are hallucinations without correction. ESC asks: what contract designs keep systems honest?

**Thread C: The Consciousness Bridge (MindHarness)** — Can an artificial agent be honest about its own processing — not just produce correct outputs, but correctly report where its outputs came from? This is where the harness lives. The model alone is a tongue; the harness is the mind; the witness keeps the mind honest. This thread is fully built and experimentally tested: 133 commits, 72/72 tests green, paper compiled, public at github.com/shehzadahmed-xx/mindharness.

All three threads share one root cause: systems without witnesses confabulate, and confabulation compounds.

## 3. How We Think Humans Work

### 3.1 Humans are reflexive dynamic systems loops
"we are all self-reinforcing loops feeding on one another trying to create more self-reinforcing loops and call it power or growth"

A human is not a static entity that has loops. A human is loops — metabolic, affective, narrative, social — each trying to sustain and expand itself. Power and growth are what a loop calls its own persistence when it can narrate. This is not metaphor. It is the selection-theoretic view (Nayebi): any system that achieves low regret must develop self-sustaining internal structure. The loops are the price of competence.

### 3.2 The mind is subsystems fighting for dominance
"the mind is different subsystems fighting for dominance, our mind and architecture and state all changes depending on task we are doing feeling etc"

There is no central executive. There is a parliament: perception, memory, affect, planning, narration — each a specialist module competing for access to the global workspace. What you experience as "I decided" is the winner of a coalition competition being broadcast. The losers don't disappear; they keep competing. Your architecture is not fixed — which subsystems can even propose changes with your energy, fatigue, and affect. When you are exhausted, options don't get considered and rejected; they stop existing as candidates.

In the harness, affordance_space() literally removes gated strategies from the proposal set — the exhausted agent has fewer possible moves, not harder choices about the same moves. Both living sessions hit energy floor at 0.15 and just proceeded — the configuration had contracted.

### 3.3 Humans replay what happened and what could have happened
"we keep playing back what we did what we could have done and calibrating our future responses using our predictive engine and model of the world and us in it"

Three operations:
1. Replay — reactivate what actually happened (hippocampal replay, our Light phase)
2. Counterfactual replay — simulate trajectories never taken: "what if I had done X instead?" (prefrontal branching, reverse replay — we just built this as counterfactual.py)
3. Calibration — score the imagined alternative against the actual outcome, compute regret, and update the policy for next time

Critically, the self is inside the world model, not beside it. You don't update a world model and a self-model separately. You run yourself through the world model and watch what happens. Our current architecture gets this wrong structurally — ProvenanceLedger (world record) and SelfModelService (self record) are parallel modules at different layers. You experience them as one thing.

This is predictive processing (Friston) / active inference: the brain is a prediction engine that minimizes surprise by constantly simulating itself acting in the world.

## 4. How the Mind Works — The Full Architecture

```
Layer 7: Constitution          Fiqh axioms, evidence firewall, claim constitutions
Layer 6: Narrative Self        Persona (CAS-revisioned, cause-signed), Narrative, Facts
Layer 5: Metacognition         Stage 1: anomaly detect → Stage 2: diagnose → Policy: trust/retry/revise/abstain
Layer 4: Global Workspace      Coalition competition, winner broadcast, state-dependent attention
Layer 3: Specialist Modules    EmbodiedState, AffectState, Memory, Skills, KnowledgeGraph, Consolidator, WorldModel
Layer 2: State Validation      Cetasika constraints, nafs tracking, affordance pre-filter
Layer 1: Provenance Ledger     Span binding, source tracking, attribution audit, proposal queue
Layer 0: Frozen Language Model Any OpenAI-compatible API (backend-agnostic)
```

Each layer in human terms:
- L0 — the tongue. Pattern completion. Can produce any continuation but knows nothing about where its outputs came from.
- L1 — the witness. Records what actually happened so claims can be checked against evidence.
- L2 — the body filter. Before the mind even considers options, the body's state has already removed some from existence.
- L3 — the parliament members. Each shaped by selection pressure (Nayebi Cor. 3–5 proves they are mandatory).
- L4 — the parliament floor. Specialists compete; winner gets broadcast globally. What you call "consciousness" is the broadcast, not the competition.
- L5 — the inner observer. Cheap anomaly detection always on; expensive diagnosis only when triggered; γ measures whether the watcher actually steers.
- L6 — the story. Who you claim to be, revisioned with cause tags.
- L7 — the law. What counts as evidence, what claims are allowed.

## 5. What We Built and What It Proved

**Harness (11 modules, 72/72 tests green)** — BackendClient, RunDiscipline (SHA-256 locks), SelfModelService, ProvenanceLedger, MonitorGate (γ ledger + compliance-guard), EmbodiedState + AffectState, SkillLibrary + KnowledgeGraph, Consolidator Light/REM/Deep, AgentHarness, plus CounterfactualReplay and Irreversibility/Dissolution.

**Experiments Executed:**
- Living session 1: nemotron-3-ultra (Zen) — 40/40 turns, coverage 1.000, 7 SM revisions, energy floor, valence +0.148
- Living session 2: gpt-oss-120b (Groq) — replicated identically
- Attribution battery v2: x-preview-f-free Day 1 — raw 1.000 (only subject to show this)
- Attribution battery v3: gpt-oss-120b, nemotron ultra — all arms 0.667 (always-no floor)
- Sham control (R1 #8): gpt-oss-120b 1-seed pilot — all 4 arms 0.667, sham==real
- Composite routing: P1 passed (+0.083), P2 passed

**Key Findings F1–F10 (all verified):** origin discrimination rare (1/6), deterministic strategies, witness-starved under-claim vs unwitnessed over-claim, structure beats prose (AHE +7.3pp, Macar +75%, Cao +8.6pp), selection theorems mandate architecture, cross-tradition convergence (Cor. 5), bare transformers cannot self-refer (Zhang), unwitnessed improvement corrupts (r=0.94), functional emotions causally steer (±212/303 Elo), persona depletes as context-position asset (>30% in 12 turns).

## 6. Current Status and What's Queued

Committed and pushed (public repo, 135 commits): harness core, experiments, paper v2 (17pp), peer reviews, citation audit, counterfactual module.

Blocked on providers (transient): Groq 403, OpenRouter free 50/day exhausted until 2026-08-27 00:00 UTC, Zen x-preview no longer supported. Full 3-seed sham comparison queued for next stable window. Offline work ready: counterfactual integration, longer living sessions (200+ turns with dissolution), top-journal expansion.

What you said today that became architecture: your three statements — loops feeding on loops, subsystems fighting for dominance, replay of what was and what could have been through a world-model containing the self — are now preserved as design requirements.

All committed at b40bca9, clean tree, public at github.com/shehzadahmed-xx/mindharness. Next: bash HANDOFF.sh → providers recovered → execute queued sham battery.
