// mindharness/provenance — L1 Witness
// Port of tools/harness_core/provenance.py — Cordis plugin for ctx.provenance
// Service: append-only Span binding + attribution audit + proposal queue
// Events: session/event (durable), agent/request (live)

export type ProvenanceSource = 'model_prior' | 'memory_lookup' | 'ledger_rule' | 'monitor_override' | 'external_tool';

export interface Span {
  start: number;
  end: number;
  source: ProvenanceSource;
  ref?: string;
  confidence?: number;
}

export interface BoundEmission {
  turnId: number;
  text: string;
  spans: Span[];
  meta?: Record<string, unknown>;
}

function isCovered(s: Span): boolean {
  return s.source !== 'memory_lookup' || !!s.ref;
}

export class ProvenanceLedger {
  private byTurn = new Map<number, BoundEmission[]>();

  bind(turnId: number, text: string, spans: Span[], meta: Record<string, unknown> = {}): BoundEmission {
    for (const s of spans) {
      if (!['model_prior','memory_lookup','ledger_rule','monitor_override','external_tool'].includes(s.source)) {
        throw new Error(`unknown provenance source ${s.source}`);
      }
    }
    const em: BoundEmission = { turnId, text, spans: [...spans], meta };
    const arr = this.byTurn.get(turnId) ?? [];
    arr.push(em);
    this.byTurn.set(turnId, arr);
    return em;
  }

  allEmissions(): BoundEmission[] {
    return [...this.byTurn.values()].flat();
  }

  // attribution_audit — S126 protocol: claimed vs recorded
  attributionAudit(claims: Array<{claimSource: string, recordedSource: string}>): {accuracy: number} {
    if (!claims.length) return {accuracy: 0};
    const correct = claims.filter(c => c.claimSource === c.recordedSource).length;
    return {accuracy: correct / claims.length};
  }

  coverage(): {covered: number, total: number} {
    const all = this.allEmissions().flatMap(e => e.spans);
    return { covered: all.filter(isCovered).length, total: all.length };
  }
}

// Cordis service definition
export const provenanceService = {
  id: 'ctx.provenance',
  create: () => new ProvenanceLedger(),
};
