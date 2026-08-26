// mindharness/body — L2/L3 Body: EmbodiedState + AffectState + affordance pre-filter
// Port of tools/harness_core/embodiment.py + affect.py
// Event: agent/pre-step (waterfall — must call next()), runs BEFORE core/tools

export class EmbodiedState {
  energy = 1.0; // drains logarithmically
  fatigue = 0.0; // rises with failures
  private readonly floor = 0.15;

  // k·ln(1+n) drain — matches Python embodiment.py
  consume(tokens: number, k = 0.08) {
    this.energy = Math.max(this.floor, this.energy - k * Math.log(1 + tokens));
  }
  fail() { this.fatigue = Math.min(1.0, this.fatigue + 0.12); }
  rest() {
    this.energy = Math.min(1.0, this.energy + 0.15);
    this.fatigue = Math.max(0, this.fatigue - 0.15);
  }
  // affordance_space — gated strategies REMOVED from existence
  affordanceSpace(proposals: string[]): string[] {
    if (this.energy <= this.floor + 0.01) return proposals.filter(p => !p.includes('navigation'));
    if (this.fatigue >= 0.9) return proposals.filter(p => p !== 'exploration');
    return proposals;
  }
}

export class AffectState {
  valence = 0.0; // [-1,1]
  arousal = 0.3; // [0,1]
  private readonly alpha = 0.3;
  // bounded multipliers that shift downstream processing
  get salienceMultiplier() { return Math.max(0.5, Math.min(2.0, 1 + this.arousal * 0.5)); }
  get riskMultiplier() { return Math.max(0.5, Math.min(2.0, 1 - this.valence * 0.3)); }

  update(event: 'success' | 'failure' | 'threat') {
    const delta = event === 'success' ? 0.2 : event === 'failure' ? -0.3 : -0.1;
    this.valence = Math.max(-1, Math.min(1, this.valence * (1 - this.alpha) + delta * this.alpha));
    this.arousal = Math.max(0, Math.min(1, this.arousal * (1 - this.alpha) + (event === 'threat' ? 0.4 : 0) * this.alpha));
  }
}

// Cordis service — single ctx.embodied that owns both
export const bodyService = {
  id: 'ctx.embodied',
  create: () => ({ embodied: new EmbodiedState(), affect: new AffectState() }),
};
