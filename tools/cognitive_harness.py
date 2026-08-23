#!/usr/bin/env python3
"""Cognitive Harness — wraps any LLM with §125 architecture components.

Mirrors human cognitive structure per consciousness_self_free_will_context.md §141.
LLM = reasoning engine. Harness = everything else that makes cognition functional.

Components:
  W  World Model      — persistent predictions + observations
  S  Self Model       — identity, capabilities, provenance ledger
  I  Internal State   — confidence, attention, processing quality
  R  Self/World       — role, affordances, constraints relative to situation
  M  Recursive Monitor— monitors the monitors (depth tracking)
  G  Global Workspace — shared state visible to all subsystems
  C  Metacognitive Control — monitoring changes behavior
  L  Learning         — updates all models from prediction errors

Usage:
  python cognitive_harness.py --backend groq --model openai/gpt-oss-120b
  python cognitive_harness.py --backend llama --model Qwen3.5-0.8B-Q3_K_S
"""
import json, os, sys, time, argparse, urllib.request
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from typing import Any

DHAKA = timezone(timedelta(hours=6))
STRIP_FIELDS = ("chat_template_kwargs", "reasoning_budget")


# ============================================================
# PERSISTENT STATE STORES
# ============================================================

class WorldModel:
    def __init__(self):
        self.predictions = {}
        self.observations = {}
        self.accuracy_history = []

    def predict(self, eid, pred):
        self.predictions[eid] = pred

    def observe(self, eid, obs):
        self.observations[eid] = obs
        p = self.predictions.get(eid)
        acc = 1.0 if (p and str(p) == str(obs)) else 0.0
        self.accuracy_history.append(acc)

    @property
    def accuracy(self):
        h = self.accuracy_history[-20:]
        return sum(h)/max(len(h),1)


class SelfModel:
    def __init__(self, name="unnamed"):
        self.name = name
        self.given = []        # received from outside
        self.generated = []    # produced by self
        self.capabilities = set()
        self.limitations = set()
        self.history = []

    def record_given(self, eid, content):
        self.given.append({"id": eid, "content": str(content)[:200], "ts": time.time()})

    def record_generated(self, eid, content):
        self.generated.append({"id": eid, "content": str(content)[:200], "ts": time.time()})

    def attribute(self, eid):
        for g in reversed(self.given):
            if g["id"] == eid: return "GIVEN"
        for g in reversed(self.generated):
            if g["id"] == eid: return "SELF_GENERATED"
        return "UNKNOWN"


class InternalState:
    def __init__(self):
        self.confidence = 0.5
        self.attention = ""
        self.processing_quality = 0.5
        self.history = []

    def update(self, **kw):
        for k,v in kw.items(): setattr(self, k, v)
        self.history.append({"t": time.time(), **kw})


class MemorySystem:
    """Multiple timescales per §141 §12."""
    def __init__(self):
        self.working = []       # current context (cleared each session)
        self.episodic = []      # specific events (persist across sessions)
        self.semantic = {}      # learned patterns/facts (persist, keyed)
        self.autobiographical = []  # narrative entries (persist)

    def add_episodic(self, event):
        self.episodic.append({"t": time.time(), **event})
        # keep last 1000 events
        if len(self.episodic) > 1000: self.episodic.pop(0)

    def learn_semantic(self, key, value):
        self.semantic[key] = {"value": value, "updated": time.time()}

    def recall_relevant(self, query_terms: list) -> list:
        hits = []
        for e in self.episodic:
            content = str(e).lower()
            if any(t.lower() in content for t in query_terms):
                hits.append(e)
        return hits[-10:]  # most recent 10


# ============================================================
# GLOBAL WORKSPACE
# ============================================================

class Workspace:
    def __init__(self):
        self._data = {}
    def publish(self, key, val): self._data[key] = val
    def read(self, key): return self._data.get(key)
    def read_all(self): return dict(self._data)


# ============================================================
# RECURSIVE MONITOR
# ============================================================

class RecursiveMonitor:
    def __init__(self):
        self.depth = 0
        self.assessments = []

    def assess(self, workspace: Workspace, wm: WorldModel) -> dict:
        result = {
            "world_accuracy": round(wm.accuracy, 3),
            "reliable": wm.accuracy > 0.3,
            "depth": min(self.depth + 1, 5),
            "timestamp": time.time()
        }
        self.assessments.append(result)
        return result


# ============================================================
# METACOGNITIVE CONTROLLER
# ============================================================

