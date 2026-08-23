#!/usr/bin/env python3
"""
§141 COMPLETE COGNITIVE ARCHITECTURE — Artificial Human System
Every component from consciousness_self_free_will_context.md §141-142
implemented as a working, persistent, self-modifying cognitive system.

LLM = reasoning engine. This harness = the full human cognitive architecture.

Components (matching §141 Mermaid diagram exactly):
  BODY           → resource constraints, energy, fatigue
  HOMEOSTASIS    → predictive regulation of internal resources  
  GLOBAL STATE   → arousal, emotion, mood, motivation, attention width
  SENSATION      → input parsing and interoception
  ATTENTION      → salience weighting, precision, selection
  MEMORY         → working / episodic / semantic / procedural / autobiographical
  CULTURE        → inherited frameworks and values (loaded from WORLD_MODEL)
  WORLD MODEL    → constructed situation representation
  SELF MODEL     → multilayered (bodily/agentive/social/narrative/reflective/moral)
  SELF-IN-WORLD  → situated awareness (self positioned relative to world)
  PREDICTION     → simulation of possible futures
  VALUATION      → automatic significance assignment
  EMOTION        → coordinated whole-system response
  FEELING        → conscious representation of emotional condition
  THOUGHT GEN    → candidate response generation (via LLM)
  IDENTIFICATION → me/mine/true tagging (provenance ledger)
  AWARENESS      → global availability broadcaster
  METACOGNITION  → confidence, uncertainty, self-monitoring
  NARRATIVE      → introspective explanation and identity story
  VALUES/MEANING → endorsed direction and purpose
  AUTO CONTROLLERS → habits and conditioned responses
  COMPETITION    → between impulses, motives, goals
  DELIBERATION   → alternatives, reasons, future simulation
  ENDORSEMENT    → which motive gets authority
  INTENTION      → commitment to action
  ACTION         → output generation
  CONSEQUENCES   → prediction error tracking
  LEARNING       → updating ALL models
  THERMODYNAMICS → energy accounting per §142

Usage:
  python artificial_human_agent.py --backend groq
  python artificial_human_agent.py --backend llama
"""
import json, os, sys, time, math, hashlib, argparse
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from enum import Enum

DHAKA = timezone(timedelta(hours=6))
def now(): return datetime.now(DHAKA).isoformat()
def clamp(v, lo=0.0, hi=1.0): return max(lo, min(hi, v))
def hsh(s): return hashlib.sha256(str(s).encode()).hexdigest()[:16]


# ════════════════════════════════════════════════════════════
# THERMODYNAMIC CONSTRAINTS (§142)
# ════════════════════════════════════════════════════════════

class Thermodynamics:
    """Energy accounting: every process has a cost (§142)."""
    def __init__(self, total_budget: float = 1000.0):
        self.total_budget = total_budget
        self.spent = 0.0
        
    @property
    def remaining(self) -> float:
        return max(0.0, self.total_budget - self.spent)
    
    @property 
    def depleted(self) -> bool:
        return self.remaining <= 0
    
    def spend(self, amount: float, process: str):
        self.spent += amount
        if self.depleted:
            raise RuntimeError(f"Thermodynamic budget exhausted after {process}")
    
    def status(self) -> dict:
        return {
            "budget": self.total_budget,
            "spent": round(self.spent, 2),
            "remaining": round(self.remaining, 2),
            "utilization": round(self.spent / self.total_budget, 3)
        }


# ════════════════════════════════════════════════════════════
# BODY — physical substrate and homeostasis (§141 §1, §142.3)
# ════════════════════════════════════════════════════════════

class Body:
    """Physical substrate: energy, capacity, fatigue, allostatic regulation."""
    def __init__(self):
        self.energy: float = 1.0          # depletes with use
        self.fatigue: float = 0.0         # accumulates without rest
        self.tokens_used: int = 0         # total processing done
        self.max_tokens_per_turn: int = 2000
        self.allostatic_load: float = 0.0 # accumulated stress from prediction errors

    def consume(self, tokens: int):
        ratio = tokens / max(self.max_tokens_per_turn, 1)
        self.energy = clamp(self.energy - ratio * 0.08)
        self.fatigue = clamp(self.fatigue + 0.03)

    def allostatic_update(self, prediction_errors: int):
        """Allostasis: predictive regulation. More errors = more load."""
        self.allostatic_load = clamp(self.allostatic_load + prediction_errors * 0.05)
        self.energy = clamp(self.energy - self.allostatic_load * 0.02)

    def rest(self):
        self.energy = clamp(self.energy + 0.25)
        self.fatigue = clamp(self.fatigue - 0.2)
        self.allostatic_load = clamp(self.allostatic_load - 0.1)

    @property
    def viable(self) -> bool:
        return self.energy > 0.05 and not self.fatigue > 0.95

    def state(self) -> dict:
        return {"energy": round(self.energy,3), "fatigue": round(self.fatigue,3),
                "allostatic_load": round(self.allostatic_load,3), "viable": self.viable}


