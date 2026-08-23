#!/usr/bin/env python3
"""
§141 Artificial Human Agent — Full Cognitive Architecture
Every node from the Mermaid diagram, implemented as working Python.
LLM = reasoning engine. This harness = everything else that makes it functional.

Usage:
  python artificial_human_agent.py --backend groq
  python artificial_human_agent.py --backend llama
"""
import json, os, sys, time, math, hashlib, argparse
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from typing import Any, Optional

DHAKA = timezone(timedelta(hours=6))
def now(): return datetime.now(DHAKA).isoformat()
def clamp(v, lo=0.0, hi=1.0): return max(lo, min(hi, v))
def hsh(s): return hashlib.sha256(str(s).encode()).hexdigest()[:16]


class Body:
    def __init__(self, max_tokens=2000):
        self.max_tokens = max_tokens; self.tokens_used = 0
        self.energy = 1.0; self.fatigue = 0.0
    def consume(self, tokens):
        self.tokens_used += tokens
        self.energy = clamp(self.energy - (tokens/self.max_tokens)*0.05)
        self.fatigue = clamp(self.fatigue + 0.02)
    def rest(self):
        self.energy = clamp(self.energy+0.2); self.fatigue = clamp(self.fatigue-0.15)
    @property
    def depleted(self): return self.energy < 0.1

@dataclass
class GlobalState:
    arousal: float = 0.5; mood: float = 0.5; motivation: float = 0.7
    attentional_width: float = 0.7; urgency: float = 0.3
    def processing_config(self):
        return {"threat_sensitivity": clamp(self.arousal*(1-self.mood)),
                "exploration": clamp(self.mood*self.attentional_width),
                "speed": clamp(0.5+self.arousal*0.5),
                "risk_tolerance": clamp(self.mood*(1-self.urgency)+0.2),
                "creativity": clamp(self.attentional_width*self.mood)}

class Memory:
    def __init__(self):
        self.working=[];self.episodic=[];self.semantic={};self.autobiographical=[]
    def episodic_add(self,e):
        self.episodic.append({"t":now(),**e})
        if len(self.episodic)>500:self.episodic.pop(0)
    def semantic_learn(self,k,v):self.semantic[k]={"value":v,"learned":now()}
    def autobiographical_add(self,e):self.autobiographical.append({"t":now(),"entry":e})
    def recall(self,terms,limit=10):
        scored=[(sum(1 for t in terms if t.lower() in str(e).lower()),e) for e in self.episodic]
        scored=[(s,e) for s,e in scored if s>0];scored.sort(key=lambda x:-x[0])
        return [e for _,e in scored[:limit]]

class Attention:
    def __init__(self,gs):self.gs=gs
    def filter_inputs(self,inputs):
        cfg=self.gs.processing_config();threat_sens=cfg["threat_sensitivity"]
        scored=[]
        for inp in inputs:
            content=str(inp.get("content","")).lower();base=inp.get("salience",0.5)
            threat_bonus=sum(2 for w in["crisis","failure","loss","risk"]if w in content)*threat_sens
            novelty=inp.get("novelty",0.3)*self.gs.attentional_width
            scored.append({**inp,"weight":clamp(base+threat_bonus+novelty)})
        scored.sort(key=lambda x:-x["weight"])
        return scored[:max(3,int(len(scored)*self.gs.attentional_width))]

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
        self.generated_items.append({"id":eid,"content":str(c)[:200],"source":"SELF"})
    def attribute(self,eid):
        for g in reversed(self.given_items):
            if g["id"]==eid:return"GIVEN"
        for g in reversed(self.generated_items):
            if g["id"]==eid:return"SELF_GENERATED"
        return"UNKNOWN"
    @property
    def attribution_accuracy(self):
        if not self.attribution_log:return-1.0
        return sum(1 for a in self.attribution_log if a.get("correct"))/len(self.attribution_log)
    def set_values(self,v):self.moral["endorsed_values"]=v
    def update_narrative(self,s):self.narrative["story"]=s

