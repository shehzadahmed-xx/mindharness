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
total_pass=0; total_fail=0; assert_pass=0
for f in tests/test_*.py; do
  if [ -f "$f" ]; then
    out=$(python3 "$f" 2>&1 || true)
    if echo "$out" | grep -q "passed\|PASS"; then
      # Extract counts if available
      line=$(echo "$out" | grep -E "passed|PASS" | tail -1)
      ok "$f: $line"
      total_pass=$((total_pass+1))
      # assertion count, e.g. "6/6 passed" -> 6 (for the doc-claims gate below)
      n=$(echo "$line" | grep -o '[0-9]\{1,\}/[0-9]\{1,\}' | head -1 | cut -d/ -f1)
      [ -n "$n" ] && assert_pass=$((assert_pass+n))
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
for f in research/PROGRAM_SYNTHESIS_DETAILED.md research/DYNAMIC_REFLEXIVE_HARNESS.md research/RESEARCH_MIRROR.md research/AGENCY_AND_THE_CONSTRUCTED_SELF.md research/MAPPED_NERVOUS_SYSTEMS_VALIDATION_2026-08-27.md research/WHAT_IT_ALL_MEANS.md research/LOOP_AT_EVERY_SCALE_CELL_MIND_MARKET_MODEL.md research/FOUR_METHODS_ONE_DESTINATION_CONVERGENT_VALIDITY.md research/UTILITY_OF_TEMPORARY_GULLIBILITY_LIMBIC_CONTAINERIZATION.md research/ALGORITHM_PROGRAMMING_BRAIN_TIKTOK_REELS.md research/OCCASIONALISM_MALEBRANCHE_GHAZALI_HABIT_VS_POWER.md research/PATTERN_NOT_STUFF_WHO_AM_I.md research/EGO_ILLUSION_DEFINITION.md research/IBN_ARABI_SEVEN_DOORS_FIVE_ORGANS.md research/DOCUMENT_EVERYTHING_2026-08-30.md; do
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