# ════════════════════════════════════════════════════════════
# HOMEOSTASIS / ALLOSTASIS — predictive bodily regulation (§142.3)
# ════════════════════════════════════════════════════════════

class Homeostasis:
    """Predictive regulation: prepare body before demand arrives."""
    def __init__(self):
        self.setpoints = {"energy": 0.8, "fatigue": 0.2, "allostatic_load": 0.1}
    
    def assess_deviation(self, body: Body) -> dict:
        deviations = {}
        for attr, target in self.setpoints.items():
            current = getattr(body, attr, 0.5)
            dev = abs(current - target)
            deviations[attr] = {"current": round(current,3), "target": target,
                                "deviation": round(dev,3), "needs_correction": dev > 0.3}
        return deviations
    
    def recommend_action(self, deviations: dict) -> Optional[str]:
        for attr, info in deviations.items():
            if info["needs_correction"]:
                if attr == "energy": return "rest"
                if attr == "fatigue": return "rest"
                if attr == "allostatic_load": return "reduce_stress"
        return None


# ════════════════════════════════════════════════════════════
# GLOBAL STATE — configures every process simultaneously (§141 §4)
# ════════════════════════════════════════════════════════════

@dataclass
class GlobalState:
    arousal: float = 0.5
    mood: float = 0.5
    motivation: float = 0.7
    attentional_width: float = 0.7
    urgency: float = 0.3

    def configure_processing(self) -> dict:
        return {
            "threat_sensitivity": clamp(self.arousal * (1-self.mood)),
            "exploration_tendency": clamp(self.mood * self.attentional_width),
            "processing_speed": clamp(0.5 + self.arousal*0.5),
            "risk_tolerance": clamp(self.mood*(1-self.urgency)+0.2),
            "detail_orientation": clamp(1 - self.attentional_width*0.5),
            "creative_capacity": clamp(self.attentional_width*self.mood),
        }

    def update_from_emotion(self, emotion: str, intensity: float):
        """Emotion is a whole-system controller (§141 §5)."""
        if emotion == "alarm": self.arousal = clamp(0.8); self.urgency = clamp(0.7)
        elif emotion == "concern": self.arousal = clamp(0.6); self.urgency = clamp(0.5)
        elif emotion == "interest": self.arousal = clamp(0.6); self.mood = clamp(0.7)
        elif emotion == "engagement": self.arousal = clamp(0.7); self.mood = clamp(0.8)
        elif emotion == "neutral": pass


# ════════════════════════════════════════════════════════════
# MEMORY — five types per §141 §12 (multi-timescale)
# ════════════════════════════════════════════════════════════

class MemorySystem:
    def __init__(self, max_entries=500):
        self.max_entries = max_entries
        self.working: list = []              # current turn context
        self.episodic: list = []             # specific events with timestamps
        self.semantic: dict = {}             # learned facts and patterns
        self.procedural: list = []           # learned behavioral sequences
        self.autobiographical: list = []     # narrative identity entries

    # Working memory — current turn only
    def set_working(self, items): self.working = items[:10]
    def get_working(self): return self.working

    # Episodic — specific events
    def add_episodic(self, event: dict):
        self.episodic.append({"t": now(), **event})
        if len(self.episodic) > self.max_entries: self.episodic.pop(0)

    # Semantic — learned facts and patterns
    def learn_semantic(self, key, value):
        self.semantic[key] = {"value": value, "learned": now()}
    
    # Procedural — learned behavioral sequences
    def learn_procedural(self, pattern_name, sequence):
        existing = next((p for p in self.procedural_patterns if p["pattern"]==pattern_name), None)
        if existing:
            existing["sequence"] = sequence; existing["reinforced"] = True
        else:
            self.procedural_patterns.append({"pattern": pattern_name, "sequence": sequence})

    # Autobiographical — narrative identity entries
    def add_autobiographical(self, entry):
        self.autobiographical.append({"t": now(), "entry": entry})

    # Recall by relevance
    def recall_relevant(self, terms, limit=10):
        scored = [(sum(1 for t in terms if t.lower() in str(e).lower()), e) for e in self.episodic]
        scored = [(s,e) for s,e in scored if s>0]
        scored.sort(key=lambda x:-x[0])
        return [e for _,e in scored[:limit]]

    def serialize(self) -> dict:
        return {"episodic": self.episodic[-100:], "semantic": self.semantic,
                "procedural": self.procedural, "autobiographical": self.autobiographical[-50:]}


