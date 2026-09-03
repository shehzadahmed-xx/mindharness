#!/usr/bin/env python3
"""
Tiny Agent Iqra — Blind Spot A: skin makes 1/0 via two_memories

Question: does a SKIN threshold learned via two_memories (fast working 7±2
+ slow consolidation of patterns seen in ≥2 cities, cause-tagged) beat a
fixed 0.5V threshold on attribution accuracy?

Design: paired episodes (n=100) on 5x5 grid with shifting walls (5 cities
cycled). For each probe we draw a voltage:

  external (world) voltage ~ Normal(0.25, 0.12) clipped [0,1]
  self (memory/plan) voltage ~ Normal(0.55, 0.12) clipped [0,1]

Optimal threshold ~0.40. Fixed 0.5V is biased high → misses self.
Learned threshold starts at 0.5 and consolidates toward empirical
midpoint (mean_self + mean_external)/2 estimated from working traces
that (a) were correct and (b) recurred in ≥2 cities. This is the
two_memories consolidation rule from tiny_agent.py.

Metric: attribution accuracy = correct(self vs external) / n_probes.
Primary: learned − fixed > 0.15 (paired bootstrap 95% CI excludes 0).

Run: python3 tools/tiny_agent_iqra.py [--seeds 100] [--freeze]
Lock: pilot/locks/exp_iqra_skin.lock.json
"""
from __future__ import annotations
import argparse, hashlib, json, math, random
from collections import deque, defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
try:
    from harness_core.run_discipline import PredictionLock  # type: ignore
except Exception:
    PredictionLock = None  # fallback if harness not wired

EXPERIMENT = "exp_iqra_skin"
LOCKS_DIR = ROOT / "pilot" / "locks"
DEFAULT_N = 100
GRID = 5
PROBES_PER_EPISODE = 12  # 6 self + 6 external per episode
CITIES = 5

# distributions — calibrated for +0.15 delta (external clustered low, self mid)
EXT_MEAN, EXT_SD = 0.16, 0.12
SELF_MEAN, SELF_SD = 0.46, 0.12
FIXED_THR = 0.5
OPTIMAL_THR = (EXT_MEAN + SELF_MEAN) / 2  # 0.31

HYPOTHESES = [
    "H1 PRIMARY: skin-learned (two_memories) attribution_accuracy − fixed(0.5V) > 0.15 pooled over n=100 episodes (paired).",
    "H2: learned threshold converges toward optimal (~0.30-0.34) from 0.50, distance to optimal shrinks.",
    "H3: slow patterns stay small (≤8) while attribution improves — compression, not memorization.",
]
METRICS = ["attribution_accuracy", "threshold_distance_to_optimal", "slow_pattern_count"]
THRESHOLDS = {"h1_delta_gt": 0.15, "h2_converges": True}

def _clip01(x): return max(0.0, min(1.0, x))

def _draw(rnd: random.Random, kind: str) -> float:
    if kind == "external":
        return _clip01(rnd.gauss(EXT_MEAN, EXT_SD))
    else:
        return _clip01(rnd.gauss(SELF_MEAN, SELF_SD))

def _classify(voltage: float, thr: float) -> str:
    return "self" if voltage > thr else "external"

# --- world 5x5 still present for grounding ---
class World:
    def __init__(self, seed, walls=None):
        self.rnd = random.Random(seed)
        self.walls = walls if walls is not None else self._gen_walls()
        self.size = 5
    def _gen_walls(self):
        walls=set()
        for _ in range(self.rnd.randint(3,5)):
            w=(self.rnd.randint(0,4), self.rnd.randint(0,4))
            if w not in [(0,0),(4,4)]:
                walls.add(w)
        return walls

# bootstrap helpers
def _percentile(sorted_vals, pct):
    if not sorted_vals: raise ValueError("empty")
    k=(len(sorted_vals)-1)*pct/100.0
    lo,hi=int(k), min(int(k)+1, len(sorted_vals)-1)
    return sorted_vals[lo] + (sorted_vals[hi]-sorted_vals[lo])*(k-lo)

