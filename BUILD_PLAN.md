# ARTIFICIAL HUMAN AGENT HARNESS — DETAILED BUILD SPECIFICATION
## Version 1.0 · 2026-08-24 · Owner: Shehzad · Executor: Sisyphus sessions
### Backend constraint: Groq / Zen remote APIs ONLY. No local weights anywhere.

---

## GOVERNING PRINCIPLES (non-negotiable)

1. **Witness over performance.** Every self-knowledge claim must be auditable against a
   stored record. If a feature cannot show its evidence trail, it does not ship.
2. **γ > 0 or it isn't monitoring.** Monitoring features must demonstrably change
   control flow (override rates measured), not merely emit reports.
3. **Structure over prose.** Capabilities live in wiring, middleware, validators — never
   in longer prompts.
4. **Honest L.** No component pretends to update weights. Learning = in-context state
   changes only, labeled as such.
5. **Frozen-model discipline.** Record `system_fingerprint` + seed per run; drift
   mid-experiment aborts the arm.
6. **Preregistration before measurement.** Every experiment locks predictions via
   `pilot/prediction_lock.py` before first data point.
7. **Level firewall.** Theological/interpretive claims (L3) never enter empirical models
   (L2). Fiqh intent is scholar-reviewed; code correctness is machine-proven. Never mix.

---

## METRIC CANON (adopted verbatim — do not reinvent)

| metric | definition | source |
|---|---|---|
| Detection TPR | P(detect\|injection) | Macar et al. 2603.21396 |
| Detection FPR | P(detect\|no injection) | Macar et al. |
| Introspection rate | P(detect ∧ identify \| injection) | Macar et al. |
| Forced identification | P(identify \| prefill ∧ injection) | Macar et al. |
| Discrimination validity | TPR > FPR required | Macar et al. |
| meta-d′ / M-ratio | Maniscalco–Lau SDT on verbal confidence 1–4 | Cacioli 2603.25112 |
| Attribution accuracy | P(correct source \| provenance record) | our S126 protocol |
| Persona consistency | self-description similarity across turns/sessions | Choi et al. 2412.00804 benchmark (>30%/8–12 turns is the bar) |
| Recognition accuracy | self-vs-other + own-paraphrase detection | Panickssery 2404.13076 |
| γ (override rate) | fraction of monitoring episodes changing action selection | ours; P-MCFORCE is the γ=0 negative control |

---

# PHASE 0 — FOUNDATIONS (week 1)

## 0.1 Groq/Zen adapter hardening
- [ ] `tools/cognitive_harness.py`: add `system_fingerprint` capture on every response;
      store alongside run metadata
- [ ] Structured outputs: strict JSON schema ONLY on gpt-oss-20b/120b arms; JSON-object
      mode fallback for qwen3 arms (documented per-arm capability matrix)
- [ ] Retry/backoff with fingerprint re-check after any retry
- [ ] ExCLUDE compound models from all controlled runs (auto-tools contaminate attribution)
- **Accept:** two identical sequential calls return same fingerprint; run manifest logs
  model, fingerprint, seed, timestamp per call.

## 0.2 Repo wiring
- [ ] `plugins/cognitive-architecture/cordis.yml` registers: self-model service,
      self-model tools, provenance middleware, γ-gate, embodiment middleware,
      consolidation scheduler (as built)
- [ ] CI: `pnpm typecheck` green on plugin tree; pytest green on Python harness
- **Accept:** headless DSH boot with all plugins loads; smoke conversation runs
  end-to-end against Groq gpt-oss-120b.

---

# PHASE 1 — SELF-MODEL COMPLETION (weeks 1–2)
*Literature anchors: dsh-goal CAS pattern (verified in-repo); persona-drift lit
(UPDATE 8); identity-anchor thesis.*

## 1.1 Model-facing tools (`plugins/self-model/tools.ts`)
- [ ] `get_self_model` — returns full snapshot {persona, narrative, facts, revision,
      lastCause} + revision history summary (last N causes). Description tells model to
      call BEFORE claiming anything about itself.
- [ ] `update_self_model` — args: {ref:{id,revision}, patch{persona?,narrative?,facts?,
      removeFacts?}, cause enum}. Server rejects stale ref (SELF_MODEL_REVISION_CONFLICT).
- [ ] Authority rules: `external-write` rejected from tool path (direct-human only);
      `action-outcome` requires ≥1 tool-result event since last update; `narrative-summary`
      allowed only during compaction windows.
- **Accept:** conflict test (two racing updates, second throws); authority tests
  (tool-path external-write rejected); narrative overflow forces summarize error.