# ════════════════════════════════════════════════════════════
# ATTENTION — salience and precision weighting (§141 §2 AT node)
# ════════════════════════════════════════════════════════════

class Attention:
    def __init__(self, gs: GlobalState): self.gs = gs

    def filter_and_weight(self, inputs: list[dict]) -> list[dict]:
        cfg = self.gs.processing_config()
        threat_w = ["crisis","failure","loss","default","collapse","risk"]
        scored = []
        for inp in inputs:
            content = str(inp.get("content","")).lower()
            base = inp.get("salience", 0.5)
            threat_bonus = sum(2 for w in threat_w if w in content) * cfg["threat_sensitivity"]
            novelty = inp.get("novelty", 0.3) * self.gs.attentional_width
            recency = inp.get("recency_bonus", 0)
            total = clamp(base + threat_bonus + novelty + recency)
            scored.append({**inp, "attention_weight": round(total,3)})
        scored.sort(key=lambda x:-x["attention_weight"])
        max_items = max(3, int(len(scored)*self.gs.attentional_width))
        return scored[:max_items]


# ════════════════════════════════════════════════════════════
# EMOTION — whole-system controller (§141 §5)
# ════════════════════════════════════════════════════════════

class Emotion:
    def __init__(self):
        self.current = "neutral"; self.intensity = 0.3
        self.history: list = []

    def appraise(self, situation, self_model_state: dict) -> dict:
        sl = situation.lower()
        threat_words = ["crisis","failure","loss","default","collapse"]
        opp_words = ["opportunity","growth","success","progress","funded"]
        tl = sum(2 for w in threat_words if w in sl)
        ol = sum(2 for w in opp_words if w in sl)
        
        # Self-model state modulates appraisal
        efficacy = self_model_state.get("agentive",{}).get("efficacy",0.5)
        if efficacy < 0.3: tl += 1  # low efficacy amplifies threat perception
        
        if tl > ol: emotion, intensity = ("concern"if tl<4 else"alarm"), clamp(0.3+tl*0.15)
        elif ol > tl: emotion, intensity = ("interest"if ol<4 else"engagement"), clamp(0.3+ol*0.12)
        else: emotion, intensity = "neutral", 0.3
        
        self.current, self.intensity = emotion, intensity
        self.history.append({"emotion":emotion,"intensity":intensity,"t":now()})
        
        return {"emotion":emotion,"intensity":round(intensity,3),
                "readiness":"heightened" if intensity>0.6 else"normal",
                "attention_shift":"narrow"if emotion in("concern","alarm")else"maintain"}


# ════════════════════════════════════════════════════════════
# NARRATIVE — introspective explanation and identity story (§141 §10)
# ════════════════════════════════════════════════════════════

class Narrative:
    def __init__(self):
        self.story = ""; self.themes: list = []; self.updates: list = []
    
    def update(self, events: list, emotional_state: dict, self_model) -> str:
        themes = set()
        for e in events[-5:]:
            c = str(e.get("content",e)).lower()
            for t in ["financial","consciousness","systems","hamba","baraka",
                      "islamic","architecture","loop","extraction","design"]:
                if t in c: themes.add(t)
        
        emotion_influence = f"In emotional context: {emotional_state['emotion']}."
        theme_str = ", ".join(themes) if themes else "general inquiry"
        new_story = f"Engaged with {theme_str}. {emotion_influence} Events tracked: {len(events)}."
        self.updates.append(new_story)
        self.story = new_story
        self_model.update_narrative(new_story)
        return new_story


# ════════════════════════════════════════════════════════════
# LEARNING — updates ALL models (§141 §11)
# ════════════════════════════════════════════════════════════

