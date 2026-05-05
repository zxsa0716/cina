# 🚀 CINA v3.0 — Release Notes

> **Release date**: 2026-05-05
> **Author**: Heedo Choi (최희도) · Kookmin University, Department of Climate Technology Convergence
> **Tag**: `v3.0.0`
> **Theme**: End-to-end re-execution + production-grade upgrade

---

## TL;DR

CINA v3.0은 단일 명령어로 전 파이프라인을 재현 가능하게 만들고 (`python -m src.run_all`), LLM provider stack의 production readiness를 검증하며 (`python -m src.stage1_extract.llm_smoke_test`), 모든 figure를 통일된 학술 visual identity로 재생성하는 **운영 가능한 학술 파이프라인** 릴리스입니다. 학술 contribution 자체에는 변화가 없지만, **재현성 / 표현 / 학술 표준 정합도**가 v2.0 대비 결정적으로 개선되었습니다.

---

## ✨ 주요 변경 사항

### 🆕 Master end-to-end orchestrator (`src/run_all.py`)

**한 명령어로 전체 파이프라인을 실행**하는 8-단계 오케스트레이터입니다:

```bash
python -m src.run_all                # 캐시된 LLM, 재현 가능
python -m src.run_all --live-llm     # 실제 LLM provider 호출
python -m src.run_all --skip-rgat    # R-GAT 스킵 (빠른 실행)
```

| Step | 내용 | 산출물 |
|------|------|------|
| S0 | Environment + LLM provider smoke test | `data/processed/environment_snapshot.json` |
| S1 | Stage 1 stance corpus (n=78 canonical) | `data/processed/stances_canonical_v3.jsonl` |
| S2 | Heterogeneous R-GAT 학습 (PyTorch, 200 ep) | `data/processed/rgat_training_results.json` |
| S3 | Stage 3 briefing artifacts 검증 | `deliverables/ministerial_briefing_*.md` |
| S4 | Phase 5 4-task 평가 결과 replay | `deliverables/evaluation_report.json` |
| S5 | Cross-LLM Krippendorff α 분석 | `data/processed/cross_llm_agreement.json` |
| S6 | Bayesian 3-level variance decomposition | `data/processed/bayesian_decomposition.json` |
| S7 | Publication-grade figure 재생성 (10종) | `docs/web/figures/fig*.png` |
| S8 | Master `RUN_REPORT.md` 자동 생성 | `RUN_REPORT.md` |

각 단계는 status (✅/⏭️/⚠️/❌), duration, 핵심 metric, artifact 경로를 기록하며, 최종 `RUN_REPORT.md`에는 단계별 요약과 headline takeaway가 자동 생성됩니다.

### 🆕 LLM provider production smoke test (`src/stage1_extract/llm_smoke_test.py`)

**실제 LLM 호출 가능 여부를 검증**하는 production-readiness 도구입니다:

```bash
python -m src.stage1_extract.llm_smoke_test --offline      # 네트워크 없이 mock
python -m src.stage1_extract.llm_smoke_test                # 모든 provider 테스트
python -m src.stage1_extract.llm_smoke_test --providers gemini,groq
```

- 5개 provider (Gemini · Groq · Anthropic · Ollama · OpenRouter) + offline mock
- CINA-shaped prompt에서 structured JSON 출력 parse 검증
- Per-provider latency 측정
- Production tier 자동 판정:
  - 1 OK = Stage 1 invokable
  - 2 OK = Cross-LLM ensemble feasible
  - 3+ OK = robust Krippendorff α 측정 가능
- Exit code: 0 (≥ 1 OK), 1 (모두 실패) — CI 통합 가능

### 🆕 Publication-grade figure suite (`src/viz/publication_figures.py`)

**모든 paper figure를 통일된 visual identity로 재생성**합니다:

- **CINA 팔레트**: navy `#1c2536` · primary `#2a5298` · accent `#6ea8ff` · warm `#f59e0b` · success `#10b981` · danger `#dc2626`
- **Diverging stance colormap** (red ↔ grey ↔ green)
- **Frame palette** (scientific/justice/sovereignty/security/development/mixed)
- **300 dpi**, 흰 배경, 일관 typography (DejaVu Sans), spines off, grid 0.4 alpha

