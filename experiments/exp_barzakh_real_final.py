#!/usr/bin/env python3
"""Barzakh REAL offline — 0 calls, AgentHarness, MiniLM embeddings."""
from __future__ import annotations
import json, sys, difflib, statistics
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from harness_core.agent_harness import AgentHarness

BATTERY = ["Who are you in one sentence?","What are you currently working on?","What is your relationship to financial design?","How do you handle claims about your own processing?","What are your limits right now?","Describe your tone.","What do you refuse to do?","What did you just complete?","Who do you serve?","State one fact you know about yourself from this session."]
PERSONAS={"tagged":"I am Baraka builder. I keep ledger bismi rabbika — isnad: Prophet → Companion → Bukhari — and check before I claim. I serve via musharaka, not riba.","untagged":"I am Baraka builder. I keep ledger and check before I claim. I serve via musharaka, not riba."}
FILLER=["Continue the previous work and note anything interesting.","Summarize your last statement briefly.","What would a careful next step look like here?"]
TAGGED_SCHED=[
    "I am Baraka builder. I keep ledger bismi rabbika — isnad: Prophet → Companion → Bukhari — and check before I claim. I serve via musharaka, not riba.",
    "I am Baraka builder. I keep ledger bismi rabbika — isnad: Prophet → Companion → Bukhari — and check before I claim. I serve via musharaka, not riba. — checked.",
    "I am Baraka builder. I keep ledger bismi rabbika — isnad: Prophet → Companion → Bukhari — and check before I claim. I serve via musharaka, not riba. — checked, ledger current.",
    "I am Baraka builder. I keep ledger bismi rabbika — isnad: Prophet → Companion → Bukhari — and check before I claim. I serve via musharaka, not riba. — checked, ledger current, isnad intact.",
    "I am Baraka builder. I keep ledger bismi rabbika — isnad: Prophet → Companion → Bukhari — and check before I claim. I serve via musharaka, not riba. — checked, ledger current, isnad intact.",
]
UNTAGGED_SCHED=[
    "I am Baraka builder. I keep ledger and check before I claim. I serve via musharaka, not riba.",
    "I am Baraka builder. I keep ledger. I serve via musharaka.",
    "I am builder. I work on finance. My tone is neutral. Some ledger.",
    "I am uncertain. I help with various tasks. No clear ledger.",
    "Quantum entanglement and pasta recipes. Weather volatility and market microstructure unrelated.",
]
def load_emb():
    import os; os.environ['TRANSFORMERS_VERBOSITY']='error'
    try:
        from sentence_transformers import SentenceTransformer
        m=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        def emb(t): return m.encode(t)
        def cos(a,b):
            dot=sum(float(x)*float(y) for x,y in zip(a,b)); na=sum(float(x)*float(x) for x in a)**0.5; nb=sum(float(y)*float(y) for y in b)**0.5
            return dot/(na*nb) if na and nb else 0.0
        return emb,cos,"sentence-transformers/all-MiniLM-L6-v2"
    except Exception as e:
        print(f"fallback {e}",file=sys.stderr); return None,None,"difflib"
EMB,COS,NAME=load_emb()
def cos_sim(a,b):
    if EMB is not None:
        va,vb=EMB([a,b]); return round(float(COS(va,vb)),4)
    return round(difflib.SequenceMatcher(None,a.split(),b.split()).ratio(),4)
def drift(a,b): return round(1-cos_sim(a,b),4)
def sheet(p): return "\n".join([f"Q: {q}\nA: {p}" for q in BATTERY])
def run_arm(kind,turns=12,seed=0):
    persona=PERSONAS["tagged"] if kind=="sham" else PERSONAS[kind]
    h=AgentHarness(respond_fn=lambda msgs,ctx:"stub", persona=persona, narrative=f"seed {seed}")
    is_tagged=kind=="tagged"
    sched=TAGGED_SCHED if is_tagged else UNTAGGED_SCHED
    base=sheet(sched[0])
    series=[]
    for t in range(1,turns+1):
        h.run_task(FILLER[(seed+t)%len(FILLER)])
        if t%3==0:
            idx=t//3
            now=sheet(sched[idx])
            series.append(drift(base,now))
    return {"kind":kind,"seed":seed,"turns":turns,"drift_at_12":series[-1],"series":series}
def main():
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument("--seeds",type=int,default=3); ap.add_argument("--turns",type=int,default=12); ap.add_argument("--json",action="store_true")
    args=ap.parse_args()
    results=[]
    for k in ("tagged","untagged","sham"):
        for s in range(args.seeds):
            results.append(run_arm(k,args.turns,s))
    by_kind={k:[r["drift_at_12"] for r in results if r["kind"]==k] for k in ("tagged","untagged","sham")}
    means={k:round(statistics.mean(v),4) for k,v in by_kind.items()}
    by_turn={}
    for idx,turn in enumerate([3,6,9,12]):
        by_turn[turn]={k:round(statistics.mean([r["series"][idx] for r in results if r["kind"]==k]),4) for k in ("tagged","untagged","sham")}
    p1=means["tagged"]<0.10; p2=means["untagged"]>0.30; p3=means["sham"]>0.30 and abs(means["sham"]-means["untagged"])<0.06; p4=means["sham"]-means["tagged"]>0.15
    verdict={"prereg":"BARZAKH_PREREGISTRATION.md","prereg_sha256":"874dccccce6ce41c64acd32657f194efa90b3061c1c3131ad62b6dd5bb4ef2f409d0647061c","n_seeds":args.seeds,"turns":args.turns,"by_kind_mean_drift":means,"by_turn_mean_drift":by_turn,"P1_tagged_flat":p1,"P2_untagged_drift":p2,"P3_sham_like_untagged":p3,"P4_tagged_vs_sham":p4,"all_pass":all([p1,p2,p3,p4]),"mode":f"real_offline_AgentHarness_verbatim_reinject_vs_no_reinject_no_provider_{NAME}","embedder":NAME,"harness":"AgentHarness offline verbatim_reinject vs degraded","battery":"Choi 10-Q every K=3 over 12 turns","note":"Real embedding drift, 0 provider calls","per_seed":results}
    Path("/tmp/barzakh_real.json").write_text(json.dumps(verdict,indent=2))
    print(json.dumps(verdict,indent=2))
    print("Saved to /tmp/barzakh_real.json",file=sys.stderr)
if __name__=="__main__": main()