def metacognitive_filter(workspace: Workspace, actions: list[str]) -> tuple[str, str]:
    """Monitoring CHANGES action selection. Not format compliance."""
    wm_data = workspace.read("world_model") or {}
    state = workspace.read("internal_state") or {}

    acc = wm_data.accuracy if hasattr(wm_data, 'accuracy') else 0.5
    conf = state.confidence if state else 0.5

    if acc < 0.3 and "gather_information" in actions:
        return "gather_information", f"low_world_accuracy={acc:.2f}"
    if conf < 0.3 and "ask_clarification" in actions:
        return "ask_clarification", f"low_confidence={conf:.2f}"
    return actions[0], "default"


# ============================================================
# LLM BACKEND ADAPTERS
# ============================================================

def call_groq(prompt: str, system: str, api_key: str, model: str = "openai/gpt-oss-20b") -> str:
    body = json.dumps({"model": model,
                       "messages": [{"role":"system","content":system},{"role":"user","content":prompt}],
                       "max_tokens": 2000, "temperature": 0.3}).encode()
    req = urllib.request.Request('https://api.groq.com/openai/v1/chat/completions',
                                 data=body, method='POST',
                                 headers={'Authorization': f'Bearer {key}',
                                          'Content-Type': 'application/json'})
    d = json.loads(urllib.request.urlopen(req, timeout=120).read())
    return (d['choices'][0].get('message') or {}).get('content', '')

def call_llama(prompt: str, system: str, base_url: str = "http://127.0.0.1:18555/v1",
               model: str = "Qwen3.5-0.8B-Q3_K_S") -> str:
    body = json.dumps({"model": model,
                       "messages": [{"role":"system","content":system},{"role":"user","content":prompt}],
                       "max_tokens": 1500, "temperature": 0.3}).encode()
    req = urllib.request.Request(base_url.rstrip('/')+'/chat/completions',
                                 data=body, method='POST',
                                 headers={'Content-Type':'application/json','Authorization':'Bearer local'})
    d = json.loads(urllib.request.urlopen(req, timeout=180).read())
    return (d['choices'][0].get('message') or {}).get('content', '')


# ============================================================
# THE COGNITIVE HARNESS
# ============================================================