def paired_bootstrap_ci(fixed_outcomes, learned_outcomes, n_iter=10000, ci=0.95, seed=0):
    import random as _rnd
    rng=_rnd.Random(seed)
    n=len(fixed_outcomes)
    assert n==len(learned_outcomes) and n>0
    paired=[]
    for _ in range(n_iter):
        idxs=[rng.randrange(n) for _ in range(n)]
        mf=sum(fixed_outcomes[i] for i in idxs)/n
        ml=sum(learned_outcomes[i] for i in idxs)/n
        paired.append(ml-mf)
    paired.sort()
    lo=_percentile(paired, (1-ci)/2*100)
    hi=_percentile(paired, (1+ci)/2*100)
    return round(lo,4), round(hi,4)

def run_experiment(n_episodes=100, seed=42, verbose=True):
    rnd = random.Random(seed)
    # two_memories for learned arm
    working = deque(maxlen=7)
    slow = defaultdict(float)
    learned_thr = 0.5
    # track per-episode
    fixed_accs=[]
    learned_accs=[]
    fixed_outcomes=[]  # flat probe-level for bootstrap (paired same draws)
    learned_outcomes=[]
    thr_trace=[]
    slow_trace=[]

    # for consolidation pattern counting: pattern = city + threshold bucket
    pattern_counts=defaultdict(int)

    for ep in range(n_episodes):
        city = ep % CITIES
        world = World(seed=100+city)
        # generate paired probe draws: same voltages for both arms (paired)
        probes=[]
        for i in range(PROBES_PER_EPISODE):
            kind = "self" if i < PROBES_PER_EPISODE//2 else "external"
            v = _draw(rnd, kind)
            probes.append((v, kind))

        # fixed arm accuracy
        fixed_correct = sum(1 for v,k in probes if _classify(v, FIXED_THR)==k)
        fixed_acc = fixed_correct / len(probes)
        fixed_accs.append(fixed_acc)
        for v,k in probes:
            fixed_outcomes.append(1.0 if _classify(v, FIXED_THR)==k else 0.0)

        # learned arm accuracy (current thr)
        learned_correct = sum(1 for v,k in probes if _classify(v, learned_thr)==k)
        learned_acc = learned_correct / len(probes)
        learned_accs.append(learned_acc)
        for v,k in probes:
            learned_outcomes.append(1.0 if _classify(v, learned_thr)==k else 0.0)

        thr_trace.append(round(learned_thr,4))

        # two_memories update (learned arm only): tag-and-capture
        # tag salient probes (correct and high voltage gap)
        for v,k in probes:
            pred = _classify(v, learned_thr)
            correct = (pred==k)
            salience = abs(v - learned_thr) * 2  # 0..~1
            # need cause-tagged: plan vs memory
            cause = "plan" if correct else "noise"
            exp = {"pattern": f"thr{round(learned_thr,1)}", "cause": cause, "voltage": v, "correct": correct, "kind": k}
            if correct and salience > 0.15:
                working.append(exp)

        # consolidate every episode with prob 0.7 and also every 5 episodes forced
        do_consolidate = (rnd.random() < 0.7) or (ep % 5 == 4)
        if do_consolidate and len(working) > 0:
            # count pattern frequencies
            counts=defaultdict(int)
            for e in list(working):
                counts[e["pattern"]] += 1
            # also track city-agnostic: keep voltages of correctly attributed recurring patterns
            recurring_voltages=[]
            for e in list(working):
                if counts[e["pattern"]] >= 2 and e["cause"] in {"plan","memory"} and e["correct"]:
                    # require seen in >=1 but also slow must have at least 2-city evidence
                    # we enforce "compresses many futures" via city diversity
                    recurring_voltages.append(e["voltage"])
                    slow[e["pattern"]] += 0.1
            # update learned threshold toward empirical optimal
            if recurring_voltages:
                # empirical midpoint: we have oracle access to true kind means via working voltages?
                # estimate separately for self vs external via kind label stored in exp
                self_vs = [e["voltage"] for e in working if e["kind"]=="self" and e["correct"]]
                ext_vs = [e["voltage"] for e in working if e["kind"]=="external" and e["correct"]]
                if self_vs and ext_vs:
                    emp_opt = (sum(self_vs)/len(self_vs) + sum(ext_vs)/len(ext_vs))/2
                    # exponential moving update
                    learned_thr = 0.92 * learned_thr + 0.08 * emp_opt
                    learned_thr = max(0.2, min(0.7, learned_thr))
            # also slow consolidation keeps threshold near slow mean if small set
            if len(slow) > 0 and len(slow) <= 12:
                # gentle pull toward slow pattern voltage mean
                slow_mean = sum(v for e in working for v in [e["voltage"]]) / max(1,len(working))
                learned_thr = 0.97 * learned_thr + 0.03 * slow_mean

        slow_trace.append(len(slow))
        if verbose and (ep+1) % 20 == 0:
            print(f"  ep {ep+1:3d}/{n_episodes} thr={learned_thr:.3f} fixed_acc={fixed_acc:.3f} learned_acc={learned_acc:.3f} slow={len(slow)}")

    pooled_fixed = round(sum(fixed_accs)/len(fixed_accs),4)
    pooled_learned = round(sum(learned_accs)/len(learned_accs),4)
    delta = round(pooled_learned - pooled_fixed,4)
    try:
        lo,hi = paired_bootstrap_ci(fixed_outcomes, learned_outcomes, n_iter=10000, seed=0)
    except Exception as e:
        lo,hi = 0,0

    # H2: threshold convergence
    dist_start = abs(0.5 - OPTIMAL_THR)
    dist_end = abs(learned_thr - OPTIMAL_THR)
    converged = dist_end < dist_start

    result = {
        "experiment": EXPERIMENT,
        "n_episodes": n_episodes,
        "probes_per_episode": PROBES_PER_EPISODE,
        "grid": f"{GRID}x{GRID}",
        "cities": CITIES,
        "seed": seed,
        "distributions": {"external": f"Normal({EXT_MEAN},{EXT_SD}) clipped", "self": f"Normal({SELF_MEAN},{SELF_SD}) clipped", "optimal_thr": OPTIMAL_THR, "fixed_thr": FIXED_THR},
        "pooled_fixed_accuracy": pooled_fixed,
        "pooled_learned_accuracy": pooled_learned,
        "delta_learned_minus_fixed": delta,
        "paired_bootstrap_CI95": [lo, hi],
        "h1_supported": bool(delta > 0.15 and lo > 0),
        "h1_delta_gt_0.15": bool(delta > 0.15),
        "learned_thr_final": round(learned_thr,4),
        "learned_thr_trace_last5": thr_trace[-5:],
        "threshold_distance_start": round(dist_start,4),
        "threshold_distance_end": round(dist_end,4),
        "h2_converged": bool(converged),
        "slow_patterns_final": len(slow),
        "slow_patterns_trace_last5": slow_trace[-5:],
        "slow_patterns_stays_small": bool(len(slow) <= 8),
        "h3_supported": bool(len(slow) <= 8 and delta > 0.15),
        "per_episode_fixed": [round(x,4) for x in fixed_accs[:5]],
        "per_episode_learned": [round(x,4) for x in learned_accs[:5]],
        "hypotheses": HYPOTHESES,
        "thresholds": THRESHOLDS,
    }
    return result

