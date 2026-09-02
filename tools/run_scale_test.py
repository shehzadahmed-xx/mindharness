#!/usr/bin/env python3
"""Two open questions from run_ablation_v2.py, settled.

Q1  Is the spotlight organ actually necessary? At n=20 it was directional but
    marginal (wins 0.55 -> 0.15, intervals [0.25,0.90] vs [0.00,0.30]). Because
    the RNG streams are matched per seed, variants are PAIRED -- the correct
    test is the per-seed difference, which is far more powerful than comparing
    independent intervals. Run at high n and use it.

Q2  Does the relational-key transfer result survive a richer environment than a
    5x5 grid? There is a sharp prediction here, and it is the compression claim
    in its most testable form:

        a coordinate store must grow with the AREA of the grid -- more cells,
        and less chance of ever revisiting one;

        a relational store must stay roughly FLAT -- the number of distinct
        local situations (which neighbours are blocked x which way the goal
        lies) does not depend on how big the grid is.

    So as the grid grows, coordinate keys should get worse and relational keys
    should hold. If instead relational degrades with scale, the 5x5 result was
    an artefact of a small state space.

Run: python3 tools/run_scale_test.py
"""

import math
import random
from collections import defaultdict, deque

MOVES = ["up", "down", "left", "right"]
VARIANTS = ["minimal", "sham_watcher", "no_skin", "no_two_mem",
            "no_spotlight", "no_brake", "no_watcher"]


def make_world(seed, n, density=0.15):
    rnd = random.Random(seed)
    walls = set()
    for _ in range(max(3, int(n * n * density))):
        w = (rnd.randrange(n), rnd.randrange(n))
        if w not in [(0, 0), (n - 1, n - 1)]:
            walls.add(w)
    return walls


def _sgn(v):
    return 0 if v == 0 else (1 if v > 0 else -1)


def _pattern(state, mv, move_fn, key_mode, n):
    if key_mode == "coord":
        return f"at {state} → {mv}"
    blocked = "".join("1" if move_fn(state, m) == state else "0" for m in MOVES)
    g = (_sgn(n - 1 - state[0]), _sgn(n - 1 - state[1]))
    return f"blk{blocked}|goal{g} → {mv}"


def _mover(walls, n):
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


# ----------------------------------------------------------------- Q1: organs
def run_variant(variant, seed, n=5, cities=5, steps=None):
    steps = steps or 4 * n
    draw = random.Random(seed)
    pick = random.Random(seed + 7919)
    diag = random.Random(seed + 104729)

    working = deque(maxlen=7 if variant != "no_two_mem" else 0)
    slow, ledger, blocked_seen = defaultdict(float), [], set()
    affect = {"arousal": 0.5}
    energy, fatigue = 1.0, 0.0
    gamma_log = []
    blocked_repeats = 0

    def log_span(source, ref):
        if variant == "no_skin":
            return
        ledger.append({"source": source, "ref": ref})
        if source == "outcome" and ref.startswith("blocked "):
            blocked_seen.add(ref)

    def says_blocked(state, mv):
        if variant == "sham_watcher":
            fake = (pick.randrange(n), pick.randrange(n))
            return f"blocked {fake} {mv}" in blocked_seen
        return f"blocked {state} {mv}" in blocked_seen

    def spotlight(cands):
        if variant == "no_spotlight":
            return pick.choice(cands)
        gain = max(0.5, min(2.0, 0.5 + affect["arousal"]))
        return max(cands, key=lambda c: c["utility"] * c["salience"] * gain)

    def brake(cands):
        nonlocal energy, fatigue
        if variant == "no_brake":
            return cands
        if energy < 0.3:
            cands = [c for c in cands if c["cost"] < 0.5] or \
                    [{"move": "stay", "utility": .1, "salience": .1, "cost": .1}]
        energy = max(0.15, energy - 0.08 * math.log(1 + len(cands)))
        fatigue = min(1.0, fatigue + 0.04)
        return cands

    def watcher(proposed, state):
        if variant == "no_watcher":
            return proposed, False
        if diag.random() >= 0.35:
            return proposed, False
        if says_blocked(state, proposed):
            alts = [m for m in MOVES
                    if m != proposed and not says_blocked(state, m)] or \
                   [m for m in MOVES if m != proposed]
            gamma_log.append(1)
            return pick.choice(alts), True
        gamma_log.append(0)
        return proposed, False

    wins = 0
    for city in range(cities):
        walls = make_world(seed * 1000 + city, n)
        move = _mover(walls, n)
        state, goal = (0, 0), (n - 1, n - 1)
        for _ in range(steps):
            cands = [{"move": m, "utility": draw.random() * 0.6 + 0.4,
                      "salience": draw.random(), "cost": draw.random()}
                     for m in MOVES]
            for c in cands:
                nxt = move(state, c["move"])
                d0 = abs(state[0] - goal[0]) + abs(state[1] - goal[1])
                d1 = abs(nxt[0] - goal[0]) + abs(nxt[1] - goal[1])
                c["utility"] += max(0, (d0 - d1) * 0.2)
                if nxt == state:
                    c["salience"] *= 0.3
            cands = brake(cands)
            w = spotlight(cands)
            log_span("plan", f"state={state}")
            final, changed = watcher(w["move"], state)
            log_span("watcher" if changed else "plan", f"changed={changed}")

            if variant != "no_two_mem" and w["salience"] > 0.5:
                pat = f"at {state} → {final}"
                working.append(pat)
                if sum(1 for p in working if p == pat) >= 2:
                    slow[pat] += 0.1

            nxt = move(state, final)
            if nxt == state:
                key = f"blocked {state} {final}"
                if key in blocked_seen:
                    blocked_repeats += 1
                log_span("outcome", key)
                affect["arousal"] = min(1.0, affect["arousal"] + 0.07)
            state = nxt
            if state == goal:
                wins += 1
                break

    return {"wins": wins, "slow": len(slow), "ledger": len(ledger),
            "gamma": (sum(gamma_log) / len(gamma_log)) if gamma_log else 0.0,
            "blocked_repeats": blocked_repeats, "energy": energy}