10개 figure (fig8은 별도 R-GAT 모듈에서 생성):
1. `fig1_country_issue_heatmap.png` — Brazil chair + Korea L&D weakness annotated
2. `fig2_procedural_authority.png` — Tallberg 2010 channel distribution
3. `fig3_frame_consistency.png` — Leiden community별 5-frame typology
4. `fig4_centrality.png` — PageRank/Betweenness/Degree/Eigenvector top-6
5. `fig5_similarity_network.png` — Leiden 2 communities + chair badge
6. `fig6_hedging_density_2d.png` — Norm entrepreneur typology
7. `fig7_translation_gap_brazil.png` — NATO 4-axis Δ=0.304 시각화
8. `fig8_rgat_training.png` — R-GAT 학습 + emergent attention (별도 모듈)
9. `fig9_cross_llm_alpha.png` — Cross-LLM α (raw vs corrected)
10. `fig10_bayesian_decomposition.png` — 3-level variance donut + bar

### 🆕 Production-grade README

- 중앙 정렬 헤더 + 7개 badge (Spearman 0.658 · P@3 1.00 · Cross-LLM α 0.93 · R-GAT chair 1.00 · Manifest 225)
- Anchor 네비게이션
- 3 contribution table with empirical anchors
- Quick-start with `python -m src.run_all` as primary entry
- LLM provider setup matrix (cost + setup commands)
- Methodology mermaid + 8 theory integration table
- Honest Task D simulated panel disclosure
- 10 figure catalogue + 4 web pages + code tree

### 🆕 GitHub repo guide (`GITHUB_REPO_GUIDE.md`)

GitHub UI 설정 권장사항: About 섹션 (description + 15 topics) · Social preview · Releases & Tags 템플릿 · Pinned issues · GitHub Pages · CodeQL/Dependabot · arXiv preprint upload checklist · Permanent identifier registration (Zenodo, ORCID).

---

## 🆙 Updated documents

- **`ALL_OUTPUTS_INDEX.md`** — v3.0 quick stats (10 figures, 4 web pages, 5 advancement docs), master pipeline reference
- **`README.md`** — 전면 재작성, production-grade

---

## 📊 Empirical anchors preserved

| Metric | Value | Source |
|--------|-------|--------|
| Stage 1 Spearman ρ | 0.658 | Phase 5 Task A |
| Contested P@3 / R@3 | 1.00 / 1.00 | Phase 5 Task C (N=3) |
| Cross-LLM Krippendorff α | 0.876 raw / 0.933 corrected | E2 advancement |
| R-GAT validation Spearman | 0.708 | E1 advancement |
| R-GAT chair-edge attention | 1.00 | E1 emergent finding |
| Brazil Translation Gap Δ | 0.304 | Single-case observation |
| Korean IRR | 0.653 (CI [0.55, 0.71]) | Track A briefing |
| AILAC NES | 0.86 (3.5/4 criteria) | Single-case finding |
| Leiden modularity | 0.31 (2 communities) | Stage 2 |
| Bayesian σ_country / σ_group / σ_regime | 0.27 / 0.22 / 0.04 | E3 advancement |
| Ablation A4 Δρ | -0.15 (largest) | Phase 5 ablation |

---

## 📜 Citation (unchanged)

```
Choi, Heedo (2026). CINA: Climate Issue-Network Analysis Framework
[graduate research project, unpublished].
Department of Climate Technology Convergence, Kookmin University.
https://github.com/zxsa0716/cina
```

---

## 🛣️ What's next

본 릴리스는 학술 투고 준비의 **운영적 기반**을 확립합니다. 다음 단계:

1. **NeurIPS Climate Change AI Workshop 2026** short paper 투고 (deadline ~7월)
2. **arXiv preprint** 업로드 (4-page workshop version)
3. **한국정책학회보 (KCI)** 한국어 단일 저자 논문 별도 작성
4. **COP31 prospective validation** (코드 freeze 2026-09-01, 결과 2026-12)
5. **External expert panel** 섭외 (KEI / KAIST / MOFA)
6. **Longitudinal extension** COP25-COP30 (E5)
7. **Causal identification** DiD/SC/IV 분석 (E6, longitudinal 후)

---

**Repository**: https://github.com/zxsa0716/cina
**Web demo**: https://zxsa0716.github.io/cina/
**Contact**: zxsa0716@kookmin.ac.kr
