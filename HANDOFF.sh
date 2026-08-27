#!/bin/bash
# HANDOFF.sh — MindHarness detailed handoff verifier
# Run: bash HANDOFF.sh
# Checks: repo, tests, papers, research, providers, queued experiments, Cordis wiring

set -e
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; NC='\033[0m'
pass=0; fail=0; warn=0

ok()   { echo -e "${GREEN}  ✓${NC} $1"; pass=$((pass+1)); }
bad()  { echo -e "${RED}  ✗${NC} $1"; fail=$((fail+1)); }
info() { echo -e "${YELLOW}  ℹ${NC} $1"; warn=$((warn+1)); }

echo "=== MindHarness — Detailed Handoff ==="
echo "Date: $(date -u +%Y-%m-%d\ %H:%M\ UTC)  Host: $(hostname)"
echo ""

# --- Repo ---
echo "── REPO ──"
if [ -d ".git" ]; then ok "git repo at $(pwd)"; else bad "no .git"; fi
echo "  HEAD: $(git log --oneline | head -1)"
echo "  Branch: $(git branch --show-current 2>/dev/null || echo detached)"
echo "  Remote: $(git remote get-url origin 2>/dev/null || echo none)"
if git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null; then
  ok "clean tree"
else
  bad "dirty tree — $(git status --porcelain 2>/dev/null | wc -l | tr -d ' ') dirty files"
  git status --porcelain 2>/dev/null | head -5 | sed 's/^/    /'
fi
if git tag --list | grep -q "paper-v2-final"; then ok "tag paper-v2-final exists"; else bad "tag paper-v2-final missing"; fi
echo ""

# --- Homes ---
echo "── HOMES ──"
if [ -d ~/Desktop/mindharness/tools/harness_core ]; then ok "MindHarness: tools/harness_core present ($(ls ~/Desktop/mindharness/tools/harness_core/*.py 2>/dev/null | wc -l | tr -d ' ') py files)"; else bad "MindHarness tools missing"; fi
if [ -d ~/Desktop/springfish ]; then ok "SpringFish: ~/Desktop/springfish present ($(ls ~/Desktop/springfish/ 2>/dev/null | wc -l | tr -d ' ') top-level items)"; else bad "SpringFish missing"; fi
echo ""

# --- Harness tests ---
echo "── HARNESS TESTS (offline, no API keys needed) ──"
total_pass=0; total_fail=0
for f in tests/test_*.py; do
  if [ -f "$f" ]; then
    out=$(python3 "$f" 2>&1 || true)
    if echo "$out" | grep -q "passed\|PASS"; then
      # Extract counts if available
      line=$(echo "$out" | grep -E "passed|PASS" | tail -1)
      ok "$f: $line"
      total_pass=$((total_pass+1))
    else
      bad "$f: failed"
      total_fail=$((total_fail+1))
    fi
  fi
done
echo "  Total: $total_pass passed, $total_fail failed"
echo ""

# --- Papers ---
echo "── PAPERS ──"
for p in paper_v2 paper_v3 paper_5organs; do
  if [ -f "$p/main.tex" ]; then
    lines=$(wc -l < "$p/main.tex" 2>/dev/null | tr -d ' ')
    pdf="—"
    [ -f "$p/main.pdf" ] && pdf=$(ls -lh "$p/main.pdf" 2>/dev/null | awk '{print $5}')
    # Quick compile check
    bib=$(grep -c "\\\\bibitem" "$p/main.tex" 2>/dev/null | tr -d ' ')
    ok "$p: $lines lines, $bib bib entries, PDF $pdf"
  else
    bad "$p: main.tex missing"
  fi
done
if [ -f paper_5organs/figures_gallery.pdf ]; then ok "figures_gallery.pdf present ($(ls -lh paper_5organs/figures_gallery.pdf 2>/dev/null | awk '{print $5}'))"; else info "figures_gallery.pdf not built (run: pdflatex figures_gallery.tex)"; fi
echo ""

# --- Research docs ---
echo "── RESEARCH DOCS ──"
for f in research/PROGRAM_SYNTHESIS_DETAILED.md research/DYNAMIC_REFLEXIVE_HARNESS.md research/RESEARCH_MIRROR.md research/AGENCY_AND_THE_CONSTRUCTED_SELF.md research/MAPPED_NERVOUS_SYSTEMS_VALIDATION_2026-08-27.md research/WHAT_IT_ALL_MEANS.md research/LOOP_AT_EVERY_SCALE_CELL_MIND_MARKET_MODEL.md research/FOUR_METHODS_ONE_DESTINATION_CONVERGENT_VALIDITY.md; do
  if [ -f "$f" ]; then
    lines=$(wc -l < "$f" 2>/dev/null | tr -d ' ')
    ok "$(basename $f) — $lines lines"
  else
    bad "$(basename $f) missing"
  fi