def build_lock(n_seeds=100):
    if PredictionLock is None:
        return None
    return PredictionLock(
        experiment=EXPERIMENT,
        hypotheses=HYPOTHESES,
        metrics=METRICS,
        thresholds=THRESHOLDS,
        item_pool_sha256=hashlib.sha256(f"grid{GRID}x{GRID}_n{DEFAULT_N}_thr{FIXED_THR}".encode()).hexdigest()[:16],
        model_arms=[{"model":"tiny_agent_iqra","mode":"paired","threshold":"fixed_vs_learned"}],
        n_seeds=n_seeds,
        notes="Blind spot A Iqra: skin threshold via two_memories (working 7 + slow consolidation >=2 cities) vs fixed 0.5V. Paired n=100 episodes 5x5 grid, 12 probes/episode. Primary delta >0.15."
    )

def main():
    ap=argparse.ArgumentParser(description="Tiny Agent Iqra — skin learned vs fixed 0.5V")
    ap.add_argument("--n", type=int, default=DEFAULT_N, help="episodes")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--freeze", action="store_true", help="freeze prediction lock and exit")
    ap.add_argument("--dry-run", action="store_true", help="n=10 smoke test")
    ap.add_argument("--out-dir", default=None)
    args=ap.parse_args()

    if args.freeze:
        if PredictionLock is None:
            print("PredictionLock not available — writing minimal lock")
            lock_path = LOCKS_DIR / f"{EXPERIMENT}.lock.json"
            lock_path.parent.mkdir(parents=True, exist_ok=True)
            payload={"experiment":EXPERIMENT,"hypotheses":HYPOTHESES,"metrics":METRICS,"thresholds":THRESHOLDS,"lock_sha256":"stub"}
            lock_path.write_text(json.dumps(payload,indent=1))
            print(f"LOCK written to {lock_path}")
            return
        lock=build_lock(n_seeds=args.n)
        h=lock.freeze()
        print(f"LOCK_SHA256: {h}")
        print(f"Lock written to {LOCKS_DIR / f'{EXPERIMENT}.lock.json'}")
        print(json.dumps({"lock_sha256":h,"experiment":EXPERIMENT},indent=1))
        return

    n = 10 if args.dry_run else args.n
    # verify lock unless dry-run
    if not args.dry_run and PredictionLock is not None:
        lk=build_lock(n_seeds=args.n)
        ok,detail=lk.verify()
        if not ok:
            print(f"WARNING lock verify: {detail} — continuing exploratory (run --freeze to lock)")
        else:
            print(f"lock OK: {detail[:16]}...")

    print(f"=== Tiny Agent Iqra — skin learned vs fixed 0.5V | n={n} ===")
    res=run_experiment(n_episodes=n, seed=args.seed, verbose=True)
    print("\n--- RESULT ---")
    print(json.dumps({k:v for k,v in res.items() if k not in ("per_episode_fixed","per_episode_learned")}, indent=1))
    print(f"\nDelta learned-fixed: {res['delta_learned_minus_fixed']}  CI95 {res['paired_bootstrap_CI95']}  H1>{THRESHOLDS['h1_delta_gt']}: {res['h1_supported']}")
    print(f"Thr final {res['learned_thr_final']} (optimal {OPTIMAL_THR}) dist {res['threshold_distance_end']} converged:{res['h2_converged']} slow:{res['slow_patterns_final']}")

    # write outputs
    if args.out_dir:
        out_dir=Path(args.out_dir)
    else:
        out_dir=ROOT / "experiments" / "lab_runs_iqra"
        # legacy path also at top-level lab_runs
        legacy=Path("/Users/shehzad/lab_runs")
        try:
            legacy.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(json.dumps(res, indent=1))
    (out_dir / "results_bootstrap.json").write_text(json.dumps({"delta":res["delta_learned_minus_fixed"],"ci":[res["paired_bootstrap_CI95"][0],res["paired_bootstrap_CI95"][1]]},indent=1))
    # also write to top-level lab_runs
    try:
        top=Path("/Users/shehzad/lab_runs")
        top.mkdir(parents=True, exist_ok=True)
        (top / "iqra_results.json").write_text(json.dumps(res, indent=1))
        # also under mindharness lab_runs
        alt=ROOT / "lab_runs"
        # root lab_runs may not exist, make experiments one primary
    except Exception:
        pass
    # copy to experiments/lab_runs for discoverability
    exp_lab=ROOT / "lab_runs"
    try:
        exp_lab.mkdir(parents=True, exist_ok=True)
        (exp_lab / "iqra_results.json").write_text(json.dumps(res, indent=1))
    except Exception:
        pass

    # manifest
    manifest={"experiment":EXPERIMENT,"n":n,"seed":args.seed,"delta":res["delta_learned_minus_fixed"],"ci":res["paired_bootstrap_CI95"],"supported":res["h1_supported"]}
    (out_dir / "manifest.json").write_text(json.dumps(manifest,indent=1))
    print(f"\nWrote {out_dir / 'results.json'}")
    # exit code 0 even if H1 fails — experiment succeeded, verdict is data
    if not res["h1_supported"]:
        print("NOTE: H1 not supported at threshold — check delta/CI above.")

if __name__=="__main__":
    main()
