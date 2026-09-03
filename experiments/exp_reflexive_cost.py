#!/usr/bin/env python3
"""
Reflexive Cost — Blind Spot C: moving P reflexivity cost

Question: what does it cost when P moves because the model reads its own
output as the next P? Frozen P (prompt/prior stays fixed) vs moving P
(prompt = previous output) — measure H(P(t+1),Q) − H(P(t),Q) drift per turn.

Q = fixed task distribution (ground-truth categories over vocab).
P(t) = model's current prior/context distribution over same vocab.
H(P,Q) = cross-entropy H(Q,P) = −Σ Q(v) log P(v)  (how surprised Q is by P).
         Equivalent to KL(Q||P) + H(Q); H(Q) constant so drift tracks KL.

Moving P updates: P(t+1) = α·P(t) + (1−α)·Softmax(bias + output_sample)
where output_sample is drawn from P(t) but biased (self-reinforcement β>0).
This captures reflexivity: reading own output amplifies its own modes.

Design:
  n = 20 independent runs × 12 turns each, paired frozen vs moving on same seed.
  Primary: mean drift per turn Δ = H(P(t+1),Q)−H(P(t),Q) > 0 under moving, ≈0 frozen.
  Also: cumulative drift over 12 turns, and per-turn slope.

Variant: counterfactual vs narrative phrasing of P.
  Counterfactual P0 is already off-Q (higher H0 → drifts faster / same?),
  Narrative P0 is on-Q (drifts slower). We test interaction:
  Δ_moving(counterfactual) vs Δ_moving(narrative).

Run: python3 experiments/exp_reflexive_cost.py [--freeze]
Lock: pilot/locks/exp_reflexive_cost.lock.json
"""
from __future__ import annotations
import argparse, hashlib, json, math, random
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
try:
    from harness_core.run_discipline import PredictionLock  # type: ignore
except Exception:
    PredictionLock = None

EXPERIMENT = "exp_reflexive_cost"
LOCKS_DIR = ROOT / "pilot" / "locks"
N_RUNS = 20
N_TURNS = 12
VOCAB = 8
ALPHA = 0.75  # carry
BETA = 0.9    # self-reinforcement bias (logit boost for sampled mode)
TEMP = 0.9

HYPOTHESES = [
    "H1 PRIMARY: moving P mean drift per turn Δ = H(P(t+1),Q)-H(P(t),Q) > 0 and exceeds frozen P drift (paired, 95% CI excludes 0).",
    "H2: cumulative drift over 12 turns moving >> frozen (moving accumulates, frozen ≈0).",
    "H3 VARIANT: counterfactual-phrased P drifts faster than narrative-phrased P under moving (Δ_cf > Δ_narr).",
]
METRICS = ["drift_per_turn", "cumulative_drift", "variant_delta"]
THRESHOLDS = {"h1_drift_gt": 0.0, "h2_cumulative_gt": 0.1, "h3_cf_gt_narr": True}

# fixed Q: slightly peaked (tasks not uniform)
def make_Q():
    # peaked Q: e.g. [0.25,0.18,0.15,0.12,0.10,0.08,0.07,0.05]
    raw=[0.25,0.18,0.15,0.12,0.10,0.08,0.07,0.05]
    s=sum(raw)
    return [x/s for x in raw]

Q = make_Q()
H_Q = -sum(q*math.log(q+1e-12) for q in Q)

def cross_entropy(P, Q):
    # H(Q,P) = -sum Q log P
    return -sum(q*math.log(max(p,1e-12)) for p,q in zip(P,Q))

def softmax(logits, temp=1.0):
    m=max(logits)
    exps=[math.exp((l-m)/temp) for l in logits]
    s=sum(exps)
    return [e/s for e in exps]

