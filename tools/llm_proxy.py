#!/usr/bin/env python3
"""LLM shim proxy for SpringFish (frozen engine, zero modification).

Listens on 127.0.0.1:18080 (engine default LLM_BASE_URL). Receives the engine's
llama.cpp-flavoured chat requests, strips fields the cloud backend rejects,
forwards to an OpenAI-compatible upstream (Groq / OpenCode Zen), returns the
response verbatim. If upstream rejects response_format=json_schema, retries
with json_object, then without response_format.

Upstream selected by env: PROXY_UPSTREAM_URL, PROXY_KEY, PROXY_MODEL.
"""
import json
import os
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = os.environ["PROXY_UPSTREAM_URL"].rstrip("/")
KEY = os.environ["PROXY_KEY"]
MODEL = os.environ.get("PROXY_MODEL", "")
STRIP = ("chat_template_kwargs", "reasoning_budget")  # llama.cpp-only extensions


def forward(body: dict):
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        UPSTREAM.rstrip("/") + "/chat/completions", data=data, method="POST",
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {KEY}",
                 "User-Agent": "springfish-shim/0.1"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.status, json.loads(r.read().decode())


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        with open('/tmp/shim_hits.log', 'a') as lg:
            lg.write(f'HIT {self.path} bytes={n}\n')
        incoming = json.loads(self.rfile.read(n))
        if MODEL:
            incoming["model"] = MODEL

        incoming["max_tokens"] = max(int(incoming.get("max_tokens") or 0), 1500)
        msgs = incoming.get("messages") or []
        if msgs and msgs[0].get("role") == "system":
            msgs[0]["content"] = str(msgs[0].get("content", "")) + (
                " Output exactly one JSON object and nothing else - "
                "no reasoning, no prose, no markdown fences.")
        attempts = [incoming]
        degraded = {k: v for k, v in incoming.items() if k != "response_format"}
        rf = incoming.get("response_format")
        if rf and rf.get("type") == "json_schema":
            degraded["response_format"] = {"type": "json_object"}
            attempts += [degraded, {k: v for k, v in incoming.items() if k != "response_format"}]
        else:
            attempts.append(degraded)

        last = b'{"error":"proxy: all attempts failed"}'
        status = 502
        for attempt in attempts:
            for k in STRIP:
                attempt.pop(k, None)
            try:
                status, payload = forward(attempt)
                last = json.dumps(payload).encode()
                break
            except urllib.error.HTTPError as e:
                last = e.read()
                status = e.code
                with open('/tmp/shim_hits.log', 'a') as lg:
                    lg.write(f'  UPSTREAM-ERR {e.code} bytes={len(last)} {last[:150]!r}\n')
            except Exception as e:  # noqa: BLE001
                last = json.dumps({"error": str(e)}).encode()
                status = 502
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(last)))
        self.end_headers()
        self.wfile.write(last)
        with open('/tmp/shim_hits.log', 'a') as lg:
            lg.write(f'SENT {status} bytes={len(last)}\n')
        open('/tmp/shim_last_response.json','wb').write(last)


if __name__ == "__main__":
    print("shim on 127.0.0.1:18080 ->", UPSTREAM, "model:", MODEL or "(passthrough)")
    ThreadingHTTPServer(("127.0.0.1", 18080), Handler).serve_forever()
