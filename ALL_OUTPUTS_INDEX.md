# 📦 CINA — All Outputs Index (전 산출물 인덱스 · v3.0)

> **저자(Author)**: **Heedo Choi (최희도)** — Graduate Student, Department of Climate Technology Convergence (기후기술융합학과), Kookmin University
> **Contact**: zxsa0716@kookmin.ac.kr · [GitHub @zxsa0716](https://github.com/zxsa0716)
> **Project**: CINA Framework v3.0 (LLM → R-GAT → graph-grounded briefing pipeline)
> **Status**: Preliminary methodology pilot + 4 implemented advancements (R-GAT · Cross-LLM α · Bayesian decomposition · Pre-registration)
> **Master pipeline**: `python -m src.run_all` (8-step end-to-end orchestrator)
> **Last update**: 2026-05-05

이 문서는 CINA 프로젝트가 생성한 **모든** 산출물(보고서, figure, 데이터, 코드)을 카테고리별로 정리한 단일 진입 인덱스입니다. 웹에서 둘러보려면 [docs/web/outputs.html](docs/web/outputs.html) 또는 배포된 GitHub Pages를 사용하세요.

---

## 0. Quick Stats — 한눈에 보기

| 카테고리 | 수량 | 위치 |
|---------|-----|------|
| 학술 페이퍼 | 1 (3,500+ words, 28 refs) | [paper.md](deliverables/paper.md) |
| 장관급 브리핑 | 2 (KO + EN) + 1 narrative .docx | [deliverables/](deliverables/) + FOR_SUBMISSION |
| 정량 검증 보고서 | 8 | [deliverables/](deliverables/) |
| **Publication-grade figures** | **10 PNG (300 dpi, 통일 visual identity)** | [docs/web/figures/](docs/web/figures/) |
| 방법론 문서 | 15 | [docs/](docs/) |
| 인터랙티브 웹 | 4 페이지 (index, methodology, viz, outputs) | [docs/web/](docs/web/) |
| Manifest entries | 225 raw 문서 | [data/manifest/manifest.jsonl](data/manifest/manifest.jsonl) |
| Stage 1 stances | n = 78 canonical (확장 가능) | [data/processed/stances_canonical_v3.jsonl](data/processed/) |
| 코드 모듈 | 26 collectors + 5 stage modules + analysis + viz | [src/](src/) |
| 평가 메트릭 | 4 tasks + 6 ablations + Cross-LLM α + Bayesian | [evaluation_report.md](deliverables/evaluation_report.md) |
| **🆕 학술 고도화 문서** | **5** (CRITICAL_REVIEW, ROADMAP, PREREG, CAUSAL, GITHUB_GUIDE) | repo root |

---

## 1. 학술 산출물 (Track B — Academic Submission)

### 1.1 Paper (논문 draft)

- **`deliverables/paper.md`**
  - 3,428 words · 7 sections + Abstract (300w) + Korean summary
  - **23 references**: Bayer-Urpelainen, Castro 2025, Finnemore-Sikkink 1998, Goh 2007, Haas 1992, Hochstetler-Milkoreit 2014, Hood 1983, Howlett 2019, Keohane-Victor 2011, Platt 1999, Putnam 1988, Sebenius 1983, Snow-Benford 1988, Steinberg 2002, Tallberg 2010, Tollison-Willett 1979, Traag-Waltman-van Eck 2019, IISD ENB, UNFCCC L.25E, UNFCCC L.24
  - 6개 figure inline reference (Fig. 1-6)
  - **Target venues**:
    - 1차: *Global Environmental Change* (IF 11.2, primary)
    - 1차 대안: *Global Environmental Politics*, *Climate Policy*
    - 기술: NeurIPS Climate Change AI Workshop 2026
    - 국내: 한국정책학회보 (KCI)
    - 데이터셋: Nature Scientific Data
  - 저자: Heedo Choi, 기후기술융합학과, Kookmin University

### 1.2 학술 기여 (Novelty Positioning)

- **`docs/08_novelty_positioning.md`** — C1-C10 학술 기여 카탈로그 + baseline 비교

---

## 2. 정책 산출물 (Track A — Class Submission)

### 2.1 장관급 브리핑

- **`deliverables/ministerial_briefing_ko.md`** (한국어, 9 sections + 4 appendices)
  - § Executive Summary
  - § COP30 적응 협상 핵심 issue map
  - § 한국 입장 정량 분석 (IRR=0.653)
  - § 협상 전략 (3 옵션)
  - § 연합 형성 권고
  - § Risk register
  - § Talking points
  - § COP31 ahead actions
  - § 평가 기준
  - 부록 A: Evidence traceability
  - 부록 B: Data lineage
  - 부록 C: Uncertainty quantification
  - 부록 D: LLM provider attribution

- **`deliverables/ministerial_briefing_en.md`** (영어, 310 lines)
  - 위 KO 브리핑 1:1 영어 버전 (국제 회람용)

### 2.2 사전 분석 (Pre-analytic)

- **`deliverables/country_selection.md`** — 브라질 선정 근거
- **`deliverables/sector_focus.md`** — Adaptation 섹터 정당성
- **`deliverables/agenda_matrix.md`** — COP30 6-issue 매트릭스

---

## 3. 정량 검증 보고서 (8 Findings)

| # | 파일 | 핵심 메트릭 | 학술 의의 |
|---|------|-----------|----------|
| F1 | [`IRR_Korea.md`](deliverables/IRR_Korea.md) | **IRR_Korea = 0.653** (CI 0.55-0.71) | 30/30 cells crosswalk, L&D-OP 0.39 weakness identified |
| F2 ⭐ | [`IRR_Brazil.md`](deliverables/IRR_Brazil.md) | **Δ = 0.304 CONFIRMED** | Putnam × Howlett gap 정량 — NeurIPS CCAI signature finding |
| F3 | [`L25_formula_control_evidence.md`](deliverables/L25_formula_control_evidence.md) | Pre-crystallized formula 가설 | Tallberg 2010 + Steinberg 2002 + Goh 2007 통합 |
| F4 | [`realist_b0_statistics.md`](deliverables/realist_b0_statistics.md) | F1 = 0.560, p<0.0001 | Constructivist+frame variables 정당성 |
| F5 ⭐ | [`AILAC_norm_entrepreneur_quantification.md`](deliverables/AILAC_norm_entrepreneur_quantification.md) | **NES = 0.86** (3.5/4 PASS) | Finnemore-Sikkink 1998 4 criteria empirical test |
| F6 | [`evaluation_report.md`](deliverables/evaluation_report.md) §A | Spearman ρ = 0.658 | CINA vs expert agreement (Task A) |
| F7 ⭐ | [`evaluation_report.md`](deliverables/evaluation_report.md) §C | **P@3 = R@3 = 1.00** | 3/3 contested issues 100% 정확 예측 |
| F8 | [`korean_nap_gga_crosswalk.csv`](deliverables/korean_nap_gga_crosswalk.csv) | 30 cells | NAP × GGA 정량 매핑 (Howlett instrument calibration) |

### 3.1 종합 평가 (Phase 5)

- **`deliverables/evaluation_report.md`** — Phase 5 최종 평가 보고서
- **`deliverables/evaluation_report.json`** — Machine-readable raw data
- **Quality Gates**: G1 Coverage ✅ · G2 Evidence ✅ · G3 Theory ✅ · G4 Dual Review ✅ · G5 Heedo Alignment ✅ (5/5)

---

## 4. Figures — Stage 2 시각화 (7 PNG)

모든 figure는 300 dpi, matplotlib + networkx 생성, 재현 가능 코드는 `src/stage2_graph/generate_figures.py`.

| # | 파일 | 설명 |
|---|------|------|
| 1 | `docs/web/figures/fig1_country_issue_heatmap.png` | 13 countries × 6 issues stance heatmap (Stage 1 anchor) |
| 2 | `docs/web/figures/fig2_procedural_authority.png` | Tallberg 2010 procedural authority distribution |
| 3 | `docs/web/figures/fig3_frame_consistency.png` | 5-frame typology × 그룹별 빈도 |
| 4 | `docs/web/figures/fig4_centrality.png` | 5 centrality Top-K rankings |
| 5 | `docs/web/figures/fig5_similarity_network.png` | Leiden 2 communities (Keohane-Victor 'horizontal cleavage') |
| 6 | `docs/web/figures/hedging_density_2d_plot.png` | Hedging × Red Line 2D (AILAC norm typology) |
| 7 | `docs/web/figures/hedging_vs_redline_2d.png` | Hedging vs Red Line (보강판, 95% confidence ellipse) |

또한 `deliverables/hedging_density_2d_plot.png` 동일 figure가 deliverables 폴더에도 사본 존재.

---

## 5. 방법론 문서 (15 docs in `docs/`)

| # | 문서 | 범위 |
|---|------|------|
| 01 | Theoretical Foundations | Regime Complex · Two-Level Games · Issue Linkage · Epistemic Communities |
| 02 | Methodology | 3-stage pipeline 공식 사양 |
| 03 | Data Architecture | StanceRecord schema v1.3 |
| 04 | Stage 1 Stance Extraction | Multi-sample k=5 + Bayesian CI + Platt calibration |
| 05 | Stage 2 Graph Analysis | R-GAT + Leiden + Apriori hyperedge mining |
| 06 | Stage 3 Briefing Generation | Graph-Grounded Generation + 7-rule verification |
| 07 | Evaluation Protocol | Task A-D + threshold + ablation matrix |
| 08 | Novelty Positioning | C1-C10 학술 기여 |
| 09 | Ministerial Briefing Template | Track A 출력 양식 |
| 10 | Council Protocol | 5-agent Phase A-E + Quality Gate 5종 |
| 11 | Source Catalog | Tier 1-4 소스 분류 |
| 12 | Data Collection Master Plan | 225 manifest 수집 계획 |
| 13 | Reference Tables | 20 countries × 12 groups × 6 issues × 16 sessions |
| 14 | Schema v1.3 Changes | NATO + frame + procedural changelog |
| 15 | Stage 2 Features (Procedural Authority) | chair_status + drafts_text edge type |

추가:
- **`CINA_FRAMEWORK.md`** (project root) — 핵심 프레임워크 마스터 정의서
- **`README.md`** (project root) — 프로젝트 개요 + Citation + Quickstart

---

## 6. 데이터 (Data Architecture)

### 6.1 Public (in repo)

- **`data/manifest/manifest.jsonl`** — 225 raw 문서 metadata (license, sha256, source, version)
- **`data/manifest/coverage_summary.json`** — 14 source systems 커버리지 통계
- **`data/README.md`** — 데이터 폴더 사용 안내
- **`docs/web/assets/data.json`** — 웹사이트 임베디드 실데이터 (Stage 1 + Stage 2 + IRR + Tasks)

### 6.2 Tier 1-4 Source Catalog (14 systems)

- **Tier 1 (Primary)**: UNFCCC Documents Portal (97), NDC Registry (53), IISD ENB (4)
- **Tier 2 (Calibration)**: Castro et al. 2025 ENB Dataset
- **Tier 3 (Context)**: IPCC AR6 WGII (4 chapters), COP30 Brazilian Presidency (6)
- **Tier 4 (Adjacent)**: IMF ND-GAIN (19/20 CINA), OWID CO2 (14MB), PRIMAP-hist v2.6.1 (72MB), WRI Climate Watch (183MB), OECD Measuring Progress 2024, Climate Action Tracker (10), Brazil Plano Clima (16 sectoral), Korea MOFA/MOE (4)

### 6.3 Private (excluded from public repo, Zenodo planned)

- `data/raw/` — ~720MB raw 다운로드 (저작권/license 이유로 Zenodo 별도)
- `data/processed/stances_complete_v1.jsonl` — 60 records 완전 추출본
- `data/processed/graph_analysis_v2.json` — Leiden + centrality 산출

---

## 7. 코드 (`src/` — MIT License)

### 7.1 파이프라인

- **`src/pipeline.py`** — End-to-end CLI orchestrator
- **`src/stage1_extract/`** — 5 LLM provider abstraction
  - `extract.py` / `extract_v2.py` — multi-sample + calibration
  - `providers/` — gemini, groq_provider, ollama_provider, openrouter, anthropic_provider, base
- **`src/stage2_graph/`** — NetworkX heterogeneous graph
  - `advanced_analysis.py` — Leiden (igraph + leidenalg) + 5 centralities
  - `generate_figures.py` — figure 생성 reproducible code
- **`src/stage3_brief/`** — Graph-Grounded Generation
- **`src/evaluation/`** — Phase 5 4-task + Ablation
  - `run_full_evaluation.py` — entry point
- **`src/validate/`** — Evidence validator (post-hoc 7-rule)

### 7.2 데이터 수집 (26 collectors)

- **`src/collect/`** — UNFCCC, NDC, ENB, IPCC, IMF, PRIMAP, WRI, Brazil, Korea, Castro 2025, OECD, CAT, ...
  - `manifest.py` — license/sha256 추적 inscriptor
  - `http_client.py` — rate-limit + 재시도 + checkpoint

### 7.3 Council 5-Agent System

- **`src/council/`** — 5-agent council infrastructure
  - `init_council.py` — 세션 초기화
  - `run_round.py` — Phase A→E orchestration
  - `state_manager.py` — 세션간 지속성
  - `state_schema.py` — Quality Gate 사양

### 7.4 Pipeline Scripts (P-series)

- `src/p01_chair_pipeline.py` — Brazil COP30 chair 권한 파이프
- `src/p01_merge_chair_metadata.py` — chair metadata 병합
- `src/p02_negative_authority_irr.py` / `_v2.py` — Brazil Δ 산출
- `src/p03_realist_b0_statistics.py` — Realist baseline F1
- `src/p04_hedging_density_2d_plot.py` — Figure 6 생성

---

## 8. 웹사이트 (Public Demo)

- **`docs/web/index.html`** — 메인 랜딩 (11 섹션, ~621 lines)
  - Hero (4 metrics) → Overview → Methodology → Korea Case → Brazil Case → Coalition Map → Findings → Evaluation → Figures → Council Process → Data
- **`docs/web/outputs.html`** — 본 인덱스의 웹 버전 (전 산출물 카탈로그)
- **`docs/web/assets/style.css`** — 모던 다크 테마 (~544 lines)
- **`docs/web/assets/script.js`** — 애니메이션 카운터 + 스크롤 관찰자
- **`docs/web/assets/data.json`** — 임베디드 실데이터 (22KB)
- **`docs/web/figures/`** — 7 PNG (위 §4 참조)
- **`docs/web/CINA_WEB_DEMO_README.md`** — 웹 데모 사용 안내

**배포 URL** (활성화 후): `https://zxsa0716.github.io/cina/web/`

---

## 9. 평가 결과 요약 (Phase 5)

```
Combined Rubric: 4.76 / 5  (Accept-eligible)
Quality Gates:    5 / 5    (G1 Coverage · G2 Evidence · G3 Theory · G4 Dual Review · G5 Heedo Alignment)

Task A (Stance Accuracy)
  Spearman ρ = 0.658  ✅ (≥ 0.6)
  MAE = 0.183         ✅ (≤ 0.25)

Task B (Coalition Detection)
  ARI proxy = 0.42    ✅ (≥ 0.4)

Task C (Outcome Prediction) ⭐
  P@3 = 1.00          ✅ (≥ 0.6)
  R@3 = 1.00          ✅ (≥ 0.6)

Task D (Briefing Quality)
  Mean panel = 4.53/5      ✅ (≥ 4.0)
  Krippendorff α = 0.905   ✅ (≥ 0.7)

Ablation A4 (Evidence grounding 제거): −0.15 ρ
  → 가장 load-bearing 컴포넌트
```

---

## 10. 경험적 관찰 (Observations)

> **Note**: 본 프로젝트는 단일 사례 회고 검증 파일럿이며, 아래 항목은 일반화 결론이 아닌 관찰입니다. 본 paper.md §5.6 한계 단락 참조. 자세한 비판적 자기 평가는 [`CRITICAL_REVIEW.md`](CRITICAL_REVIEW.md) 참조.

### Primary observations (3)

1. **Leiden 2 communities** — Stage 2 그래프 분석이 Keohane-Victor (2011) regime complex 'horizontal cleavage' 가설과 부합하는 분할 산출 (modularity 0.31, n=13). 더 큰 노드 셋에서의 재현 필요.
2. **Stance variance만으로 contested 3/3 정확 예측** (Task C, P@3=R@3=1.00 on N=3). 작은 표본의 고무적 신호. COP31 prospective 검증 예정.
3. **GGA-IND Authority-axis 6.1 (최저)** — Howlett (2019) framework 내에서 자발적 어휘의 정량적 상관물.

### Single-case findings (2) — 일반화 주장 없음

4. **Brazil 단일 사례 Δ = 0.304** — 의장국 1개의 국내(Plano Clima) ↔ 국제(L.25E) 정책수단 차이. Putnam × Howlett 교차점 후보 메트릭으로 제안. COP25-30 chair 국가들에 대한 replication 필요.
5. **L.25 advance↔final 텍스트 차이 zero** — 단일 이슈의 "pre-crystallized formula" 후보 신호. 최소 3개 chair-led 결정문에서 replication 필요.

### 부가 정량 결과

- Task A Spearman ρ = 0.658 (전문가 reference 대비)
- Realist baseline F1 = 0.560 (p<0.0001) — frame/instrument 변수의 추가 신호 필요성
- Korean IRR = 0.653, L&D-OP = 0.39 (한국 외교 권고 근거)
- Task D simulated 패널 평균 4.53/5 (**simulated panel — 실제 외부 전문가 검증 아님; LLM persona prompting의 self-evaluation 편향 가능성**)

---

## 11. 라이선스 / Citation

### License
- **Code** (`src/`, `*.py`): MIT License
- **Documentation, briefings, deliverables** (`docs/`, `deliverables/`): CC BY 4.0
- **Third-party data** (`data/raw/`): per-source (UNFCCC Open · IPCC Open · CC BY 4.0 · CC BY-NC-SA 4.0 등 — `manifest.jsonl` 추적)

### Citation

> **Note**: 본 프로젝트는 대학원 연구 과제로 진행 중이며, 아직 동료심사 학술지 게재 단계가 아닙니다 (No DOI assigned). 인용 시 다음 형식을 사용해 주세요:

```
Choi, Heedo (2026). CINA: Climate Issue-Network Analysis Framework
[graduate research project, unpublished].
Department of Climate Technology Convergence, Kookmin University.
https://github.com/zxsa0716/cina
```

---

## 12. 진행 단계 (Phase Tracker)

- ✅ **Phase 0** Framework + 15 docs scaffolding
- ✅ **Phase 1** Stage 1 LLM extraction (98 stances, 5 providers operational)
- ✅ **Phase 2** Stage 2 graph analysis (Leiden 2 communities, 5 centralities)
- ✅ **Phase 3** Stage 3 briefing generation (KO + EN, 9 sections + 4 appendices)
- ✅ **Phase 4** Class submission ready (Track A)
- ✅ **Phase 5** Quantitative evaluation (4-task + Ablation, 5/5 gates PASS)
- ⏭️ **Phase 6 (계획)** Real expert evaluators (KEI/KAIST/MOFA/MoE/GEP) + Castro 2025 SWISSUbase formal access + Stage 2 R-GAT torch implementation + journal submission

---

**작성**: 2026-05-04
**저자**: Heedo Choi, 기후기술융합학과, Kookmin University
**연락처**: zxsa0716@kookmin.ac.kr
**리포지토리**: https://github.com/zxsa0716/cina
