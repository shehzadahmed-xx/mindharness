"""Negative-control for fingerprint drift (fix #4).

Audit: "Fingerprint drift is self-reference problem: check is inside harness
being checked. No test for the check itself."

This file is the tested witness that the drift check is not just code but
*exercised*: a fake fingerprint injected mid-run must abort when
strict_fingerprint=True and must be logged-but-not-aborted otherwise.

Run: python3 tests/test_backend_fingerprint_drift.py
     python3 -m pytest tests/test_backend_fingerprint_drift.py -q
No network required — _post_curl is mocked.
"""

from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from harness_core.backend import BackendClient, FingerprintDrift
import harness_core.backend as backend_mod


class _FakeCurl:
    """Sequence (fingerprint, payload) via _post_curl patch."""

    def __init__(self, payloads: list[tuple[str | None, dict]]):
        self.payloads = payloads
        self.calls = 0

    def __call__(self, payload, headers):
        fp, data = self.payloads[min(self.calls, len(self.payloads) - 1)]
        self.calls += 1
        body = {**data}
        if fp is not None:
            body["system_fingerprint"] = fp
        # omit key entirely when fp is None to exercise None branch
        elif "system_fingerprint" in body:
            del body["system_fingerprint"]
        return json.dumps(body).encode(), 200


# ---------------------------------------------------------------------------
# 1. strict_fingerprint=True — fake drift must abort (negative control)
# ---------------------------------------------------------------------------

def test_strict_mode_aborts_on_fake_fingerprint():
    """Injecting a fake fingerprint mid-run aborts the arm in strict mode."""
    opener = _FakeCurl([
        ("fp_A", {"choices": [{"message": {"content": "a"}}], "usage": {}}),
        ("fp_FAKE", {"choices": [{"message": {"content": "b"}}], "usage": {}}),
    ])
    c = BackendClient(api_key="k", strict_fingerprint=True, model="openai/gpt-oss-120b")
    with patch.object(BackendClient, "_post_curl", opener):
        c.simple("first")
        try:
            c.simple("second")
            assert False, "expected FingerprintDrift on fake fingerprint"
        except FingerprintDrift as e:
            assert "fp_A -> fp_FAKE" in str(e)
            assert "strict mode" in str(e).lower()
    # prior call succeeded, second never produced a record
    assert len(c.records) == 1
    # deviation was recorded before abort
    assert any("fp_FAKE" in d for d in c.deviations)
    assert c.fingerprints_seen == ["fp_A", "fp_FAKE"]


def test_strict_mode_abort_message_contains_rotation():
    opener = _FakeCurl([
        ("fp_before", {"choices": [{"message": {"content": "x"}}], "usage": {}}),
        ("fp_after", {"choices": [{"message": {"content": "y"}}], "usage": {}}),
    ])
    c = BackendClient(api_key="k", strict_fingerprint=True)
    with patch.object(BackendClient, "_post_curl", opener):
        c.simple("one")
        try:
            c.simple("two")
            assert False
        except FingerprintDrift as e:
            msg = str(e)
            assert "fp_before" in msg and "fp_after" in msg
            assert "system_fingerprint rotated" in msg


# ---------------------------------------------------------------------------
# 2. strict_fingerprint=False — drift is logged but NOT aborting
# ---------------------------------------------------------------------------

def test_non_strict_logs_drift_without_abort():
    """Without strict mode, drift is recorded in deviations but call succeeds."""
    opener = _FakeCurl([
        ("fp_A", {"choices": [{"message": {"content": "a"}}], "usage": {}}),
        ("fp_B", {"choices": [{"message": {"content": "b"}}], "usage": {}}),
        ("fp_B", {"choices": [{"message": {"content": "c"}}], "usage": {}}),
    ])
    c = BackendClient(api_key="k", strict_fingerprint=False, model="openai/gpt-oss-120b")
    with patch.object(BackendClient, "_post_curl", opener):
        _, r1 = c.simple("first")
        _, r2 = c.simple("second")
        _, r3 = c.simple("third")
    assert r1.fingerprint == "fp_A"
    assert r2.fingerprint == "fp_B"
    assert r3.fingerprint == "fp_B"
    assert len(c.records) == 3
    assert len(c.deviations) == 1
    assert "fp_A -> fp_B" in c.deviations[0]
    assert c.fingerprints_seen == ["fp_A", "fp_B"]


