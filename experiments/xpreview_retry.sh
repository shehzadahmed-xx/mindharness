#!/bin/bash
# x-preview-f-free battery with provider-health gating + infinite retry.
# Skips dead-provider windows automatically; completes when upstream holds.
cd /Users/shehzad/Desktop/springfish
KEY=$(python3 -c "import json; print(json.load(open('/Users/shehzad/.local/share/opencode/auth.json'))['opencode']['key'])")
MODEL="x-preview-f-free"
BASE="https://opencode.ai/zen/v1"
attempt=0
while true; do
  attempt=$((attempt+1))
  # health gate: only launch the real battery when upstream responds
  HEALTH=$(curl -s --max-time 25 "$BASE/chat/completions" \
    -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
    -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"ok\"}],\"max_tokens\":8}" | head -c 60)
  if echo "$HEALTH" | grep -q '"id"'; then
    echo "[$(date '+%H:%M:%S')] attempt $attempt: provider UP — launching battery"
    if python3 experiments/exp_s126_v3.py --api-key "$KEY" --model "$MODEL" \
         --base-url "$BASE" --seeds 5; then
      echo "[$(date '+%H:%M:%S')] BATTERY COMPLETE"
      break
    else
      echo "[$(date '+%H:%M:%S')] battery failed mid-run; re-gating"
    fi
  else
    echo "[$(date '+%H:%M:%S')] attempt $attempt: provider DOWN ($HEALTH)"
  fi
  sleep 40
done
