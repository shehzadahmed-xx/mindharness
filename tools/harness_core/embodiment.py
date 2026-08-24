"""EmbodiedState middleware (Phase 4.1).

Energy/fatigue as first-class state; affordance gating removes strategies from
the proposal SET entirely (pre-conscious filter per Merleau-Ponty layer).

AC-4.1a  energy<0.35 removes attend_sustained from returned dict ENTIRELY
AC-4.1b  rest() restores affordances; energy clamped >= 0.15
"""

from __future__ import annotations

import math


class EmbodiedState:
    ENERGY_FLOOR = 0.15

    def __init__(self, energy: float = 1.0, fatigue: float = 0.0,
                 k_energy_per_log_token: float = 0.02) -> None:
        self.energy = energy
        self.fatigue = fatigue
        self.k = k_energy_per_log_token

    # -- drives ---------------------------------------------------------------

    def consume_tokens(self, n: int) -> None:
        if n <= 0:
            return
        self.energy = max(self.ENERGY_FLOOR,
                          self.energy - self.k * math.log(1 + n))
        self.fatigue = min(1.0, self.fatigue + 0.01 * math.log(1 + n))

    def register_failure(self) -> None:
        self.fatigue = min(1.0, self.fatigue + 0.05)

    def rest(self, minutes: float) -> None:
        frac = minutes / 30.0
        self.energy = min(1.0, self.energy + 0.1 * frac)
        self.fatigue = max(0.0, self.fatigue - 0.15 * frac)

    # -- pre-conscious affordance filter ---------------------------------------
    # GATING SEMANTICS: unavailable strategies are ABSENT from the dict — they
    # never appear as options rather than appearing and being rejected.

    def affordance_space(self) -> dict[str, bool]:
        space: dict[str, bool] = {}
        space['communicate'] = True                       # body-independent
        if self.fatigue < 0.8:
            space['navigate'] = True
        if self.energy >= 0.35 and self.fatigue <= 0.6:
            space['attend_sustained'] = True
        if self.energy >= 0.45:
            space['create'] = True
        if self.fatigue < 0.9:
            space['reach'] = True
        return space

    def phenomenal_field_size(self) -> float:
        base = self.energy * (1 - 0.4 * self.fatigue)
        return max(0.1, round(base, 4))

    def strain(self) -> float:
        """Composite 0..1 feed for the monitor's Stage-1 detector."""
        return round(min(1.0, 0.6 * (1 - self.energy) + 0.4 * self.fatigue), 4)