def test_non_strict_multiple_drifts_all_logged():
    opener = _FakeCurl([
        ("fp_1", {"choices": [{"message": {"content": "a"}}], "usage": {}}),
        ("fp_2", {"choices": [{"message": {"content": "b"}}], "usage": {}}),
        ("fp_3", {"choices": [{"message": {"content": "c"}}], "usage": {}}),
    ])
    c = BackendClient(api_key="k", strict_fingerprint=False)
    with patch.object(BackendClient, "_post_curl", opener):
        c.simple("a")
        c.simple("b")
        c.simple("c")
    assert len(c.records) == 3
    assert len(c.deviations) == 2
    assert c.fingerprints_seen == ["fp_1", "fp_2", "fp_3"]


# ---------------------------------------------------------------------------
# 3. Self-reference aware: check is inside harness — test the check itself
# ---------------------------------------------------------------------------

def test_negative_control_injected_via_direct_patch():
    """Fake fingerprint injected by patching internal _fingerprint field.

    This proves the check is not bypassed by mock shape — any path that
    sets self._fingerprint then returns a different fingerprint triggers drift.
    """
    opener = _FakeCurl([
        ("fp_injected", {"choices": [{"message": {"content": "x"}}], "usage": {}}),
    ])
    c = BackendClient(api_key="k", strict_fingerprint=True)
    # simulate prior state as if harness already ran once with a different fp
    c._fingerprint = "fp_original"
    c.fingerprints_seen = ["fp_original"]
    with patch.object(BackendClient, "_post_curl", opener):
        try:
            c.simple("injected")
            assert False, "patched internal fingerprint should still trigger drift"
        except FingerprintDrift as e:
            assert "fp_original -> fp_injected" in str(e)


def test_check_lives_inside_harness():
    """The drift check is inside BackendClient.chat — the self-reference target.

    Guards against the audit failure mode where the check is moved outside the
    harness and the test still passes while the harness itself is unchecked.
    """
    src = inspect.getsource(backend_mod.BackendClient.chat)
    assert "strict_fingerprint" in src, "drift check must reference strict_fingerprint"
    assert "FingerprintDrift" in src, "drift check must raise FingerprintDrift"
    assert "system_fingerprint rotated" in src


# ---------------------------------------------------------------------------
# 4. Negative controls for false positives
# ---------------------------------------------------------------------------

def test_stable_fingerprint_never_drifts():
    opener = _FakeCurl([
        ("fp_same", {"choices": [{"message": {"content": "a"}}], "usage": {}}),
        ("fp_same", {"choices": [{"message": {"content": "b"}}], "usage": {}}),
        ("fp_same", {"choices": [{"message": {"content": "c"}}], "usage": {}}),
    ])
    for strict in (True, False):
        c = BackendClient(api_key="k", strict_fingerprint=strict)
        with patch.object(BackendClient, "_post_curl", opener):
            c.simple("1")
            c.simple("2")
            c.simple("3")
        assert c.deviations == [], f"no deviation when fingerprint stable (strict={strict})"
        assert c.fingerprints_seen == ["fp_same"]
        assert len(c.records) == 3


def test_none_fingerprint_never_triggers_drift():
    """None fingerprints (older providers) must not be treated as drift."""
    opener = _FakeCurl([
        (None, {"choices": [{"message": {"content": "a"}}], "usage": {}}),
        (None, {"choices": [{"message": {"content": "b"}}], "usage": {}}),
        ("fp_real", {"choices": [{"message": {"content": "c"}}], "usage": {}}),
    ])
    c = BackendClient(api_key="k", strict_fingerprint=True)
    with patch.object(BackendClient, "_post_curl", opener):
        _, r1 = c.simple("1")
        _, r2 = c.simple("2")
        _, r3 = c.simple("3")
    assert r1.fingerprint is None
    assert r2.fingerprint is None
    assert c.deviations == []
    assert c.fingerprints_seen == ["fp_real"]


def test_manifest_and_records_still_capture_fingerprint():
    """Per-call manifest fields (Part F) still populated under both modes."""
    opener = _FakeCurl([
        ("fp_X", {"choices": [{"message": {"content": "hi"}}], "usage": {"prompt_tokens": 5, "completion_tokens": 3}}),
    ])
    for strict in (True, False):
        c = BackendClient(api_key="k", strict_fingerprint=strict, seed=42, model="openai/gpt-oss-120b")
        with patch.object(BackendClient, "_post_curl", opener):
            _, rec = c.simple("hello")
        assert rec.fingerprint == "fp_X"
        assert rec.model == "openai/gpt-oss-120b"
        assert rec.seed == 42
        assert rec.prompt_sha256 and rec.response_sha256
        assert rec.ts  # timestamp present


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"  PASS {fn.__name__}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  FAIL {fn.__name__}: {e}")
            import traceback
            traceback.print_exc()
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
