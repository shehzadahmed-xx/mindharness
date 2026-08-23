#!/usr/bin/env python3
"""LLM shim proxy for SpringFish (frozen engine, zero modification).

Listens on 127.0.0.1:18080 (engine default LLM_BASE_URL). Receives the engine's
llama.cpp-flavoured chat requests, adapts them for cloud OpenAI-compatible
backends (Groq / OpenCode Zen), returns responses verbatim.

Adaptations learned from live debugging:
  * strips llama.cpp-only fields (chat_template_kwargs, reasoning_budget)
  * bumps max_tokens (hidden reasoning eats small budgets -> truncated JSON)
  * appends strict "JSON only" instruction to the system message
  * response_format ladder: json_schema -> json_object -> none
  * honours Retry-After on 429 (up to 3 waits, capped)
  * optional alternate model on persistent 429 (PROXY_ALT_MODEL)

Env: PROXY_UPSTREAM_URL, PROXY_KEY, PROXY_MODEL, PROXY_ALT_MODEL (optional).
"""
import json
import os
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = os.environ["PROXY_UPSTREAM_URL"].rstrip("/")
KEY = os.environ["PROXY_KEY"]
MODEL = os.environ.get("PROXY_MODEL", "")
ALT_MODEL = os.environ.get("PROXY_ALT_MODEL", "")
STRIP = ("chat_template_kwargs", "reasoning_budget")
HITS = "/tmp/shim_hits.log"


def log(msg: str):
    with open(HITS, "a") as lg:
        lg.write(msg + "\n")


def call_upstream(body: dict):
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        UPSTREAM + "/chat/completions", data=data, method="POST",
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {KEY}",
                 "User-Agent": "springfish-shim/0.1"})
    last_err = None
    for attempt in range(4):  # initial + 3 backoff retries on 429
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.status, json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            raw = e.read()
            if e.code == 429 and attempt < 3:
                wait = min(float(e.headers.get("Retry-After") or 12), 45.0)
                log(f"  429-backoff {wait:.1f}s")
                time.sleep(wait)
                last_err = e
                continue
            raise HTTPUpstream(e.code, raw)
    raise HTTPUpstream(last_err.code if last_err else 502,
                       b'{"error":"rate limited beyond retries"}')


class HTTPUpstream(Exception):
    def __init__(self, code, body_bytes):
        self.code = code
        self.body = body_bytes
        super().__init__(f"upstream {code}")


def adapt(incoming: dict) -> list[dict]:
    """Build the ordered list of request variants to try."""
    incoming["max_tokens"] = max(int(incoming.get("max_tokens") or 0), 1500)
    msgs = incoming.get("messages") or []
    if msgs and msgs[0].get("role") == "system":
        msgs[0]["content"] = str(msgs[0].get("content", "")) + (
            " Output exactly one JSON object and nothing else - "
            "no reasoning, no prose, no markdown fences.")
    base = {k: v for k, v in incoming.items() if k != "response_format"}
    rf = incoming.get("response_format") or {}
    out = []
    if rf.get("type") == "json_schema":
        jo = dict(base)
        jo["response_format"] = {"type": "json_object"}
        out += [incoming, jo, base]
    else:
        out += [incoming, base]
    return out


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        incoming = json.loads(self.rfile.read(n))
        if MODEL:
            incoming["model"] = MODEL
        log(f"HIT {self.path} bytes={n}")

        variants = adapt(incoming)
        status, last = 502, b'{"error":"proxy: all attempts failed"}'
        alt_used = False
        idx = 0
        while variants and idx < len(variants) + 4:  # bounded incl. appended retries
            variant = variants[idx]
            for k in STRIP:
                variant.pop(k, None)
            idx += 1
            try:
                status, payload = call_upstream(variant)
                last = json.dumps(payload).encode()
                break
            except HTTPUpstream as e:
                status, last = e.code, e.body
                if e.code == 429 and ALT_MODEL and not alt_used \
                        and variant.get("model") != ALT_MODEL:
                    variant["model"] = ALT_MODEL
                    variants.append(variant)          # primary model, retried later
                    no_rf = {k: v for k, v in variant.items()
                             if k != "response_format"}
                    variants.append(no_rf)
                    alt_used = True
                    log(f"  FALLING-BACK to {ALT_MODEL}")
                log(f"  UPSTREAM-ERR {e.code} bytes={len(e.body)}")
            except Exception as e:  # noqa: BLE001
                status, last = 502, json.dumps({"error": str(e)}).encode()
                break

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(last)))
        self.end_headers()
        self.wfile.write(last)
        log(f"SENT {status} bytes={len(last)}")


if __name__ == "__main__":
    print(f"shim on 127.0.0.1:18080 -> {UPSTREAM} model={MODEL or '(passthrough)'}"
          f" alt={ALT_MODEL or '-'}")
    ThreadingHTTPServer(("127.0.0.1", 18080), Handler).serve_forever()