def drift_for_run(rnd: random.Random, Q, variant: str, moving: bool):
    """
    Returns: list of H per turn (len N_TURNS+1) and per-turn drifts.
    variant: 'narrative' (P0 close to Q) vs 'counterfactual' (P0 off-Q)
    moving: if False, P frozen at P0 (drift 0); if True, reflexive update.
    """
    if variant == "narrative":
        # P0 close to Q: small perturbation
        logits=[math.log(max(q,1e-9))+rnd.gauss(0,0.15) for q in Q]
    else:  # counterfactual
        # P0 off-Q: uniform or inverted
        logits=[rnd.gauss(0,0.8) for _ in Q]  # random off-Q
    P = softmax(logits, temp=TEMP)
    Hs=[cross_entropy(P,Q)]
    for t in range(N_TURNS):
        if not moving:
            Hs.append(Hs[0])  # frozen
            continue
        # sample token from current P (model's output)
        r=rnd.random()
        cum=0
        sampled=-1
        for i,p in enumerate(P):
            cum+=p
            if r < cum:
                sampled=i
                break
        if sampled==-1:
            sampled=len(P)-1
        # output distribution = one-hot smoothed then logit-biased toward sampled
        # build next logits: log P + bias on sampled
        logits_next=[]
        for i,p in enumerate(P):
            base=math.log(max(p,1e-9))
            if i==sampled:
                base+=BETA
            # add small noise
            base+=rnd.gauss(0,0.08)
            logits_next.append(base)
        P_next_unnorm=softmax(logits_next, temp=TEMP)
        # mix with α
        P = [ALPHA*p + (1-ALPHA)*pn for p,pn in zip(P, P_next_unnorm)]
        # renormalize
        s=sum(P)
        P=[x/s for x in P]
        Hs.append(cross_entropy(P,Q))
    drifts=[Hs[t+1]-Hs[t] for t in range(N_TURNS)]
    return Hs, drifts

def _percentile(sv,pct):
    if not sv: raise ValueError("empty")
    k=(len(sv)-1)*pct/100.0
    lo,hi=int(k), min(int(k)+1,len(sv)-1)
    return sv[lo] + (sv[hi]-sv[lo])*(k-lo)

def paired_bootstrap_ci(a,b,n_iter=10000,ci=0.95,seed=0):
    import random as _rnd
    rng=_rnd.Random(seed)
    n=len(a)
    assert n==len(b)
    paired=[]
    for _ in range(n_iter):
        idxs=[rng.randrange(n) for _ in range(n)]
        ma=sum(a[i] for i in idxs)/n
        mb=sum(b[i] for i in idxs)/n
        paired.append(mb-ma)
    paired.sort()
    lo=_percentile(paired,(1-ci)/2*100)
    hi=_percentile(paired,(1+ci)/2*100)
    return round(lo,4),round(hi,4)