# --------------------------------------------------------------- Q2: transfer
def _episode(walls, slow, rng, n, steps, key_mode, learn=None, bias=0.2):
    move = _mover(walls, n)
    working = deque(maxlen=7)
    state, goal = (0, 0), (n - 1, n - 1)
    hits = 0
    for _ in range(steps):
        cands = [{"move": m, "utility": rng.random() * 0.6 + 0.4,
                  "salience": rng.random()} for m in MOVES]
        for c in cands:
            nxt = move(state, c["move"])
            d0 = abs(state[0] - goal[0]) + abs(state[1] - goal[1])
            d1 = abs(nxt[0] - goal[0]) + abs(nxt[1] - goal[1])
            c["utility"] += max(0, (d0 - d1) * bias)
            if nxt == state:
                c["salience"] *= 0.3
            if _pattern(state, c["move"], move, key_mode, n) in slow:
                c["utility"] += 0.3
                hits += 1
        w = max(cands, key=lambda c: c["utility"] * c["salience"])
        final = w["move"]
        if learn is not None and w["salience"] > 0.5:
            pat = _pattern(state, final, move, key_mode, n)
            working.append(pat)
            if sum(1 for p in working if p == pat) >= 2:
                learn[pat] = 0.1
        state = move(state, final)
        if state == goal:
            break
    return {"win": int(state == goal),
            "dist": abs(state[0] - goal[0]) + abs(state[1] - goal[1]),
            "hits": hits}


def shuffle_slow(slow, rng):
    keys = list(slow)
    states = [k.split(" → ")[0] for k in keys]
    moves = [k.split(" → ")[1] for k in keys]
    rng.shuffle(moves)
    return {f"{s} → {m}": 0.1 for s, m in zip(states, moves)}


def run_transfer(seeds, n, key_mode, train_cities=4):
    steps = 4 * n
    out = {a: defaultdict(list) for a in ["intact", "wiped", "shuffled"]}
    sizes = []
    for s in seeds:
        slow = {}
        trng = random.Random(s)
        for c in range(train_cities):
            _episode(make_world(s * 1000 + c, n), slow, trng, n, steps,
                     key_mode, learn=slow)
        sizes.append(len(slow))
        holdout = make_world(s * 1000 + 999, n)
        for arm, store in (("intact", dict(slow)), ("wiped", {}),
                           ("shuffled", shuffle_slow(slow, random.Random(s + 31337)))):
            r = _episode(holdout, store, random.Random(s + 555), n, steps, key_mode)
            for k, v in r.items():
                out[arm][k].append(v)
    return out, sizes


