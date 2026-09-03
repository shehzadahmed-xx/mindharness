#!/usr/bin/env python3
"""Is deletion without a record of deletion actually deletion?

MOTIVATION, stated honestly. The no-deleting theorem says quantum information
is not destroyed under unitary evolution, and Landauer's principle says erasure
is not annihilation but *export* -- the information leaves the system and shows
up as heat. That is physics. The claim tested here is the information-level
*conjecture* the physics motivates, not a consequence of it:

    a damping mechanism with no record of what it discarded does no net work,
    because it cannot distinguish "never learned" from "learned and discarded",
    and so re-acquires what it just dropped.

If true, the damping organ is not independent of the boundary organ: you can
only forget into an outside. If false, erasure works fine without an export
record and the thermodynamic reading does not transfer to this level. Both are
publishable; the second is more interesting.

DESIGN. The relational-key navigator (the variant that transfers), with a
capacity-limited slow store. When the store is full, the lowest-weight pattern
is dropped. Arms differ ONLY in whether that drop is recorded:

  damped_with_record   capacity limit + discard log. A pattern that was
                       previously discarded needs REQ_EVIDENCE sightings to be
                       re-admitted rather than one.
  damped_no_record     capacity limit, discards not recorded. Every pattern is
                       re-admitted on first sighting, discarded or not.
  undamped             no capacity limit. Baseline for what damping buys.

ANTI-RIGGING. The record does NOT block re-admission -- that would guarantee
zero re-acquisitions by construction, which is the failure mode this programme
keeps finding in its own instruments. It only raises the evidence bar. Whether
a higher bar produces a better store is genuinely open: it could clean the
store, or it could lose patterns that were useful.

PRIMARY OUTCOME is B5, held-out transfer -- not the re-acquisition count, which
is closer to mechanical.

Run: python3 experiments/exp_erasure_is_export.py [n_seeds]
"""

from __future__ import annotations

import json
import random
import statistics
import sys
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOVES = ["up", "down", "left", "right"]
GRID = 8
STEPS = 4 * GRID
TRAIN_CITIES = 6
CAP = 10             # slow-store capacity; forgetting only happens when full
REQ_EVIDENCE = 2     # sightings needed to re-admit a previously discarded key
ARMS = ["damped_with_record", "damped_no_record", "undamped"]


def make_world(seed, n=GRID, density=0.15):
    rnd = random.Random(seed)
    walls = set()
    for _ in range(max(3, int(n * n * density))):
        w = (rnd.randrange(n), rnd.randrange(n))
        if w not in [(0, 0), (n - 1, n - 1)]:
            walls.add(w)
    return walls


def _sgn(v):
    return 0 if v == 0 else (1 if v > 0 else -1)


def _mover(walls, n=GRID):
    def move(st, a):
        x, y = st
        if a == "up":
            y = max(0, y - 1)
        elif a == "down":
            y = min(n - 1, y + 1)
        elif a == "left":
            x = max(0, x - 1)
        elif a == "right":
            x = min(n - 1, x + 1)
        return st if (x, y) in walls else (x, y)
    return move


def _key(state, mv, move_fn, n=GRID):
    """Relational key: which neighbours are blocked + coarse goal direction."""
    blocked = "".join("1" if move_fn(state, m) == state else "0" for m in MOVES)
    g = (_sgn(n - 1 - state[0]), _sgn(n - 1 - state[1]))
    return f"blk{blocked}|goal{g} → {mv}"


def episode(walls, slow, rng, arm, learn=None, discarded=None, sightings=None,
            stats=None, bias=0.2):
    move = _mover(walls)
    working = deque(maxlen=7)
    state, goal = (0, 0), (GRID - 1, GRID - 1)
    hits = 0
    for _ in range(STEPS):
        cands = [{"move": m, "utility": rng.random() * 0.6 + 0.4,
                  "salience": rng.random()} for m in MOVES]
        for c in cands:
            nxt = move(state, c["move"])
            d0 = abs(state[0] - goal[0]) + abs(state[1] - goal[1])
            d1 = abs(nxt[0] - goal[0]) + abs(nxt[1] - goal[1])
            c["utility"] += max(0, (d0 - d1) * bias)
            if nxt == state:
                c["salience"] *= 0.3
            if _key(state, c["move"], move) in slow:
                c["utility"] += 0.3
                hits += 1
        w = max(cands, key=lambda c: c["utility"] * c["salience"])
        final = w["move"]

        if learn is not None and w["salience"] > 0.5:
            k = _key(state, final, move)
            working.append(k)
            if sum(1 for p in working if p == k) >= 2:
                sightings[k] = sightings.get(k, 0) + 1
                # re-admission bar: only the recorded arm knows it discarded this
                bar = 1
                if arm == "damped_with_record" and k in discarded:
                    bar = REQ_EVIDENCE
                if k not in learn and sightings[k] >= bar:
                    if k in discarded:
                        stats["reacquired"] += 1
                        discarded.discard(k)
                    learn[k] = 0.1
                    stats["admitted"] += 1
                elif k in learn:
                    learn[k] += 0.02      # reinforce
                # DAMPING: capacity-limited forgetting
                if arm != "undamped" and len(learn) > CAP:
                    victim = min(learn, key=lambda p: learn[p])
                    del learn[victim]
                    stats["dropped"] += 1
                    if arm == "damped_with_record":
                        discarded.add(victim)   # export destination
        state = move(state, final)
        if state == goal:
            break
    return {"win": int(state == goal),
            "dist": abs(state[0] - goal[0]) + abs(state[1] - goal[1]),
            "hits": hits}