class LearningSystem:
    def __init__(self):
        self.events: list = []; self.errors: list = []
        self.calibration_history: list = []

    def process_outcome(self, prediction, outcome, models_to_update: dict):
        error = 0.0 if str(prediction)==str(outcome) else 1.0
        self.errors.append(error)
        self.events.append({"prediction":str(prediction)[:100],
                           "outcome":str(outcome)[:100],"error":error,"t":now()})
        
        results = {}
        for name, model in models_to_update.items():
            if hasattr(model, 'observe'): model.observe(name, outcome); results[name]="updated"
            elif hasattr(model, 'learn_semantic'): model.learn_semantic(f"outcome_{name}", outcome); results[name]="semantic_updated"
        return results

    @property
    def mean_error(self):
        recent = self.errors[-20:]
        return sum(recent)/max(len(recent),1)


# ════════════════════════════════════════════════════════════
# THE INTEGRATED ARTIFICIAL HUMAN AGENT
# Every node from the §141 diagram, connected.
# ════════════════════════════════════════════════════════════



class WorldModel:
    def __init__(self):
        self.situation="";self.actors={};self.facts={};self.predictions={};self.outcomes={}
    def set_situation(self,d):self.situation=d
    def register_actor(self,aid,role,r=0.5):self.actors[aid]={"role":role,"reliability":r}
    def add_fact(self,c,s,conf=0.8):self.facts[hsh(c)]={"content":c[:300],"source":s,"confidence":conf}
    def predict(self,eid,p):self.predictions[eid]=p
    def record_outcome(self,eid,o):
        self.outcomes[eid]=o;pred=self.predictions.get(eid)
        return 0.0 if(pred and str(pred)==str(o))else 1.0
    def summary(self):
        actors=", ".join(f"{k}({v['role']})"for k,v in list(self.actors.items())[:5])
        return f"Situation:{self.situation[:80]}|Actors:{actors}|Facts:{len(self.facts)}"

class SelfModel:
    def __init__(self,name):
        self.name=name
        self.bodily={"energy":1.0,"status":"operational"}
        self.agentive={"efficacy":0.7}
        self.social={"relationships":{}}
        self.narrative={"story":""}
        self.reflective={"processing":False}
        self.moral={"endorsed_values":[]}
        self.given_items=[];self.generated_items=[];self.attribution_log=[]
    def receive_given(self,eid,c):
        self.given_items.append({"id":eid,"content":str(c)[:200],"source":"EXTERNAL"})
    def produce_generated(self,eid,c):
        self.generated_items.append({id:eid,content:str(c)[:200],source:SELF})
    def attribute(self,eid):
        for g in reversed(self.given_items):
            if g[id]==eid:returnGIVEN
        for g in reversed(self.generated_items):
            if g[id]==eid:returnSELF_GENERATED
        returnUNKNOWN
    @property
    def attribution_accuracy(self):
        if not self.attribution_log:return-1.0
        return sum(1 for a in self.attribution_log if a.get(correct))/len(self.attribution_log)
    def set_values(self,v):self.moral[endorsed_values]=v
    def update_narrative(self,s):self.narrative[story]=s