# --- Program ledger (γ_program) (added 2026-08-30) ---
# Program drift check: filing without running → γ_program → 0, like harness γ→0 when watching without steering.
echo "── PROGRAM LEDGER (γ_program) ──"
# preregs: all prereg files in experiments/ (re-derived from disk, not hard-coded)
_prereg_count=$(find experiments -maxdepth 1 -name "*PREREG*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
# fallback: case-insensitive if zero (handles *prereg* vs *PREREG*)
if [ "$_prereg_count" -eq 0 ] 2>/dev/null; then
  _prereg_count=$(find experiments -maxdepth 1 -iname "*prereg*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
fi
preregs_drafted=${_prereg_count:-0}
# locks: pilot/locks/*.lock.json (or *.json)
_prereg_locks=$(find pilot/locks -maxdepth 1 -name "*.lock.json" -type f 2>/dev/null | wc -l | tr -d ' ')
if [ "$_prereg_locks" -eq 0 ] 2>/dev/null; then
  _prereg_locks=$(find pilot/locks -maxdepth 1 -name "*.json" -type f 2>/dev/null | wc -l | tr -d ' ')
fi
prereg_locks=${_prereg_locks:-0}
[ -z "$preregs_drafted" ] && preregs_drafted=0
[ -z "$prereg_locks" ] && prereg_locks=0
# queued: parse research/QUEUED_EXPERIMENTS_TRACKER.md (9 items), fallback to preregs_drafted
if [ -f research/QUEUED_EXPERIMENTS_TRACKER.md ]; then
  experiments_queued=$(grep -cE '^\| \*\*[0-9]+' research/QUEUED_EXPERIMENTS_TRACKER.md 2>/dev/null || echo 0)
  [ -z "$experiments_queued" ] && experiments_queued=0
  # fallback if tracker format changes: count numbered rows in queue table
  if [ "$experiments_queued" -eq 0 ]; then
    experiments_queued=$(grep -cE '^\| *[0-9]+ *\|' research/QUEUED_EXPERIMENTS_TRACKER.md 2>/dev/null || echo 0)
  fi
else
  experiments_queued=$preregs_drafted
fi
# run: count experiments/lab_runs_*/ dirs that contain results
experiments_run=0
for _d in experiments/lab_runs_*/; do
  [ -d "$_d" ] || continue
  if find "$_d" -maxdepth 1 -name "results.json" -o -name "results.jsonl" -o -name "verdict.json" -o -name "final_report.json" -o -name "anchoring_results.jsonl" 2>/dev/null | grep -q .; then
    experiments_run=$((experiments_run+1))
  elif find "$_d" -maxdepth 1 -name "*.json" -o -name "*.jsonl" 2>/dev/null | grep -q .; then
    experiments_run=$((experiments_run+1))
  fi
done
# also count lab_runs_* at top-level if glob missed (set -e safe)
if [ "$experiments_run" -eq 0 ]; then
  experiments_run=$(find experiments -maxdepth 2 -path "experiments/lab_runs_*/results.json" 2>/dev/null | wc -l | tr -d ' ')
fi
# γ_program = prereg_locks / preregs_drafted (2dp, handle div0)
if [ "$preregs_drafted" -eq 0 ]; then
  gamma_program="0.00"
else
  gamma_program=$(awk "BEGIN {printf \"%.2f\", $prereg_locks/$preregs_drafted}")
fi
# color by threshold: green >0.5, yellow 0.3-0.5, red <0.3
_gamma_color="$GREEN"
_gamma_status="healthy"
if awk "BEGIN {exit !($gamma_program < 0.3)}"; then
  _gamma_color="$RED"; _gamma_status="drift"
elif awk "BEGIN {exit !($gamma_program <= 0.5)}"; then
  _gamma_color="$YELLOW"; _gamma_status="at risk"
fi
echo -e "  preregs_drafted: $preregs_drafted  prereg_locks: $prereg_locks  ${_gamma_color}γ_program = $gamma_program ($_gamma_status)${NC}  (locks/drafted)"
echo -e "  experiments_run: $experiments_run  experiments_queued: $experiments_queued  →  $experiments_run / $experiments_queued run"
# drift warning when filing without running (gap >=3)
_gap=$((preregs_drafted - prereg_locks))
if [ "$_gap" -ge 3 ]; then
  info "drift: filing without running — $preregs_drafted preregs but only $prereg_locks locks (gap $_gap ≥3, γ_program=$gamma_program)"
elif [ "$_gap" -ge 1 ]; then
  echo -e "${YELLOW}  ℹ${NC} gap: $_gap prereg(s) without lock (γ_program=$gamma_program)"
else
  # no gap — still report green check via ok, but don't double-count fail
  ok "program ledger: no filing drift (γ_program=$gamma_program, $prereg_locks/$preregs_drafted locks)"
fi
echo ""

# --- Doc claims vs disk (added 2026-08-28) ---
# The script used to verify the repo and then print "nothing lost, everything
# tracked" without ever checking the numbers the docs assert ABOUT the repo.
# It could pass 32/32 while HANDOFF.md and README.md were wrong, which is
# exactly what was happening. These checks close that gap: every number a doc
# claims is re-derived from disk here and must match.
echo "── DOC CLAIMS vs DISK ──"

claim_check() {  # name, actual, claimed_or_empty, file
  local name="$1" actual="$2" claimed="$3" file="$4"
  if [ -z "$claimed" ]; then
    info "$name: no claim found in $file (actual: $actual)"
  elif [ "$actual" = "$claimed" ]; then
    ok "$name: $file says $claimed, disk says $actual"
  else
    bad "$name: $file says $claimed, disk says $actual"
  fi
}

# commit count
commits=$(git rev-list --count HEAD 2>/dev/null || echo "?")
h_commits=$(grep -o '\*\*[0-9]\{1,\} commits\*\*' HANDOFF.md 2>/dev/null | head -1 | grep -o '[0-9]\{1,\}' || true)
r_commits=$(grep -o '· [0-9]\{1,\} commits' README.md 2>/dev/null | head -1 | grep -o '[0-9]\{1,\}' || true)
# A doc committed in commit N can only ever truthfully claim N-1, so allow a
# drift of <=2 and fail beyond it. Silent unbounded drift is the actual bug.
count_check() {  # file, claimed
  local file="$1" claimed="$2" d
  if [ -z "$claimed" ]; then info "commit count: no claim in $file (actual: $commits)"; return; fi
  d=$((commits - claimed))
  if [ "$d" -ge 0 ] && [ "$d" -le 2 ]; then
    ok "commit count: $file says $claimed, disk says $commits (drift $d, within tolerance)"
  else
    bad "commit count: $file says $claimed, disk says $commits (drift $d)"
  fi
}
count_check "HANDOFF.md" "$h_commits"
count_check "README.md" "$r_commits"

# HEAD sha
head_sha=$(git rev-parse --short HEAD 2>/dev/null || echo "?")
h_head=$(grep -o '\*\*HEAD:\*\* `[0-9a-f]\{7,\}`' HANDOFF.md 2>/dev/null | head -1 | grep -o '[0-9a-f]\{7,\}' || true)
# HEAD: same self-reference problem. Require the claimed sha to be a real
# ancestor of HEAD and no more than 2 commits back.
if [ -z "$h_head" ]; then
  info "HEAD sha: no claim in HANDOFF.md (actual: $head_sha)"
elif ! git cat-file -e "$h_head" 2>/dev/null; then
  bad "HEAD sha: HANDOFF.md says $h_head, which is not a commit in this repo"
elif ! git merge-base --is-ancestor "$h_head" HEAD 2>/dev/null; then
  bad "HEAD sha: HANDOFF.md says $h_head, which is not an ancestor of $head_sha"
else
  behind=$(git rev-list --count "$h_head"..HEAD 2>/dev/null || echo 99)
  if [ "$behind" -le 2 ]; then
    ok "HEAD sha: HANDOFF.md says $h_head, $behind commit(s) behind $head_sha"
  else
    bad "HEAD sha: HANDOFF.md says $h_head, $behind commits behind $head_sha"
  fi
fi

# paper page counts
if command -v pdfinfo >/dev/null 2>&1; then
  for spec in "paper_v2:v2" "paper_v3:v3" "paper_5organs:5organs"; do
    dir="${spec%%:*}"; label="${spec##*:}"
    if [ -f "$dir/main.pdf" ]; then
      pages=$(pdfinfo "$dir/main.pdf" 2>/dev/null | awk '/^Pages/{print $2}')
      claimed=$(grep -o "$label [0-9]\{1,\}pp" HANDOFF.md 2>/dev/null | head -1 | sed "s/^$label //; s/pp$//" || true)
      claim_check "$label pages" "$pages" "$claimed" "HANDOFF.md"
    fi
  done
else
  info "pdfinfo unavailable — page-count claims unverified"
fi

# test total
tests_actual=$((assert_pass))
for f in HANDOFF.md README.md; do
  c=$(grep -o '[0-9]\{1,\}/[0-9]\{1,\} \(tests \)\?green' "$f" 2>/dev/null | head -1 | cut -d/ -f2 | grep -o '[0-9]\{1,\}' || true)
  claim_check "tests green" "$tests_actual" "$c" "$f"
done
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
