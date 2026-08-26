# Parliament of Models — Next Programme Direction
*2026-08-27 — Many tongues, one harness. From single-model MindHarness v2 (symbolic parliament + one LLM) to parliament of models (each subsystem is a different LLM competing for one microphone).*

> Not one tongue in a harness. Many tongues, each powering a different subsystem, competing for one microphone. The harness is not around the models. The harness is the competition, the broadcast, the witness, and the veto.

## The move

**v2 (current, proven):** symbolic parliament + one LLM

```
Symbolic modules + one LLM = mind
  if energy < 0.15: remove navigation  (scalar check)
  competition = if statements
```

**Next (parliament):** parliament of models

```
Perception (VLM) + Memory (RAG LLM) + Affect (steered LLM) + Planner (reasoner) + Habit (skill LLM) + Narrator (press secretary LLM)
  → all bid via salience × utility
  → winner broadcast in Layer 4 Workspace
  → witness (provenance ledger) arbitrates claims
```

Each subsystem gets its own weights, prompt, temperature — different minds in the same head. The volume knob (arousal) and risk dial (valence) become actual prompt modulations per subsystem, not scalar multipliers.

## Why this is stronger

- **Specialization:** Perception gets a VLM, memory gets retrieval-tuned, affect gets valence/arousal-steered, planner gets reasoner, habit gets skill LLM, narrator gets instruction-tuned. Not one model pretending to be a parliament, but a parliament that actually is different.
- **Real competition:** Models bid with different proposals, scored by salience × utility, winner broadcast competing against other coalitions. Not symbolic `if` but scored bids.
- **Emergent human-likeness:** Don't code "narrator confabulates." Give narrator LLM only the broadcast (not the competition) and ask "why did you do that?" — pattern completion generates the most coherent story where "I" did it, with confidence, because that is what LLMs do when they only have the winner. Choice blindness and Gazzaniga's interpreter fall out as structural consequences, not programmed bugs.
- **Witness as arbiter:** When models disagree, ledger decides — not by authority but by checkability. "Did you generate this?" is a query to the ledger any subsystem can make, overruling the narrator's story.

## Cost

- N models = N calls/turn (parallel, not sequential). Workspace competition must be fast (~1-2s, 1500ms budget) or parliament never votes.
- Each model's training matters more: hallucinating perception poisons every winning bid globally.

## Cordis bundle sketch — dsh-mindharness-parliament

```yaml
# bundles/dsh-mindharness-parliament/cordis.patch.yml
# Many models, one workspace, witness as arbiter
- insert:
    - id: mh.perception
      name: mindharness/parliament-perception
      service: ctx.perception
      package: mindharness/parliament-perception
      llm: { provider: opencode, model: qwen3-vl, temperature: 0.2 }

    - id: mh.memory
      name: mindharness/parliament-memory
      service: ctx.memory
      package: mindharness/parliament-memory
      llm: { provider: opencode, model: gpt-oss-120b, temperature: 0.1 }

    - id: mh.affect
      name: mindharness/parliament-affect
      service: ctx.affect
      package: mindharness/parliament-affect
      llm: { provider: opencode, model: claude-haiku-4-5, temperature: 0.7 }

    - id: mh.planner
      name: mindharness/parliament-planner
      service: ctx.planner
      package: mindharness/parliament-planner
      llm: { provider: opencode, model: deepseek-v4-reasoner, temperature: 0.6 }

    - id: mh.habit
      name: mindharness/parliament-habit
      service: ctx.habit
      package: mindharness/parliament-habit
      llm: { provider: opencode, model: minimax-m3, temperature: 0.3 }

    - id: mh.narrator
      name: mindharness/parliament-narrator
      service: ctx.narrator
      package: mindharness/parliament-narrator
      llm: { provider: opencode, model: muse-spark-1.2-contributor-free, temperature: 0.8 }

    - id: mh.workspace
      name: mindharness/parliament-workspace
      service: ctx.workspace
      package: mindharness/parliament-workspace
      events: [agent/pre-step]
      dependsOn: [mh.perception, mh.memory, mh.affect, mh.planner, mh.habit]
      config:
        competition: "salience × utility"
        broadcast: "winner content + provenance spans to all subsystems"
        timeoutMs: 1500

    - id: mh.witness
      name: mindharness/parliament-witness
      service: ctx.provenance
      package: mindharness/provenance
      events: [session/event, agent/request, agent/pre-step]

    - id: mh.body-gate
      name: mindharness/parliament-body
      service: ctx.embodied
      package: mindharness/body
      events: [agent/pre-step]
```

Harness is not around the models. Harness is the competition, the broadcast, the witness, and the veto — the relations that make many tongues into one mind. Five invariants still hold, but now each is powered by a model that *is* that invariant.

## Program status

- v3 stays clean single-model harness paper (the proven 72/72, 40/40, sham queued) — this is the explicit next direction, not a replacement.
- Next step: generate 7 package stubs for dsh-mindharness-parliament the same way as dsh-mindharness, wire model_registry per subsystem, run 20-seed 4-arm battery as many-model vs single-model.
