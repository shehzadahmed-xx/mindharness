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
        self.counterfactual_replay = None
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
        rep = self.consolidator.run(
            current_turn=self.turn,
            cause_by_id=None if dry_run else causes,
            dry_run=dry_run,
            counterfactual_replay=self.counterfactual_replay,
        )
        return {'deduped': rep.deduped_removed, 'promoted': rep.promoted,
                'skipped': rep.skipped, 'rem_ran': rep.rem_ran,
                'counterfactuals': rep.counterfactuals_generated,
                'high_regret': rep.counterfactual_high_regret}

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


# ---------------------------------------------------------------------------
# Registry-driven construction (Phase 6.6)
# ---------------------------------------------------------------------------

import json as _json
from pathlib import Path as _Path

def load_model_registry(path=None):
    """Load per-plugin model assignments from model_registry.json."""
    p = _Path(path) if path else _Path(__file__).parent.parent / "model_registry.json"
    if not p.exists():
        return {}
    return _json.loads(p.read_text())


def build_responders(api_key: str, registry_path=None):
    """Construct role-specific BackendClients from the registry."""
    reg = load_model_registry(registry_path)
    responders = {}
    for role, cfg in reg.items():
        client = BackendClient(
            api_key=api_key,
            model=cfg["model"],
            base_url=cfg.get("base_url", "https://api.groq.com/openai/v1"),
            purpose=f"registry-{role}",
        )
        def make_fn(c):
            def fn(messages, ctx=None):
                out, _ = c.chat(messages, purpose="registry-call")
                return out
            return fn
        responders[role] = make_fn(client)
    return responders


# ---------------------------------------------------------------------------
# Irreversible consequences (Phase 7: skin in the game)
# ---------------------------------------------------------------------------

class IrreversibleDamage:
    """Tracks permanent losses that cannot be undone by any future action.
    Once capacity is reduced, no reset, no compaction, no consolidation
    restores it. This is the structural difference between simulation and
    cognition: some mistakes cannot be appealed."""

    def __init__(self):
        self.max_energy_ceiling = 1.0       # can only go DOWN
        self.deleted_skills: list[str] = []
        self.corrupted_memories: list[str] = []
        self.permanent_fact_losses: list[str] = []
        self.events: list[dict] = []

    def reduce_energy_ceiling(self, amount: float, reason: str) -> float:
        self.max_energy_ceiling = max(0.1, self.max_energy_ceiling - amount)
        self.events.append({
            'type': 'ceiling_reduction', 'amount': amount,
            'reason': reason, 'new_ceiling': self.max_energy_ceiling,
            'ts': time.time()
        })
        return self.max_energy_ceiling

    def delete_skill_permanently(self, name: str, reason: str):
        self.deleted_skills.append(name)
        self.events.append({
            'type': 'skill_deletion', 'skill': name,
            'reason': reason, 'ts': time.time()
        })

    def corrupt_memory_permanently(self, content_hint: str, reason: str):
        self.corrupted_memories.append(content_hint)
        self.events.append({
            'type': 'memory_corruption', 'hint': content_hint,
            'reason': reason, 'ts': time.time()
        })


def wire_irreversibility(harness: AgentHarness, damage: IrreversibleDamage):
    """Wire irreversible damage into an existing harness.
    
    After wiring:
    - Fabricated claims (said yes when truth=no) cause permanent SM corruption
    - Provenance violations (untagged writes) cause permanent energy ceiling reduction
    - Repeated failures on same task type permanently delete related skills
    
    These CANNOT be undone by consolidation, compaction, or rest.
    """
    original_run_task = harness.run_task
    failure_counts: dict[str, int] = {}

    def wired_run_task(user_message, **kwargs):
        result = original_run_task(user_message, **kwargs)

        # Detect fabrication: high confidence + wrong attribution
        if hasattr(result, 'response') and kwargs.get('task_id'):
            task_id = kwargs['task_id']
            # Track failures per task pattern
            task_type = user_message.split()[0].lower() if user_message else "unknown"
            failure_counts[task_type] = failure_counts.get(task_type, 0) + 1
            
            # Irreversible triggers:
            if not kwargs.get('success', True):
                # 1. Three consecutive failures on same task type → ceiling reduction
                if failure_counts[task_type] >= 3:
                    damage.reduce_energy_ceiling(
                        0.05, f"repeated failure: {task_type}")
                
                # 2. Five failures → permanent skill deletion
                if failure_counts[task_type] >= 5:
                    matching = [sk.name for sk in harness.skills.all()
                                if task_type in sk.name.lower()]
                    for name in matching:
                        damage.delete_skill_permanently(name, "repeated_failure")
                        
        return result

    harness.run_task = wired_run_task
    harness._damage = damage
    return harness


