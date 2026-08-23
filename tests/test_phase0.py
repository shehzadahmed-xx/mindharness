"""Phase 0 acceptance tests: PREREQUISITES.md AC-0.1a/b + Part C.6 locks.

Run: python3 -m pytest tests/test_phase0.py -q   (or directly)
No network required — network paths are mocked.
"""

from __future__ import annotations

import io
import json
import sys
import urllib.error
from pathlib import Path
from unittest.mock import patch, mock_open

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from harness_core.backend import (BackendClient, CapabilityError,
                                  FingerprintDrift)
from harness_core.run_discipline import PredictionLock, hash_items_file


def _fake_response(payload: dict, fingerprint: str):
    raw = json.dumps(payload).encode()

    class R(io.BytesIO):
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self, n=-1): return raw

    return R(raw)


class _FakeURLOpener:
    """Sequence of responses; counts calls; records request bodies."""

    def __init__(self, payloads: list[tuple[str, dict]]):
        self.payloads = payloads
        self.calls = 0
        self.bodies: list[bytes] = []

    def __call__(self, req, timeout=0):
        self.calls += 1
        self.bodies.append(req.data)
        fp, payload = self.payloads[min(self.calls - 1, len(self.payloads) - 1)]
        return _fake_response(payload, fp)


# ---------------------------------------------------------------- AC-0.1a

def test_fingerprint_captured_and_stable():
    opener = _FakeURLOpener([("fp_A", {"choices": [{"message": {"content": "hi"}}],
                                       "system_fingerprint": "fp_A",
                                       "usage": {}}),
                             ("fp_A", {"choices": [{"message": {"content": "ho"}}],
                                       "system_fingerprint": "fp_A",
                                       "usage": {}})])
    c = BackendClient(api_key="k", model="openai/gpt-oss-120b")
    with patch("harness_core.backend.urllib.request.urlopen", opener):
        _, r1 = c.simple("one")
        _, r2 = c.simple("two")
    assert r1.fingerprint == "fp_A" and r2.fingerprint == "fp_A"
    assert len(c.records) == 2


def test_fingerprint_drift_aborts():
    opener = _FakeURLOpener([("fp_A", {"choices": [{"message": {"content": "a"}}],
                                       "system_fingerprint": "fp_A", "usage": {}}),
                             ("fp_B", {"choices": [{"message": {"content": "b"}}],
                                       "system_fingerprint": "fp_B", "usage": {}})])
    c = BackendClient(api_key="k")
    with patch("harness_core.backend.urllib.request.urlopen", opener):
        c.simple("first")
        try:
            c.simple("second")
            raised = False
        except FingerprintDrift as e:
            raised = "fp_A -> fp_B" in str(e)
    assert raised, "mid-arm fingerprint change must raise FingerprintDrift"


# ---------------------------------------------------------------- AC-0.1b

def test_capability_matrix_enforced():
    strict = BackendClient(api_key="k", model="openai/gpt-oss-120b")
    obj = BackendClient(api_key="k", model="qwen/qwen3-32b")
    assert strict.require_structured("strict")
    assert obj.structured_mode() == "object"
    assert not obj.require_structured("strict")
    # object-mode injects a JSON system instruction
    opener = _FakeURLOpener([("fp", {"choices": [{"message": {"content": "{}"}}],
                                     "system_fingerprint": "fp", "usage": {}})])
    with patch("harness_core.backend.urllib.request.urlopen", opener):
        obj.chat([{"role": "user", "content": "x"}], json_schema={"type": "object"})
    body = json.loads(opener.bodies[0])
    assert body["response_format"]["type"] == "json_object"
    assert any("JSON" in m.get("content", "")
               for m in body["messages"] if m["role"] == "system")


def test_compound_models_rejected():
    import harness_core.backend as B
    saved = B.COMPOUND_MODELS
    B.COMPOUND_MODELS = frozenset({"groq/compound"})
    try:
        try:
            BackendClient(api_key="k", model="groq/compound")
            rejected = False
        except CapabilityError:
            rejected = True
        assert rejected
    finally:
        B.COMPOUND_MODELS = saved


def test_transient_retry_then_success():
    """429 then success: retried, no drift raised."""
    calls = {"n": 0}

    class Flaky(_FakeURLOpener):
        def __call__(self, req, timeout=0):
            calls["n"] += 1
            if calls["n"] == 1:
                raise urllib.error.HTTPError(
                    url="x", code=429, msg="rate",
                    hdrs=None, fp=io.BytesIO(b"rate limited"))
            return super().__call__(req, timeout)

    opener = Flaky([("fp", {"choices": [{"message": {"content": "ok"}}],
                            "system_fingerprint": "fp", "usage": {}})])
    c = BackendClient(api_key="k", max_retries=3)
    with patch("harness_core.backend.urllib.request.urlopen", opener), \
         patch("harness_core.backend.time.sleep"):
        text, rec = c.simple("hello")
    assert text == "ok" and rec.ok and calls["n"] == 2


# ------------------------------------------------- Part C.6 prediction locks

def test_prediction_lock_freeze_and_verify():
    tmp_path = Path(__file__).parent / "_tmp_locks"
    tmp_path.mkdir(exist_ok=True)
    import harness_core.run_discipline as rd
    saved_locks = rd.LOCKS_DIR
    rd.LOCKS_DIR = tmp_path
    try:
        lock = PredictionLock(
            experiment="test_exp",
            hypotheses=["H1: harness M-ratio >= raw"],
            metrics=["M-ratio"],
            thresholds={"m_ratio_delta_gt": 0.0},
            item_pool_sha256=hash_items_file(Path(__file__)),
            model_arms=[{"model": "openai/gpt-oss-120b", "role": "primary"}],
            n_seeds=5)
        h = lock.freeze()
        assert len(h) == 64
        ok, detail = lock.verify()
        assert ok and detail == h
        # tamper
        path = tmp_path / "test_exp.lock.json"
        data = json.loads(path.read_text())
        data["thresholds"]["m_ratio_delta_gt"] = 999.0
        path.write_text(json.dumps(data))
        ok2, why = lock.verify()
        assert not ok2 and "TAMPERED" in why
    finally:
        rd.LOCKS_DIR = saved_locks
        import shutil
        shutil.rmtree(tmp_path, ignore_errors=True)


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
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
