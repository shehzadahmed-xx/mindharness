#!/usr/bin/env python3
"""Prediction lock for SpringFish held-out scenario C3 (pilot protocol v0.2 §8 step 3).

Fail-closed: refuses to overwrite an existing PREDICTION_LOCK.json; dry-run by
default; writes only with --lock. Standard library only.

Usage:
    python3 prediction_lock.py <predictions_dir> [--operator NAME] [--lock]
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

SCHEMA = "springfish.prediction_lock/v1"
DHAKA = timezone(timedelta(hours=6))
ALLOWED_SUFFIXES = {".json", ".csv", ".md", ".txt", ".yaml", ".yml"}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("predictions_dir")
    ap.add_argument("--operator", default="")
    ap.add_argument("--lock", action="store_true",
                    help="actually write PREDICTION_LOCK.json (default: dry run)")
    args = ap.parse_args()

    root = Path(args.predictions_dir).resolve()
    if not root.is_dir():
        print(f"ERROR: not a directory: {root}"); return 2

    lock_path = root / "PREDICTION_LOCK.json"
    if lock_path.exists():
        print(f"FAIL-CLOSED: {lock_path} already exists — locks are immutable.")
        print("If predictions changed, create a NEW directory and lock that instead.")
        return 1

    files = sorted(
        p for p in root.rglob("*")
        if p.is_file() and p.name != "PREDICTION_LOCK.json"
        and p.suffix.lower() in ALLOWED_SUFFIXES
    )
    if not files:
        print("ERROR: no prediction artifacts found."); return 2

    entries = [{"path": str(p.relative_to(root)), "sha256": sha256_file(p),
                "bytes": p.stat().st_size} for p in files]
    lines = "".join(f"{e['path']}  {e['sha256']}\n" for e in entries)
    root_hash = hashlib.sha256(lines.encode()).hexdigest()

    record = {
        "schema": SCHEMA,
        "locked_at": datetime.now(DHAKA).isoformat(timespec="seconds"),
        "timezone": "Asia/Dhaka",
        "operator": args.operator,
        "heldout_scenario": "C3",
        "freeze_reference": "pilot/HELDOUT_FREEZE.json",
        "prediction_root_sha256": root_hash,
        "root_definition": ("sha256 of ascii-sorted lines '<relpath>  <sha256>' "
                            "newline-terminated, LF endings"),
        "files": entries,
        "binding": ("Agent configurations are frozen as of this hash. The participant "
                    "reveal session may now proceed (protocol §8 step 4). No agent may "
                    "be re-run, re-prompted or re-seeded after this lock."),
    }

    print(f"{len(entries)} files, prediction_root={root_hash}")
    if not args.lock:
        print("DRY RUN — nothing written. Re-run with --lock to write the lock.")
        return 0
    lock_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE {lock_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