def run_experiment(n_runs=N_RUNS, n_turns=N_TURNS, seed=42, verbose=True):
    rnd=random.Random(seed)
    # We pair frozen vs moving per run per variant with same P0 seed stream
    # Use separate sub-rnds per run for reproducibility but paired across moving/frozen
    records=[]
    # aggregate per-turn drifts
    moving_drifts_all=[]  # flat per-turn
    frozen_drifts_all=[]
    moving_cf_drifts=[]
    moving_narr_drifts=[]

    for run in range(n_runs):
        sub_seed=rnd.randint(0,2**31-1)
        # narrative variant
        r1=random.Random(sub_seed)
        Hs_f_narr,_=drift_for_run(r1, Q, variant="narrative", moving=False)
        r2=random.Random(sub_seed)
        Hs_m_narr, drifts_m_narr=drift_for_run(r2, Q, variant="narrative", moving=True)
        # counterfactual variant (next sub-seed)
        sub_seed2=rnd.randint(0,2**31-1)
        r3=random.Random(sub_seed2)
        Hs_f_cf,_=drift_for_run(r3, Q, variant="counterfactual", moving=False)
        r4=random.Random(sub_seed2)
        Hs_m_cf, drifts_m_cf=drift_for_run(r4, Q, variant="counterfactual", moving=True)

        # frozen drifts are zero by construction but compute for check
        frozen_drifts_narr=[Hs_f_narr[t+1]-Hs_f_narr[t] for t in range(n_turns)]
        frozen_drifts_cf=[Hs_f_cf[t+1]-Hs_f_cf[t] for t in range(n_turns)]

        moving_drifts_all.extend(drifts_m_narr + drifts_m_cf)
        frozen_drifts_all.extend(frozen_drifts_narr + frozen_drifts_cf)
        moving_narr_drifts.extend(drifts_m_narr)
        moving_cf_drifts.extend(drifts_m_cf)

        records.append({
            "run": run,
            "variant_narr": {"H0": round(Hs_m_narr[0],4), "H12": round(Hs_m_narr[-1],4), "mean_drift": round(sum(drifts_m_narr)/len(drifts_m_narr),4), "cumulative": round(Hs_m_narr[-1]-Hs_m_narr[0],4)},
            "variant_cf": {"H0": round(Hs_m_cf[0],4), "H12": round(Hs_m_cf[-1],4), "mean_drift": round(sum(drifts_m_cf)/len(drifts_m_cf),4), "cumulative": round(Hs_m_cf[-1]-Hs_m_cf[0],4)},
        })
        if verbose and (run+1)%5==0:
            print(f"  run {run+1}/{n_runs} narr drift {sum(drifts_m_narr)/len(drifts_m_narr):.4f} cf drift {sum(drifts_m_cf)/len(drifts_m_cf):.4f}")

    mean_moving = sum(moving_drifts_all)/len(moving_drifts_all) if moving_drifts_all else 0
    mean_frozen = sum(frozen_drifts_all)/len(frozen_drifts_all) if frozen_drifts_all else 0
    mean_moving_cf = sum(moving_cf_drifts)/len(moving_cf_drifts) if moving_cf_drifts else 0
    mean_moving_narr = sum(moving_narr_drifts)/len(moving_narr_drifts) if moving_narr_drifts else 0

    # cumulative (H12-H0) per run moving vs frozen
    cum_moving=[r["variant_narr"]["cumulative"] for r in records] + [r["variant_cf"]["cumulative"] for r in records]
    cum_frozen=[0.0]*len(cum_moving)  # frozen always 0
    cum_mean_moving=sum(cum_moving)/len(cum_moving)

    # bootstrap CI for per-turn drift moving vs frozen
    # we need paired per-turn observations — already paired by construction (same P0)
    # Use flat arrays: each turn is a paired observation
    lo,hi=paired_bootstrap_ci(frozen_drifts_all, moving_drifts_all, n_iter=10000, seed=0)
    lo_cum,hi_cum=paired_bootstrap_ci(cum_frozen, cum_moving, n_iter=10000, seed=1)
    # variant CI cf vs narr
    lo_v,hi_v=paired_bootstrap_ci(moving_narr_drifts, moving_cf_drifts, n_iter=10000, seed=2)

    result={
        "experiment": EXPERIMENT,
        "n_runs": n_runs,
        "n_turns": n_turns,
        "vocab": VOCAB,
        "alpha": ALPHA, "beta": BETA, "temp": TEMP,
        "Q": [round(x,4) for x in Q],
        "H_Q": round(H_Q,4),
        "seed": seed,
        "mean_drift_per_turn_moving": round(mean_moving,4),
        "mean_drift_per_turn_frozen": round(mean_frozen,4),
        "delta_moving_minus_frozen": round(mean_moving - mean_frozen,4),
        "drift_CI95": [lo,hi],
        "h1_supported": bool(mean_moving > 0 and lo > 0),
        "mean_cumulative_moving": round(cum_mean_moving,4),
        "mean_cumulative_frozen": 0.0,
        "cumulative_CI95": [lo_cum, hi_cum],
        "h2_supported": bool(cum_mean_moving > 0.1 and lo_cum > 0),
        "variant_mean_cf": round(mean_moving_cf,4),
        "variant_mean_narr": round(mean_moving_narr,4),
        "variant_delta_cf_minus_narr": round(mean_moving_cf - mean_moving_narr,4),
        "variant_CI95": [lo_v, hi_v],
        "h3_supported": bool(mean_moving_cf > mean_moving_narr and lo_v > 0) if lo_v is not None else False,
        "per_run": records[:3],
        "hypotheses": HYPOTHESES,
        "thresholds": THRESHOLDS,
        "notes": "H(P,Q)=cross-entropy. Moving P reads own sampled token as next context → self-reinforcement β. Frozen P stays at P0."
    }
    return result

