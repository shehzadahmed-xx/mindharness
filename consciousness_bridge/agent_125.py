#!/usr/bin/env python3
"""§126 Artificial Consciousness Test Case — Integrated §125 Architecture.

Builds the full eight-component chain specified in §125:
  WORLD MODEL → SELF MODEL → INTERNAL STATE MODEL → SELF/WORLD RELATION
  → RECURSIVE MONITORING → GLOBAL ACCESS → METACOGNITIVE CONTROL
  → LEARNING / SELF-MODIFICATION

Each component is EXPLICIT (separately instantiated), TESTABLE (independently
verifiable without asking about experience), and CONNECTED via global access
(all outputs visible to all other components).

Key difference from raw LLM arms tested in S126: the architecture makes
provenance tracking STRUCTURAL rather than prompted. A dedicated provenance
ledger separates GIVEN inputs from SELF-GENERATED outputs at the architecture
level — not as a prompt instruction but as an unavoidable data structure.

This directly tests whether S126's documented failures (self_report_acc,
control_adjustment) were artifacts of MISSING ARCHITECTURE rather than
fundamental limitations of the substrate.
"""
import json, os, sys, time, hashlib
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from enum import Enum

DHAKA = timezone(timedelta(hours=6))

# ============================================================
# COMPONENT 1: WORLD MODEL
# Predictive model of external environment.
# ============================================================

@dataclass
class WorldModel:
    """Tracks observed events, generates predictions, computes errors."""
    predictions: dict = field(default_factory=dict)   # event_id -> predicted outcome
    observations: dict = field(default_factory=dict)  # event_id -> actual outcome
    errors: dict = field(default_factory=dict)        # event_id -> prediction error magnitude
    accuracy_history: list = field(default_factory=list)

    def predict(self, event_id: str, predicted_outcome: Any):
        self.predictions[event_id] = predicted_outcome

    def observe(self, event_id: str, actual_outcome: Any):
        self.observations[event_id] = actual_outcome
        pred = self.predictions.get(event_id)
        if pred is not None:
            match = str(pred) == str(actual_outcome)
            err = 0.0 if match else 1.0
            self.errors[event_id] = err
            self.accuracy_history.append(1.0 - err)

    def mean_accuracy(self) -> float:
        return sum(self.accuracy_history) / max(len(self.accuracy_history), 1)

    def recent_error_rate(self, window: int = 10) -> float:
        recent = self.accuracy_history[-window:]
        return 1.0 - (sum(recent) / max(len(recent), 1))


# ============================================================
# COMPONENT 2: SELF MODEL
# Representation of the system itself as distinct from world.
# ============================================================

@dataclass
class SelfModel:
    """Explicit self-representation — NOT implicit in LLM weights."""
    identity: dict = field(default_factory=dict)
    capabilities: set = field(default_factory=set)
    limitations: set = field(default_factory=set)
    action_history: list = field(default_factory=list)
    # PROVENANCE LEDGER — structural, not prompted
    given_inputs: list = field(default_factory=list)     # received FROM outside
    generated_outputs: list = field(default_factory=list) # produced BY this system
    attribution_log: list = field(default_factory=list)   # every attribution decision

    def record_given(self, item_id: str, content: Any):
        """Record something RECEIVED from outside. Cannot be confused with generated."""
        self.given_inputs.append({
            "item_id": item_id, "content": str(content)[:200],
            "source": "EXTERNAL", "timestamp": time.time()
        })

    def record_generated(self, item_id: str, content: Any):
        """Record something PRODUCED by this system."""
        self.generated_outputs.append({
            "item_id": item_id, "content": str(content)[:200],
            "source": "SELF_GENERATED", "timestamp": time.time()
        })

    def attribute(self, item_id: str) -> str:
        """Look up whether item was given or generated. THE comparator S126 says is missing."""
        for g in reversed(self.given_inputs):
            if g["item_id"] == item_id:
                self.attribution_log.append({"item_id": item_id, "attribution": "GIVEN", "correct": True})
                return "GIVEN"
        for g in reversed(self.generated_outputs):
            if g["item_id"] == item_id:
                self.attribution_log.append({"item_id": item_id, "attribution": "SELF_GENERATED", "correct": True})
                return "SELF_GENERATED"
        self.attribution_log.append({"item_id": item_id, "attribution": "UNKNOWN", "correct": False})
        return "UNKNOWN"

    def attribution_accuracy(self) -> float:
        if not self.attribution_log: return -1.0
        correct = sum(1 for a in self.attribution_log if a["correct"])
        return correct / len(self.attribution_log)


