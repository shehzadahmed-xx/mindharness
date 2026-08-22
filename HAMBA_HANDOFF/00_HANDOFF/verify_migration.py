#!/usr/bin/env python3
"""Verify every file listed by the SpringFish migration checksum manifest."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
manifest = root / "00_HANDOFF" / "CHECKSUMS.sha256"
failed = []
checked = 0
for line in manifest.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    expected, relative = line.split("  ", 1)
    target = root / relative
    observed = sha256(target) if target.is_file() else "MISSING"
    checked += 1
    if observed != expected:
        failed.append({"path": relative, "expected": expected, "observed": observed})

print(f"checked={checked} mismatches={len(failed)}")
for item in failed[:20]:
    print(item)
raise SystemExit(1 if failed else 0)

