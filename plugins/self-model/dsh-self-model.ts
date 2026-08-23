/**
 * dsh-self-model — SM node of the cognitive architecture.
 * Event-sourced, revisioned, compare-and-set self-model domain following the
 * dsh-goal pattern exactly (GoalRef CAS fence, fold validation, tombstones).
 *
 * The `cause` field is the AUTH tag / structural comparator: every durable
 * change to the self-model records WHY it happened, so narrator-narrated fusion
 * becomes auditable rather than invisible.
 *   - 'narrative-summary': harness summarization rewrote the story (N)
 *   - 'action-outcome':    agent updated its own record from what it did
 *                          (efference copy — S126's provenance case)
 *   - 'external-write':    written by direct human authority
 *
 * Backend note: designed for remote LLMs (Groq / Zen). No weight access is
 * assumed anywhere; all introspective claims route through this auditable
 * record, which is the point.
 *
 * @module @deepseek-ai/dsh-self-model
 */

import type { Context } from '@deepseek-ai/cordis'
import type { Branded } from '@deepseek-ai/dsh-brand'
import { HarnessError } from '@deepseek-ai/dsh-llm'

// ─── Domain types ────────────────────────────────────────────────────────────

/** Identifies one self-model across its durable revisions. */
export type SelfModelId = Branded<'SelfModelId'>

/** Compare-and-set identity for one exact self-model revision. */
export interface SelfModelRef {
  readonly id: SelfModelId
  /** Positive revision; every durable mutation increments it. */
  readonly revision: number
}

/** Why this revision exists. Doubles as the AUTH tag. */
export type SelfModelCause =
  | 'narrative-summary'
  | 'action-outcome'
  | 'external-write'

/** Full durable state written by every non-clear self-model mutation. */
export interface SelfModelSnapshot extends SelfModelRef {
  /** Stable character. Analogous to V sitting outside L: changes rarely,
   *  and only through explicit edit, never through log drift. */
  readonly persona: string
  /** N: the story. Rewritten by summarization, never appended raw. */
  readonly narrative: string
  /** Durable, agent-asserted facts about own capabilities/limits/history. */
  readonly facts: Readonly<Record<string, string>>
}

/** Current projection, including derived bookkeeping. */
export interface SelfModelView extends SelfModelSnapshot {
  /** Epoch ms of the create mutation. */
  readonly createdAt: number
  /** Epoch ms of the latest mutation. */
  readonly updatedAt: number
  /** Cause of the current revision. */
  readonly lastCause: SelfModelCause
}

/** Fields changed by an update; at least one must be present. */
export interface UpdateSelfModelRequest {
  readonly persona?: string
  readonly narrative?: string
  /** Merge semantics: keys present here overwrite; others survive. */
  readonly facts?: Readonly<Record<string, string>>
  /** Keys to delete from facts. */
  readonly removeFacts?: readonly string[]
}

// ─── Fold ────────────────────────────────────────────────────────────────────

type Clear = { readonly cleared: SelfModelRef }
export type SelfModelEvent =
  | { readonly selfModel: SelfModelSnapshot; readonly cause: SelfModelCause }
  | Clear

function positiveInteger(value: unknown, label: string): number {
  if (!Number.isSafeInteger(value) || (value as number) < 1) {
    throw new Error(`${label} must be a positive safe integer`)
  }
  return value as number
}

/** Require one exact next revision of the current self-model (CAS fence). */
function expectNextRevision(
  next: SelfModelRef,
  current: SelfModelRef | undefined,
  operation: string,
): void {
  if (current === undefined) {
    if (next.revision !== 1) {
      throw new Error(`self-model ${operation} requires revision 1 when none exists`)
    }
    return
  }
  if (next.id !== current.id || next.revision !== current.revision + 1) {
    throw new Error(`self-model ${operation} must advance the current self-model by one revision`)
  }
}

/** Last-wins fold over the single-writer event stream. */
export function applySelfModelFold(
  current: SelfModelView | undefined,
  event: SelfModelEvent,
): SelfModelView | undefined {
  if ('cleared' in event) {
    expectNextRevision(event.cleared, current, 'clear')
    return undefined
  }
  const { selfModel: next, cause } = event
  expectNextRevision(next, current, `${cause} update`)
  if (!Number.isSafeInteger(current?.createdAt)) {
    return { ...next, createdAt: Date.now(), updatedAt: Date.now(), lastCause: cause }
  }
  return { ...next, createdAt: current!.createdAt, updatedAt: Date.now(), lastCause: cause }
}