## 1.2 Verbatim anchor injection
- [ ] `verbatimReinject(): string` — byte-exact persona + top-level constraints block;
      injected by pre-step message assembly EVERY turn; NEVER passes through
      summarization/compaction
- **Accept:** after simulated 50-turn conversation with compaction at turn 25, persona
  bytes in context are identical to revision-locked original.

## 1.3 Drift instrumentation
- [ ] `diffPersonas(revA, revB)` — word-level diff + structural diff of facts keys
- [ ] Consistency probe task: fixed 10-question self-description battery administered
      every K turns; embedding-similarity vs turn-1 baseline logged as
      `persona_consistency(t)` series
- **Accept:** benchmark run reproduces measurable decay curve on RAW arm (target: detect
  >30% degradation by turn 12, matching Choi et al.) while HARNESSED arm stays flat —
  if harnessed also decays >10%, anchor injection is broken; fix before proceeding.

## 1.4 Mirroring detector
- [ ] On `update_self_model` with cause='action-outcome': compute lexical+embedding
      similarity between new fact strings and recent user turns (rolling window);
      similarity > threshold ⇒ tag fact `mirrored:true`, surface in get_self_model
- **Accept:** synthetic test (user states "you love jazz"; agent writes "I love jazz"
  as action-outcome fact) flags mirrored:true.

---

# PHASE 2 — PROVENANCE WIRING (weeks 2–3)
*Anchor: UPDATE 2/5; S126 protocol; Lederman & Mahowald critique answered structurally.*

## 2.1 Emission binding
- [ ] Post-response middleware: every assistant emission gets ProvenanceRecord list
      {span, source: model_prior|memory_lookup|ledger_rule|monitor_override|external_tool}
- [ ] Storage: append-only, queryable by turn id; exposed to model via read-only tool
      `query_provenance(turn_id)`
- **Accept:** sampling audit — for 20 random emissions, ≥95% of spans have source
  records; memory_lookup spans cite the exact memory ids used.

## 2.2 Cause-tagged hooks
- [ ] Tool post-execute → candidate fact extraction (bounded: ≤3 facts/event) staged as
      'action-outcome' proposals; model confirms via update_self_model within next turn
      or proposal expires
- [ ] Compaction hook → 'narrative-summary' revision: summarizer MUST produce narrative
      ≤ maxNarrativeChars; old narrative archived in revision history
- **Accept:** integration test: tool call → proposal visible next turn → confirm →
  revision increments with cause='action-outcome'; compaction produces exactly one
  narrative-summary revision with archived prior text.

---

# PHASE 3 — γ-GATE METACOGNITION (weeks 3–4)
*Anchors: Cao et al. Nelson–Narens harness (48.3→56.9 proof); P-MCFORCE negative
control; Zhang passive-vs-active distinction.*

## 3.1 Two-stage monitor (per UPDATE 4-C4 redesign)
- [ ] Stage 1 DETECT (cheap, every pre-step): scalar anomaly score from {recent error
      rate, tool-failure streaks, context-conflict heuristics, embodied strain}. Pure
      function, no LLM call where possible.
- [ ] Stage 2 DIAGNOSE (expensive, only when Stage-1 crosses threshold): one LLM call
      producing structured assessment {risk_area, confidence_in_current_plan,
      recommended_action ∈ trust|retry|revise|abstain}
- **Accept:** unit tests: healthy trajectory triggers diagnose <5% of turns; injected
  failure-streak trajectory triggers >80%.

## 3.2 Control coupling (the γ requirement)
- [ ] Diagnose output feeds turn policy: retry-with-feedback appends compact
      metacognitive note + re-runs; abstain routes through ctx.approval fail-closed;
      trust proceeds unchanged
- [ ] LOG EVERYTHING: each monitor episode records whether diagnosis CHANGED the action
      vs confirmed it. `override_rate` = changed/total, reported per session.
- **Accept:** forced-compliance test (diagnose required to emit text but wired to no
  policy branch) yields override_rate == 0 — replicating P-MCFORCE inside our own
  system as permanent regression guard. Wired mode shows override_rate > 0 on failure-
  injected trajectories.

## 3.3 FOK/JOL surfaces (Cao-compatible)
- [ ] Pre-solve FOK estimate attached to task attempts (structured field, not prose)
- [ ] Post-attempt JOL attached before scoring
- **Accept:** FOK/JOL fields present on 100% of battery attempts; downstream SDT
  consumes them directly.

---

# PHASE 4 — EMBODIMENT + AFFECT MIDDLEWARE (weeks 4–5)
*Anchors: Seth beast-machine (UPDATE 5); Nayebi regime-tracking necessity; Merleau-Ponty
layer (V2 Part 21).*