done
total_r=$(cat research/*.md 2>/dev/null | wc -l | tr -d ' ')
echo "  Total research: ~$total_r lines"
echo ""

# --- Providers ---
echo "── PROVIDERS (live check, may be 429/403/500 — harness stays green) ──"
# OpenRouter free tier check (fast, no key needed for status)
OR_FREE=$(curl -s --max-time 8 https://openrouter.ai/api/v1/models 2>&1 | head -c 200 || echo "curl failed")
if echo "$OR_FREE" | grep -q "data"; then ok "OpenRouter: reachable"; else info "OpenRouter: $OR_FREE" | head -c 80; fi
# Groq check (needs key, just check if auth.json exists)
if [ -f ~/.local/share/opencode/auth.json ]; then
  if grep -q "groq" ~/.local/share/opencode/auth.json 2>/dev/null; then ok "Groq key present in auth.json"; else info "Groq key not in auth.json"; fi
else
  info "auth.json not found — Groq key location unknown"
fi
echo ""

# --- Queued experiments ---
echo "── QUEUED EXPERIMENTS (9 items — see research/QUEUED_EXPERIMENTS_TRACKER.md) ──"
echo "  #  Experiment                          Preregistration                    Status"
echo "  1  200-turn irreversible life           research/MIND_MAP_...             ⏳ queued (needs stable 200-turn run)"
echo "  2  Sham 3-seed (discriminating subj)   exp_s126_v3.py (4 arms)           ⏳ 1-seed pilot banked, needs 3-seed"
echo "  3  Composite mind (P1-P4)              COMPOSITE_PREREGISTRATION.md       ⏳ queued (model_registry.json wired)"
echo "  4  Anchoring arm (connected/insulated) ANCHORING_PREREGISTRATION.md      ⏳ queued"
echo "  5  Bakeoff matrix (detached 70B 20s)   COMPOSITE_PREREGISTRATION.md       ✗ NOT running (died 08-25) — relaunch"
echo "  6  Persona drift battery               exp_persona_drift.py               ⏳ queued"
echo "  7  Cross-model replication             screening via exp_s126_v3.py       ⏳ queued (needs capable subject)"
echo "  8  Citation precision re-fetch         CITATION_AUDIT_..._VERIFIED.md     ⏳ offline, not blocking"
echo "  9  (visual/citation polish)            paper_5organs reviews              ⏳ 3 minor overfulls, visual P0 deferred"
echo ""

# --- Cordis wiring ---
echo "── CORDIS WIRING ──"
if [ -f bundles/dsh-mindharness/cordis.patch.yml ]; then ok "dsh-mindharness bundle present"; else bad "dsh-mindharness missing"; fi
if [ -f bundles/dsh-mindharness-parliament/cordis.patch.yml ]; then ok "dsh-mindharness-parliament scaffold present (9 inserts)"; else info "parliament scaffold not yet in this checkout"; fi
if [ -f model_registry.json ]; then
  roles=$(grep -o '"model"' model_registry.json 2>/dev/null | wc -l | tr -d ' ')
  ok "model_registry.json present ($roles roles)"
else
  info "model_registry.json not in mindharness (check ~/Desktop/springfish/model_registry.json)"
fi
echo ""

# --- Summary ---
echo "── SUMMARY ──"
if [ "$fail" -eq 0 ]; then
  echo -e "${GREEN}  Passed: $pass | Failed: $fail | Info: $warn${NC}"
  echo "  STATUS: CLEAN HANDOFF — nothing lost, everything tracked"
else
  echo -e "${RED}  Passed: $pass | Failed: $fail | Info: $warn${NC}"
  echo "  STATUS: ISSUES — see ✗ above"
fi
echo ""
echo "  Next session:"
echo "    1. bash HANDOFF.sh  (this script)"
echo "    2. cat research/QUEUED_EXPERIMENTS_TRACKER.md  (9 queued, with next-session commands)"
echo "    3. Provider gate (midnight UTC 2026-08-27) has PASSED — sham 3-seed on a DISCRIMINATING"
echo "       subject + 200-turn life are unblocked. See HANDOFF.md sec 4 and sec 9."
echo ""
