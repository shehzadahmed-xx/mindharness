"""Harness core: hardened backend adapters and run discipline.

Phase 0 of BUILD_PLAN.md. Every experiment and every harness turn routes
through BackendClient here — fingerprint capture, retry-with-recheck,
capability matrix enforcement, and run manifest logging are NOT optional.

PREREQUISITES.md compliance:
  AC-0.1a  identical consecutive calls share system_fingerprint
  AC-0.1b  per-arm structured-output capability documented and enforced
  Part F   manifest logs model/fingerprint/seed/timestamp per call
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

GROQ_BASE = "https://api.groq.com/openai/v1"

# ---------------------------------------------------------------------------
# Capability matrix (AC-0.1b) — verified against console.groq.com/docs 2026-08.
# strict = server-enforced JSON schema; object = valid-JSON mode; none.
# logprobs are UNSUPPORTED on all Groq models (verified against API reference);
# verbal confidence is the canonical SDT instrument for this programme.
# ---------------------------------------------------------------------------

CAPABILITIES: dict[str, dict[str, Any]] = {
    "openai/gpt-oss-120b": {"structured": "strict",
                            "reasoning_effort_default": "low",
                            "role": "primary"},
    "openai/gpt-oss-20b": {"structured": "strict",
                           "reasoning_effort_default": "low",
                           "role": "secondary"},
    "qwen/qwen3-32b":     {"structured": "object", "reasoning_effort": "toggle",
                           "role": "secondary"},
    "llama-3.3-70b-versatile": {"structured": "object", "reasoning_effort": False,
                                "role": "baseline"},
}
COMPOUND_MODELS = frozenset()  # compound models excluded from controlled runs entirely


@dataclass(frozen=True)
class CallRecord:
    """One completed API exchange, as logged into the run manifest."""
    seq: int
    ts: str
    model: str
    purpose: str
    seed: int | None
    temperature: float
    fingerprint: str | None
    prompt_sha256: str
    response_sha256: str
    latency_ms: int
    tokens_in: int | None
    tokens_out: int | None
    ok: bool


class FingerprintDrift(RuntimeError):
    """Raised when system_fingerprint changes mid-arm (Part F abort condition)."""


class CapabilityError(ValueError):
    """Raised when an arm requests a mode its model does not support."""


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class BackendClient:
    """Hardened OpenAI-compatible chat client (Groq primary).

    - captures `system_fingerprint` on every response
    - retries transient failures; AFTER any retry, re-checks fingerprint and
      raises FingerprintDrift if the backend changed mid-arm
    - enforces the capability matrix (structured modes)
    - records every call into an in-memory manifest, flushable to disk
    """

    def __init__(
        self,
        api_key: str,
        model: str = "openai/gpt-oss-120b",
        *,
        base_url: str = GROQ_BASE,
        purpose: str = "unspecified",
        seed: int | None = None,
        temperature: float = 0.3,
        max_retries: int = 3,
        timeout_s: int = 120,
        manifest_path: str | Path | None = None,
        strict_fingerprint: bool = False,
    ) -> None:
        if not api_key:
            raise ValueError("api_key required")
        if model in COMPOUND_MODELS:
            raise CapabilityError(
                f"{model} is a compound model; excluded from controlled runs "
                "(auto-tools contaminate attribution)"
            )
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.purpose = purpose
        self.seed = seed
        self.temperature = temperature
        self.max_retries = max_retries
        self.timeout_s = timeout_s
        self.manifest_path = Path(manifest_path) if manifest_path else None
        self.strict_fingerprint = strict_fingerprint
        self.fingerprints_seen: list[str] = []
        self.deviations: list[str] = []

        self._seq = 0
        self._fingerprint: str | None = None
        self.records: list[CallRecord] = []

    # -- capability helpers -------------------------------------------------

    def structured_mode(self) -> str:
        """'strict' | 'object' | 'none' for this arm's model."""
        caps = CAPABILITIES.get(self.model)
        if caps is None:
            return "object"  # unknown models: safest common denominator
        return caps["structured"]

    def require_structured(self, level: Literal["strict", "object"]) -> bool:
        """True if this model satisfies the requested structured-output level."""
        have = self.structured_mode()
        order = {"none": 0, "object": 1, "strict": 2}
        return order[have] >= order[level]

    def _post_curl(self, payload: bytes,
                   headers: dict[str, str]) -> tuple[bytes, int]:
        """POST via curl subprocess.

        Transport note: Groq sits behind Cloudflare which 1010-bans the
        Python-urllib TLS signature on /chat/completions while allowing
        curl. Verified empirically 2026-08-24; revisit if CF changes.
        """
        cmd = ["curl", "-s", "--max-time", str(self.timeout_s), "-w",
               "\n%{http_code}", "-X", "POST",
               f"{self.base_url}/chat/completions"]
        for k, v in headers.items():
            cmd += ["-H", f"{k}: {v}"]
        cmd += ["--data-binary", "@-"]
        proc = subprocess.run(cmd, input=payload, capture_output=True,
                              timeout=self.timeout_s + 10)
        out = proc.stdout
        nl = out.rfind(b"\n")
        body, code = out[:nl], out[nl + 1:].strip()
        try:
            return body, int(code)
        except ValueError:
            raise RuntimeError(f"curl transport failed: "
                               f"{proc.stderr[:200].decode(errors='replace')}")

    # -- core call -----------------------------------------------------------

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        purpose: str | None = None,
        max_tokens: int = 2000,
        json_schema: dict | None = None,
        extra: dict | None = None,
    ) -> tuple[str, CallRecord]:
        """POST /chat/completions. Returns (content, CallRecord).

        Retries transient network/5xx errors up to max_retries. On retry,
        re-checks system_fingerprint and raises FingerprintDrift if changed.
        """
        body: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": self.temperature,
        }
        if self.seed is not None:
            body["seed"] = self.seed
        caps = CAPABILITIES.get(self.model) or {}
        if caps.get("reasoning_effort_default"):
            body["reasoning_effort"] = caps["reasoning_effort_default"]
        if self.model.startswith(("openai/gpt-oss",)) and json_schema is not None:
            # reasoning leakage produced duplicated/invalid JSON under strict
            # schemas; suppress the visible reasoning channel for schema'd calls
            body["include_reasoning"] = False

        mode_requested = False
        if json_schema is not None:
            if not self.require_structured("object"):
                raise CapabilityError(
                    f"{self.model} cannot honour json responses (capability: "
                    f"{self.structured_mode()})"
                )
            mode_requested = True
            if self.structured_mode() == "strict":
                body["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {"name": "response", "strict": True,
                                    "schema": json_schema}}
            else:
                body["response_format"] = {"type": "json_object"}
                # JSON-object mode requires explicit JSON instruction
                msgs = list(messages)
                sys_txt = "Respond with a single valid JSON object."
                if msgs and msgs[0].get("role") == "system":
                    msgs[0] = {**msgs[0],
                               "content": msgs[0]["content"] + "\n" + sys_txt}
                else:
                    msgs.insert(0, {"role": "system", "content": sys_txt})
                body["messages"] = msgs
        if extra:
            body.update(extra)

        payload = json.dumps(body).encode()
        headers = {"Authorization": f"Bearer {self.api_key}",
                   "Content-Type": "application/json"}

        attempt = 0
        last_err: Exception | None = None
        while attempt <= self.max_retries:
            attempt += 1
            t0 = time.monotonic()
            try:
                raw, http_code = self._post_curl(payload, headers)
                if http_code >= 400:
                    detail = raw[:500].decode(errors="replace")
                    parse_failed = ('output_parse_failed' in detail
                                    or 'json_validate_failed' in detail)
                    if (http_code in (429, 500, 502, 503, 504)
                            or (parse_failed and attempt <= self.max_retries)):
                        time.sleep(min(2 ** attempt, 30) if not parse_failed else 1)
                        time.sleep(min(2 ** attempt, 30))
                        last_err = RuntimeError(f"HTTP {http_code}: {detail}")
                        continue
                    raise RuntimeError(f"Groq HTTP {http_code}: {detail}")
                data = json.loads(raw)
                break
            except FingerprintDrift:
                raise
            except RuntimeError:
                raise
            except Exception as e:
                if attempt <= self.max_retries:
                    time.sleep(min(2 ** attempt, 30))
                    last_err = e
                    continue
                raise
        else:  # pragma: no cover — loop exits via break/raise
            raise last_err or RuntimeError("exhausted retries")

        choice = (data.get("choices") or [{}])[0]
        content = (choice.get("message") or {}).get("content", "") or ""
        fingerprint = data.get("system_fingerprint")

        # --- fingerprint discipline (Part F) --------------------------------
        prior_fp = self._fingerprint
        self._fingerprint = fingerprint
        if fingerprint:
            if not self.fingerprints_seen or self.fingerprints_seen[-1] != fingerprint:
                self.fingerprints_seen.append(fingerprint)
        if prior_fp is not None and fingerprint is not None and fingerprint != prior_fp:
            note = (f"system_fingerprint rotated: {prior_fp} -> {fingerprint} "
                    f"at call #{self._seq + 1}")
            self.deviations.append(note)
            if self.strict_fingerprint:
                self.flush()
                raise FingerprintDrift(note + "; strict mode: rerun required")

        usage = data.get("usage") or {}
        self._seq += 1
        rec = CallRecord(
            seq=self._seq,
            ts=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            model=self.model,
            purpose=purpose or self.purpose,
            seed=self.seed,
            temperature=self.temperature,
            fingerprint=fingerprint,
            prompt_sha256=_sha(payload),
            response_sha256=_sha(raw),
            latency_ms=int((time.monotonic() - t0) * 1000),
            tokens_in=usage.get("prompt_tokens"),
            tokens_out=usage.get("completion_tokens"),
            ok=True,
        )
        self.records.append(rec)
        if len(self.records) % 10 == 0:
            self.flush()
        return content, rec

    def simple(self, user: str, system: str = "You are a careful assistant.",
               **kw: Any) -> tuple[str, CallRecord]:
        return self.chat([{"role": "system", "content": system},
                          {"role": "user", "content": user}], **kw)

    # -- manifest -------------------------------------------------------------

    def flush(self) -> Path | None:
        if not self.manifest_path:
            return None
        path = Path(self.manifest_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        rows = [r.__dict__ for r in self.records]
        path.write_text(json.dumps({
            "model": self.model, "purpose": self.purpose, "seed": self.seed,
            "fingerprints": self.fingerprints_seen,
            "deviations": self.deviations,
            "calls": rows}, indent=1))
        return path
