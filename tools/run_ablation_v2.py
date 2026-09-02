#!/usr/bin/env python3
"""Navigator ablation, corrected: 8 variants x N seeds, with a reachable watcher.

Two defects in run_all_analysis.py this corrects.

1. THE WATCHER COULD NOT FIRE.
   Its steering branch required a ledger span with source == "memory". No span
   anywhere in either file was ever logged with that source, so the branch was
   unreachable and gamma was 0.00 in all seven variants -- including the intact
   ones. The no_watcher ablation therefore removed something that already did
   nothing. Instrumented over the original: 221 diagnoses fired, 0 spans with
   source "memory", 0 changed acts.

   Fixed by giving the watcher something real to do: consult the record before
   acting. If the ledger already shows this move blocked from this state, veto
   it and take an alternative. gamma = changed/diagnosed becomes a measurement,
   and blocked_repeats measures whether the steering was any use.

2. THE VARIANTS WERE NOT COMPARABLE.
   A single global random.seed(42) was shared across variants, but ablations
   consume different numbers of draws -- no_spotlight calls random.choice,
   no_brake skips the candidate filter -- so each variant saw a different
   candidate stream and a different effective world. Fixed with separate RNG
   streams: for a given seed every variant sees identical worlds and identical
   candidate draws, and only the variant logic differs.

Also removed: hardcoded "+0.571 vs +0.005" and "H(P,Q) ~1.0 -> ~0.47" printed
inside the results block of the original. Nothing in this experiment computes
those; they belong to the swarm/fragility work.

A sham_watcher arm is included -- identical machinery, wrong key. It should
raise gamma without lowering blocked_repeats, which is what separates a watcher
that steers from one that merely performs the checking motion.

Run: python3 tools/run_ablation_v2.py [n_seeds]
"""

import math
import random
import sys
from collections import defaultdict, deque

CITIES, STEPS = 5, 20
MOVES = ["up", "down", "left", "right"]
VARIANTS = ["minimal", "tuned", "sham_watcher", "no_skin", "no_two_mem",
            "no_spotlight", "no_brake", "no_watcher"]


def make_world(seed):
    rnd = random.Random(seed)
    walls = set()
    for _ in range(rnd.randint(3, 5)):
        w = (rnd.randint(0, 4), rnd.randint(0, 4))
        if w not in [(0, 0), (4, 4)]:
            walls.add(w)
    return walls