def build_lock():
    if PredictionLock is None:
        return None
    return PredictionLock(
        experiment=EXPERIMENT,
        hypotheses=HYPOTHESES,
        metrics=METRICS,
        thresholds=THRESHOLDS,
        item_pool_sha256=hashlib.sha256(f"vocab{VOCAB}_alpha{ALPHA}_beta{BETA}".encode()).hexdigest()[:16],
        model_arms=[{"model":"reflexive_cost","mode":"paired_frozen_vs_moving","variants":["counterfactual","narrative"]}],
        n_seeds=N_RUNS,
        notes=f"Blind spot C moving P reflexivity cost: n={N_RUNS} runs x {N_TURNS} turns paired frozen vs moving, + counterfactual vs narrative variant. Drift H(P(t+1),Q)-H(P(t),Q)."
    )

def main():
    ap=argparse.ArgumentParser(description="Reflexive Cost — frozen P vs moving P")
    ap.add_argument("--runs", type=int, default=N_RUNS)
    ap.add_argument("--turns", type=int, default=N_TURNS)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--freeze", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out-dir", default=None)
    args=ap.parse_args()

    if args.freeze:
        if PredictionLock is None:
            print("PredictionLock not available — writing minimal lock")
            lp=LOCKS_DIR / f"{EXPERIMENT}.lock.json"
            lp.parent.mkdir(parents=True, exist_ok=True)
            lp.write_text(json.dumps({"experiment":EXPERIMENT,"hypotheses":HYPOTHESES,"metrics":METRICS,"thresholds":THRESHOLDS,"lock_sha256":"stub"},indent=1))
            print(f"LOCK -> {lp}")
            return
        lk=build_lock()
        h=lk.freeze()
        print(f"LOCK_SHA256: {h}")
        print(f"Lock -> {LOCKS_DIR / f'{EXPERIMENT}.lock.json'}")
        print(json.dumps({"lock_sha256":h,"experiment":EXPERIMENT},indent=1))
        return

    n_runs=3 if args.dry_run else args.runs
    n_turns=4 if args.dry_run else args.turns

    if not args.dry_run and PredictionLock is not None:
        lk=build_lock()
        ok,detail=lk.verify()
        if not ok:
            print(f"WARNING lock verify: {detail} — continuing exploratory (run --freeze)")
        else:
            print(f"lock OK: {detail[:16]}...")

    print(f"=== Reflexive Cost — frozen vs moving P | runs={n_runs} turns={n_turns} ===")
    res=run_experiment(n_runs=n_runs, n_turns=n_turns, seed=args.seed, verbose=True)
    print("\n--- RESULT ---")
    print(json.dumps({k:v for k,v in res.items() if k!="per_run"}, indent=1))
    print(f"\nPer-turn drift moving {res['mean_drift_per_turn_moving']} vs frozen {res['mean_drift_per_turn_frozen']} delta {res['delta_moving_minus_frozen']} CI95 {res['drift_CI95']} H1:{res['h1_supported']}")
    print(f"Cumulative moving {res['mean_cumulative_moving']} CI95 {res['cumulative_CI95']} H2:{res['h2_supported']}")
    print(f"Variant cf {res['variant_mean_cf']} narr {res['variant_mean_narr']} delta {res['variant_delta_cf_minus_narr']} CI95 {res['variant_CI95']} H3:{res['h3_supported']}")

    if args.out_dir:
        out_dir=Path(args.out_dir)
    else:
        out_dir=ROOT / "experiments" / "lab_runs_reflexive"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(json.dumps(res, indent=1))
    (out_dir / "manifest.json").write_text(json.dumps({"experiment":EXPERIMENT,"runs":n_runs,"turns":n_turns,"seed":args.seed,"h1":res["h1_supported"]},indent=1))
    try:
        top=Path("/Users/shehzad/lab_runs")
        top.mkdir(parents=True, exist_ok=True)
        (top / "reflexive_results.json").write_text(json.dumps(res, indent=1))
        alt=ROOT / "lab_runs"
        alt.mkdir(parents=True, exist_ok=True)
        (alt / "reflexive_results.json").write_text(json.dumps(res, indent=1))
    except Exception:
        pass
    print(f"\nWrote {out_dir / 'results.json'}")

if __name__=="__main__":
    main()
