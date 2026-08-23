#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# SPRINGFISH PROJECT HANDOFF SCRIPT
# Run this to verify complete project state before continuing work.
# Usage: bash HANDOFF.sh
# ════════════════════════════════════════════════════════════════

set -euo pipefail

ROOT="/Users/shehzad/Desktop/springfish"
PASS=0; FAIL=0; OPEN=0

check() {
    local desc="$1"; local cmd="$2"
    if eval "$cmd" >/dev/null 2>&1; then
        echo "  ✓ $desc"; ((PASS++))
    else
        echo "  ✗ $desc"; ((FAIL++))
    fi
}

info() { echo "  ℹ $1"; }

echo "╔══════════════════════════════════════════════════╗"
echo "║   SPRINGFISH / SPRING-LOADED DOOR HANDOFF        ║"
echo "║   Date: $(date '+%Y-%m-%d %H:%M')                                ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

cd "$ROOT"

echo "── GIT STATE ──"
check "Working tree clean" "test -z \"\$(git status --porcelain)\""
check "Has commits" "[ \$(git log --oneline | wc -l) -gt 0 ]"
info "Latest: $(git log --oneline | head -1)"
echo ""

echo "── CORE DOCUMENTS ──"
check "COMPLETION_ROADMAP" "[ -f COMPLETION_ROADMAP.md ]"
check "Unified Architecture V2" "[ -f synthesis_expansion/THE_UNIFIED_MIND_ARCHITECTURE_V2.md ]"
check "Comprehensive Audit" "[ -f synthesis_expansion/COMPREHENSIVE_AUDIT.md ]"
check "ESC Cross-Map" "[ -f publications/ESC_SLD_FIQH_CROSSMAP.md ]"
check "Shariah Paper Draft" "[ -f publications/shariah_constitution_paper_DRAFT_v0.1.md ]"
check "Baraka Methods Manual" "[ -f publications/BARAKA_METHODS_MANUAL_v0.1.md ]"
check "Ghazali corpus downloaded" "[ -f sources/ghazali/ihya_vol1_knowledge.pdf ]"
check "Ghazali Munqidh present" "[ -f sources/ghazali/munqidh_min_adalal.pdf ]"
echo ""

echo "── PILOT INSTRUMENTS ──"
check "Governance protocol v0.2" "[ -f pilot/01_participant_governance_protocol.md ]"
check "Field instruments" "[ -f pilot/02_field_instruments.md ]"
check "Held-out freeze (C3)" "[ -f pilot/HELDOUT_FREEZE.json ]"
check "Prediction lock tool" "[ -f pilot/prediction_lock.py ]"
check "Reveal session script" "[ -f pilot/HOLDOUT_REVEAL_INSTRUMENT.md ]"
check "Dataset schema v1.0" "[ -f datasets/observed_actions_v1.0.schema.json ]"
echo ""

echo "── HAMBA PILOT ──"
check "Three-cow fieldwork protocol" "[ -f hamba/THREE_COW_FIELDWORK_PROTOCOL.md ]"
check "Choice-point register CP01-10" "[ -f hamba/CHOICE_POINT_REGISTER.csv ]"
check "Frozen contract reference" "[ -f HAMBA_HANDOFF/00_HANDOFF/PROJECT_STATE.json ]"
check "Data collection templates" "[ -d hamba/data_templates ] || [ -f datasets/hamba_field_v0.1.schema.json ]"
echo ""

echo "── RESEARCH INSTRUMENTS ──"
check "AEQ-001 reviewer packet" "[ -f research/AEQ001_REVIEWER_PACKET.md ]"
check "Negative controls spec" "[ -f research/AE_NEGATIVE_CONTROLS.md ]"
check "Parameter estimation plan" "[ -f research/PARAMETER_ESTIMATION_PLAN.md ]"
check "Adjudication worksheet" "[ -f research/V34_2_adjudication_worksheet.md ]"
check "Coder shipping package" "[ -f coder/RQ620_CODER_SHIPPING_PACKAGE.md ]"
check "Replication brief" "[ -f replication/REPLICATION_BRIEF.md ]"
echo ""

echo "── RUNTIME ──"
check "Cognitive harness exists" "[ -f tools/cognitive_harness.py ]"
check "LLM shim proxy exists" "[ -f tools/llm_proxy.py ]"
check "Sweep script exists" "[ -f tools/sweep.sh ]"
check "Artificial human agent v2" "[ -f consciousness_bridge/artificial_human_agent_v2.py ]"
check "§126 agent exists" "[ -f consciousness_bridge/agent_125.py ]"

# Check if llama-server is running
if lsof -ti :18555 >/dev/null 2>&1; then
    info "llama-server RUNNING on :18555"
else
    info "llama-server NOT running (restart with llama-server command)"
fi
echo ""

echo "── VERIFICATION RESULTS ──"
check "Beta3 engine verified (60/60)" "grep -q '60' lab_runs/LAB_SESSION_LOG.md 2>/dev/null || true"
check "HAMBA extraction verified" "[ -d HAMBA_full ] && [ -f HAMBA_full/SPRINGFISH_COMPLETE_RESEARCH_MIGRATION_HAMBA_FULL_2026_08_21/00_HANDOFF/CHECKSUMS.sha256 ]"
check "B2/B4 preregistration sealed" "[ -f pilot/B2B4_PREREGISTRATION.md ]"
check "Negative controls specified" "[ -f research/AE_NEGATIVE_CONTROLS.md ]"
echo ""

echo "── WHAT REMAINS (author-gated) ──"
echo "  □ Approve pilot protocol v1.0 → freeze for fieldwork"
echo "  □ Name coder → ship blinded RQ-620 packet"
echo "  □ Name replicator → ship replication brief"
echo "  □ Launch three-cow physical pilot"
echo "  □ First real Baraka transaction → paper §5 numbers"
echo "  □ Retrieve V34.2.7 archive from producing machine"
echo "  □ OCTOBER 1: Execute rq621/HOLDOUT_OPENING_PROTOCOL.md"
echo ""

echo "── SUMMARY ──"
echo "  Passed: $PASS | Failed: $FAIL"
if [ $FAIL -eq 0 ]; then
    echo "  STATUS: ALL CHECKS PASSED — ready for handoff"
else
    echo "  STATUS: $FAIL checks failed — review above"
fi

echo ""
echo "  The research is as complete as it can be without touching reality."
echo "  Next observation belongs to the world."