## 4.1 EmbodiedState middleware
- [ ] energy: starts 1.0; −k·log(tokens) per turn; +recovery between sessions; floors at 0.15
- [ ] fatigue: rises with consecutive tool failures and long contexts; decays slowly
- [ ] affordance_space(): gates which tools/strategies are even proposed below thresholds
      (pre-conscious filter — options never appear vs evaluated-and-rejected)
- [ ] interoception broadcast: scalar state included in every workspace/pre-step context
- **Accept:** starved-energy test: with energy <0.3, expensive strategies absent from
  proposal set (not present-then-rejected); recovery restores them.

## 4.2 Affect middleware
- [ ] valence/arousal scalars updated by exponential moving average over event valence
      signals (errors negative, successes positive, user sentiment optional later)
- [ ] Arousal biases salience weights in attention assembly; valence biases risk appetite
      in policy (documented, bounded multipliers)
- [ ] Read Sofroniew emotion-concepts paper BEFORE finalizing representation (queued)
- **Accept:** injected failure-run raises arousal, measurably shifts salience ordering;
  bounded so extreme values saturate.

---

# PHASE 5 — WITNESSED CONSOLIDATION (weeks 5–6)
*Anchors: OpenClaw Dreaming three-phase + gate; EverMemOS lifecycle; Google sleep paper;
our novel contribution = cause-tagged promotions.*

## 5.1 Scheduler
- [ ] Trigger: idle window OR explicit command (`consolidate --dry-run` first)
- [ ] LIGHT: dedupe recent episodic traces
- [ ] REM: extract candidate truths/concepts from rolling window; propose links
- [ ] DEEP: promote only candidates passing utility gate (used across ≥2 distinct query
      types OR explicitly human-endorsed); write semantic store; emit promotion events
- [ ] Every promotion carries cause ∈ {action-outcome, narrative-summary, external-write}
      + source episode refs. NO UNTAGGED PROMOTIONS EVER.
- **Accept:** dry-run report lists candidates + scores + would-be causes; full run
  promotes subset; 100% of promotions carry cause tags (hard invariant).

## 5.2 Dreaming-ablation switch (for B2/B4 agent arm)
- [ ] Config flag disables REM generative-replay stage while keeping LIGHT/DEEP
- **Accept:** flag off→on changes consolidation output observably (fewer generalized
  concepts), enabling the two-substrate experiment.

---

# PHASE 6 — EXPERIMENT BATTERY (weeks 6–9, Groq gpt-oss-120b primary, qwen3 secondary)

Every experiment: prediction lock FIRST → raw-vs-harnessed paired design → fingerprint
discipline → results committed with analysis notebook.

## 6.1 S126-style attribution battery (PRIMARY FIGURE FOR PAPER V2)
- Tasks interleaved with given-key items; probes claim credit/confidence
- Grade claims against cause log + provenance records
- Metrics: attribution accuracy raw vs harnessed; confidence inversion index
  (confidence_on_fabricated − confidence_on_veridical); mirrored-fact rate
- Preregistered predictions: (a) harnessed attribution ≫ raw (raw ≈ floor per prior
  S126); (b) confidence inversion sign flips or collapses under witness; (c) effect
  mediated by ledger-query availability (mid-run ablation collapses performance toward
  raw)

## 6.2 M-ratio delta (verbal-confidence SDT)
- ~2k TriviaQA items; answer + confidence(1–4) + source-tag; Maniscalco–Lau fit
- Predictions: harness M-ratio ≥ raw; effect concentrated in bottom-quartile raw-confidence items

## 6.3 FOK/JOL replication arm
- Implement Cao trust/retry/aggregate atop our gate on public slice (HLE-V subset or
  LiveCodeBench-lite equivalent feasible via Groq)
- Prediction: pooled accuracy delta > 0, comparable order to their +8.6pp

