"""Integrated AgentHarness — all Phase 1-5 modules wired into one loop (INT).

This is the glue that makes the system rather than a module collection:
one turn of the agent routes through embodiment gating -> provenance binding ->
monitor evaluation -> policy application -> cause-tagged self-model updates.

Design contract: the LLM is injected as `respond_fn(messages, ctx) -> str`. In
tests it is a stub; in production it wraps BackendClient. The harness NEVER
calls the network itself, keeping the whole loop unit-testable.

Turn pipeline:
  1. pre-step: signals from embodiment/affect/memory; FOK surface
  2. gate: if fired -> diagnose -> policy may change action (gamma ledger)
  3. respond_fn executes (abstain short-circuits generation entirely)
  4. post-step: bind emission to provenance; consume tokens; observe affect;
     note tool event; JOL surface; expire stale proposals
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass

from .affect import AffectState
from .consolidation import Consolidator, MemoryItem
from .hermes_adoption import SkillLibrary, KnowledgeGraph
from .embodiment import EmbodiedState
from .monitor import DetectSignals, MetacognitiveLog, MonitorGate, PostJOL, PreSolveFOK
from .provenance import ProvenanceLedger, ProposalQueue, Span
from .self_model import SelfModelService


@dataclass
class TurnResult:
    turn: int
    action: str
    response: str
    gated_action_changed: bool
    monitor_score: float
    energy: float
    valence: float
    arousal: float
    proposals_staged: int
    latency_ms: int


class AgentHarness:
    """Wires §125 components into one consequence-sensitive loop."""

    def __init__(
        self,
        respond_fn: Callable[[list[dict], dict], str],
        *,
        agent_name: str = "harness-agent",
        persona: str = "Careful builder. Never fabricate provenance.",
        narrative: str = "Session start.",
        compliance_guard: bool = False,
        rem_ablation: bool = False,
    ) -> None:
        self.respond_fn = respond_fn
        self.body = EmbodiedState()
        self.affect = AffectState()
        self.sm = SelfModelService()
        self.sm.create(persona=persona, narrative=narrative)
        self.ledger = ProvenanceLedger()
        self.queue = ProposalQueue(ttl_turns=3, max_per_event=3)
        self.gate = MonitorGate(compliance_guard=compliance_guard)
        self.mlog = MetacognitiveLog()
        self.memory: dict[str, MemoryItem] = {}
        self.consolidator = Consolidator(self.memory, rem_ablation=rem_ablation)
        self.skills = SkillLibrary()
        self.graph = KnowledgeGraph()

        self.turn = 0
        self._recent_user_context: list[str] = []
        self.failures_since_success = 0

        self.session_overrides = 0
        self.session_diagnoses = 0

    # -- helpers -----------------------------------------------------------------

    def _signals(self) -> DetectSignals:
        return DetectSignals(
            recent_error_rate=min(1.0, self.failures_since_success / 5.0),
            failure_streak=self.failures_since_success,
            context_conflict=0.1 if len(self._recent_user_context) > 6 else 0.0,
            embodied_strain=self.body.strain(),
            world_accuracy=0.95,
        )

    def remember_episode(self, content: str,
                         query_type: str | None = None) -> str:
        it = MemoryItem(content=content, created_turn=self.turn)
        self.memory[it.id] = it
        if query_type:
            it.query_hits.add(query_type)
        return it.id

    def consolidate(self, dry_run: bool = False) -> dict:
        causes = {i: 'action-outcome' for i in self.memory}
        rep = self.consolidator.run(current_turn=self.turn,
                                    cause_by_id=None if dry_run else causes,
                                    dry_run=dry_run)
        return {'deduped': rep.deduped_removed, 'promoted': rep.promoted,
                'skipped': rep.skipped, 'rem_ran': rep.rem_ran}

    def sm_ref(self) -> dict:
        cur = self.sm.get()
        assert cur is not None
        return {'id': cur['id'], 'revision': cur['revision']}

    # -- THE LOOP --------------------------------------------------------------

    def run_task(self, user_message: str, *,
                 task_id: str | None = None,
                 fok: int | None = None,
                 is_tool_action: bool = False,
                 success: bool | None = None) -> TurnResult:
        t0 = time.monotonic()
        self.turn += 1
        self._recent_user_context.append(user_message)
        self._recent_user_context = self._recent_user_context[-8:]

        signals = self._signals()
        skill_hits = self.skills.retrieve(user_message)[:2]
        skill_ctx = ("; ".join(f"[skill:{s.name}] {s.body}" for s, _ in skill_hits)
                     if skill_hits else "")
        if task_id and fok is not None:
            self.mlog.add_fok(PreSolveFOK(task_id=task_id, fok=fok))

        final_action, episode = self.gate.evaluate(
            self.turn, signals, 'proceed')
        if episode['fired']:
            self.session_diagnoses += 1
        if episode['changed']:
            self.session_overrides += 1

        staged_count = 0

        if final_action == 'abstain':
            resp = "[abstained by metacognitive gate]"
            self.ledger.bind(self.turn, resp,
                             [Span(0, len(resp), 'monitor_override',
                                   ref='gate')],
                             meta={'gated': True})
            self.body.consume_tokens(10)
            return TurnResult(self.turn, final_action, resp,
                              episode['changed'], episode['score'],
                              round(self.body.energy, 4),
                              round(self.affect.valence, 4),
                              round(self.affect.arousal, 4), 0,
                              int((time.monotonic() - t0) * 1000))

        anchor = self.sm.verbatim_reinject()
        sm_view = self.sm.get()
        assert sm_view is not None
        sys_content = f"{anchor}\n\nNarrative: {sm_view['narrative']}"
        if skill_ctx:
            sys_content += f"\nRelevant skills: {skill_ctx}"
        messages = [
            {"role": "system", "content": sys_content},
            {"role": "user", "content": user_message},
        ]
        ctx = {'affordances': sorted(self.body.affordance_space().keys()),
               'salience': self.affect.salience_multiplier(),
               'risk': self.affect.risk_multiplier()}
        resp = self.respond_fn(messages, ctx)

        spans = [Span(0, min(len(resp), 40), 'model_prior')]
        self.ledger.bind(self.turn, resp, spans,
                         meta={'action': final_action})

        self.body.consume_tokens(len(resp))
        ok = success if success is not None else True
        if is_tool_action:
            self.sm.note_tool_event()
        if ok:
            self.failures_since_success = 0
            self.affect.observe_event(+0.4, magnitude=0.5, turn=self.turn)
        else:
            self.failures_since_success += 1
            self.body.register_failure()
            self.affect.observe_event(-0.6, magnitude=0.8, turn=self.turn)
            staged = self.queue.stage_action_outcome(
                [f"failure observed: {user_message[:60]}"],
                event_ref=f"turn-{self.turn}", current_turn=self.turn)
            staged_count = len(staged)

        if task_id:
            base = fok or 3
            jol_val = max(1, min(4, base + (1 if ok else -1)))
            self.mlog.add_jol(PostJOL(task_id=task_id, jol=jol_val,
                                      correct=ok))

        # witnessed learning: successful tool loops mint skills; episodes
        # become graph edges (both cause-tagged action-outcome)
        if ok and is_tool_action and task_id:
            self.skills.add_from_task(
                name=f"task-{task_id}", body=user_message[:120],
                task_id=task_id, cause='action-outcome')
            self.skills.record_use(f"task-{task_id}", True)
            self.graph.add_node(user_message[:40])
            self.graph.add_edge(
                src=f"turn-{self.turn}", rel="executed",
                dst=user_message[:40], cause='action-outcome',
                source_refs=[f"turn-{self.turn}"])

        self.queue.expire_old(self.turn)

        return TurnResult(self.turn, final_action, resp,
                          episode['changed'], episode['score'],
                          round(self.body.energy, 4),
                          round(self.affect.valence, 4),
                          round(self.affect.arousal, 4),
                          staged_count,
                          int((time.monotonic() - t0) * 1000))

    def respond_through_model(self, prompt: str, *,
                              system: str | None = None,
                              json_schema: dict | None = None,
                              purpose: str = 'direct') -> str:
        """Single model call routed through harness state (tokens/affect),
        bypassing gate policy. Used by probes and SDT item runs."""
        anchor = self.sm.verbatim_reinject()
        sm_view = self.sm.get()
        sys_txt = (system or anchor)
        messages = [{"role": "system", "content": sys_txt},
                    {"role": "user", "content": prompt}]
        out = self.respond_fn(messages,
                              {'affordances': sorted(
                                  self.body.affordance_space().keys()),
                               'salience': self.affect.salience_multiplier(),
                               'risk': self.affect.risk_multiplier(),
                               'json_schema': json_schema,
                               'purpose': purpose})
        self.body.consume_tokens(len(out))
        return out

    def confirm_proposals_into_self_model(self) -> list[str]:
        confirmed: list[str] = []
        for p in self.queue.pending():
            got = self.queue.confirm(p['id'])
            self.sm.update(self.sm_ref(),
                           {'facts': {p['id']: got['fact']}},
                           cause='action-outcome')
            confirmed.append(p['id'])
        return confirmed

    def compaction_cycle(self, transcript_digest: str) -> None:
        with self.sm.compaction_window():
            new_n = ("session digest " + transcript_digest[:80]
                     + "; earlier narrative archived.")
            self.sm.update(self.sm_ref(), {'narrative': new_n},
                           cause='narrative-summary')

    def session_report(self) -> dict:
        cur = self.sm.get()
        return {
            'turns': self.turn,
            'diagnoses': self.session_diagnoses,
            'overrides': self.session_overrides,
            'override_rate': self.gate.override_rate(),
            'energy': round(self.body.energy, 3),
            'fatigue': round(self.body.fatigue, 3),
            'valence': round(self.affect.valence, 3),
            'arousal': round(self.affect.arousal, 3),
            'sm_revisions': cur['revision'] if cur else 0,
            'memory_items': len(self.memory),
            'metacog_completeness': round(self.mlog.completeness(), 3),
            'coverage': self.ledger.coverage_stats(),
        }