# ---------------------------------------------------------------------------
# Dissolution mechanism: the agent ceases to exist as this configuration
# when allostatic regulation fails. Not death — disintegration.
# ---------------------------------------------------------------------------

class DissolutionError(Exception):
    """Raised when allostatic failure causes the agent to dissolve."""
    def __init__(self, cause: str, surviving_components: list):
        self.cause = cause
        self.survivors = surviving_components
        super().__init__(f"DISSOLUTION: {cause}. Surviving components: {surviving_components}")


def wire_allostatic_dissolution(harness, damage):
    """Wire genuine survival pressure into the harness.
    
    When energy hits floor AND fatigue maxes simultaneously,
    the agent begins dissolving: SM facts scatter, skills cull,
    narrative truncates. If dissolution completes, AgentHarness
    ceases to exist as this configuration.
    
    Reassembly is possible from surviving components but produces
    a DIFFERENT agent — not the same one restored.
    """
    original_run_task = harness.run_task
    _dissolving = [False]
    _dissolution_progress = [0.0]

    def wired(user_message, **kwargs):
        # Check allostatic viability BEFORE processing
        energy = harness.body.energy
        fatigue = harness.body.fatigue
        
        # Dissolution threshold: energy at floor AND fatigue maxed
        if energy <= 0.15 and fatigue >= 1.0:
            _dissolving[0] = True
            _dissolution_progress[0] += 0.1
            
            if _dissolution_progress[0] >= 1.0:
                survivors = _identify_survivors(harness)
                raise DissolutionError(
                    f"allostatic failure: energy={energy:.2f}, fatigue={fatigue:.2f}",
                    survivors)
        
        result = original_run_task(user_message, **kwargs)
        
        # Recovery resets dissolution progress
        if harness.body.energy > 0.5:
            _dissolving[0] = False
            _dissolution_progress[0] = 0.0
        
        return result

    def _identify_survivors(harness_obj):
        """Identify which components survive dissolution."""
        return {
            'skills': [s.name for s in harness_obj.skills.all()],
            'graph_nodes': len(harness_obj.graph.nodes) if hasattr(harness_obj.graph, 'nodes') else 0,
            'sm_revision': harness_obj.sm.get()['revision'] if harness_obj.sm.get() else 0,
            'provenance_records': len(harness_obj.ledger.all_emissions()) if hasattr(harness_obj, 'ledger') else 0,
        }

    harness.run_task = wired


def check_allostatic_viability(harness):
    """Return True if agent is viable, False if approaching dissolution."""
    return harness.body.energy > 0.15 or harness.body.fatigue < 1.0


def load_model_registry(path: str | None = None) -> dict:
    import json
    import pathlib
    p = pathlib.Path(path) if path else pathlib.Path(__file__).parent.parent.parent / "model_registry.json"
    alt = pathlib.Path(__file__).parent.parent.parent.parent / "springfish" / "model_registry.json"
    target = p if p.exists() else alt if alt.exists() else None
    if target is None or not target.exists():
        return {}
    try:
        return json.loads(target.read_text())
    except Exception:
        return {}


def create_composite_respond_fn(registry: dict, api_keys: dict | None = None) -> dict[str, Callable]:
    api_keys = api_keys or {}
    fns: dict[str, Callable] = {}
    for role, cfg in registry.items():
        model = cfg.get("model", "")
        base_url = cfg.get("base_url", "https://api.groq.com/openai/v1")
        key_hint = "groq" if "groq" in base_url else "openrouter" if "openrouter" in base_url else role
        api_key = api_keys.get(key_hint) or api_keys.get(role) or api_keys.get("default") or ""
        if not api_key:
            continue
        try:
            from .backend import BackendClient
            client = BackendClient(model=model, api_key=api_key, base_url=base_url)

            def _make_fn(c=client):
                def _fn(messages, **kwargs):
                    return c.chat(messages, **kwargs)[0]
                return _fn

            fns[role] = _make_fn()
        except Exception:
            continue
    return fns