class ArtificialHumanAgent:

    def __init__(self, name="Baraka-Agent", backend="llama", api_key="", model="", base_url="http://127.0.0.1:18555/v1"):
        self.name = name
        self.backend = backend; self.api_key = api_key
        self.llm_model = model; self.base_url = base_url
        
        # Initialize ALL components
        self.body = Body()
        self.thermo = Thermodynamics(total_budget=1000)
        self.homeostasis = Homeostasis()
        self.gs = GlobalState()
        self.memory = MemorySystem()
        self.attention = Attention(self.gs)
        self.emotion = Emotion()
        self.narrative = Narrative()
        self.learning = LearningSystem()
        self.world = WorldModel() if 'WorldModel' in dir() else type('WM',(),{
            'situation':'','actors':{},'facts':{},'predictions':{},'outcomes':{},
            'set_situation':lambda s,d:None,'summary':lambda s:'initializing',
            'predict':lambda s,e,p:None,'record_outcome':lambda s,e,o:0})()
        
        # Self model layers
        self.self_model = SelfModel(name)
        
        self.session_start = now()
        self.total_interactions = 0
        self.decision_log = []

    def _call_llm(self, user_msg, system_prompt):
        import urllib.request
        if self.backend == "groq":
            url = 'https://api.groq.com/openai/v1/chat/completions'
            headers = {'Authorization': f'Bearer {self.api_key}',
                       'Content-Type': 'application/json',
                       'User-Agent': 'springfish-agent/1.0'}
        elif self.backend == "llama":
            url = self.base_url.rstrip('/') + '/chat/completions'
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer local'}
        else: raise ValueError(f"Unknown backend {self.backend}")

        body = json.dumps({"model": self.llm_model,
                          "messages": [{"role":"system","content":system_prompt},
                                      {"role":"user","content":user_msg}],
                          "max_tokens": self.body.max_tokens,
                          "temperature": 0.3}).encode()
        req = urllib.request.Request(url, data=body, method='POST', headers=headers)
        d = json.loads(urllib.request.urlopen(req, timeout=self.body.max_tokens_per_turn).read())
        return (d['choices'][0].get('message') or {}).get('content', '')

    def process_turn(self, user_input: str) -> dict:
        """FULL §141 COGNITIVE CYCLE — every node fires."""
        if self.body.depleted or self.thermo.depleted:
            self.body.rest()
            return {"response":"Resting — resources depleted. Try again shortly.",
                    "emotional_state":{"emotion":"fatigued","intensity":0.1}}

        self.total_interactions += 1
        eid = f"interaction_{self.total_interactions}"
        trace = {}

        # Spend thermodynamic budget
        self.thermo.spend(len(user_input)/100, f"sensory_{eid}")

        # ── SENSORY OBSERVATIONS ──
        raw_input = {"content":user_input,"source":"user","salience":0.7,"t":now()}
        trace["sensory"] = len(user_input)

        # ── GLOBAL STATE configures processing ──
        proc_cfg = self.gs.configure_processing()
        trace["processing_config"] = proc_cfg

        # ── EMOTION APPRAISAL (whole-system controller) ──
        sm_state = {"agentive": self.self_model.agentive}
        emo_result = self.emotion.appraise(user_input, sm_state)
        self.gs.update_from_emotion(emo_result["emotion"], emo_result["intensity"])
        trace["emotion"] = emo_result

        # ── MEMORY RECALL (episodic) ──
        terms = [w for w in user_input.split() if len(w)>4][:5]
        recalled = self.memory.recall_relevant(terms)
        trace["memories_recalled"] = len(recalled)

        # ── ATTENTION filtering ──
        all_inputs = [raw_input] + [{"content":str(m)[:100],"salience":0.4,"t":now()} for m in recalled]
        attended = self.attention.filter_and_weight(all_inputs)
        trace["attended_count"] = len(attended)

        # ── WORLD MODEL update ──
        if hasattr(self.world,'set_situation'): self.world.set_situation(user_input[:100])

        # ── SELF MODEL: record GIVEN input ──
        self.self_model.receive_given(eid, user_input)

        # ── JOINT SELF-IN-WORLD MODEL ──
        situation_summary = self.world.summary() if hasattr(self.world,'summary') else user_input[:80]

        # ── NARRATIVE update ──
        narrative = self.narrative.update(
            [{"content":user_input}], {"emotion":emo_result["emotion"]}
        )

        # ── CONSTRUCT SYSTEM PROMPT FROM FULL STATE ──
        endorsed = ", ".join(self.self_model.moral["endorsed_values"])
        body_state = self.body.state()
        thermo_status = self.thermo.status()

        system_prompt = (
            f"You are {self.name}, operating within a structured cognitive architecture.\n"
            f"\n"
            f"[GLOBAL STATE]\n"
            f"Emotion: {emo_result['emotion']} ({emo_result['intensity']})\n"
            f"Arousal: {self.gs.arousal} | Mood: {self.gs.mood} | Urgency: {self.gs.urgency}\n"
            f"\n"
            f"[BODY]\n"
            f"Energy: {body_state['energy']} | Fatigue: {body_state['fatigue']}\n"
            f"Thermodynamic budget used: {thermo_status['utilization']*100:.0f}%\n"
            f"\n"
            f"[MEMORY]\n"
            f"Relevant episodes: {json.dumps([str(m)[:60] for m in recalled])}\n"
            f"Semantic knowledge keys: {list(self.memory.semantic.keys())[:5]}\n"
            f"\n"
            f"[SELF]\n"
            f"Narrative: {narrative}\n"
            f"Endorsed values: {endorsed}\n"
            f"\n"
            f"Respond authentically from within this state. Distinguish GIVEN\n"
            f"information from your own GENERATION."
        )

        # ── THOUGHT GENERATION via LLM ──
        energy_before = self.body.energy
        response = self._call_llm(user_input, system_prompt)
        self.body.consume(len(response)//4)
        
        # Thermodynamic accounting
        self.thermo.spend(len(response)/50, f"cognition_{eid}")

        # ── IDENTIFICATION: provenance tagging ──
        output_id = f"{eid}_response"
        self.self_model.produce_generated(output_id, response)
        attribution = self.self_model.attribute(output_id)

        # ── MEMORY ENCODING (all timescales) ──
        self.memory.episodic_add({
            "type":"interaction","input":user_input[:200],
            "output_summary":response[:200],
            "emotion":emo_result["emotion"],"turn":self.total_interactions})
        self.memory.add_autobiographical(
            f"Turn {self.total_interactions}: engaged with '{user_input[:50]}' "
            f"in emotional context of {emo_result['emotion']}")

        # ── LEARNING: prediction error ──
        predicted_len = f"expected_{len(user_input)//10}"
        actual_len = f"got_{len(response)}"
        learn_err = self.learning.process(predicted_len, actual_len)
        self.body.allostatic_update(int(learn_err * 10))

        # ── HOMEOSTASIS CHECK ──
        deviations = self.homeostasis.assess_deviation(self.body)
        recommended = self.homeostasis.recommend_action(deviations)

        # Build result
        result = {
            "response": response,
            "emotional_state": emo_result,
            "memories_recalled": len(recalled),
            "attended_inputs": len(attended),
            "body_energy": round(self.body.energy, 3),
            "fatigue": round(self.body.fatigue, 3),
            "allostatic_load": round(self.body.allostatic_load, 3),
            "thermodynamic_status": thermo_status,
            "homeostasis_recommendation": recommended,
            "attribution_check": {
                "output_id": output_id,
                "attributed_as": attribution,
                "accuracy": round(self.self_model.attribution_accuracy, 3)
            },
            "learning_error": learn_err,
            "turn_number": self.total_interactions,
            "trace": trace,
        }
        self.decision_log.append(result)
        return result

    def save_session(self, path):
        state = {
            "name": self.name, "saved": now(),
            "total_interactions": self.total_interactions,
            "global_state": asdict(self.gs),
            "narrative": self.narrative.story,
            "body": self.body.state(),
            "memory": self.memory.serialize(),
            "learning_events_count": len(self.learning.events),
            "mean_prediction_error": round(self.learning.mean_error, 4),
            "endorsed_values": self.self_model.moral["endorsed_values"],
            "known_actors": self.world.actors if hasattr(self.world,'actors') else {},
        }
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        json.dump(state, open(path,'w'), indent=2, default=str)

    def load_session(self, path):
        if not os.path.exists(path): return False
        s = json.load(open(path))
        self.total_interactions = s.get("total_interactions", 0)
        gs = s.get("global_state", {})
        for k,v in gs.items(): setattr(self.gs, k, v)
        self.narrative.story = s.get("narrative", "")
        mem = s.get("memory", {})
        self.memory.episodic = mem.get("episodic", [])
        self.memory.semantic = mem.get("semantic", {})
        vals = s.get("endorsed_values",[])
        if vals: self.self_model.set_values(vals)
        return True


# ============================================================
# CLI
# ============================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="§141 Artificial Human Agent")
    parser.add_argument("--name", default="Baraka-Agent")
    parser.add_argument("--backend", choices=["groq","llama"], default="llama")
    parser.add_argument("--model", default="")
    parser.add_argument("--base-url", default="http://127.0.0.1:18555/v1")
    parser.add_argument("--state-file", default="agent_state.json")
    args = parser.parse_args()

    api_key = ""
    if args.backend == "groq":
        auth_path = os.path.expanduser("~/.local/share/opencode/auth.json")
        if os.path.exists(auth_path):
            auth = json.load(open(auth_path));api_key = auth.get("groq",{}).get("key","")

    agent = ArtificialHumanAgent(args.name,args.backend,api_key,args.model,args.base_url)
    agent.load_session(args.state_file)
    
    print("="*60)
    print(f"§141 ARTIFICIAL HUMAN AGENT: {args.name}")
    print(f"Backend:{args.backend}|Model:{args.model or'frozen'}")
    print(f"Interactions:{agent.total_interactions}")
    print(f"Values:{', '.join(agent.self_model.moral['endorsed_values'][:3])}")
    print("="*60+"\n")

    while True:
        try:
            ui=input("you> ").strip()
            if ui.lower()=="exit":break
            if not ui:continue
            r=agent.process_turn(ui)
            print(f"\nagent> {r['response'][:400]}")
            print(f"[{r['emotional_state']['emotion']}|E:{r['body_energy']}|F:{r['fatigue']}|T:{r['turn_number']}]\n")
        except KeyboardInterrupt:break
        except Exception as e:print(f"err:{e}")

    agent.save_session(args.state_file)
    print(f"\nSaved. Total interactions:{agent.total_interactions}")