def run_variant(variant, seed, cities=CITIES, steps=STEPS):
    # Separate streams: `draw` is identical across variants for a given seed, so
    # every variant faces the same worlds and the same candidate values.
    draw = random.Random(seed)
    pick = random.Random(seed + 7919)
    diag = random.Random(seed + 104729)

    working = deque(maxlen=7 if variant != "no_two_mem" else 0)
    slow = defaultdict(float)
    ledger = []
    blocked_seen = set()          # what the record actually contains
    affect = {"valence": 0.0, "arousal": 0.5}
    energy, fatigue = 1.0, 0.0
    gamma_log = []
    blocked_attempts = 0
    blocked_repeats = 0

    def log_span(claim, source, ref):
        if variant == "no_skin":
            return                # no ledger -> leakage, and no record to consult
        ledger.append({"claim": claim, "source": source, "ref": ref})
        if source == "outcome" and ref.startswith("blocked "):
            blocked_seen.add(ref)

    def record_says_blocked(state, mv):
        if variant == "sham_watcher":
            # same form, wrong content: a lookup of identical shape, wrong key
            fake = (pick.randint(0, 4), pick.randint(0, 4))
            return f"blocked {fake} {mv}" in blocked_seen
        return f"blocked {state} {mv}" in blocked_seen

    def spotlight(cands):
        if variant == "no_spotlight":
            return pick.choice(cands)
        gain = max(0.5, min(2.0, 0.5 + affect["arousal"]))
        for c in cands:
            c["bid"] = c["utility"] * c["salience"] * gain
        return max(cands, key=lambda c: c["bid"])

    def brake(cands):
        nonlocal energy, fatigue
        if variant == "no_brake":
            return cands
        if energy < 0.3:
            cands = [c for c in cands if c["cost"] < 0.5]
            if not cands:
                cands = [{"move": "stay", "utility": 0.1,
                          "salience": 0.1, "cost": 0.1}]
        energy = max(0.15, energy - 0.08 * math.log(1 + len(cands)))
        fatigue = min(1.0, fatigue + 0.04)
        return cands

    def watcher(proposed, state):
        """Slower loop consults the record before the act, and may veto it."""
        if variant == "no_watcher":
            return proposed, False
        if diag.random() >= 0.35:          # Stage1 cheap: diagnose sometimes
            return proposed, False
        if record_says_blocked(state, proposed):
            alts = [m for m in MOVES
                    if m != proposed and not record_says_blocked(state, m)]
            if not alts:
                alts = [m for m in MOVES if m != proposed]
            gamma_log.append({"diagnosed": True, "changed": True})
            return pick.choice(alts), True
        gamma_log.append({"diagnosed": True, "changed": False})
        return proposed, False

    def tag_and_capture(pattern, cause, salience):
        if variant == "no_two_mem":
            return
        if salience > 0.5:
            working.append({"pattern": pattern, "cause": cause})

    def consolidate():
        if variant == "no_two_mem":
            return
        seen = defaultdict(int)
        for exp in working:
            seen[exp["pattern"]] += 1
        for exp in working:
            if seen[exp["pattern"]] >= 2 and exp["cause"] in {"plan", "memory"}:
                slow[exp["pattern"]] += 0.1

    total_wins = 0
    for city in range(cities):
        walls = make_world(seed * 1000 + city)

        def move(state, a):
            x, y = state
            if a == "up":
                y = max(0, y - 1)
            elif a == "down":
                y = min(4, y + 1)
            elif a == "left":
                x = max(0, x - 1)
            elif a == "right":
                x = min(4, x + 1)
            nxt = (x, y)
            return state if nxt in walls else nxt

        state, goal = (0, 0), (4, 4)
        for _ in range(steps):
            cands = [{"move": m,
                      "utility": draw.random() * 0.6 + 0.4,
                      "salience": draw.random(),
                      "cost": draw.random()} for m in MOVES]
            bias = 0.8 if variant == "tuned" else 0.2
            for c in cands:
                nxt = move(state, c["move"])
                d_now = abs(state[0] - 4) + abs(state[1] - 4)
                d_nxt = abs(nxt[0] - 4) + abs(nxt[1] - 4)
                c["utility"] += max(0, (d_now - d_nxt) * bias)
                if nxt == state and c["move"] != "stay":
                    c["salience"] *= 0.3
                if variant == "tuned" and f"at {state} → {c['move']}" in slow:
                    c["utility"] += 0.3

            cands = brake(cands)
            winner = spotlight(cands)
            proposed = winner["move"]
            log_span(f"propose {proposed} from {state}",
                     source="plan", ref=f"state={state}")
            final, changed = watcher(proposed, state)
            log_span(f"act {final}", source="watcher" if changed else "plan",
                     ref=f"changed={changed}")

            tag_and_capture(f"at {state} → {final}", "plan", winner["salience"])
            new_state = move(state, final)

            if new_state == state and final != "stay":
                blocked_attempts += 1
                key = f"blocked {state} {final}"
                if key in blocked_seen:
                    blocked_repeats += 1
                log_span(f"blocked at {state} moving {final}",
                         source="outcome", ref=key)
                affect["valence"] = max(-1.0, affect["valence"] - 0.08)
                affect["arousal"] = min(1.0, affect["arousal"] + 0.07)
            elif new_state == goal:
                affect["valence"] = min(1.0, affect["valence"] + 0.1)
                affect["arousal"] = max(0.0, affect["arousal"] - 0.05)

            state = new_state
            if draw.random() < 0.25:
                consolidate()
            if state == goal:
                total_wins += 1
                break

    diagnosed = sum(1 for e in gamma_log if e["diagnosed"])
    changed = sum(1 for e in gamma_log if e["changed"])
    return {"wins": total_wins,
            "slow": len(slow),
            "ledger": len(ledger),
            "gamma": changed / max(1, diagnosed),
            "diagnosed": diagnosed,
            "changed": changed,
            "blocked_attempts": blocked_attempts,
            "blocked_repeats": blocked_repeats,
            "energy": energy,
            "fatigue": fatigue}


