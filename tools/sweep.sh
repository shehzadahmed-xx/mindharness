#!/usr/bin/env zsh
# Usage: sweep.sh CASE SEEDS_DIR
V=/Users/shehzad/Desktop/springfish/runtime/.venv/bin/python
E="/Users/shehzad/Desktop/springfish/SPRINGFISH_COMPLETE_RESEARCH_AND_HANDOFF_LOCAL_PC_2026_08_04/01_WORKSPACE_SNAPSHOT/restored_beta3_engine"
CASE=$1
OUT=$2
mkdir -p "$OUT"
cd "$E" || exit 1
export PYTHONPATH="$E" SPRINGFISH_LLM_MODE=${SPRINGFISH_LLM_MODE:-openai}
export LLM_MODEL_NAME=${LLM_MODEL_NAME:-Qwen3.5-0.8B-Q3_K_S}
export LLM_BASE_URL=${LLM_BASE_URL:-http://127.0.0.1:18555/v1}
for S in 1 2 3 4 5 6 7 8; do
  if [ -d "$OUT/seed_$S.json" ]; then
    echo "seed $S already"
  else
    SPRINGFISH_SEED=$S $V -m springfish.cli run --case $CASE ${CALIB:+--calibrated-personas} --output "$OUT/seed_$S.json" >/dev/null 2>&1
    [ -d "$OUT/seed_$S.json" ] && echo "seed $S OK" || echo "seed $S FAILED"
  fi
done
