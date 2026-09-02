#!/usr/bin/env python3
"""Confirmatory replication of the relational-vs-coordinate transfer result.

Governed by preregs/RELATIONAL_TRANSFER_CONFIRMATORY.md and
pilot/locks/relational_transfer_confirmatory.lock.json, both committed to git
before the first seed here was executed. Seeds 500001..520000 are disjoint from
every range used in the exploratory work (1..20000).

Verifies its own lock before running: if this file or the prereg has changed
since the lock was frozen, the run aborts.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import importlib.util
spec = importlib.util.spec_from_file_location("st", ROOT / "tools" / "run_scale_test.py")
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)

SEED_START, N = 500001, 20000
GRIDS = (5, 8, 12)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def verify_lock():
    lk = ROOT / "pilot/locks/relational_transfer_confirmatory.lock.json"
    d = json.loads(lk.read_text())
    for rel, want in d["frozen_sha256"].items():
        got = sha(ROOT / rel)
        assert got == want, f"LOCK BROKEN: {rel}\n  frozen {want}\n  now    {got}"
    assert d["seed_range"] == [SEED_START, SEED_START + N - 1], "seed range altered"
    print(f"lock verified: {d['lock_id']}  seeds {d['seed_range']}\n")


def main():
    verify_lock()
    seeds = list(range(SEED_START, SEED_START + N))
    res = {}
    print(f"{'grid':>5} {'key':11} {'store':>7} {'hits/ep':>8} {'hits/pat':>9} "
          f"{'intact-wiped':>26} {'intact-shuffled':>26}")
    print("-" * 100)
    for g in GRIDS:
        for mode in ("coord", "relational"):
            tr, sizes = st.run_transfer(seeds, g, mode)
            store = st.mean(sizes)
            hits = st.mean(tr["intact"]["hits"])
            mw, lw, hw, _ = st.paired(tr["intact"]["win"], tr["wiped"]["win"])
            ms, ls, hs, _ = st.paired(tr["intact"]["win"], tr["shuffled"]["win"])
            res[(g, mode)] = dict(store=store, hits=hits, hpp=hits / store,
                                  iw=(mw, lw, hw), ish=(ms, ls, hs))
            print(f"{g:5d} {mode:11} {store:7.2f} {hits:8.1f} {hits/store:9.2f} "
                  f"{mw:+7.4f}[{lw:+.4f},{hw:+.4f}] {ms:+7.4f}[{ls:+.4f},{hs:+.4f}]",
                  flush=True)

    r = res[(5, "relational")]
    c = res[(5, "coord")]
    verdicts = []
    verdicts.append(("R1  relational intact-wiped >= +0.020, CI excl 0",
                     r["iw"][0] >= 0.020 and r["iw"][1] > 0,
                     f"{r['iw'][0]:+.4f} [{r['iw'][1]:+.4f},{r['iw'][2]:+.4f}]"))
    verdicts.append(("R2  PRIMARY relational intact-shuffled >= +0.010, CI excl 0",
                     r["ish"][0] >= 0.010 and r["ish"][1] > 0,
                     f"{r['ish'][0]:+.4f} [{r['ish'][1]:+.4f},{r['ish'][2]:+.4f}]"))
    verdicts.append(("R3  coord intact-wiped <= 0.000",
                     c["iw"][0] <= 0.0, f"{c['iw'][0]:+.4f}"))
    verdicts.append(("R4  coord intact-shuffled CI not entirely above 0",
                     not (c["ish"][1] > 0), f"CI lower {c['ish'][1]:+.4f}"))
    verdicts.append(("R5  relational hits/pattern >= 2x coord",
                     r["hpp"] >= 2 * c["hpp"],
                     f"{r['hpp']:.2f} vs {c['hpp']:.2f} = {r['hpp']/c['hpp']:.2f}x"))
    rel_hpp = [res[(g, "relational")]["hpp"] for g in GRIDS]
    co_hpp = [res[(g, "coord")]["hpp"] for g in GRIDS]
    verdicts.append(("R6  rel hits/pattern strictly up AND coord strictly down",
                     all(a < b for a, b in zip(rel_hpp, rel_hpp[1:])) and
                     all(a > b for a, b in zip(co_hpp, co_hpp[1:])),
                     f"rel {[round(x,2) for x in rel_hpp]} coord {[round(x,2) for x in co_hpp]}"))
    verdicts.append(("R7  relational intact-shuffled CI excl 0 at ALL grids",
                     all(res[(g, "relational")]["ish"][1] > 0 for g in GRIDS),
                     " ".join(f"g{g}:{res[(g,'relational')]['ish'][1]:+.4f}" for g in GRIDS)))

    print("\n" + "=" * 100)
    print("PREREGISTERED VERDICTS")
    print("=" * 100)
    for name, ok, detail in verdicts:
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name:58} {detail}")
    n_pass = sum(1 for _, ok, _ in verdicts if ok)
    print(f"\n  {n_pass}/{len(verdicts)} predictions held. "
          f"PRIMARY (R2): {'PASS' if verdicts[1][1] else 'FAIL'}")

    out = ROOT / "experiments/confirmatory_transfer_results.json"
    out.write_text(json.dumps(
        {"seed_range": [SEED_START, SEED_START + N - 1], "n": N,
         "cells": {f"{g}_{m}": {k: v for k, v in res[(g, m)].items()}
                   for g in GRIDS for m in ("coord", "relational")},
         "verdicts": [{"id": v[0].split()[0], "pass": v[1], "detail": v[2],
                       "text": v[0]} for v in verdicts]}, indent=1, default=str))
    print(f"\n  written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
