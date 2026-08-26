// mindharness/metacognition — L5 Metacognition: γ-gate + compliance guard
// Port of tools/harness_core/monitor.py
// Events: agent/pre-step (Stage1 cheap), agent/request (Stage2 if triggered)

export type Policy = 'TRUST' | 'RETRY' | 'REVISE' | 'ABSTAIN';

export interface GateResult {
  anomalyScore: number;
  diagnosed: boolean;
  policy: Policy;
}

export class MonitorGate {
  // Stage1: cheap, always on — pure function of error rate, streak, context conflict, embodied strain
  stage1(errorRate: number, streak: number, strain: number): number {
    return Math.min(1, errorRate * 0.6 + Math.min(streak / 5, 1) * 0.3 + strain * 0.1);
  }
  // Stage2: expensive, triggered — structured diagnosis
  stage2(score: number): GateResult {
    const diagnosed = score > 0.5;
    let policy: Policy = 'TRUST';
    if (diagnosed) policy = score > 0.8 ? 'ABSTAIN' : score > 0.65 ? 'REVISE' : 'RETRY';
    return { anomalyScore: score, diagnosed, policy };
  }
  // γ = changed / diagnosed — does watching actually steer?
  gamma(changed: number, diagnosed: number): number {
    return diagnosed === 0 ? 0 : changed / diagnosed;
  }
}

// Compliance guard — reports but never steers (γ=0 permanently) — negative control proving inert monitoring
export class ComplianceGuard extends MonitorGate {
  override stage2(score: number): GateResult {
    const r = super.stage2(score);
    return { ...r, policy: 'TRUST' }; // never changes action
  }
  override gamma(): number { return 0; }
}

export const monitorService = {
  id: 'ctx.monitor',
  create: () => new MonitorGate(),
};

export const complianceGuardService = {
  id: 'ctx.monitor.compliance',
  create: () => new ComplianceGuard(),
};
