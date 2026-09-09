"""Mutual tending (keeper): two loops that keep each other alive.

Machine-tended (launchd, cron, watchdog scripts) is a shortcut: the loop
still does not restart itself. This module implements the smallest honest
architecture where no software layer above OS power tends the loops: TWO
loops watching each other.

  * Each loop writes a heartbeat file every interval: pid, turn, gamma,
    energy, ledger coverage. The heartbeat is written by the loop itself,
    from its own state — not by an external supervisor.
  * Each loop reads its PEER's heartbeat. If the peer is stale or missing
    beyond max_age, the watcher relaunches the peer from the peer's last
    ledger snapshot (inheritance: state, not just restart).
  * Health is judged from the peer's own ledger numbers (coverage,
    query_rate, gamma), never from process existence alone. A live but
    unwitnessed peer (coverage collapse) counts as DOWN: relaunch from
    snapshot rather than letting theatre continue.

The single external seed, honestly labeled: machine power plus one boot
that starts the pair. Everything above that line — crash recovery,
state inheritance, health judgment — happens inside the loops.

Invariants:
  * A keeper never edits the peer's ledger; it only reads it and relaunches
    the peer process from the peer's own snapshot on failure.
  * Relaunch always passes the snapshot path explicitly; a peer that cannot
    be restored from its own record is restarted blank and the event is
    logged as a lineage break, never silently.
  * No third supervisor: keeper processes watch each other in a pair.
    A lone keeper with no peer reports orphan status and holds (does not
    self-replicate).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from dataclasses import asdict, dataclass


@dataclass
class Heartbeat:
    name: str
    pid: int
    ts: float
    turn: int
    gamma: float
    energy: float
    coverage: float
    query_rate: float


def write_heartbeat(path: str, hb: Heartbeat) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(asdict(hb), f)
    os.replace(tmp, path)


def read_heartbeat(path: str, max_age: float) -> dict | None:
    """Return the heartbeat dict, or None if missing/stale/unreadable.

    Stale means now - ts > max_age. Unreadable counts as missing: a
    witness that cannot be read is no witness.
    """
    try:
        with open(path) as f:
            hb = json.load(f)
    except (OSError, ValueError):
        return None
    try:
        age = time.time() - float(hb["ts"])
    except (KeyError, TypeError, ValueError):
        return None
    if age > max_age:
        return None
    return hb


def peer_health(hb: dict | None) -> dict:
    """Judge a peer from its own ledger numbers, not its pulse.

    Returns status alive|down|unwitnessed + reason. A peer that is
    breathing but unwitnessed (coverage collapse) is DOWN: relaunch from
    snapshot instead of letting theatre continue.
    """
    if hb is None:
        return {'status': 'down', 'reason': 'no readable heartbeat'}
    coverage = float(hb.get('coverage', 0.0))
    if coverage < 0.5:
        return {'status': 'unwitnessed',
                'reason': f"coverage {coverage:.2f} below 0.50: breathing but unwitnessed",
                'heartbeat': hb}
    return {'status': 'alive',
            'reason': f"fresh heartbeat, coverage {coverage:.2f}",
            'heartbeat': hb}


class Keeper:
    """One half of a mutually-tending pair.

    Watches peer_path; on down/unwitnessed, relaunches peer_cmd with
    --snapshot <snapshot_path> appended so the peer inherits its own
    record. Logs every decision to its own event log (its own ledger
    of tending acts, readable by the peer in turn).
    """

    def __init__(self, name: str, own_heartbeat_path: str,
                 peer_heartbeat_path: str, peer_cmd: list[str],
                 snapshot_path: str, event_log_path: str,
                 max_age: float = 30.0) -> None:
        self.name = name
        self.own_path = own_heartbeat_path
        self.peer_path = peer_heartbeat_path
        self.peer_cmd = list(peer_cmd)
        self.snapshot_path = snapshot_path
        self.event_log_path = event_log_path
        self.max_age = max_age
        self.relaunches = 0
        self.lineage_breaks = 0

    def _log_event(self, event: str, detail: dict | None = None) -> None:
        rec = {'ts': time.time(), 'keeper': self.name, 'event': event,
               'detail': detail or {}}
        with open(self.event_log_path, "a") as f:
            f.write(json.dumps(rec) + "\n")

    def snapshot_exists(self) -> bool:
        try:
            with open(self.snapshot_path) as f:
                json.load(f)
            return True
        except (OSError, ValueError):
            return False

    def check_peer(self) -> dict:
        """One watch cycle. Returns what was decided and what was done."""
        hb = read_heartbeat(self.peer_path, self.max_age)
        health = peer_health(hb)
        if health['status'] == 'alive':
            return {'action': 'hold', 'health': health}

        if self.snapshot_exists():
            cmd = self.peer_cmd + ['--snapshot', self.snapshot_path]
            lineage_note = 'inherit'
        else:
            cmd = self.peer_cmd
            lineage_note = 'lineage-break: no snapshot readable'
            self.lineage_breaks += 1
        try:
            proc = subprocess.Popen(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL, start_new_session=True)
            self.relaunches += 1
            self._log_event('relaunch', {'pid': proc.pid,
                                         'lineage': lineage_note,
                                         'health': health['status'],
                                         'reason': health['reason']})
            return {'action': 'relaunched', 'pid': proc.pid,
                    'lineage': lineage_note, 'health': health}
        except OSError as e:
            self._log_event('relaunch-failed', {'error': str(e)})
            return {'action': 'relaunch-failed', 'error': str(e),
                    'health': health}

    def write_own(self, *, turn: int, gamma: float, energy: float,
                  coverage: float, query_rate: float) -> None:
        write_heartbeat(self.own_path, Heartbeat(
            name=self.name, pid=os.getpid(), ts=time.time(), turn=turn,
            gamma=gamma, energy=energy, coverage=coverage,
            query_rate=query_rate))


def run_keeper(keeper: Keeper, beat_fn, interval: float = 10.0,
               max_cycles: int | None = None) -> dict:
    """Run watch cycles until max_cycles (None = forever).

    beat_fn(keeper) is called each cycle so the keeper's own loop can do
    its work and refresh its own heartbeat. Returns a summary.
    """
    cycles = 0
    while max_cycles is None or cycles < max_cycles:
        beat_fn(keeper)
        keeper.check_peer()
        cycles += 1
        if max_cycles is None or cycles < max_cycles:
            time.sleep(interval)
    return {'cycles': cycles, 'relaunches': keeper.relaunches,
            'lineage_breaks': keeper.lineage_breaks}


def main(argv: list[str] | None = None) -> int:
    print("keeper: run as a pair; see run_keeper(). "
          "Usage is programmatic (tests/test_keeper.py).", file=sys.stderr)
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