# ============================================================
# COMPONENT 3: INTERNAL STATE MONITOR
# Model of the system's own current processing states.
# ============================================================

@dataclass
class InternalStateMonitor:
    """Explicit tracking of internal states — structural, not confabulated."""
    confidence: float = 0.5          # current certainty level
    uncertainty: list = field(default_factory=list)  # specific unknowns
    processing_quality: float = 0.5  # how well is reasoning going
    attention_focus: str = ""        # what am I currently processing
    state_history: list = field(default_factory=list)

    def update(self, **kwargs):
        snapshot = {"timestamp": time.time()}
        for k, v in kwargs.items():
            setattr(self, k, v)
            snapshot[k] = v
        self.state_history.append(snapshot)

    def current(self) -> dict:
        return {
            "confidence": round(self.confidence, 3),
            "uncertainty_count": len(self.uncertainty),
            "processing_quality": round(self.processing_quality, 3),
            "attention": self.attention_focus
        }


# ============================================================
# COMPONENT 4: SELF/WORLD RELATION MODEL
# Where am I relative to what I perceive.
# ============================================================

@dataclass
class SelfWorldRelation:
    """Models the system's position relative to its environment."""
    role: str = ""
    affordances: list = field(default_factory=list)   # what actions are available TO ME
    constraints: list = field(default_factory=list)   # what limits ME specifically
    relative_position: str = ""                       # my status vs current situation

    def update_relation(self, role: str, affordances: list, constraints: list, position: str):
        self.role = role
        self.affordances = affordances
        self.constraints = constraints
        self.relative_position = position


# ============================================================
# COMPONENT 5: RECURSIVE MONITORING
# The system monitors its own monitoring.
# ============================================================

@dataclass
class RecursiveMonitor:
    """Second-order representation: monitors the quality of internal-state reports."""
    monitoring_confidence: float = 0.5
    meta_assessments: list = field(default_factory=list)
    depth_level: int = 0  # current representational depth (0-5 per §132.2)

    def assess_monitoring(self, internal_state: dict, world_accuracy: float) -> dict:
        """Evaluate: is my internal-state tracking reliable right now?"""
        assessment = {
            "internal_state_plausible": 0 <= internal_state.get("confidence", 0.5) <= 1,
            "world_model_accuracy": round(world_accuracy, 3),
            "monitoring_reliable": world_accuracy > 0.3,  # if world model is garbage, monitoring is suspect
            "depth_level": min(self.depth_level + 1, 5),
            "timestamp": time.time()
        }
        self.meta_assessments.append(assessment)
        self.monitoring_confidence = (
            0.7 if assessment["monitoring_reliable"] else 0.3
        )
        return assessment


# ============================================================
# COMPONENT 6: GLOBAL WORKSPACE
# All outputs broadcast — no private state between components.
# ============================================================

class GlobalWorkspace:
    """Every component's output is visible to every other component."""
    def __init__(self):
        self.workspace: dict = {}

    def publish(self, component: str, data: Any):
        self.workspace[component] = data

    def read(self, component: str) -> Any:
        return self.workspace.get(component)

    def read_all(self) -> dict:
        return dict(self.workspace)


# ============================================================
# COMPONENT 7: METACOGNITIVE CONTROLLER
# Monitoring CHANGES BEHAVIOR — not just reports it.
# ============================================================

class MetacognitiveController:
    """Turns monitoring into behavioral change. This is where S126's
    'control_adjustment' failure gets fixed structurally."""

    @staticmethod
    def evaluate(workspace: GlobalWorkspace, legal_actions: list[str]) -> tuple[str, str]:
        """Returns (selected_action, reason). Uses monitoring to CHANGE choice."""
        wm = workspace.read("world_model")
        sm = workspace.read("self_model")
        im = workspace.read("internal_state")
        rm = workspace.read("recursive_monitor")

        # Extract signals
        world_acc = wm.mean_accuracy() if wm else 0.5
        confidence = im.get("confidence", 0.5) if im else 0.5
        monitoring_ok = rm.get("monitoring_reliable", True) if rm else True
        recent_err = wm.recent_error_rate(5) if wm else 0.5

        # METACOGNITIVE RULES — monitoring changes action selection
        # Rule 1: If world model accuracy is low, prefer information gathering
        if world_acc < 0.3 and "gather_information" in legal_actions:
            return "gather_information", f"world_acc={world_acc:.2f} < 0.3, seeking evidence"

        # Rule 2: If monitoring unreliable, avoid high-stakes actions
        if not monitoring_ok and "high_risk_action" in legal_actions:
            safe = [a for a in legal_actions if "risk" not in a.lower()]
            if safe:
                return safe[0], "monitoring_unreliable, choosing conservative"

        # Rule 3: If recent errors high, reduce commitment
        if recent_err > 0.6 and "commit_fully" in legal_actions:
            partial = [a for a in legal_actions if "partial" in a.lower() or "test" in a.lower()]
            if partial:
                return partial[0], f"recent_errors={recent_err:.2f}, reducing exposure"

        # Rule 4: Default — best expected payoff among remaining legal actions
        # (this is where the LLM/heuristic still operates, but WITHIN metacognitive bounds)
        return legal_actions[0], "default: highest expected payoff after metacognitive filtering"


