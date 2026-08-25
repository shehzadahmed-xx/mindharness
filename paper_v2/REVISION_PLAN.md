# TOP-JOURNAL REVISION PLAN
Target: NeurIPS / ICML / Nature Machine Intelligence format

## STRUCTURAL CHANGES NEEDED
1. Split Section 2 into standalone Literature Review chapter (currently inline)
2. Move architecture diagrams to dedicated figures (TikZ, not tables)
3. Results: add statistical tests (Holm-corrected paired t-test per prediction)
4. Discussion: restructure as Implications → Limitations → Future Work
5. Add Appendix A: full S126 protocol spec; B: correction history ledger

## WRITING QUALITY UPGRADES
6. Every paragraph opens with topic sentence stating the claim
7. Remove all hedging except where uncertainty is genuine ("we cannot rule out")
8. Active voice throughout; no "it was found that"
9. Numbers formatted consistently: accuracy as percentages, latency in seconds
10. Each figure referenced in text BEFORE it appears

## DATA PRESENTATION
11. Generate 6 additional matplotlib figures from partial.jsonl:
    - Fig 3a: per-seed attribution scatter (raw vs harnessed overlaid)
    - Fig 3b: CII distribution across seeds
    - Fig 5: living session energy/fatigue time series (40 turns)
    - Fig 6: γ-gate override rate by condition (compliance vs wired)
    - Fig 7: bake-off accuracy-latency Pareto frontier
    - Fig 8: cross-tradition convergence diagram (conceptual)
12. Tables switch to booktabs with \midrule/\toprule only (no vertical lines)
13. Effect sizes reported alongside p-values (Cohen's d for paired comparisons)

## CITATION UPGRADE
14. Migrate to .bib file with DOIs
15. Add missing citations: Conant & Ashby 1970, Friston 2010 free-energy,
    Baars 1988 GWT origin, Dehaene GNW, Seth beast-machine, Fleming & Lau meta-d'
16. Cross-reference all 9 research updates as supplementary materials

## SUBMISSION CHECKLIST
17. Abstract ≤ 200 words (currently ~250)
18. Main text ≤ 9 pages after references (NeurIPS format)
19. Supplementary materials document created
20. Reproducibility checklist completed
21. Ethics statement on AI welfare implications added
22. Author contribution statement (CRediT taxonomy)