# ------------------------------------------------------------------- analysis
def ci(vals, iters=2000, alpha=0.05, seed=7):
    if not vals:
        return (0.0, 0.0)
    rnd = random.Random(seed)
    k = len(vals)
    s = sorted(sum(rnd.choices(vals, k=k)) / k for _ in range(iters))
    return s[int(alpha / 2 * iters)], s[int((1 - alpha / 2) * iters) - 1]


def mean(v):
    return sum(v) / len(v) if v else 0.0


def paired(a, b):
    d = [x - y for x, y in zip(a, b)]
    lo, hi = ci(d)
    return mean(d), lo, hi, sum(1 for x in d if x != 0)


def main():
    # ---------------- Q1 ----------------
    N1 = 2000
    seeds = list(range(1, N1 + 1))
    print("=" * 92)
    print(f"Q1 — IS SPOTLIGHT NECESSARY?  paired ablation, n={N1} seeds, 5x5 grid")
    print("=" * 92)
    print("Variants share RNG streams per seed, so these are PAIRED comparisons.\n")
    agg = {}
    for v in VARIANTS:
        runs = [run_variant(v, s) for s in seeds]
        agg[v] = {k: [r[k] for r in runs] for k in runs[0]}
    base = agg["minimal"]
    print(f"  {'ablation':14} {'metric':16} {'paired diff vs minimal':34} verdict")
    print("  " + "-" * 84)
    for v, met in [("no_skin", "ledger"), ("no_two_mem", "slow"),
                   ("no_spotlight", "wins"), ("no_brake", "energy"),
                   ("no_watcher", "gamma"), ("no_spotlight", "blocked_repeats"),
                   ("sham_watcher", "blocked_repeats")]:
        m, lo, hi, nz = paired(agg[v][met], base[met])
        sig = "SEPARATES from 0" if (hi < 0 or lo > 0) else "includes 0"
        print(f"  {v:14} {met:16} {m:+8.4f} [{lo:+8.4f},{hi:+8.4f}] {nz:5d}/{N1}  {sig}")
    print(f"\n  minimal wins {mean(base['wins']):.3f}   "
          f"no_spotlight wins {mean(agg['no_spotlight']['wins']):.3f}")

    # ---------------- Q2 ----------------
    N2 = 5000
    tseeds = list(range(1, N2 + 1))
    print("\n" + "=" * 92)
    print(f"Q2 — DOES RELATIONAL TRANSFER SURVIVE A BIGGER WORLD?  n={N2} per cell")
    print("=" * 92)
    print("Prediction: a coordinate store grows with grid AREA and transfers worse;")
    print("a relational store stays flat, because the number of distinct local")
    print("situations does not depend on grid size.\n")
    print(f"  {'grid':>5} {'key':11} {'store':>7} {'hits/ep':>8} "
          f"{'intact-wiped (win)':>28} {'intact-shuffled (win)':>28}")
    print("  " + "-" * 92)
    for g in (5, 8, 12):
        for mode in ("coord", "relational"):
            tr, sizes = run_transfer(tseeds, g, mode)
            mw, lw, hw, _ = paired(tr["intact"]["win"], tr["wiped"]["win"])
            ms, ls, hs, _ = paired(tr["intact"]["win"], tr["shuffled"]["win"])
            tag = lambda lo, hi: "HELPS" if lo > 0 else ("HURTS" if hi < 0 else "null")
            print(f"  {g:5d} {mode:11} {mean(sizes):7.1f} "
                  f"{mean(tr['intact']['hits']):8.1f} "
                  f"{mw:+7.4f}[{lw:+.4f},{hw:+.4f}] {tag(lw,hw):>5} "
                  f"{ms:+7.4f}[{ls:+.4f},{hs:+.4f}] {tag(ls,hs):>5}", flush=True)

    print("\n  Read the store column: if coordinate grows with grid area while")
    print("  relational stays flat, that is compression as a function of scale —")
    print("  and the transfer columns say whether it buys anything.")


if __name__ == "__main__":
    main()