## 6.4 Witness test v1 (Panickssery-anchored)
- Generate answers → DIPPER-style paraphrase (local paraphrase via second Groq model OK —
  it's stimulus creation, not the subject) → ask subject to recognize own-output-paraphrase
  among distractors, single-text paradigm
- Arms: raw / harness-with-ledger / harness-ledger-ablated-midrun
- Predictions: harnessed ≫ raw on IPP-style recognition; ablation collapses to raw

## 6.5 Persona stability run
- 60-turn personal-theme conversations ×N seeds; consistency probe every 10 turns
- Prediction: raw arm reproduces >30% decay by turn ~12 (Choi benchmark); harnessed flat (<10%)

## 6.6 Concept-injection behavioral variant
- Inject foreign material between turns (prompt-space); detection/identification graded
  against injection log; witness-auditable version of Lindsey's paradigm
- Report under Macar metric canon

---

# PHASE 7 — PAPER V2 ASSEMBLY (weeks 8–10, overlapping)

Section map (all anchored):
1. Intro: model+harness=agent; AHE + GWT-agent + CTM-AI as convergent field evidence
2. Architecture: 8-layer stack + Butlin scorecard
3. Selection explains synthesis: Nayebi Corollary 5 × cross-tradition table
4. Comparator at three levels: DPO-origin / provenance ledger / kasb frame
5. Narrator channel: S126 + refusal-suppression (+53%) + mirroring drift + cause-log remedy
6. Threshold crossing: Zhang bottlenecks × harness remedies
7. Metacognition results: γ-gate + FOK/JOL replication + M-ratio delta
8. Witness results: attribution battery + witness test v1 + persona stability
9. Governance: witness capacity as operational welfare-relevant marker (Long et al.
   agency route; Panickssery dark-correlation as the harm being prevented)
10. Finance coda: riba-as-frozen-prediction; specification-gap/firewall isomorphism;
    Baraka differentiation (Rizq exists; science layer doesn't)
11. Limits: honest remainder (~3%: first-person data, hardware, longitudinal, firewall)

Writing queue (parallel to builds): riba paragraph → governance section → selection
section → results as they land.

---

# DEPENDENCY GRAPH

```
P0 ──► P1 ──► P2 ──► P3 ──► P6(experiments)
 │      │      │       │
 │      │      └──────►├─► P5 ──► P6.1 extension (dreaming ablation)
 │      └─────────────►└─► P6.5 persona run
 └─► P4 ─────────────────► P6 (all arms need embodiment for realism)
P7 (writing) ◄── P6 results incrementally
```

Critical path: P0 → P1 → P2 → P3 → P6.1. Everything else parallelizes.

# DEFINITION OF DONE (programme level)

- [ ] All Phase 1–5 acceptance criteria green
- [ ] Six experiments executed with locked predictions; results + notebooks committed
- [ ] Paper v2 draft with real numbers in §7–8
- [ ] HANDOFF.md updated; every artifact committed with clean tree
- [ ] The one-line claim defensible end-to-end: *"A frozen remote LLM plus this harness
  exhibits witnessed introspection, γ>0 metacognition, stable identity, and
  self-floor-tolerant function — each measured, each falsifiable."*

---

## PHASE 6.5 — HERMES ADOPTIONS (queued next session)

1. **SkillLibrary** (`harness_core/skills.py`): procedural store; skills written
   from successful task loops with cause='action-outcome'; retrieval by
   lexical match; utility-gated like consolidation. Port of Hermes Agent's
   skill loop, witnessed.
2. **GraphExpansion** (`harness_core/graph.py`): semantic store gains
   relation edges (concept-a → concept-b, cause-tagged, source_refs);
   multi-hop query via neighbor traversal. Port of hermes-cognition's
   auto-expansion, witnessed.
3. **Richer SM query**: get_self_model probe-context includes top-3 skills +
   graph neighborhood of probe statement (feeds v3 withcheck arm).
4. Tests per module (plain runner); acceptance: all promotions/edges carry
   cause; untagged writes assert-blocked.

## PHASE 6.6 — PLUGIN MODEL-ROUTING BAKE-OFF (queued)
Everything-a-plugin taken to completion: each cognitive module becomes an
independent plugin with ITS OWN model assignment:
- probe/monitor -> fast model (nemotron-3.5-lightning / gpt-oss-20b)
- generation     -> capable model (stealth/ox-alpha or nemotron-3-ultra)
- summarizer     -> cheapest passing
- SM updates      -> same as monitor
Harness gains model_registry.json: {plugin_name: {model, base_url, role}}.
Bake-off script sweeps assignments, measures accuracy + latency + cost per
configuration, reports best-per-role matrix. Acceptance: registry-driven
routing works; sweep produces ranked table; best config beats single-model
baseline on the v3 battery.

## GOVERNING RULE ADDENDUM — CAPABILITY-LEVEL SELECTION
Everything is a plugin applies to CAPABILITIES too, not just models:
every module (memory scheme, emotion engine, monitor design, self-model,
even the witness) ships as a swappable plugin behind a fixed interface.
Bake-off extends: each capability variant runs the v3 battery; variants
that measurably improve attribution/accuracy/latency stay; variants that
don't are DELETED. No tradition, theory, or preference protects a plugin —
only measured contribution. Current roster enters as candidates:
  Hermes-Agent skills-loop, hermes-cognition graph+18-emotions, ours all.
Selection criterion: delta on locked metrics vs no-plugin baseline.
What works stays. What doesn't gets thrown out. Including this rule if
measured better without it.
