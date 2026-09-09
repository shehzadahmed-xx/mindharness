"""Keeper acceptance tests — mutual tending with no third supervisor.

Run: python3 tests/test_keeper.py   (plain runner, no pytest)
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from harness_core.keeper import (Heartbeat, Keeper, peer_health,
                                 read_heartbeat, run_keeper,
                                 write_heartbeat)

PASS = 0
FAIL = 0


def check(name: str, fn) -> None:
    global PASS, FAIL
    try:
        fn()
        PASS += 1
        print(f"  PASS {name}")
    except Exception as e:  # noqa: BLE001
        FAIL += 1
        print(f"  FAIL {name}: {e}")


def tmp() -> str:
    d = tempfile.mkdtemp(prefix="keeper-test-")
    return d


def fresh_hb(coverage: float = 0.97) -> Heartbeat:
    return Heartbeat(name="a", pid=os.getpid(), ts=time.time(), turn=10,
                     gamma=0.1, energy=0.8, coverage=coverage,
                     query_rate=0.6)


def test_heartbeat_round_trip():
    d = tmp()
    p = os.path.join(d, "hb.json")
    write_heartbeat(p, fresh_hb())
    hb = read_heartbeat(p, max_age=30.0)
    assert hb is not None and hb['coverage'] == 0.97, hb


def test_stale_and_corrupt_read_as_missing():
    d = tmp()
    p = os.path.join(d, "hb.json")
    old = fresh_hb()
    old.ts = time.time() - 1000.0
    write_heartbeat(p, old)
    assert read_heartbeat(p, max_age=30.0) is None
    with open(p, "w") as f:
        f.write("{not json")
    assert read_heartbeat(p, max_age=30.0) is None
    assert read_heartbeat(os.path.join(d, "nope.json"), 30.0) is None


def test_peer_health_judges_ledger_not_pulse():
    assert peer_health(None)['status'] == 'down'
    assert peer_health({**fresh_hb().__dict__, 'coverage': 0.2})['status'] == 'unwitnessed'
    alive = peer_health({**fresh_hb().__dict__, 'coverage': 0.9})
    assert alive['status'] == 'alive', alive


def _keeper_in(d: str, peer_cmd: list[str]) -> Keeper:
    snap = os.path.join(d, "snap.json")
    with open(snap, "w") as f:
        json.dump({'turn': 10, 'note': 'inherit me'}, f)
    return Keeper(name="k", own_heartbeat_path=os.path.join(d, "own.json"),
                  peer_heartbeat_path=os.path.join(d, "peer.json"),
                  peer_cmd=peer_cmd, snapshot_path=snap,
                  event_log_path=os.path.join(d, "events.jsonl"),
                  max_age=30.0)


def test_check_peer_holds_when_alive():
    d = tmp()
    k = _keeper_in(d, [sys.executable, "-c", "pass"])
    write_heartbeat(k.peer_path, fresh_hb(coverage=0.97))
    r = k.check_peer()
    assert r['action'] == 'hold', r
    assert k.relaunches == 0


def test_check_peer_relaunches_from_snapshot_with_inheritance():
    d = tmp()
    marker = os.path.join(d, "snap.started")
    stub = ("import sys; "
            "i = sys.argv.index('--snapshot'); "
            "open(sys.argv[i+1] + '.started', 'w').write('inherited'); ")
    k = _keeper_in(d, [sys.executable, "-c", stub])
    r = k.check_peer()  # no peer heartbeat file: down
    assert r['action'] == 'relaunched', r
    assert r['lineage'] == 'inherit', r
    deadline = time.time() + 10
    while not os.path.exists(os.path.join(d, "snap.json.started")):
        assert time.time() < deadline, "peer stub never started"
        time.sleep(0.2)
    assert k.relaunches == 1
    events = open(k.event_log_path).read()
    assert 'relaunch' in events and 'inherit' in events


def test_lineage_break_logged_when_no_snapshot():
    d = tmp()
    k = Keeper(name="k", own_heartbeat_path=os.path.join(d, "own.json"),
               peer_heartbeat_path=os.path.join(d, "peer.json"),
               peer_cmd=[sys.executable, "-c", "pass"],
               snapshot_path=os.path.join(d, "missing.json"),
               event_log_path=os.path.join(d, "events.jsonl"),
               max_age=30.0)
    r = k.check_peer()
    assert r['action'] == 'relaunched', r
    assert r['lineage'].startswith('lineage-break'), r
    assert k.lineage_breaks == 1


def test_run_keeper_cycles_and_own_beat():
    d = tmp()
    k = _keeper_in(d, [sys.executable, "-c", "pass"])
    write_heartbeat(k.peer_path, fresh_hb(coverage=0.97))

    def beat(kk: Keeper) -> None:
        kk.write_own(turn=11, gamma=0.0, energy=0.9,
                     coverage=0.96, query_rate=0.5)

    out = run_keeper(k, beat, interval=0, max_cycles=3)
    assert out == {'cycles': 3, 'relaunches': 0, 'lineage_breaks': 0}, out
    own = read_heartbeat(k.own_path, max_age=30.0)
    assert own is not None and own['turn'] == 11, own


if __name__ == '__main__':
    for name, fn in sorted(
            [(k, v) for k, v in globals().items() if k.startswith('test_')]):
        check(name, fn)
    print(f"\ntrainer-keeper: {PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)