def _sgn(v):
    return 0 if v == 0 else (1 if v > 0 else -1)


def _pattern(state, mv, move_fn, key_mode):
    """How an experience is keyed in the slow store.

    coord       'at (x, y) -> move'  — a route fragment. Names the CELL, so it
                is tied to the city it was learned in.
    relational  'blk0101|goal(1,1) -> move' — which neighbours are blocked plus
                the coarse direction of the goal. Names the SITUATION, so it is
                the same key in any city where the same local geometry occurs.

    The agent already computes adjacency (it needs move_fn for the goal bias),
    so the relational key uses no information the coordinate key did not have.
    """
    if key_mode == "coord":
        return f"at {state} → {mv}"
    blocked = "".join("1" if move_fn(state, m) == state else "0" for m in MOVES)
    g = (_sgn(4 - state[0]), _sgn(4 - state[1]))
    return f"blk{blocked}|goal{g} → {mv}"


def _episode(walls, slow, bias, uses_slow, rng, steps=STEPS, learn=None,
             key_mode="coord"):
    """One city. If `learn` is a dict, consolidate into it. Returns stats."""
    working = deque(maxlen=7)
    state, goal = (0, 0), (4, 4)
    blocked = 0
    used_steps = steps
    hits = 0

    def move(st, a):
        x, y = st
        if a == "up":
            y = max(0, y - 1)
        elif a == "down":
            y = min(4, y + 1)
        elif a == "left":
            x = max(0, x - 1)
        elif a == "right":
            x = min(4, x + 1)
        return st if (x, y) in walls else (x, y)

    for t in range(steps):
        cands = [{"move": m, "utility": rng.random() * 0.6 + 0.4,
                  "salience": rng.random(), "cost": rng.random()}
                 for m in MOVES]
        for c in cands:
            nxt = move(state, c["move"])
            d_now = abs(state[0] - 4) + abs(state[1] - 4)
            d_nxt = abs(nxt[0] - 4) + abs(nxt[1] - 4)
            c["utility"] += max(0, (d_now - d_nxt) * bias)
            if nxt == state and c["move"] != "stay":
                c["salience"] *= 0.3
            if uses_slow and _pattern(state, c["move"], move, key_mode) in slow:
                c["utility"] += 0.3
                hits += 1
        winner = max(cands, key=lambda c: c["utility"] * c["salience"])
        final = winner["move"]
        nxt = move(state, final)
        if nxt == state:
            blocked += 1
        if learn is not None and winner["salience"] > 0.5:
            pat = _pattern(state, final, move, key_mode)
            working.append(pat)
            seen = defaultdict(int)
            for p in working:
                seen[p] += 1
            if seen[pat] >= 2:
                learn[pat] = 0.1
        state = nxt
        if state == goal:
            used_steps = t + 1
            break

    return {"win": int(state == goal),
            "dist": abs(state[0] - 4) + abs(state[1] - 4),
            "steps": used_steps,
            "blocked": blocked,
            "hits": hits}


def shuffle_slow(slow, rng):
    """Same size, same states, permuted moves — memory's sham control."""
    keys = list(slow.keys())
    states = [k.split(" → ")[0] for k in keys]
    moves = [k.split(" → ")[1] for k in keys]
    rng.shuffle(moves)
    return {f"{s} → {m}": 0.1 for s, m in zip(states, moves)}


def run_transfer(seeds, train_cities=4, bias=0.2, key_mode="coord"):
    """Held-out-city transfer test.

    Trains one agent per seed on `train_cities` novel cities, then runs a city
    it has never seen — three times, from the same trained state, differing
    only in what the slow store contains:

        intact    the store as learned
        wiped     empty (does having any slow help?)
        shuffled  same size, same states, moves permuted (does the CONTENT help,
                  or only the +0.3 bonus mechanics?)

    Bias is held at `bias` in every arm, so the goal-seeking term is constant
    and slow content is the only thing that varies. The held-out episode uses an
    identical RNG stream across arms, so all three see the same candidate draws.
    """
    out = {a: defaultdict(list) for a in ["intact", "wiped", "shuffled"]}
    slow_sizes = []
    for s in seeds:
        # --- train: identical across arms ---
        slow = {}
        train_rng = random.Random(s)
        for c in range(train_cities):
            _episode(make_world(s * 1000 + c), slow, bias, True, train_rng,
                     learn=slow, key_mode=key_mode)
        slow_sizes.append(len(slow))

        # --- held-out city, never seen ---
        holdout = make_world(s * 1000 + 999)
        arms = {"intact": dict(slow),
                "wiped": {},
                "shuffled": shuffle_slow(slow, random.Random(s + 31337))}
        for arm, store in arms.items():
            r = _episode(holdout, store, bias, True, random.Random(s + 555),
                         key_mode=key_mode)
            for k, v in r.items():
                out[arm][k].append(v)
    return out, slow_sizes


