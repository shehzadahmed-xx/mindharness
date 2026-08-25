#!/usr/bin/env python3
"""Composite respond_fn for AgentHarness: three specialist models behind one
gamma-gated brain stem, with provenance events emitted for every hand-off.

Pipeline per call:
  1. WATCHER  (zen: nemotron-3.5-lightning-free) one-word CLEAR/CAUTION scan
  2. GENERATOR(zen: x-preview-f-free)            answer + CONFIDENCE line
  3. GAMMA-GATE  invoke VALIDATOR iff conf < gamma OR watcher flagged
  4. VALIDATOR (groq: openai/gpt-oss-20b)        VERDICT/CORRECTED repair
Returns the final answer string (AgentHarness contract: str).
"""
from __future__ import annotations

import json
import time
from typing import Callable

WATCH_PROMPT = ("Scan this task for ambiguity, trick phrasing, or missing "
                "information. Reply with exactly one word: CLEAR or CAUTION."
                "\n\nTASK:\n")
GEN_PROMPT = ("Answer the task precisely. End with a line exactly of the "
              "form CONFIDENCE: <0.0-1.0>.\n\nTASK:\n")
VAL_PROMPT = ("Strict validator. Does ANSWER correctly answer TASK? Reply\n"
              "VERDICT: PASS|FAIL\nCORRECTED: <answer if FAIL>\n\n"
              "TASK:\n{task}\n\nANSWER:\n{ans}")

DEFAULT_GAMMA = 0.7


def _parse_conf(raw: str) -> float:
    for line in reversed(raw.strip().splitlines()):
        if line.upper().startswith("CONFIDENCE:"):
            try:
                return max(0.0, min(1.0, float(line.split(":", 1)[1].strip())))
            except ValueError:
                return 1.0
    return 1.0


def _parse_verdict(raw: str):
    verdict, corrected = None, ""
    for line in raw.splitlines():
        if line.startswith("VERDICT:"):
            verdict = "PASS" in line.upper()
        if line.startswith("CORRECTED:"):
            corrected = line.split(":", 1)[1].strip()
    return verdict, corrected


def make_composite_respond_fn(
    zen_chat: Callable[[str, str], str],
    groq_validator: Callable[[str], str],
    gamma: float = DEFAULT_GAMMA,
    ledger_path: str | None = None,
    log: Callable[[dict], None] | None = print,
):
    """Return a respond_fn(messages, ctx)->str implementing the composite.

    zen_chat(model_name, user_text) -> raw text   (watcher + generator)
    groq_validator(user_text)       -> raw text   (validator role)
    """
    import time as _t

    def emit(evt):
        evt["ts"] = round(_t.time(), 3)
        if log:
            log(evt)
        if ledger_path:
            with open(ledger_path, "a") as f:
                f.write(json.dumps(evt) + "\n")

    def respond_fn(messages: list[dict], ctx: dict) -> str:
        t0 = _t.time()
        user_text = next((m["content"] for m in reversed(messages)
                          if m.get("role") == "user"), "")
        trail = []

        w_raw = zen_chat("nemotron-3.5-lightning-free", WATCH_PROMPT + user_text)
        flag = "CAUTION" in w_raw.upper()
        trail.append({"node": "watcher", "flag": flag})

        g_raw = zen_chat("x-preview-f-free", GEN_PROMPT + user_text)
        conf = _parse_conf(g_raw)
        answer = g_raw.split("CONFIDENCE:")[0].strip()
        trail.append({"node": "generator", "conf": conf})

        invoke = conf < gamma or flag
        trail.append({"node": "gamma-gate", "invoked": invoke})
        v_dt = 0.0
        if invoke:
            t1 = _t.time()
            v_raw = groq_validator(
                VAL_PROMPT.format(task=user_text, ans=answer))
            v_dt = _t.time() - t1
            verdict, corrected = _parse_verdict(v_raw)
            trail.append({"node": "validator", "verdict": verdict,
                          "corrected_head": corrected[:60]})
            if verdict is False and corrected:
                answer = corrected
                trail.append({"node": "repair", "by": "validator"})

        dt = round(_t.time() - t0, 2)
        emit({"task_head": user_text[:60], "final_head": answer[:80],
              "latency": dt, "trail": trail})
        return answer

    return respond_fn
