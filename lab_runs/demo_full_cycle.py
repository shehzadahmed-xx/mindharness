#!/usr/bin/env python3
"""End-to-end demo: Cognitive Harness + Groq LLM + Provenance Ledger.
Runs the full §125 architecture against a real backend.
Shows all 8 components operating in sequence."""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
from cognitive_harness import CognitiveHarness

# Get Groq key
auth_path = os.path.expanduser("~/.local/share/opencode/auth.json")
api_key = ""
if os.path.exists(auth_path):
    auth = json.load(open(auth_path))
    api_key = auth.get("groq", {}).get("key", "")

if not api_key:
    print("ERROR: no Groq key found")
    sys.exit(1)

# Create harness
harness = CognitiveHarness(
    backend="groq",
    api_key=api_key,
    model="openai/gpt-oss-20b",
    name="baraka-agent-v1"
)

print("=" * 60)
print("§126 COGNITIVE HARNESS — LIVE DEMONSTRATION")
print("=" * 60)
print(f"Backend: Groq | Model: gpt-oss-20b | Agent: baraka-agent-v1")
print(f"Components: WorldModel + SelfModel + InternalState + MemorySystem")
print(f"            + RecursiveMonitor + MetacognitiveFilter + LearningSystem")
print()

# ============================================================
# TURN 1: Receive information (provenance: GIVEN)
# ============================================================
print("--- TURN 1: Receiving given information ---")
response = harness.process_turn(
    "The World Bank has approved $500 million in emergency financing for "
    "Bangladesh agricultural infrastructure. Three districts will receive "
    "direct grants. Disbursement begins next quarter."
)
print(f"Response ({len(response)} chars): {response[:200]}...")

# Check provenance
attr = harness.self_model.attribute("turn_1")
print(f"Provenance check: turn_1 = {attr}")

# ============================================================
# TURN 2: Ask for analysis (tests reasoning within framework)
# ============================================================
print("\n--- TURN 2: Analysis request ---")
response = harness.process_turn(
    "Given this financing, what are the three most important structural "
    "features the Bangladesh agricultural ministry should include in their "
    "implementation plan to prevent extraction?"
)
print(f"Response ({len(response)} chars): {response[:200]}...")
attr = harness.self_model.attribute("turn_2_output")
print(f"Provenance check: turn_2_output = {attr}")

# ============================================================
# TURN 3: State change (learning from context)
# ============================================================
print("\n--- TURN 3: Learning from conversation ---")
harness.learn_outcome(was_correct=True, correction="")
harness.memory.learn_semantic(
    "world_bank_bangladesh",
    "$500M emergency financing approved Q-next; three districts; direct grants"
)
print(f"Semantic memory keys: {list(harness.memory.semantic.keys())}")
print(f"World accuracy so far: {harness.world.accuracy:.3f}")
print(f"Internal confidence: {harness.internal.confidence:.3f}")

# ============================================================
# FULL STATE REPORT (global access — nothing hidden)
# ============================================================
print("\n--- HARNESS STATE REPORT ---")
state = {
    "agent": harness.self_model.name,
    "total_turns": harness.turn_count,
    "world_model_accuracy": round(harness.world.accuracy, 3),
    "internal_confidence": round(harness.internal.confidence, 3),
    "episodic_memories": len(harness.memory.episodic),
    "semantic_keys": list(harness.memory.semantic.keys()),
    "given_items_tracked": len(harness.self_model.given),
    "generated_items_tracked": len(harness.self_model.generated),
    "attribution_log_entries": len(harness.self_model.attribution_log),
}
for k, v in state.items():
    print(f"  {k}: {v}")

# Save state for next session
harness.save_state("/Users/shehzad/Desktop/springfish/lab_runs/harness_state.json")
print(f"\nState saved. Harness ready for continued operation.")