def boot_ci(vals, iters=5000, alpha=0.05, seed=12345):
    """Percentile bootstrap over seeds. Stdlib only."""
    if not vals:
        return (0.0, 0.0)
    rnd = random.Random(seed)
    n = len(vals)
    means = []
    for _ in range(iters):
        means.append(sum(rnd.choice(vals) for _ in range(n)) / n)
    means.sort()
    lo = means[int(alpha / 2 * iters)]
    hi = means[min(iters - 1, int((1 - alpha / 2) * iters))]
    return (lo, hi)


def mean(v):
    return sum(v) / len(v) if v else 0.0


def main():
    n_seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    seeds = list(range(1, n_seeds + 1))

    print("=" * 96)
    print(f"NAVIGATOR ABLATION v2 — {len(VARIANTS)} variants x {n_seeds} seeds "
          f"x {CITIES} cities x {STEPS} steps")
    print("=" * 96)
    print("Fixes: watcher trigger now reachable (consults record, vetoes known-blocked "
          "moves);\n       per-variant RNG streams so all variants see identical worlds "
          "and candidates.")
    print("Metrics: gamma = changed/diagnosed. blocked_repeats = re-attempts of a move "
          "the\n         record already showed blocked — the thing a working watcher "
          "should reduce.\n")

    agg = {}
    for v in VARIANTS:
        runs = [run_variant(v, s) for s in seeds]
        agg[v] = {k: [r[k] for r in runs] for k in runs[0]}

    hdr = (f"{'variant':14} {'wins':>11} {'gamma':>16} "
           f"{'blk_repeats':>18} {'slow':>10} {'ledger':>8} {'energy':>7}")
    print(hdr)
    print("-" * len(hdr))
    for v in VARIANTS:
        a = agg[v]
        wl, wh = boot_ci(a["wins"])
        gl, gh = boot_ci(a["gamma"])
        bl, bh = boot_ci(a["blocked_repeats"])
        print(f"{v:14} {mean(a['wins']):5.2f}[{wl:.1f},{wh:.1f}] "
              f"{mean(a['gamma']):6.3f}[{gl:.3f},{gh:.3f}] "
              f"{mean(a['blocked_repeats']):7.1f}[{bl:5.1f},{bh:5.1f}] "
              f"{mean(a['slow']):9.1f} {mean(a['ledger']):8.1f} "
              f"{mean(a['energy']):7.2f}")

    print("\n--- ORGAN VERDICTS (vs minimal, n=%d seeds) ---\n" % n_seeds)
    base = agg["minimal"]
    checks = [
        ("no_skin", "ledger", "skin", "record destroyed -> nothing to attribute or consult"),
        ("no_two_mem", "slow", "two memories", "nothing consolidated -> cannot keep what was learned"),
        ("no_spotlight", "wins", "spotlight", "selection is random -> no systematic learning"),
        ("no_brake", "energy", "brake", "energy never floors -> runaway"),
        ("no_watcher", "gamma", "watcher", "cannot consult the record -> cannot steer"),
    ]
    for var, metric, organ, expected in checks:
        b, a = mean(base[metric]), mean(agg[var][metric])
        lo, hi = boot_ci(agg[var][metric])
        bl, bh = boot_ci(base[metric])
        sep = "SEPARATES" if (hi < bl or lo > bh) else "no separation"
        print(f"  {organ:14} {metric:7} minimal {b:7.2f}[{bl:.2f},{bh:.2f}] "
              f"-> {var:13} {a:7.2f}[{lo:.2f},{hi:.2f}]   {sep}")
        print(f"                 expected: {expected}")

    print("\n--- SHAM TEST: does watcher CONTENT matter, or only its form? ---\n")
    m, s = agg["minimal"], agg["sham_watcher"]
    for metric in ["gamma", "blocked_repeats", "wins"]:
        ml, mh = boot_ci(m[metric])
        sl, sh = boot_ci(s[metric])
        print(f"  {metric:16} real {mean(m[metric]):7.3f}[{ml:.3f},{mh:.3f}]   "
              f"sham {mean(s[metric]):7.3f}[{sl:.3f},{sh:.3f}]")
    print("\n  A watcher that only performs the motion raises gamma without lowering")
    print("  blocked_repeats. That comparison is the test; the gamma column alone is not.")

    print("\n--- TUNED vs MINIMAL ---\n")
    t = agg["tuned"]
    for metric in ["wins", "slow", "blocked_repeats"]:
        ml, mh = boot_ci(m[metric])
        tl, th = boot_ci(t[metric])
        overlap = not (th < ml or tl > mh)
        print(f"  {metric:16} minimal {mean(m[metric]):7.2f}[{ml:.2f},{mh:.2f}]   "
              f"tuned {mean(t[metric]):7.2f}[{tl:.2f},{th:.2f}]   "
              f"{'intervals overlap' if overlap else 'SEPARATES'}")
    print("\n  Note: fewer slow patterns is consistent with better generalisation AND")
    print("  with less exploration (bias 0.8 visits fewer distinct states). The")
    print("  held-out test below is what separates those.")

    # ------------------------------------------------------------------
    n_t = max(200, n_seeds * 10)
    tseeds = list(range(1, n_t + 1))
    tr, sizes = run_transfer(tseeds)
    print("\n" + "=" * 96)
    print(f"HELD-OUT CITY TRANSFER TEST — train on 4 novel cities, then one never seen "
          f"(n={n_t})")
    print("=" * 96)
    print("Bias fixed at 0.2 in every arm, so goal-seeking is constant and the ONLY")
    print(f"difference is what the slow store holds. Mean store size after training: "
          f"{mean(sizes):.1f} patterns.\n")
    print("  arm         win_rate            dist_to_goal          blocked")
    print("  " + "-" * 74)
    for arm in ["intact", "wiped", "shuffled"]:
        d = tr[arm]
        wl, wh = boot_ci(d["win"])
        dl, dh = boot_ci(d["dist"])
        bl, bh = boot_ci(d["blocked"])
        print(f"  {arm:11} {mean(d['win']):.3f}[{wl:.3f},{wh:.3f}]   "
              f"{mean(d['dist']):5.3f}[{dl:.3f},{dh:.3f}]   "
              f"{mean(d['blocked']):5.2f}[{bl:.2f},{bh:.2f}]")

    print("\n  PAIRED differences (same seed, same held-out city, same RNG stream —")
    print("  so the correct test is the per-seed difference, not independent CIs):\n")
    for a, b, q in [("intact", "wiped", "does carrying a slow store into a NEW city help at all?"),
                    ("intact", "shuffled", "does its CONTENT help, or only the +0.3 bonus mechanics?")]:
        for metric, better in [("dist", "lower"), ("win", "higher")]:
            diffs = [x - y for x, y in zip(tr[a][metric], tr[b][metric])]
            dl, dh = boot_ci(diffs)
            nz = sum(1 for d in diffs if d != 0)
            sig = "SEPARATES from 0" if (dh < 0 or dl > 0) else "includes 0"
            print(f"    {a} - {b:9} [{metric:4}, {better} better]  "
                  f"mean {mean(diffs):+.4f} [{dl:+.4f},{dh:+.4f}]  "
                  f"({nz}/{len(diffs)} pairs differ)   {sig}")
        print(f"      -> {q}\n")

    print("  Reading it: intact beating wiped shows memory transfers. intact beating")
    print("  SHUFFLED is the claim that matters — that is generality rather than the")
    print("  bonus firing on whatever happens to be stored. If intact and shuffled")
    print("  agree, the store's content did no work and only its size did.")


if __name__ == "__main__":
    main()