def run_seed(seed, arm):
    slow, discarded, sightings = {}, set(), {}
    stats = defaultdict(int)
    trng = random.Random(seed)
    for c in range(TRAIN_CITIES):
        episode(make_world(seed * 1000 + c), slow, trng, arm,
                learn=slow, discarded=discarded, sightings=sightings, stats=stats)
    holdout = make_world(seed * 1000 + 999)
    r = episode(holdout, dict(slow), random.Random(seed + 555), arm)
    net = stats["dropped"] - stats["reacquired"]
    return {"win": r["win"], "dist": r["dist"], "hits": r["hits"],
            "store": len(slow), "dropped": stats["dropped"],
            "reacquired": stats["reacquired"], "net_forgotten": net,
            "reacq_rate": stats["reacquired"] / max(1, stats["dropped"])}


def ci(v, iters=5000, a=0.05, s=7):
    if not v:
        return (0.0, 0.0)
    r = random.Random(s)
    n = len(v)
    m = sorted(sum(r.choices(v, k=n)) / n for _ in range(iters))
    return m[int(a / 2 * iters)], m[int((1 - a / 2) * iters) - 1]


def paired(a, b):
    d = [x - y for x, y in zip(a, b)]
    lo, hi = ci(d)
    return statistics.mean(d), lo, hi


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    seeds = list(range(70001, 70001 + n))
    res = {arm: [run_seed(s, arm) for s in seeds] for arm in ARMS}

    print("=" * 92)
    print(f"ERASURE IS EXPORT — does deletion without a discard record do work?  n={n} seeds")
    print("=" * 92)
    print(f"{'arm':22} {'win':>16} {'store':>7} {'dropped':>8} {'reacq':>7} "
          f"{'reacq_rate':>11} {'net_forgot':>11}")
    print("-" * 92)
    for arm in ARMS:
        r = res[arm]
        w = [x["win"] for x in r]
        lo, hi = ci(w)
        print(f"{arm:22} {statistics.mean(w):.3f}[{lo:.3f},{hi:.3f}] "
              f"{statistics.mean([x['store'] for x in r]):7.2f} "
              f"{statistics.mean([x['dropped'] for x in r]):8.2f} "
              f"{statistics.mean([x['reacquired'] for x in r]):7.2f} "
              f"{statistics.mean([x['reacq_rate'] for x in r]):11.3f} "
              f"{statistics.mean([x['net_forgotten'] for x in r]):11.2f}")

    wr, nr = res["damped_with_record"], res["damped_no_record"]
    print("\nPREREGISTERED VERDICTS")
    print("-" * 92)
    v = []
    rr_nr = statistics.mean([x["reacq_rate"] for x in nr])
    rr_wr = statistics.mean([x["reacq_rate"] for x in wr])
    v.append(("B1  no-record re-acquisition rate > 0.50", rr_nr > 0.50, f"{rr_nr:.3f}"))
    v.append(("B2  with-record re-acquisition rate < 0.10", rr_wr < 0.10, f"{rr_wr:.3f}"))
    net_nr = statistics.mean([x["net_forgotten"] for x in nr])
    drop_nr = statistics.mean([x["dropped"] for x in nr])
    frac = abs(net_nr) / max(1e-9, drop_nr)
    v.append(("B3  no-record net forgetting ~ 0 (|net| < 10% of drops)",
              frac < 0.10, f"|{net_nr:.2f}| / {drop_nr:.2f} = {frac:.3f}"))
    m, lo, hi = paired([x["win"] for x in wr], [x["win"] for x in nr])
    v.append(("B5  PRIMARY with-record beats no-record on held-out win, CI excl 0",
              lo > 0, f"{m:+.4f} [{lo:+.4f},{hi:+.4f}]"))
    for name, ok, detail in v:
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name:58} {detail}")
    print(f"\n  {sum(1 for _,o,_ in v if o)}/{len(v)} held. "
          f"PRIMARY (B5): {'PASS' if v[-1][1] else 'FAIL'}")

    out = ROOT / "experiments/erasure_is_export_results.json"
    out.write_text(json.dumps(
        {"n_seeds": n, "seed_range": [seeds[0], seeds[-1]], "cap": CAP,
         "req_evidence": REQ_EVIDENCE, "grid": GRID,
         "summary": {a: {k: statistics.mean([x[k] for x in res[a]])
                         for k in res[a][0]} for a in ARMS},
         "verdicts": [{"id": x[0].split()[0], "pass": x[1], "detail": x[2],
                       "text": x[0]} for x in v]}, indent=1))
    print(f"  written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