class Emotion:
    def __init__(self):self.current="neutral";self.intensity=0.3
    def appraise(self,situation):
        sl=situation.lower()
        tl=sum(2 for w in["crisis","failure","loss"]if w in sl)
        ol=sum(2 for w in["opportunity","growth","success"]if w in sl)
        if tl>ol:emotion,intensity=("concern"if tl<4 else"alarm"),clamp(0.3+tl*0.15)
        elif ol>tl:emotion,intensity=("interest"if ol<4 else"engagement"),clamp(0.3+ol*0.12)
        else:emotion,intensity="neutral",0.3
        self.current,self.intensity=emotion,intensity
        return{"emotion":emotion,"intensity":round(intensity,3),
               "readiness":"heightened" if intensity>0.6 else"normal"}

class Learning:
    def __init__(self):self.errors=[];self.events=[]
    def process(self,pred,outcome):
        err=0.0 if str(pred)==str(outcome)else 1.0
        self.errors.append(err);self.events.append({"pred":str(pred)[:100],"error":err})
        return err
    @property
    def mean_error(self):
        r=self.errors[-20:];return sum(r)/max(len(r),1)

class NarrativeGenerator:
    def __init__(self):self.current=""
    def update(self,events,self_model):
        themes=set()
        for e in events[-3:]:
            c=str(e.get("content",e)).lower()
            if"financ"in c or"invest"in c:themes.add("financial-systems")
            if"conscious"in c:themes.add("consciousness")
            if"loop"in c:themes.add("systems")
        self.current=f"Engaged with:{', '.join(themes)or'general'}. Events:{len(events)}."
        return self.current


