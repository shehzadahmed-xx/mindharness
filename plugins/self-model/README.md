# dsh-self-model — SM node, first slice

Event-sourced self-model plugin for the DeepSeek Harness, mirroring `dsh-goal`'s
verified pattern (GoalRef-style CAS fence: `revision must equal current + 1`,
tombstone clears, strict fold validation — checked against
`packages/goal/goal/src/{types,fold,index}.ts` in the real repo).

## Why `cause` is the important field

Every durable mutation records its authority channel:

| cause | meaning | comparator role |
|---|---|---|
| `action-outcome` | agent updated own record from something it did | efference copy; the S126 provenance case |
| `narrative-summary` | summarization rewrote the story | N maintenance, not raw log growth |
| `external-write` | direct human authority wrote it | outside-the-loop ground truth |

This is the structural comparator from the consciousness programme expressed as an
event field: narrator-narrated fusion stops being invisible because every change to
"who I am" carries a signed reason. An agent whose self-model only ever changes via
`action-outcome` and `narrative-summary` has a checkable introspection history;
claims of self-knowledge can be audited against the cause log.

## What this deliberately is NOT

- **Not L (learning).** Nothing here touches weights. Narrative is bounded
  (`maxNarrativeChars`, overflow forces summarize-not-append) precisely so nobody
  mistakes log growth for learning. The two honest L options remain:
  in-context growth + summarization (free), or external fine-tuning loop via a
  custom adapter (separate project).
- **Not V.** `persona` is stable character edited explicitly; session-scoped
  objectives stay in `ctx.goals`. The distinction stands.

## Backend

Designed for remote models (Groq / Zen). Zero weight access assumed anywhere.
All self-knowledge claims route through the auditable record — with no residual
stream to read, observable channels are the ONLY channels, which is what the
provenance discipline requires anyway.

## Next steps (in order)

1. Wire into `plugins/cognitive-architecture/cordis.yml` alongside existing plugin
2. Model-facing tools: `get_self_model` / `update_self_model` via `defineTool`
   (inject `['selfModel', 'tools', 'systemPrompt']`), following tool-goal's shape
3. Compaction hook emits `narrative-summary` updates on context compression
4. Tool post-execute hook emits bounded `action-outcome` fact updates
   (e.g., capability discoveries, repeated-failure facts)
5. First test: S126-style battery against remote backend — attribution accuracy
   of self-model claims vs the cause log
