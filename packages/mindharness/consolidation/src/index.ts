// mindharness/consolidation — Offline: Light → REM → Counterfactual → Deep
// Port of tools/harness_core/consolidation.py + counterfactual.py
// Events: session/event, agent/turn-stopping

export interface MemoryItem {
  id: string;
  text: string;
  queryTypes: Set<string>;
  endorsed?: boolean;
  cause: string; // must be valid, or promotion BLOCKED
}

export class Consolidator {
  // Light — dedupe near-identical traces, merge signal into survivor
  light(items: MemoryItem[]): MemoryItem[] {
    const seen = new Map<string, MemoryItem>();
    for (const it of items) {
      const key = it.text.slice(0, 40).toLowerCase();
      if (!seen.has(key)) seen.set(key, it);
      else {
        const survivor = seen.get(key)!;
        for (const q of it.queryTypes) survivor.queryTypes.add(q);
      }
    }
    return [...seen.values()];
  }

  // REM — concept extraction, ablatable (dream deprivation)
  rem(items: MemoryItem[], ablate = false): MemoryItem[] {
    if (ablate) return [];
    return items.filter(it => it.text.length > 20).slice(0, 10);
  }

  // Counterfactual — variant → simulate → regret (tools/harness_core/counterfactual.py)
  counterfactual(item: MemoryItem, variantFn: (s:string)=>string, simulateFn: (s:string)=>number): {variant: string, regret: number} | null {
    const variant = variantFn(item.text);
    const imaginedScore = simulateFn(variant);
    const actualScore = simulateFn(item.text);
    const regret = imaginedScore - actualScore;
    return regret > 0.1 ? { variant, regret } : null;
  }

  // Deep — utility gate: ≥2 query types OR human endorsement, cause-tagged, untagged BLOCKED
  deep(candidates: MemoryItem[]): MemoryItem[] {
    return candidates.filter(it => {
      if (!it.cause) throw new Error('untagged promotion BLOCKED');
      return it.queryTypes.size >= 2 || !!it.endorsed;
    });
  }
}

export const consolidatorService = {
  id: 'ctx.consolidator',
  create: () => new Consolidator(),
};
