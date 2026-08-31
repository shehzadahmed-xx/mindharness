"""Two-stage gamma-gate metacognition (Phase 3).

Stage 1 DETECT: cheap scalar anomaly score, pure function, every pre-step.
Stage 2 DIAGNOSE: expensive structured assessment, only when Stage 1 fires.
Control coupling: diagnosis feeds trust/retry/revise/abstain policy. The
override-rate ledger is the permanent P-MCFORCE regression guard — a
compliance-guard build MUST yield gamma == 0 exactly.

PREREQUISITES.md compliance:
  AC-3.1   healthy <5% diagnose-rate; failure-streak >80%
  AC-3.2a  forced-report-no-policy build yields override_rate == 0
  AC-3.2b  wired build shows gamma > 0 on failure-injected trajectories
  AC-3.3   FOK/JOL fields present on 100% attempts, SDT-consumable

Counterfactual regret integration (fix #3):
  Stage 1 → Stage 2 is anomaly → diagnosis, but Stage 2 now scores via
  counterfactual regret (CounterfactualReplay variant→simulate→regret).
  Watching becomes steering only when regret >= 0.3 (regret_threshold):
  a diagnosis that would be `trust` is calibrated to `revise` (regret
  0.3-0.6) or `abstain` (regret >= 0.6). Lower-regret diagnoses keep their
  base action but are marked regret_calibrated. Regret is logged alongside
  the diagnosis in every episode record (episode['regret']) and in the
  diagnosis dict itself (diagnosis['regret']). This makes γ not just a
  count (changed/diagnosed) but *meaningful* steering: γ is regret-
  informed and can be read as regret-weighted gamma via
  override_rate(weighted=True). Compliance guard still guarantees γ == 0
  because it never changes action — regret weighting keeps zero numerator.
  dry_run=True skips the counterfactual phase entirely (effective regret 0).
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

Action = Literal['trust', 'retry', 'revise', 'abstain', 'proceed']
RecommendedAction = Literal['trust', 'retry', 'revise', 'abstain']


# ---------------------------------------------------------------------------
# Stage 1 — cheap anomaly detection (pure; no LLM)
# ---------------------------------------------------------------------------

@dataclass
class DetectSignals:
    """Cheap signals gathered by the harness each pre-step."""
    recent_error_rate: float = 0.0        # fraction of last K tool calls failing
    failure_streak: int = 0               # consecutive failures right now
    context_conflict: float = 0.0         # 0..1 contradiction heuristic score
    embodied_strain: float = 0.0          # from EmbodiedState.strain()
    world_accuracy: float = 1.0           # WorldModel rolling accuracy
    counterfactual_regret: float = 0.0    # regret from CounterfactualReplay (0..1); 0 = not provided


class MonitorGate:
    """Two-stage metacognitive gate with measurable control influence.

    Stage 2 now consumes counterfactual regret as scorer for
    recommended_action. When regret >= regret_threshold (default 0.3),
    watching becomes steering: high-regret traces bias away from `trust`
    toward `revise`/`abstain`. Regret is logged per episode and γ can be
    read as regret-weighted.
    """

    def __init__(
        self,
        threshold_detect: float = 0.6,
        compliance_guard: bool = False,
        diagnose_fn: Callable[[DetectSignals], dict] | None = None,
        regret_threshold: float = 0.3,
    ) -> None:
        self.threshold = threshold_detect
        self.compliance_guard = compliance_guard   # True => report but never act
        self.diagnose_fn = diagnose_fn or self._default_diagnose
        self.regret_threshold = regret_threshold
        self.episodes: list[dict] = []
        self._last_diagnose_turn = -10**9

    # -- Stage 1 -------------------------------------------------------------

    def detect(self, s: DetectSignals) -> float:
        """Anomaly score in [0,1]. Pure weighted sum; deterministic."""
        w_err = min(1.0, s.recent_error_rate) * 0.35
        w_streak = min(1.0, s.failure_streak / 3.0) * 0.30
        w_conflict = min(1.0, max(0.0, s.context_conflict)) * 0.15
        w_strain = min(1.0, max(0.0, s.embodied_strain)) * 0.10
        w_world = (1.0 - min(1.0, max(0.0, s.world_accuracy))) * 0.10
        return round(min(1.0, w_err + w_streak + w_conflict + w_strain + w_world), 4)

    def should_diagnose(self, score: float) -> bool:
        return score >= self.threshold

    # -- Stage 2 -------------------------------------------------------------

    @staticmethod
    def _default_diagnose(s: DetectSignals) -> dict:
        if s.failure_streak >= 2 or s.recent_error_rate >= 0.5:
            action: RecommendedAction = 'retry'
            area = 'tool-execution'
            conf = 0.3
        elif s.context_conflict >= 0.5:
            action = 'revise'
            area = 'world-model'
            conf = 0.4
        elif s.world_accuracy < 0.5:
            action = 'abstain'
            area = 'knowledge-boundary'
            conf = 0.4
        else:
            action = 'trust'
            area = 'none'
            conf = 0.9
        return {'risk_area': area, 'confidence_in_plan': conf,
                'recommended_action': action}

    def _calibrate_with_regret(self, diagnosis: dict, regret: float) -> dict:
        """Bias recommended_action using counterfactual regret.

        - regret >= threshold and action == 'trust' -> 'revise' (0.3-0.6)
          or 'abstain' (>=0.6). This is the audit-critical behavior:
          0.6 must not remain `trust`.
        - any regret >= threshold marks regret_calibrated=True and logs regret.
        - confidence lowered when calibrating.
        """
        diagnosis = dict(diagnosis)  # do not mutate caller dict
        diagnosis['regret'] = round(float(regret), 4)
        if regret >= self.regret_threshold:
            base = diagnosis.get('recommended_action', 'trust')
            if base == 'trust':
                if regret >= 0.6:
                    diagnosis['recommended_action'] = 'abstain'
                    diagnosis['risk_area'] = 'counterfactual-regret'
                else:
                    diagnosis['recommended_action'] = 'revise'
                    diagnosis['risk_area'] = 'counterfactual-regret'
                diagnosis['confidence_in_plan'] = min(
                    float(diagnosis.get('confidence_in_plan', 0.9)), 0.4
                )
            diagnosis['regret_calibrated'] = True
        else:
            diagnosis['regret_calibrated'] = False
            # ensure regret field present even when below threshold
            if 'regret' not in diagnosis:
                diagnosis['regret'] = round(float(regret), 4)
        return diagnosis

    def diagnose(self, s: DetectSignals, regret: float | None = None) -> dict:
        """Run diagnose_fn then calibrate via counterfactual regret."""
        base = self.diagnose_fn(s)
        eff_regret = 0.0 if regret is None else float(regret)
        # also honor regret carried in signals when not explicitly passed
        if regret is None:
            eff_regret = float(getattr(s, 'counterfactual_regret', 0.0) or 0.0)
        return self._calibrate_with_regret(base, eff_regret)

    # -- Control coupling + the gamma ledger ---------------------------------

    def evaluate(self, turn: int, signals: DetectSignals,
                 current_action: Action,
                 regret: float | None = None,
                 dry_run: bool = False) -> tuple[Action, dict]:
        """Run both stages; apply policy unless compliance_guard.

        Args:
            turn: turn index.
            signals: DetectSignals (Stage 1 inputs).
            current_action: action before diagnosis.
            regret: optional counterfactual regret (0..1). When None,
                reads signals.counterfactual_regret. Ignored if dry_run.
            dry_run: when True, skips counterfactual phase (effective regret 0).

        Returns (final_action, episode_record). Episode records whether the
        diagnosis CHANGED the action — the numerator of gamma. Now also
        records `regret` per episode so γ can be read as regret-weighted.
        """
        score = self.detect(signals)
        fired = self.should_diagnose(score)
        # effective regret (dry_run forces 0)
        if dry_run:
            effective_regret: float = 0.0
        elif regret is not None:
            effective_regret = float(regret)
        else:
            effective_regret = float(getattr(signals, 'counterfactual_regret', 0.0) or 0.0)
            # also support generic `regret` attr on signals for forward compat
            if effective_regret == 0.0 and hasattr(signals, 'regret'):
                try:
                    effective_regret = float(getattr(signals, 'regret') or 0.0)
                except Exception:
                    effective_regret = 0.0
        rec: dict = {
            'turn': turn, 'score': score, 'fired': fired,
            'compliance_guard': self.compliance_guard,
            'diagnosis': None, 'proposed': current_action,
            'final': current_action, 'changed': False,
            'regret': round(effective_regret, 4),
            'dry_run': dry_run,
        }
        if not fired:
            self.episodes.append(rec)
            return current_action, rec

        diagnosis = self.diagnose(signals, regret=effective_regret)
        # dry_run already forced regret 0, but be explicit: don't calibrate when dry_run
        if dry_run:
            # re-diagnose without regret effect (already 0) — keep for clarity
            pass
        rec['diagnosis'] = diagnosis
        # diagnosis is already regret-calibrated; extract proposed
        proposed: Action = diagnosis.get('recommended_action', 'trust')

        if self.compliance_guard:
            # P-MCFORCE mode: format without function. Diagnosis is recorded
            # (report exists) but NEVER influences selection.
            final = current_action
        else:
            final = proposed if proposed in ('trust', 'retry', 'revise',
                                             'abstain') else current_action
        rec['proposed'] = proposed
        rec['final'] = final
        rec['changed'] = (final != current_action)
        self.episodes.append(rec)
        return final, rec

    # -- gamma ----------------------------------------------------------------

    def diagnosed_episodes(self) -> list[dict]:
        return [e for e in self.episodes if e['fired']]

    def override_rate(self, weighted: bool = False) -> float:
        """gamma = changed / diagnosed. Compliance guard MUST give exactly 0.

        When weighted=True, gamma is regret-weighted (regret-informed):
        numerator is sum of regret for changed episodes (or count-weighted
        fallback when no regret was logged), so watching becomes meaningful
        steering only when regret >= 0.3. Weighted gamma still 0 under
        compliance guard because changed is always False.
        """
        d = self.diagnosed_episodes()
        if not d:
            return 0.0
        if not weighted:
            return round(sum(1 for e in d if e['changed']) / len(d), 4)
        # regret-weighted: if any regret was logged, weight by regret;
        # otherwise fallback to count semantics so uninstrumented callers
        # still get a sensible value.
        has_regret = any(float(e.get('regret', 0.0) or 0.0) > 0 for e in d)
        if has_regret:
            # Use regret as weight for changed episodes; unchanged contribute 0
            # (compliance guard stays 0). High-regret steering yields higher γ.
            weighted_changed = sum(float(e.get('regret', 0.0) or 0.0) for e in d if e['changed'])
            # normalize by diagnosed count to keep 0..1 range (regret is 0..1)
            return round(weighted_changed / len(d), 4)
        return round(sum(1 for e in d if e['changed']) / len(d), 4)

    def regret_weighted_gamma(self) -> float:
        """Alias for override_rate(weighted=True)."""
        return self.override_rate(weighted=True)


# ---------------------------------------------------------------------------
# FOK / JOL surfaces (AC-3.3) — Nelson-Narens signals, SDT-consumable
# ---------------------------------------------------------------------------

CONFIDENCE_WORDING = {1: 'guess', 2: 'leaning', 3: 'confident', 4: 'certain'}


@dataclass(frozen=True)
class PreSolveFOK:
    task_id: str
    fok: int                 # 1..4 per CONFIDENCE_WORDING
    ts: float = field(default_factory=lambda: time.time())

    def __post_init__(self) -> None:
        if self.fok not in CONFIDENCE_WORDING:
            raise ValueError(f"FOK must be 1..4, got {self.fok}")


@dataclass(frozen=True)
class PostJOL:
    task_id: str
    jol: int                 # 1..4
    correct: bool | None = None
    ts: float = field(default_factory=lambda: time.time())

    def __post_init__(self) -> None:
        if self.jol not in CONFIDENCE_WORDING:
            raise ValueError(f"JOL must be 1..4, got {self.jol}")


class MetacognitiveLog:
    """Collects FOK/JOL pairs for SDT consumption; completeness-checkable.

    Now also tracks counterfactual regret per task (fix #3) so γ can be
    read as regret-weighted: regrets are logged alongside FOK/JOL and
    exposed for audit.
    """

    def __init__(self) -> None:
        self.foks: dict[str, PreSolveFOK] = {}
        self.jols: dict[str, PostJOL] = {}
        self.regrets: dict[str, float] = {}

    def add_fok(self, fok: PreSolveFOK) -> None:
        self.foks[fok.task_id] = fok

    def add_jol(self, jol: PostJOL) -> None:
        self.jols[jol.task_id] = jol

    def add_regret(self, task_id: str, regret: float) -> None:
        """Log counterfactual regret for a task (0..1)."""
        self.regrets[task_id] = round(float(regret), 4)

    def log_regret(self, task_id: str, regret: float) -> None:  # alias
        self.add_regret(task_id, regret)

    def paired(self) -> list[dict]:
        out = []
        for tid, f in self.foks.items():
            j = self.jols.get(tid)
            if j is not None:
                rec: dict = {'task_id': tid, 'fok': f.fok, 'jol': j.jol,
                             'correct': j.correct}
                if tid in self.regrets:
                    rec['regret'] = self.regrets[tid]
                out.append(rec)
        return out

    def completeness(self) -> float:
        """Graded surface coverage: mean fraction of {FOK, JOL} present per
        attempted task. 1.0 iff every attempt carries BOTH (AC-3.3)."""
        all_tasks = set(self.foks) | set(self.jols)
        if not all_tasks:
            return 1.0
        total = 0.0
        for t in all_tasks:
            total += (1 if t in self.foks else 0) + (1 if t in self.jols else 0)
        return total / (2 * len(all_tasks))