class ArtificialHumanAgent:
    """Full §141 cognitive architecture with LLM reasoning engine.
    Every node from the Mermaid diagram wired together."""

    def __init__(self,name="Baraka-Agent",backend="llama",api_key="",model="",base_url="http://127.0.0.1:18555/v1"):
        self.name=name;self.backend=backend;self.api_key=api_key
        self.llm_model=model;self.base_url=base_url
        
        # Body
        self.body=Body(max_tokens=2000)
        # Global state
        self.gs=GlobalState()
        # Memory (multi-timescale)
        self.memory=Memory()
        # Attention
        self.attention=Attention(self.gs)
        # Emotion
        self.emotion=Emotion()
        # World model
        self.world=WorldModel()
        # Self model
        self.self_model=SelfModel(name)
        # Narrative
        self.narrative_gen=NarrativeGenerator()
        # Learning
        self.learning=Learning()
        
        self.session_start=now();self.total_interactions=0;self.decision_log=[]
        
        # Initialize endorsed values
        self.self_model.set_values(["pursue excellence","serve humanity","seek knowledge","act justly"])
        self.self_model.update_narrative(f"{name} initiated.")

    def _call_llm(self,user_msg,system_prompt):
        import urllib.request
        if self.backend=="groq":
            url='https://api.groq.com/openai/v1/chat/completions'
            headers={'Authorization':f'Bearer {self.api_key}','Content-Type':'application/json'}
        elif self.backend=="llama":
            url=self.base_url.rstrip('/')+'/chat/completions'
            headers={'Content-Type':'application/json','Authorization':'Bearer local'}
        body=json.dumps({"model":self.llm_model,
                        "messages":[{"role":"system","content":system_prompt},{"role":"user","content":user_msg}],
                        "max_tokens":1500,"temperature":0.3}).encode()
        req=urllib.request.Request(url,data=body,method='POST',headers=headers)
        d=json.loads(urllib.request.urlopen(req,timeout=120).read())
        return(d['choices'][0].get('message')or{}).get('content','')

    def process_turn(self,user_input:str)->dict:
        self.total_interactions+=1
        eid=f"interaction_{self.total_interactions}"
        trace={}
        
        # Sensory observations
        trace["input_len"]=len(user_input)
        
        # Global state configures processing
        proc_cfg=self.gs.processing_config()
        trace["processing_config"]=proc_cfg
        
        # Emotion appraisal
        emo=self.emotion.appraise(user_input)
        trace["emotion"]=emo
        
        # Memory recall
        terms=[w for w in user_input.split()if len(w)>4][:5]
        recalled=self.memory.recall(terms)
        trace["memories_recalled"]=len(recalled)
        
        # Attention filtering
        raw={"content":user_input,"source":"user","salience":0.7}
        attended=self.attention.filter_inputs([raw]+recalled)
        trace["attended_count"]=len(attended)
        
        # World model update
        self.world.set_situation(user_input[:100])
        
        # Self model — record GIVEN input
        self.self_model.receive_given(eid,user_input)
        
        # Narrative update
        narrative=self.narrative_gen.update([{"content":user_input}],self.self_model)
        
        # Construct system prompt
        endorsed=", ".join(self.self_model.moral["endorsed_values"])
        system_prompt=(f"You are {self.name}. Emotional state:{emo['emotion']}({emo['intensity']}).\n"
                      f"Memories:{json.dumps([str(m)[:60] for m in recalled])}\n"
                      f"Values:{endorsed}\nRespond authentically.")
        
        # LLM reasoning
        body_before=self.body.energy
        response=self._call_llm(user_input,system_prompt)
        self.body.consume(len(response)//4)
        
        # Provenance tagging
        output_id=f"{eid}_response"
        self.self_model.produce_generated(output_id,response)
        attribution=self.self_model.attribute(output_id)
        
        # Memory encoding
        self.memory.episodic_add({"type":"interaction","input":user_input[:200],
                                  "output":response[:200],"emotion":emo["emotion"],
                                  "turn":self.total_interactions})
        
        # Prediction error
        learn_err=self.learning.process(f"expected_{len(user_input)//10}",f"got_{len(response)}")
        
        return{"response":response,"emotional_state":emo,
               "body_energy":round(self.body.energy,3),"fatigue":round(self.body.fatigue,3),
               "attribution":{"output_id":output_id,"attributed_as":attribution},
               "learning_error":learn_err,"trace":trace}

    def save_session(self,path):
        state={"name":self.name,"saved":now(),
               "total_interactions":self.total_interactions,
               "global_state":asdict(self.gs),
               "narrative":self.narrative_gen.current,
               "episodic_memory":self.memory.episodic[-50:],
               "semantic":self.memory.semantic,
               "endorsed_values":self.self_model.moral["endorsed_values"]}
        os.makedirs(os.path.dirname(path)or".",exist_ok=True)
        json.dump(state,open(path,'w'),indent=2,default=str)

    def load_session(self,path):
        if not os.path.exists(path):return False
        s=json.load(open(path));self.total_interactions=s.get("total_interactions",0)
        gs=s.get("global_state",{})
        for k,v in gs.items():setattr(self.gs,k,v)
        self.narrative_gen.current=s.get("narrative","")
        self.memory.episodic=s.get("episodic_memory",[])
        self.memory.semantic=s.get("semantic_memory",{})
        return True


# ============================================================
# CLI
# ============================================================
if __name__=="__main__":
    parser=argparse.ArgumentParser(description="§141 Artificial Human Agent")
    parser.add_argument("--name",default="Baraka-Agent")
    parser.add_argument("--backend",choices=["groq","llama"],default="llama")
    parser.add_argument("--model",default="")
    parser.add_argument("--base-url",default="http://127.0.0.1:18555/v1")
    parser.add_argument("--state-file",default="agent_state.json")
    args=parser.parse_args()

    api_key=""
    if args.backend=="groq":
        auth_path=os.path.expanduser("~/.local/share/opencode/auth.json")
        if os.path.exists(auth_path):
            auth=json.load(open(auth_path));api_key=auth.get("groq",{}).get("key","")

    agent=ArtificialHumanAgent(args.name,args.backend,api_key,args.model,args.base_url)
    agent.load_session(args.state_file)

    print("="*60)
    print(f"§141 ARTIFICIAL HUMAN AGENT: {args.name}")
    print(f"Backend: {args.backend} | Model: {args.model}")
    print(f"Interactions: {agent.total_interactions} | Values: {agent.self_model.moral['endorsed_values'][:3]}")
    print("="*60+"\n")

    while True:
        try:
            user_input=input("you> ").strip()
            if user_input.lower()=="exit":break
            if not user_input:continue
            result=agent.process_turn(user_input)
            print(f"\nagent> {result['response'][:400]}")
            print(f"[{result['emotional_state']['emotion']}|energy:{result['body_energy']}|turn:{result['turn_number']}]\n")
        except KeyboardInterrupt:break
        except Exception as e:print(f"error: {e}")

    agent.save_session(args.state_file)
    print(f"\nSaved. Total interactions: {agent.total_interactions}")
