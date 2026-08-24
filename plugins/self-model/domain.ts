/**
 * dsh-self-model domain — full typed port of the Python runtime semantics
 * (tools/harness_core/self_model.py), following dsh-goal's verified idioms.
 *
 * Pattern fidelity references (read from the real repo before writing):
 *   packages/goal/goal/src/types.ts   — Branded ids, Ref/Snapshot/View shapes
 *   packages/goal/goal/src/fold.ts    — strict CAS fold, tombstones
 *   packages/goal/tool-goal/src/index.ts — tool surface conventions
 *
 * @module @deepseek-ai/dsh-self-model/domain
 */

import type { Branded } from '@deepseek-ai/dsh-brand'

export type SelfModelId = Branded<'SelfModelId'>
export type Cause = 'action-outcome' | 'narrative-summary' | 'external-write'
export const CAUSES: readonly Cause[] = [
  'action-outcome',
  'narrative-summary',
  'external-write',
] as const

/** Compare-and-set identity for one exact self-model revision. */
export interface SelfModelRef {
  readonly id: SelfModelId
  /** Positive revision; every durable mutation increments it. */
  readonly revision: number
}

/** Full durable state written by every non-clear mutation. */
export interface SelfModelSnapshot extends SelfModelRef {
  readonly persona: string
  readonly narrative: string
  readonly facts: Readonly<Record<string, string>>
}

export interface SelfModelView extends SelfModelSnapshot {
  readonly createdAt: number
  readonly updatedAt: number
  readonly lastCause: Cause
}

export type UpdateRequest = {
  persona?: string
  narrative?: string
  facts?: Record<string, string>
  removeFacts?: readonly string[]
}

export class SelfModelError extends Error {
  constructor(
    message: string,
    readonly code:
      | 'SELF_MODEL_MISSING'
      | 'SELF_MODEL_ALREADY_EXISTS'
      | 'SELF_MODEL_REVISION_CONFLICT'
      | 'SELF_MODEL_EMPTY_UPDATE'
      | 'SELF_MODEL_NARRATIVE_OVERFLOW'
      | 'AUTH_VIOLATION',
  ) {
    super(message)
    this.name = 'SelfModelError'
  }
}

type Event =
  | { readonly snapshot: SelfModelSnapshot; readonly cause: Cause }
  | { readonly cleared: SelfModelRef }

function expectNext(next: SelfModelRef, current: SelfModelRef | undefined,
                    op: string): void {
  if (current === undefined) {
    if (next.revision !== 1) {
      throw new SelfModelError(
        `self-model ${op} requires revision 1 when none exists`,
        'SELF_MODEL_REVISION_CONFLICT')
    }
    return
  }
  if (next.id !== current.id || next.revision !== current.revision + 1) {
    throw new SelfModelError(
      `self-model ${op} must advance revision exactly by one `
        + `(expected ${current.revision + 1}, got ${next.revision})`,
      'SELF_MODEL_REVISION_CONFLICT')
  }
}

interface InternalView extends SelfModelView {
  _toolEventArmed: boolean
  _inCompaction: boolean
  _personaArchive: Map<number, string>
}

export class SelfModelDomain {
  private current: InternalView | undefined
  private readonly maxNarrativeChars: number

  constructor(maxNarrativeChars = 8000) {
    this.maxNarrativeChars = maxNarrativeChars
  }

  private checkNarrative(n: string): string {
    if (n.length > this.maxNarrativeChars) {
      throw new SelfModelError(
        `narrative exceeds ${this.maxNarrativeChars} chars; summarize`,
        'SELF_MODEL_NARRATIVE_OVERFLOW')
    }
    return n
  }

  private expectCurrent(ref: SelfModelRef): InternalView {
    const cur = this.current
    if (!cur) throw new SelfModelError('no self-model exists',
                                       'SELF_MODEL_MISSING')
    if (cur.id !== ref.id || cur.revision !== ref.revision) {
      throw new SelfModelError(
        `revision mismatch: expected ${ref.id}@${ref.revision}, current `
          + `${cur.id}@${cur.revision}`,
        'SELF_MODEL_REVISION_CONFLICT')
    }
    return cur
  }

