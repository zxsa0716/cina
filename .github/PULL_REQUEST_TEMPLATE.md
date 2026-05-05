<!-- Thanks for contributing to CINA! Please complete the checklist below. -->

## Summary

<!-- 1-3 sentence overview of what this PR does and why. -->

## Type of change

- [ ] 🐞 Bug fix
- [ ] ✨ New feature / methodology extension
- [ ] 📚 Documentation update
- [ ] 🎨 Figure / visual improvement
- [ ] 🔬 New empirical analysis
- [ ] ⚙️ Refactor / chore
- [ ] 🧪 Test / CI improvement

## Affected stage

- [ ] Stage 0 — Data collection (`src/collect/`)
- [ ] Stage 1 — Stance extraction (`src/stage1_extract/`)
- [ ] Stage 2 — Graph analysis / R-GAT (`src/stage2_graph/`)
- [ ] Stage 3 — Briefing generation (`src/stage3_brief/`)
- [ ] Phase 5 — Evaluation (`src/evaluation/`)
- [ ] Cross-cutting (`src/run_all.py`, `src/viz/`, docs, etc.)

## Reproducibility

- [ ] `python -m src.run_all --skip-rgat` still completes successfully
- [ ] `python -m src.stage1_extract.llm_smoke_test --offline` exits 0
- [ ] All new figures: 300 dpi, white background, CINA palette consistent
- [ ] No version-numbered filenames introduced (e.g., `_v2`, `_final`)

## Honesty checklist (per CRITICAL_REVIEW.md)

- [ ] No "first quantitative measurement" / "novel" claims without evidence
- [ ] Real-vs-simulated expert validation distinction preserved
- [ ] N (sample size) explicitly disclosed for any new metric
- [ ] Existing baseline tools (NegotiateCOP, Castro 2025, RICE-N) accurately described

## Citation impact

<!-- If this PR changes empirical results, list which numbers in paper.md / README.md / RUN_REPORT.md need updating. -->

## Related issues

<!-- Closes #N -->