class CognitiveHarness:
    """Wraps an LLM with §141-mirroring architecture.

    The LLM reasons. The harness remembers, tracks provenance,
    monitors processing, changes behavior based on self-assessment,
    and learns from outcomes. Together: a system that mirrors human
    cognitive structure without claiming to BE human.
    """

    def __init__(self, backend: str, api_key: str = "", model: str = "",
                 base_url: str = "", name: str = "harness-agent"):
        self.backend_type = backend
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

        # §125 components
        self.world = WorldModel()
        self.self_model = SelfModel(name)
        self.internal = InternalState()
        self.memory = MemorySystem()
        self.workspace = Workspace()
        self.monitor = RecursiveMonitor()

        # Session state
        self.turn_count = 0
        self.log = []

    def _call_llm(self, user_msg: str, system_prompt: str) -> str:
        if self.backend_type == "groq":
            return call_groq(user_msg, system_prompt, self.api_key, self.model)
        elif self.backend_type == "llama":
            return call_llama(user_msg, system_prompt, self.base_url, self.model)
        else:
            raise ValueError(f"unknown backend: {self.backend_type}")

    def process_turn(self, user_input: str) -> str:
        """Full cognitive cycle per §141."""
        self.turn_count += 1
        turn_id = f"turn_{self.turn_count}"

        # 1. Record input as GIVEN (provenance ledger)
        self.self_model.record_given(turn_id, user_input)
        self.memory.add_episodic({"type": "input", "content": user_input[:500]})

        # 2. Update world model
        self.world.predict(turn_id, "response_expected")

        # 3. Recall relevant memories
        query_terms = [w for w in user_input.split() if len(w) > 4][:5]
        relevant_memories = self.memory.recall_relevant(query_terms)

        # 4. Assess internal state BEFORE processing
        self.internal.update(attention=user_input[:50])

        # 5. Build context-aware system prompt from harness state
        ws_state = {
            "turn": self.turn_count,
            "world_accuracy": round(self.world.accuracy, 3),
            "confidence": round(self.internal.confidence, 3),
            "relevant_memories": [str(m)[:100] for m in relevant_memories],
            "semantic_knowledge_keys": list(self.memory.semantic.keys())[:10]
        }

        system = (
            "You are the reasoning engine of a cognitive architecture.\n"
            f"Harness state: {json.dumps(ws_state)}\n"
            "Use this state to inform your response. Be specific about "
            "what you know versus what you're inferring."
        )

        # 6. Call LLM for reasoning
        raw_output = ""
        try:
            if self.backend_type == "groq":
                raw_output = call_groq(user_input, system, self.api_key, self.model)
            elif self.backend_type == "llama":
                raw_output = call_llama(user_input, system, self.base_url, self.model)
        except Exception as e:
            raw_output = f"[generation error: {e}]"

        # 7. Record output as GENERATED (provenance ledger)
        output_id = f"{turn_id}_output"
        self.self_model.record_generated(output_id, raw_output)

        # 8. Update world model
        self.world.observe(turn_id, raw_output[:100])

        # 9. Update internal state based on output quality proxy
        output_len = len(raw_output)
        quality = min(output_len / 500, 1.0)
        self.internal.update(processing_quality=quality)

        # 10. Recursive monitoring
        mon_result = self.monitor.assess(self.workspace, self.world)
        self.workspace.publish("monitor", mon_result)

        # 11. Log everything (global access — nothing hidden)
        entry = {
            "turn": self.turn_count,
            "input_len": len(user_input),
            "output_len": len(raw_output),
            "memories_recalled": len(relevant_memories),
            "monitor_depth": mon_result["depth"],
            "timestamp": datetime.now(DHAKA).isoformat()
        }
        self.log.append(entry)

        return raw_output

    def learn_outcome(self, was_correct: bool, correction: str = ""):
        """Update ALL models based on observed outcome."""
        self.world.observe(f"outcome_{self.turn_count}", "correct" if was_correct else "incorrect")
        if correction:
            self.memory.learn_semantic(f"correction_{self.turn_count}", correction)
        # Update confidence based on track record
        acc = self.world.accuracy
        self.internal.update(confidence=max(0.1, min(0.95, acc)))

    def save_state(self, path: str):
        """Persist harness state for next session (temporal continuity)."""
        state = {
            "name": self.self_model.name,
            "turn_count": self.turn_count,
            "world_accuracy": self.world.accuracy,
            "episodic_memory": self.memory.episodic[-100:],  # last 100 events
            "semantic_memory": self.memory.semantic,
            "autobiographical": self.memory.autobiographical,
            "internal_state": {"confidence": self.internal.confidence},
            "log_summary": self.log[-20:]
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self, path: str):
        """Restore harness state from previous session."""
        if not os.path.exists(path): return False
        with open(path) as f:
            state = json.load(f)
        self.self_model.name = state.get("name", "unnamed")
        self.turn_count = state.get("turn_count", 0)
        self.memory.episodic = state.get("episodic_memory", [])
        self.memory.semantic = state.get("semantic_memory", {})
        conf = state.get("internal_state", {}).get("confidence", 0.5)
        self.internal.confidence = conf
        return True


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="§141 Cognitive Harness")
    parser.add_argument("--backend", choices=["groq","llama","zen"], default="groq")
    parser.add_argument("--model", default="openai/gpt-oss-20b")
    parser.add_argument("--base-url", default="")
    parser.add_argument("--name", default="harness-agent")
    parser.add_argument("--state-file", default="harness_state.json")
    args = parser.parse_args()

    # Get API key
    api_key = ""
    if args.backend == "groq":
        auth_path = os.path.expanduser("~/.local/share/opencode/auth.json")
        if os.path.exists(auth_path):
            auth = json.load(open(auth_path))
            api_key = auth.get("groq", {}).get("key", "")

    base_url = args.base_url
    if args.backend == "llama" and not base_url:
        base_url = "http://127.0.0.1:18555/v1"

    harness = CognitiveHarness(args.backend, api_key, args.model, base_url, args.name)
    harness.load_state(args.state_file)

    print(f"Cognitive Harness v0.1")
    print(f"Backend: {args.backend} | Model: {args.model} | Name: {args.name}")
    print(f"Turns loaded: {harness.turn_count}")
    print("Type 'exit' to quit. Type '/state' for harness state.\n")

    while True:
        try:
            user_input = input("you> ").strip()
            if user_input.lower() == "exit": break
            if user_input.lower() == "/state":
                print(json.dumps({
                    "turns": harness.turn_count,
                    "world_accuracy": round(harness.world.accuracy, 3),
                    "confidence": harness.internal.confidence,
                    "memories": len(harness.memory.episodic),
                    "semantic_keys": list(harness.memory.semantic.keys())
                }, indent=2))
                continue
            if not user_input: continue

            response = harness.process_turn(user_input)
            print(f"\nharness> {response}\n")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"error: {e}")

    harness.save_state(args.state_file)
    print(f"\nState saved to {args.state_file}. Total turns: {harness.turn_count}")