// ─── Errors ──────────────────────────────────────────────────────────────────

export class SelfModelError extends HarnessError {
  constructor(message: string, code: string) {
    super(message, code)
    this.name = 'SelfModelError'
  }
}

// ─── Service ─────────────────────────────────────────────────────────────────

export const name = 'self-model'

export interface Config {
  /** Maximum characters tolerated in `narrative` before summarization is forced. */
  readonly maxNarrativeChars?: number
}

export const Config = {
  defaultMaxNarrativeChars: 8_000,
}

export class SelfModelService {
  private current: SelfModelView | undefined
  private readonly maxNarrativeChars: number

  constructor(maxNarrativeChars = Config.defaultMaxNarrativeChars) {
    this.maxNarrativeChars = maxNarrativeChars
  }

  /** Read the current self-model view, or `undefined` before first creation. */
  get(): SelfModelView | undefined {
    return this.current
  }

  /**
   * Create revision 1. Rejects when any current self-model exists that has
   * not been cleared.
   */
  create(input: {
    persona: string
    narrative: string
    facts?: Readonly<Record<string, string>>
  }): SelfModelView {
    if (this.current !== undefined) {
      throw new SelfModelError(
        `self-model "${this.current.id}" already exists at revision ${this.current.revision}`,
        'SELF_MODEL_ALREADY_EXISTS',
      )
    }
    const snapshot: SelfModelSnapshot = {
      id: `sm-${crypto.randomUUID()}` as SelfModelId,
      revision: 1,
      persona: input.persona,
      narrative: this.checkNarrative(input.narrative),
      facts: Object.freeze({ ...input.facts }),
    }
    return this.commit(snapshot, 'external-write')
  }

  /**
   * CAS update. The caller MUST pass the exact expected revision; mismatch
   * throws rather than racing. `cause` records the authority channel.
   */
  update(
    ref: SelfModelRef,
    request: UpdateSelfModelRequest & { readonly cause: SelfModelCause },
  ): SelfModelView {
    const cur = this.expectCurrent(ref)
    const { cause, ...fields } = request
    const hasAny =
      fields.persona !== undefined || fields.narrative !== undefined ||
      fields.facts !== undefined || fields.removeFacts !== undefined
    if (!hasAny) {
      throw new SelfModelError('self-model update requires at least one field', 'SELF_MODEL_EMPTY_UPDATE')
    }
    const facts: Record<string, string> = { ...cur.facts }
    if (fields.facts !== undefined) Object.assign(facts, fields.facts)
    if (fields.removeFacts !== undefined) {
      for (const key of fields.removeFacts) delete facts[key]
    }
    const next: SelfModelSnapshot = {
      id: cur.id,
      revision: cur.revision + 1,
      persona: fields.persona ?? cur.persona,
      narrative: fields.narrative !== undefined
        ? this.checkNarrative(fields.narrative)
        : cur.narrative,
      facts: Object.freeze(facts),
    }
    return this.commit(next, cause)
  }

  /** Tombstone clear. Keeps the CAS fence honest across recreations. */
  clear(ref: SelfModelRef): void {
    this.expectCurrent(ref)
    applySelfModelFold(this.current, { cleared: ref })
    this.current = undefined
  }

  private expectCurrent(ref: SelfModelRef): SelfModelView {
    if (this.current === undefined) {
      throw new SelfModelError('no self-model exists', 'SELF_MODEL_MISSING')
    }
    if (this.current.id !== ref.id || this.current.revision !== ref.revision) {
      throw new SelfModelError(
        `revision mismatch: expected ${ref.id}@${ref.revision}, `
          + `current is ${this.current.id}@${this.current.revision}`,
        'SELF_MODEL_REVISION_CONFLICT',
      )
    }
    return this.current
  }

  private checkNarrative(narrative: string): string {
    if (narrative.length > this.maxNarrativeChars) {
      throw new SelfModelError(
        `narrative exceeds ${this.maxNarrativeChars} chars; summarize instead of appending`,
        'SELF_MODEL_NARRATIVE_OVERFLOW',
      )
    }
    return narrative
  }

  private commit(snapshot: SelfModelSnapshot, cause: SelfModelCause): SelfModelView {
    const view = applySelfModelFold(this.current, { selfModel: snapshot, cause })
    // Fold returns fresh view; assign through the single-writer path.
    this.current = view
    return view!
  }
}

declare module '@deepseek-ai/cordis' {
  interface Context {
    selfModel: SelfModelService
  }
}

export const inject = []

export function apply(ctx: Context): void {
  ctx.selfModel = new SelfModelService()
}
