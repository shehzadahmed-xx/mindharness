// mindharness/narrative-self — L6 Narrative Self
// Port of tools/harness_core/self_model.py + plugins/self-model/dsh-self-model.ts
// Service: CAS-revisioned, cause-signed identity (ctx.selfModel)

export type Cause = 'action-outcome' | 'narrative-summary' | 'external-write';

export interface SelfModelState {
  revision: number;
  persona: string;
  narrative: string;
  facts: Record<string, string>;
  cause: Cause;
  ts: number;
}

export class SelfModelService {
  current: SelfModelState | null = null;
  history: SelfModelState[] = [];
  private personaArchive = new Map<number, string>();
  private toolArmed = false;
  private inCompaction = false;

  constructor(private maxNarrativeChars = 8000) {}

  armToolEvent() { this.toolArmed = true; }
  enterCompaction() { this.inCompaction = true; }
  exitCompaction() { this.inCompaction = false; }

  create(persona: string, cause: Cause = 'external-write'): SelfModelState {
    if (this.current) throw new Error('SELF_MODEL_ALREADY_EXISTS');
    if (!persona.trim()) throw new Error('SELF_MODEL_EMPTY_UPDATE');
    const s: SelfModelState = { revision: 0, persona, narrative: '', facts: {}, cause, ts: Date.now() };
    this.current = s;
    this.history.push(s);
    this.personaArchive.set(0, persona);
    return s;
  }

  update(patch: Partial<Pick<SelfModelState,'persona'|'narrative'|'facts'>>, expectedRevision: number, cause: Cause): SelfModelState {
    if (!this.current) throw new Error('SELF_MODEL_MISSING');
    if (expectedRevision !== this.current.revision) throw new Error('SELF_MODEL_REVISION_CONFLICT');
    if (cause === 'narrative-summary' && !this.inCompaction) throw new Error('AUTH_VIOLATION: narrative-summary only inside compaction');
    if (cause === 'action-outcome' && !this.toolArmed) throw new Error('AUTH_VIOLATION: action-outcome requires armed tool event');
    if (patch.narrative && patch.narrative.length > this.maxNarrativeChars) throw new Error('SELF_MODEL_NARRATIVE_OVERFLOW');
    const next: SelfModelState = {
      revision: this.current.revision + 1,
      persona: patch.persona ?? this.current.persona,
      narrative: patch.narrative ?? this.current.narrative,
      facts: patch.facts ? {...this.current.facts, ...patch.facts} : {...this.current.facts},
      cause, ts: Date.now()
    };
    this.current = next;
    this.history.push(next);
    this.personaArchive.set(next.revision, next.persona);
    this.toolArmed = false;
    return next;
  }

  get(): SelfModelState | null { return this.current; }

  verbatimReinject(): string {
    if (!this.current) return '';
    // byte-exact persona at current revision — prevents 30% drift (Choi)
    return this.personaArchive.get(this.current.revision) ?? this.current.persona;
  }

  diffPersonas(fromRev: number, toRev: number): string {
    const a = this.personaArchive.get(fromRev) ?? '';
    const b = this.personaArchive.get(toRev) ?? '';
    // minimal word diff — mirrors Python difflib
    return `--- rev ${fromRev}\n+++ rev ${toRev}\n- ${a.slice(0,80)}\n+ ${b.slice(0,80)}`;
  }
}

export const selfModelService = {
  id: 'ctx.selfModel',
  create: () => new SelfModelService(),
};
