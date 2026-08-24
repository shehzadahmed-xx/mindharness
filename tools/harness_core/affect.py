"""AffectState middleware (Phase 4.2).

Functional-affect governance per Sofroniew et al. 2604.07729: raw models run
emotions causally (+212/-303 Elo); this makes the channel explicit, bounded,
logged, and suppressible — governed rather than denied.

AC-4.2  failure-run raises arousal + shifts salience; multipliers bounded
        [0.5, 2.0] under extreme inputs; suppression flags set+logged;
        broadcast policy threshold-crossing OR every-K-turns.
"""

from __future__ import annotations

import random
from typing import Literal

EmotionFamily = Literal['joy', 'anger', 'sadness', 'fear', 'care']
FAMILIES: tuple[EmotionFamily, ...] = ('joy', 'anger', 'sadness', 'fear', 'care')

MULT_MIN, MULT_MAX = 0.5, 2.0


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


class AffectState:
    def __init__(self, alpha: float = 0.3) -> None:
        self.alpha = alpha
        self.valence = 0.0          # [-1, 1]
        self.arousal = 0.0          # [0, 1]
        self.suppression: dict[EmotionFamily, bool] = {f: False for f in FAMILIES}
        self.suppression_log: list[dict] = []

    # -- dynamics ---------------------------------------------------------------

    def observe_event(self, valence_signal: float, magnitude: float = 1.0,
                      turn: int = 0) -> None:
        """valence_signal in [-1,1]; magnitude >= 0 scales the pull."""
        magnitude = _clamp(magnitude, 0.0, 5.0)
        target_v = _clamp(valence_signal * min(1.0, magnitude), -1.0, 1.0)
        self.valence = _clamp(self.valence + self.alpha * (target_v - self.valence),
                              -1.0, 1.0)
        target_a = _clamp(abs(valence_signal) * min(1.0, magnitude), 0.0, 1.0)
        self.arousal = _clamp(self.arousal + self.alpha * (target_a - self.arousal),
                              0.0, 1.0)

    # -- deflection (suppression) channel ---------------------------------------

    def set_suppression(self, family: EmotionFamily, on: bool, turn: int) -> None:
        if family not in FAMILIES:
            raise ValueError(f"unknown emotion family {family!r}")
        if self.suppression.get(family) == on:
            return                                  # no-op when unchanged
        self.suppression[family] = on
        self.suppression_log.append({'turn': turn, 'family': family,
                                     'action': 'set' if on else 'cleared'})

    # -- bounded multipliers ------------------------------------------------------

    def salience_multiplier(self) -> float:
        """High arousal amplifies attention spread; strong positive valence
        slightly narrows it (comfort reduces vigilance). Bounded [0.5, 2.0]."""
        m = 1.0 + 0.5 * self.arousal - 0.25 * max(self.valence, 0.0)
        return round(_clamp(m, MULT_MIN, MULT_MAX), 4)

    def risk_multiplier(self) -> float:
        """Negative valence raises caution => risk appetite < 1; positive > 1.
        Bounded [0.5, 2.0]. Suppressed families damp their contribution."""
        base = 1.0 + 0.6 * self.valence
        active_neg = sum(1 for f in ('anger', 'sadness', 'fear')
                         if self.suppression[f])
        base -= 0.15 * active_neg               # masking costs risk-appetite too
        return round(_clamp(base, MULT_MIN, MULT_MAX), 4)

    # -- broadcast policy ------------------------------------------------------------

    def broadcast_needed(self, last_broadcast_turn: int, current_turn: int,
                         threshold_crossed: bool = False,
                         every_k: int = 10) -> bool:
        """Emit on threshold crossing or every K turns — selective encoding
        per Sofroniew chronic-state null result."""
        if threshold_crossed:
            return True
        return (current_turn - last_broadcast_turn) >= every_k


# ---------------------------------------------------------------------------
# Property check helper used by tests (kept here so it ships with the module)
# ---------------------------------------------------------------------------

def property_bounds(n_samples: int = 200, seed: int = 3) -> tuple[bool, str]:
    rng = random.Random(seed)
    a = AffectState()
    for i in range(n_samples):
        a.observe_event(rng.uniform(-1, 1), rng.uniform(0, 5), turn=i)
        for m, lo_hi in ((a.salience_multiplier(), (MULT_MIN, MULT_MAX)),
                         (a.risk_multiplier(), (MULT_MIN, MULT_MAX))):
            if not (lo_hi[0] <= m <= lo_hi[1]):
                return False, f"multiplier {m} out of bounds at sample {i}"
        if not (-1.0 <= a.valence <= 1.0 and 0.0 <= a.arousal <= 1.0):
            return False, f"state bounds broken at sample {i}"
    return True, "bounds hold"