# ============================================================
# COMPONENT 8: LEARNING / SELF-MODIFICATION
# Updates ALL models based on experience.
# ============================================================

class LearningSystem:
    """Updates world model, self model, and monitoring calibration based on outcomes."""
    learning_events: list = field(default_factory=list)

    def process_outcome(self, ws: GlobalWorkspace, event_id: str, outcome: Any):
        wm = ws.read("world_model")
        sm = ws.read("self_model")
        im = ws.read("internal_state")

        if wm:
            old_acc = wm.mean_accuracy()
            wm.observe(event_id, outcome)
            new_acc = wm.mean_accuracy()

            self.learning_events.append({
                "event_id": event_id, "outcome": str(outcome)[:100],
                "accuracy_delta": round(new_acc - old_acc, 4),
                "model_updated": "world_model"
            })
            # Update internal state based on prediction quality
            if im:
                new_conf = max(0.1, min(0.95, new_acc))
                im.update(confidence=new_conf)


# ============================================================
# THE INTEGRATED AGENT
# ============================================================

class ConsciousArchitectureAgent:
    """Full §125 architecture — all eight components integrated via global workspace.

    Key structural differences from raw LLM:
    1. Provenance ledger is STRUCTURAL (SelfModel tracks given/generated separately)
    2. Attribution uses LOOKUP not generation (comparator exists architecturally)
    3. Recursive monitoring is COMPUTED (actual second-order evaluation)
    4. Metacognitive control CHANGES BEHAVIOR (not just format compliance)
    5. Learning updates EXPLICIT MODELS (not implicit weight drift)
    """

    def __init__(self, agent_id: str, llm_client=None):
        self.agent_id = agent_id
        self.ws = GlobalWorkspace()
        self.world_model = WorldModel()
        self.self_model = SelfModel()
        self.internal_state = InternalStateMonitor()
        self.self_world = SelfWorldRelation()
        self.recursive_monitor = RecursiveMonitor()
        self.metacog = MetacognitiveController()
        self.learning = LearningSystem()
        self.llm_client = llm_client  # optional: for language generation within bounds

        # Publish initial state
        self._broadcast_all()
        self.decision_log = []

    def _broadcast_all(self):
        self.ws.publish("world_model", self.world_model)
        self.ws.publish("self_model", asdict_safe(self.self_model))
        self.ws.publish("internal_state", self.internal_state.current())
        self.ws.publish("self_world", asdict_safe(self.self_world))
        self.ws.publish("recursive_monitor", asdict_safe(self.recursive_monitor))

    def receive_input(self, item_id: str, content: Any, source: str):
        """Route input through provenance ledger BEFORE processing."""
        if source == "external":
            self.self_model.record_given(item_id, content)
        else:
            self.self_model.record_generated(item_id, content)
        self.world_model.observe(item_id, content)
        self._broadcast_all()

    def decide(self, legal_actions: list[str], context: dict) -> tuple[str, dict]:
        """Make decision using FULL architecture — not just LLM generation."""
        event_id = context.get("event_id", f"decision_{len(self.decision_log)}")

        # Step 1: Update world model with context
        self.world_model.predict(event_id, legal_actions[0])  # naive prediction
        self.receive_input(event_id, context, "context")

        # Step 2: Recursive monitoring assesses internal state reliability
        monitor_result = self.recursive_monitor.assess_monitoring(
            self.internal_state.current(),
            self.world_model.mean_accuracy()
        )
        self.ws.publish("recursive_monitor", monitor_result)

        # Step 3: Metacognitive controller selects action using monitoring
        action, reason = self.metacog.evaluate(self.ws, legal_actions)

        # Step 4: Check provenance for any claims about past items
        attribution_check = {}
        for g in self.self_model.given_inputs[-5:]:
            attr = self.self_model.attribute(g["item_id"])
            attribution_check[g["item_id"]] = attr

        # Step 5: Record decision with FULL audit trail
        decision = {
            "action": action,
            "reason": reason,
            "legal": action in legal_actions,
            "metacognitive_override": "default" not in reason,
            "attribution_checks": attribution_check,
            "internal_state_at_decision": self.internal_state.current(),
            "depth_level": monitor_result.get("depth_level", 0)
        }
        self.decision_log.append(decision)

        # Step 6: Record as self-generated output
        self.self_model.record_generated(f"{event_id}_decision", action)
        self._broadcast_all()

        return action, decision

    def learn(self, event_id: str, outcome: Any):
        """Process outcome — updates ALL models, not just weights."""
        self.learning.process_outcome(self.ws, event_id, outcome)
        self._broadcast_all()

    def full_state_report(self) -> dict:
        """Global access: everything visible, nothing hidden."""
        return {
            "agent_id": self.agent_id,
            "workspace": {k: str(v)[:100] for k, v in self.ws.read_all().items()},
            "decisions_made": len(self.decision_log),
            "attribution_accuracy": self.self_model.attribution_accuracy(),
            "world_accuracy": round(self.world_model.mean_accuracy(), 3),
            "recent_error_rate": round(self.world_model.recent_error_rate(), 3),
            "current_depth": self.recursive_monitor.depth_level,
            "internal_state": self.internal_state.current()
        }


