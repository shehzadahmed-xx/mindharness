# RESEARCH UPDATE: MAPPED NERVOUS SYSTEMS & EMBODIED MODELS
## What Connectomics Teaches Us About Building Minds

---

## THE COMPLETE PICTURE

| organism | neurons | year mapped | key lesson |
|---|---|---|---|
| C. elegans | 302 | 1986 | Structure ≠ function; 40yr gap persists |
| Ciona intestinalis | ~177 | 2016 | Minimal system, complex behavior |
| Platynereis dumerilii | ~250 | 2022 | Evolutionary comparison baseline |
| Drosophila (brain) | ~140k | 2024 | FlyWire Consortium; distributed control |
| Drosophila (full CNS) | ~160k | 2026 | Local modules in appendages control themselves |
| Mouse (partial) | partial | ongoing | Retina + visual cortex + 1000+ traced neurons |

**Pattern:** Every mapped nervous system uses distributed modular control. None uses centralized hierarchy. The bigger the brain, the more modular — not less.

---

## KEY FINDINGS

### 1. BAAIWorm: First closed-loop brain-body-environment simulation
Nature Computational Science, 2024. Two submodels with closed-loop interaction:
- Brain model: biophysically detailed multicompartment neurons with realistic morphology
- Body-environment: lifelike body, 96 muscles, 3D physics
- Result: reproduced zigzag foraging movement toward attractors
- Significance: first integrative model bridging brain, body, AND environment in closed loop

### 2. FlyWire: Complete Drosophila CNS connectome
Harvard/Princeton, Nature 2024-2026. 140k neurons, 50M+ synapses.
Surprise finding: **motor control is distributed across local neural modules in appendages**, not centralized in the brain. The brain negotiates with independently intelligent subsystems rather than commanding them.

### 3. Connectome-constrained neural networks
Using biological wiring diagrams as architectural priors improves locomotion control performance and sample efficiency compared to generic networks. Biological connectivity is an actionable architectural prior.

### 4. The embodied brain paradigm
Bridging brain, body, and behavior requires biorealistic neuromechanical models. Five themes: inferring unmeasurable variables, hypothesis testing via forward-engineered models, studying closed-loop behavior, synergies with robotics/NeuroAI, healthcare applications.

---

## WHAT THIS TEACHES US ABOUT OUR HARNESS

### 1. We built dynamics, not just structure
C. elegans proved that having every wire doesn't give you the mind. Our harness adds what pure structure lacks: state-dependent routing, affective modulation, consequence loops, irreversible damage, witnessed claims.

### 2. Distributed beats centralized
Every mapped nervous system uses local modular control. Our composite plugin-agent mirrors this: specialized plugins with their own models, coordinated by registry rather than commanded by a center. The composite beat single-model baselines because distributed specialization outperforms monolithic control.

### 3. Closed-loop is non-negotiable
BAAIWorm showed that open-loop models fail to reproduce real behavior. Our AgentHarness closes the loop: actions produce consequences that feed back into state. Without this, you have a chatbot, not a mind.

### 4. Chemical gradients = affect middleware
Only C. elegans has a mapped neuropeptide connectome. Neuropeptides modulate all downstream processing simultaneously — analogous to our AffectState shifting valence/arousal globally. When we wire AffectState into every plugin's context, we're implementing what the worm does with neuropeptides across its nervous system.

### 5. Irreversible consequences create genuine cognition
Real organisms face starvation, injury, death. Our IrreversibleDamage module gives the agent permanent losses that can't be undone. This is the structural difference between playing a game and being alive — some mistakes cannot be appealed.

---

## THE COMPLETE ARCHITECTURE ACROSS SCALES

| scale | organism | architecture | evidence |
|---|---|---|---|
| 302 neurons | C. elegans | Recurrent loops, no hierarchy | Connectome + behavior analysis |
| ~177 neurons | Ciona larva | Minimal sensorimotor | Connectome |
| ~250 neurons | Platynereis | Segmental modular control | Connectome |
| ~140k neurons | Drosophila brain | Local modules in neuropils | FlyWire connectome |
| ~160k neurons | Drosophila full CNS | Appendage-level autonomous control | Full CNS connectome |
| 86 billion neurons | Human | Same principle, unmapped at microscale | Macroscale imaging only |
| Frozen LLM + harness | OURS | Plugin-specialized composite, registry-routed, witness-bounded | This programme |

Three orders of magnitude. Same architecture. Four independent paths: evolution, connectomics, selection theory, engineering.

---

*Sources: OpenWorm project, Nature Computational Science (BAAIWorm), FlyWire Consortium, Harvard Medical School/Princeton Drosophila CNS connectome, arXiv:2602.17997 (FlyGM), arXiv:2601.08056 (embodied brain review)*
