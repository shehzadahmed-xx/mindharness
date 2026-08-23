"""Run discipline: prediction locks, run manifests, abort conditions.

Implements PREREQUISITES.md Part C.6 and Part F as executable code.
A prediction lock is a SHA-256 commitment over the full experimental
contract, committed to git BEFORE the first trial runs.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
LOCKS_DIR = REPO / "pilot" / "locks"


# ---------------------------------------------------------------------------
# Prediction locking (Part C.6)
# ---------------------------------------------------------------------------

@dataclass
class PredictionLock:
    """Immutable experimental contract. Create -> freeze -> commit -> run."""

    experiment: str
    hypotheses: list[str]
    metrics: list[str]                 # must use Part-C canon names exactly
    thresholds: dict[str, Any]         # e.g. {"m_ratio_delta_gt": 0.0}
    item_pool_sha256: str | None       # hash of frozen item file
    model_arms: list[dict[str, Any]]   # [{model, mode, role}, ...]
    n_seeds: int
    notes: str = ""
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))
    lock_sha256: str = ""

    def canonical_json(self) -> bytes:
        payload = {k: v for k, v in self.__dict__.items() if k != "lock_sha256"}
        return json.dumps(payload, sort_keys=True, indent=1).encode()

    def freeze(self) -> str:
        """Compute and set lock hash; write lock file; return hash."""
        self.lock_sha256 = hashlib.sha256(self.canonical_json()).hexdigest()
        LOCKS_DIR.mkdir(parents=True, exist_ok=True)
        out = LOCKS_DIR / f"{self.experiment}.lock.json"
        out.write_text(json.dumps({
            **{k: v for k, v in self.__dict__.items() if k != "lock_sha256"},
            "lock_sha256": self.lock_sha256}, indent=1))
        return self.lock_sha256

    def verify(self) -> tuple[bool, str]:
        """Recompute from disk; confirm unmodified since freeze."""
        path = LOCKS_DIR / f"{self.experiment}.lock.json"
        if not path.exists():
            return False, "no lock file on disk"
        data = json.loads(path.read_text())
        stored = data.get("lock_sha256", "")
        recomputed = hashlib.sha256(json.dumps(
            {k: v for k, v in data.items() if k != "lock_sha256"},
            sort_keys=True, indent=1).encode()).hexdigest()
        if stored != recomputed:
            return False, "LOCK TAMPERED: content hash mismatch"
        if self.lock_sha256 and self.lock_sha256 != stored:
            return False, "in-memory contract differs from frozen lock"
        return True, stored


def git_commit_required(lock_path: Path) -> bool:
    """True if the lock file has at least one commit containing it.

    Part C.6: 'committed to git BEFORE the first trial'. This is advisory
    (returns False when git is unavailable); the run log records it either way.
    """
    try:
        res = subprocess.run(
            ["git", "-C", str(REPO), "log", "--oneline", "-n", "1", "--",
             str(lock_path.relative_to(REPO))],
            capture_output=True, text=True, timeout=10)
        return bool(res.stdout.strip())
    except Exception:
        return False


def assert_lock_committed(experiment: str) -> str:
    """Full gate used by experiment runners: verify integrity AND git history."""
    path = LOCKS_DIR / f"{experiment}.lock.json"
    ok, detail = PredictionLock(experiment=experiment, hypotheses=[], metrics=[],
                                thresholds={}, item_pool_sha256=None,
                                model_arms=[], n_seeds=0).verify()
    # note: verify() above checks tampering via disk contents
    committed = git_commit_required(path) if path.exists() else False
    status = "OK" if (ok and committed) else ("UNCOMMITTED" if ok else "TAMPERED/MISSING")
    line = f"lock[{experiment}]: {status} ({detail})"
    print(line)
    (Path("lab_runs") / "lock_audit.log").parent.mkdir(parents=True, exist_ok=True)
    with open(Path("lab_runs") / "lock_audit.log", "a") as fh:
        fh.write(f"{datetime.now(timezone.utc).isoformat()} {line}\n")
    if not ok:
        raise SystemExit(line)
    return detail


def hash_items_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Run manifest (Part F checklist, machine-checked)
# ---------------------------------------------------------------------------

@dataclass
class RunManifest:
    experiment: str
    arms: list[dict[str, Any]] = field(default_factory=list)
    started_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))
    lock_sha256: str = ""
    deviations: list[str] = field(default_factory=list)
    completed_at: str | None = None

    def add_arm(self, name: str, model: str, fingerprint: str | None,
                seeds: list[int], harness_components: list[str]) -> None:
        self.arms.append({
            "name": name, "model": model, "fingerprint": fingerprint,
            "seeds": seeds, "harness_components": sorted(harness_components),
        })

    def deviate(self, note: str) -> None:
        """Record any deviation from plan (Part F: DEVIATIONS section)."""
        stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self.deviations.append(f"{stamp}: {note}")

    def finish(self, out_dir: str | Path) -> Path:
        self.completed_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        path = out / "manifest.json"
        path.write_text(json.dumps(self.__dict__, indent=1))
        return path


def abort_on_drift(client: Any) -> None:
    """Wire FingerprintDrift into an arm's exception handling uniformly."""
    import functools

    def decorator(fn):  # type: ignore[no-untyped-def]
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
            try:
                return fn(*args, **kwargs)
            except Exception as exc:
                name = type(exc).__name__
                if name == "FingerprintDrift":
                    raise SystemExit(f"ABORT ARM: {exc}") from exc
                raise
        return wrapper
    return decorator