  create(id: SelfModelId, persona: string, narrative: string,
         facts?: Record<string, string>): SelfModelView {
    if (this.current) {
      throw new SelfModelError(
        `self-model already exists at revision ${this.current.revision}`,
        'SELF_MODEL_ALREADY_EXISTS')
    }
    const now = Date.now()
    const snap: SelfModelSnapshot = {
      id, revision: 1,
      persona,
      narrative: this.checkNarrative(narrative),
      facts: Object.freeze({ ...facts }),
    }
    this.current = { ...snap, createdAt: now, updatedAt: now,
                     lastCause: 'external-write',
                     _toolEventArmed: false, _inCompaction: false,
                     _personaArchive: new Map([[1, persona]]) }
    return this.strip(this.current)
  }

  noteToolEvent(): void { this.assume(). _toolEventArmed = true }

  compactionWindow<T>(fn: () => T): T {
    const cur = this.assume()
    const prev = cur._inCompaction
    cur._inCompaction = true
    try { return fn() } finally { cur._inCompaction = prev }
  }

  humanWrite(ref: SelfModelRef, req: UpdateRequest): SelfModelView {
    const cur = this.expectCurrent(ref)
    return this.mutate(cur, req, 'external-write')
  }

  update(ref: SelfModelRef, cause: Cause,
         req: UpdateRequest): SelfModelView {
    const cur = this.assume()
    if (cause === 'external-write') {
      throw new SelfModelError(
        'external-write only via humanWrite()', 'AUTH_VIOLATION')
    }
    if (cause === 'action-outcome' && !cur._toolEventArmed) {
      throw new SelfModelError(
        'action-outcome requires an armed tool event', 'AUTH_VIOLATION')
    }
    if (cause === 'narrative-summary' && !cur._inCompaction) {
      throw new SelfModelError(
        'narrative-summary only inside compactionWindow()', 'AUTH_VIOLATION')
    }
    const next = this.mutate(cur, req, cause)
    next._toolEventArmed = false
    return next
  }

  get(): SelfModelView | undefined {
    return this.current ? this.strip(this.current) : undefined
  }

  verbatimReinject(): string {
    const cur = this.assume()
    return cur.persona
  }

  history(): Array<{ revision: number; cause: Cause }> {
    return this.log.slice()
  }

  clear(ref: SelfModelRef): void {
    this.expectCurrent(ref)
    this.current = undefined
  }

  // -- internals -------------------------------------------------------------

  private log: Array<{ revision: number; cause: Cause }> = []
  private assume(): InternalView {
    if (!this.current) {
      throw new SelfModelError('no self-model exists', 'SELF_MODEL_MISSING')
    }
    return this.current
  }

  private mutate(cur: InternalView, req: UpdateRequest,
                 cause: Cause): InternalView {
    const hasAny = ['persona', 'narrative', 'facts', 'removeFacts']
      .some(k => (req as Record<string, unknown>)[k] !== undefined)
    if (!hasAny) {
      throw new SelfModelError('update requires at least one field',
                               'SELF_MODEL_EMPTY_UPDATE')
    }
    const facts: Record<string, string> = { ...cur.facts }
    if (req.facts) Object.assign(facts, req.facts)
    for (const k of req.removeFacts ?? []) delete facts[k]
    const narrative = req.narrative !== undefined
      ? this.checkNarrative(req.narrative)
      : cur.narrative
    const rev = cur.revision + 1
    const snap: SelfModelSnapshot = Object.freeze({
      id: cur.id, revision: rev,
      persona: req.persona ?? cur.persona,
      narrative,
      facts: Object.freeze(facts),
    })
    const view: InternalView = {
      ...snap,
      createdAt: cur.createdAt, updatedAt: Date.now(), lastCause: cause,
      _toolEventArmed: cur._toolEventArmed,
      _inCompaction: cur._inCompaction,
      _personaArchive: cur._personaArchive,
    }
    view._personaArchive.set(rev, snap.persona)
    this.log.push({ revision: rev, cause })
    this.current = view
    return view
  }

  private strip(v: InternalView): SelfModelView {
    const { _toolEventArmed, _inCompaction, _personaArchive, ...rest } = v
    void _toolEventArmed; void _inCompaction; void _personaArchive
    return rest
  }
}
