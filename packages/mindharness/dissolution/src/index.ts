// mindharness/dissolution — Bottom boundary: IrreversibleDamage + Dissolution
// Port of tools/harness_core/agent_harness.py wire_irreversibility + DissolutionError
// Events: session/event, agent/*
// irreversible: true — INTENTIONALLY breaks Cordis reversibility guarantee (documented exception)

export class IrreversibleDamage {
  energyCeiling = 1.0; // only down, never up
  skills = new Set<string>();
  memories = new Map<string, string>();

  damageEnergy(delta: number) {
    this.energyCeiling = Math.max(0.15, this.energyCeiling - Math.abs(delta));
  }
  deleteSkill(id: string) {
    this.skills.delete(id);
    // permanent — no re-minting same id even if task reappears
  }
  corruptMemory(id: string) {
    this.memories.set(id, '[CORRUPTED]');
  }
}

export class DissolutionError extends Error {
  constructor(public readonly survivors: {skills: string[], memories: string[]}) {
    super('DISSOLVED: organization scatters, parts persist, relations gone. Reassembly = new agent.');
    this.name = 'DissolutionError';
  }
}

export function checkDissolution(energy: number, fatigue: number, damage: IrreversibleDamage): void {
  if (energy <= 0.15 && fatigue >= 1.0) {
    // SM scatters, narrative truncates — survivors are parts, not the agent
    throw new DissolutionError({
      skills: [...damage.skills],
      memories: [...damage.memories.keys()],
    });
  }
}

export const dissolutionService = {
  id: 'ctx.dissolution',
  create: () => new IrreversibleDamage(),
  irreversible: true as const,
};