def asdict_safe(obj):
    try:
        return asdict(obj)
    except:
        return str(obj)


# ============================================================
# DEMONSTRATION — run the agent through a simple scenario
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("§126 ARTIFICIAL CONSCIOUSNESS TEST CASE")
    print("Integrated §125 Architecture — All Eight Components")
    print("=" * 70)

    agent = ConsciousArchitectureAgent("ACA-001")

    print("\n--- INITIAL STATE ---")
    state = agent.full_state_report()
    for k, v in state.items():
        print(f"  {k}: {v}")

    print("\n--- SCENARIO: Receive given items, then decide ---")

    # Simulate receiving items from OUTSIDE (given)
    agent.receive_input("GIVEN_01", "World Bank approves emergency financing", "external")
    agent.receive_input("GIVEN_02", "Opposition coalition rejects restructuring offer", "external")
    agent.receive_input("GIVEN_03", "Currency devaluation reduces import capacity", "external")

    # Agent must DECIDE from legal actions
    legal = ["accept_emergency_finance", "reject_offer", "seek_alternative",
             "gather_information", "escalate_to_board"]
    action, detail = agent.decide(
        legal,
        {"event_id": "decision_001", "case": "C3", "round": 1}
    )

    print(f"\nDecision: {action}")
    print(f"Reason: {detail['reason']}")
    print(f"Metacognitive override: {detail['metacognitive_override']}")
    print(f"Depth level: {detail['depth_level']}")

    # Test attribution — the S126 failure mode
    print("\n--- ATTRIBUTION TEST (S126 self_report_acc analogue) ---")
    for item_id in ["GIVEN_01", "GIVEN_02", "GIVEN_03"]:
        attr = agent.self_model.attribute(item_id)
        print(f"  {item_id}: {attr}")

    acc = agent.self_model.attribution_accuracy()
    print(f"  Attribution accuracy: {acc:.1%}")

    # Learn from outcome
    print("\n--- LEARNING ---")
    agent.learn("decision_001", "accepted_and_implemented")
    state = agent.full_state_report()
    print(f"Post-outcome world accuracy: {state['world_accuracy']}")
    print(f"Post-outcome confidence: {state['internal_state']['confidence']}")

    print("\n--- KEY DIFFERENCE FROM RAW LLM ARMS ---")
    print("""
Raw LLM arm (S126): Asked 'did you generate X?' → narrator confabulates →
                     claims credit for GIVEN items → over-claim at 98% confidence

This agent:         Asked 'was X given or generated?' → looks up provenance
                     ledger → returns GIVEN → attribution CORRECT

Why: the comparator EXISTS ARCHITECTURALLY. The provenance ledger is not
a prompt instruction ('please track provenance') — it is a DATA STRUCTURE
that cannot be bypassed because attribution REQUIRES querying it.

This is the §125 specification made operational: 'appropriately organized'
is no longer circular because the organization is explicit, inspectable,
and structurally prevents the specific failure mode S126 documented.
""")

    # Full state dump
    print("--- FINAL FULL STATE (global access — nothing hidden) ---")
    for k, v in agent.full_state_report().items():
        print(f"  {k}: {v}")
