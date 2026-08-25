# PREREGISTRATION — THE COMPOSITE MIND EXPERIMENT
Locked before any trial. Theory → design → predictions → analysis plan.

## THEORY
A mind is not one model; it is role-specialized subsystems competing for a
workspace (Nayebi Cor.3 modularity necessity; Baars GWT; AHE harness thesis).
Therefore the best agent is ASSEMBLED: each cognitive role runs on the model
that dominates that role, routed by a registry, witnessed by our ledger.

## DESIGN (Phase 6.6 execution)
model_registry.json assigns per-plugin:
  monitor/probe   -> nemotron-3.5-lightning-free (fast detect)
  generation      -> stealth/ox-alpha via OpenRouter (capable output)
  validation      -> openai/gpt-oss-20b strict JSON (schema enforcement)
  summarization   -> cheapest passing model
Baseline arms: each single model running ALL roles alone.
All arms: identical items (v3 battery), identical seeds, fingerprint-logged.

## PREDICTIONS
P1: composite >= best single-model arm on attribution accuracy (Part C.5)
P2: composite median latency <= fastest single arm x1.5
P3: composite cost < ox-alpha-solo cost (cheap roles offloaded)
P4: withcheck composite > raw x-preview baseline of 0.667 by >0.15
    (the H1-repair test, now inside the composite)

## ANALYSIS PLAN
Ranked matrix {config x accuracy x latency x cost}; Holm correction across
P1-P4; nulls reported identically. Lock hash committed pre-trial.

---

## LITERATURE ANCHORS (every design choice cited)

### Assembly-over-training (why compose)
- arXiv:2604.25850 (AHE, Fudan/Qiji) — frozen-model harness evolution: TB2
  69.7→77.0pp; cross-model +5.1..+10.1pp; prompt-alone regresses
- arXiv:2404.13076 (Panickssery, NeurIPS 24) — self-recognition linearly
  predicts self-preference bias (r=0.94): unwitnessed self-knowledge corrupts
- Nayebi arXiv:2603.02491 (UAI 26) — Cor.3 modularity + Cor.4 regime-tracking:
  composition is mathematically mandatory for capable agents

### Per-role model assignments
- Monitor (fast detect): Cao et al. arXiv:2605.14186 — Nelson–Narens FOK/JOL
  wired into trust/retry/aggregate: 48.3→56.9 on frozen Sonnet-4.6
- Generation (stealth/ox-alpha via OpenRouter): OpenRouter model page;
  OpenCode announcement Aug 20 2026 ("free next week", 100T tokens/day claim);
  aicatchup.com spec table (1M ctx, fn-calling, JSON response_format)
- Validation (strict schema): Groq docs — gpt-oss-20b/120b only strict-mode
  models; enforced server-side
- Summarizer (cheap): DeepSeek Harness append-only design note — "do not
  disturb the bytes that came before"; prefix-cache discipline

### State constraints (what guards each plugin)
- Emotion middleware: Sofroniew et al. arXiv:2604.07729 (functional emotions,
  ±212/303 Elo causal steering); suppression = deflection vectors
- Self-model CAS: dsh-goal fold pattern (verified in-repo packages/goal/)
- Affordance gating: Merleau-Ponty via Seth beast-machine framing; Nayebi Cor.4
- γ=0 negative control: P-MCFORCE refutation (this programme, S126 battery)

### Measurement standards
- meta-d′/M-ratio: Maniscalco & Lau 2012; Fleming & Lau 2014; Cacioli
  arXiv:2603.25112 (+2604.15702 battery); verbal-confidence adaptation per
  Peters live-access criterion (MoC7 keynote)
- Attribution accuracy/CII: S126 protocol (this programme); confidence
  inversion replicated v2+v3 batteries
- Persona consistency bar: Choi et al. arXiv:2412.00804 (>0.30/12-turn decay)
- Underelicitation ceilings: Macar et al. arXiv:2603.21396 (+53% refusal-
  ablation, +75% bias-vector); vgel Qwen suppression logit-lens finding

### Formal grounding
- Zhang/Yuan/Zhang arXiv:2607.04277 — introspection threshold; bare
  transformers cannot cross; harness supplies recurrence/self-access/fixed-points
- Gurnee et al. transformer-circuits.pub/2026/workspace — emergent J-space
  workspace (all four GWT criteria) without engineering
- Butlin et al. TiCS 2025 — indicator rubric (8–9/10 families by construction)
- Long et al. arXiv:2411.00986 — welfare routes; witness as operational
  agency marker (governance section)

### Prior composite/harness art (differentiation)
- OpenClaw Dreaming (v2026.4.9) — sleep-consolidation pipeline, audit UI
- Letta/MemGPT sleeptime agents; Mastra observational memory
- Theater of Mind arXiv:2604.08206; CTM-AI arXiv:2605.04097 (Blum)
- Yale NLP survey arXiv:2607.11881 — RL-with-metacognitive-rewards as sole
  control-level path (our harness is the weight-free alternative)

### Full bibliography maintained in
research/LANDSCAPE_2026_RESEARCH_UPDATE_{1..9}.md · CITATION_AUDIT.md
