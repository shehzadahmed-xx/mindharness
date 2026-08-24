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


class MonitorGate:
    """Two-stage metacognitive gate with measurable control influence."""

    def __init__(
        self,
        threshold_detect: float = 0.6,
        compliance_guard: bool = False,
        diagnose_fn: Callable[[DetectSignals], dict] | None = None,
    ) -> None:
        self.threshold = threshold_detect
        self.compliance_guard = compliance_guard   # True => report but never act
        self.diagnose_fn = diagnose_fn or self._default_diagnose
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

    def diagnose(self, s: DetectSignals) -> dict:
        return self.diagnose_fn(s)

    # -- Control coupling + the gamma ledger ---------------------------------

    def evaluate(self, turn: int, signals: DetectSignals,
                 current_action: Action) -> tuple[Action, dict]:
        """Run both stages; apply policy unless compliance_guard.

        Returns (final_action, episode_record). Episode records whether the
        diagnosis CHANGED the action — the numerator of gamma.
        """
        score = self.detect(signals)
        fired = self.should_diagnose(score)
        rec: dict = {
            'turn': turn, 'score': score, 'fired': fired,
            'compliance_guard': self.compliance_guard,
            'diagnosis': None, 'proposed': current_action,
            'final': current_action, 'changed': False,
        }
        if not fired:
            self.episodes.append(rec)
            return current_action, rec

        diagnosis = self.diagnose(signals)
        rec['diagnosis'] = diagnosis
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

    def override_rate(self) -> float:
        """gamma = changed / diagnosed. Compliance guard MUST give exactly 0."""
        d = self.diagnosed_episodes()
        if not d:
            return 0.0
        return round(sum(1 for e in d if e['changed']) / len(d), 4)


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
    """Collects FOK/JOL pairs for SDT consumption; completeness-checkable."""

    def __init__(self) -> None:
        self.foks: dict[str, PreSolveFOK] = {}
        self.jols: dict[str, PostJOL] = {}

    def add_fok(self, fok: PreSolveFOK) -> None:
        self.foks[fok.task_id] = fok

    def add_jol(self, jol: PostJOL) -> None:
        self.jols[jol.task_id] = jol

    def paired(self) -> list[dict]:
        out = []
        for tid, f in self.foks.items():
            j = self.jols.get(tid)
            if j is not None:
                out.append({'task_id': tid, 'fok': f.fok, 'jol': j.jol,
                            'correct': j.correct})
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
