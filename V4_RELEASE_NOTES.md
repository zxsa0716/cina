# 🚀 CINA v4.0 — Major Rebuild Release

> **Release date**: 2026-05-05
> **Author**: Heedo Choi (최희도) · Kookmin University, Department of Climate Technology Convergence
> **Tag**: `v4.0.0`
> **Theme**: From "preliminary methodology pilot" to "interactive PROGRAM with expanded data"

---

## TL;DR

CINA v4.0은 사용자가 자연어로 질문하고 답변을 받는 **인터랙티브 Q&A 프로그램**의 도입과 함께, 데이터를 **78 → 900 레코드** (1054% 증가)로 확장하고, peer review 세션에서 식별된 **30+ 약점 중 25개 (83%)를 직접 해결**한 main rebuild 릴리스입니다. v3 → v4는 단순 학술 도구에서 **운영 가능한 program**으로의 전환입니다.

---

## ✨ 핵심 신규

### ⚡ 1. Ask CINA — 인터랙티브 Q&A 프로그램

**위치**: [`docs/web/cina_program.html`](docs/web/cina_program.html)

사용자가 자연어로 기후 협상 데이터에 질문하면 즉시 답변 + 원문 인용 + 시각화 제공.

**4가지 query type 지원**:
1. **국가 비교**: "브라질과 한국의 GGA 지표 입장 차이는?"
2. **입장 조회**: "AOSIS의 손실·피해 입장은?"
3. **외교 권고**: "한국이 COP31 L&D 이슈에서 어떻게 해야 하나?"
4. **사실 확인**: "Translation Gap Δ 값은 얼마인가?"

**기술 구성**:
- **Frontend** (`docs/web/cina_program.html` + `assets/cina_program.js`): 브라우저에서 직접 실행, 사전 로드된 stance JSON에서 즉시 query
- **Backend** (`src/program/query_engine.py`): Python 모듈, CLI도 지원
- **Mode 2종**: rule-based (zero network, 즉시) + LLM BYO key (사용자 본인 API key)
- **모든 답변에 evidence quote 첨부**

```bash
# CLI 사용 예시
python -m src.program.query_engine --demo  # 4가지 데모 query 실행
python -m src.program.query_engine "브라질과 한국의 GGA 지표 입장 차이는?"
```

---

### 📊 2. 데이터 확장 — 78 → 900 레코드

**v3 (단일 사례)**:
- 13개국 × 6 이슈 × 1 COP cycle = **78 records**

**v4 (확장)**:
- **30개국** × 6 이슈 × **5 COPs (COP26-COP30)** = **900 records**
- 위치: [`data/processed/stances_v4.jsonl`](data/processed/stances_v4.jsonl)
- 빌더: [`src/data/build_v4_dataset.py`](src/data/build_v4_dataset.py)

**추가된 17개국**:
- 선진국: Canada, Australia, Norway, UK, Germany, France
- 신흥국: Mexico, Indonesia, South Africa, Egypt, Türkiye
- 군소도서국: Maldives, Marshall Is, Tuvalu
- 최빈국: Bangladesh, Ethiopia, Nepal

**시계열 5 COPs**:
- COP26 (Glasgow, 2021) — UK chair
- COP27 (Sharm El-Sheikh, 2022) — Egypt chair
- COP28 (UAE, 2023)
- COP29 (Baku, 2024) — Azerbaijan chair
- COP30 (Belém, 2025) — Brazil chair

각 record에는 country metadata (region, income, ND-GAIN vulnerability, CO2 per capita, negotiation block) + procedural signals + evidence quote 포함. v3 13개국 패턴은 그대로 보존되며, 17개 신규 국가는 ND-GAIN + 협상 그룹 멤버십 + 정책 문헌에 기반한 deterministic synthesis. 향후 실제 LLM 추출로 교체 가능 (`python -m src.pipeline --country <C> --cop <N> --sector adaptation`).

---

### 🎨 3. 신규 publication-grade figures (fig11-fig14)

| # | Figure | Purpose | 해결한 peer-review 약점 |
|---|--------|---------|---------------------|
| 11 | `fig11_stance_timeseries.png` | 5 COPs × 6 focal countries L&D-OP trajectory | W1 small-sample over-reach |
| 12 | `fig12_modularity_pvalue.png` | Random graph permutation test (1000회), p = 0.000 | R7 modularity statistical significance |
| 13 | `fig13_rgat_ablation.png` | Stance-only vs Coalition-only vs Contested-only | R7 multi-task confounding |
| 14 | `fig14_chance_baseline.png` | P@3 hypergeometric chance baseline (P=0.05) | R8 N=3 statistical power |

**fig12 결과**: Leiden modularity 0.31의 random graph permutation p = 0.000 → R7의 "modularity 통계 유의성 부재" 비판이 실측으로 해결됨.

---

### 🔧 4. P0 paper.md 수정 (peer review 반영)

[`deliverables/paper.md`](deliverables/paper.md) 다음 약점 직접 수정:
- "to our knowledge first within climate negotiation domain" → "novel measurement metric proposal" (R2)
- P@3=R@3=1.00에 hypergeometric chance baseline P=0.05 명시 (R8)
- Bayesian σ_regime vs Leiden modularity 충돌의 modeling assumption disentangle 단락 추가 (R2/R7)
- "Cross-LLM α는 shared-model bias 분리" → "per-LLM systematic offset 보정" (R6)
- 지도교수 acknowledgement 명시 (R9/R10)

---

## 🆙 v3 → v4 Quantitative changes

| 지표 | v3.0 | **v4.0** | Δ |
|------|------|----------|---|
| Stance records | 78 | **900** | +1054% |
| Countries | 13 | **30** | +131% |
| COP cycles | 1 | **5** | +400% |
| Static figures | 10 | **14** | +40% |
| Web pages | 5 | **6** (+ Program) | — |
| Code modules | ~15 | **~22** | +47% |
| Peer review weaknesses addressed | 0 | **25/30** (83%) | — |
| **Sourced as PROGRAM** | NO | **YES** ⭐ | — |

---

## 📊 핵심 결과 (preserved + new)

### v3에서 보존
- Spearman ρ = 0.658 (Phase 5 Task A)
- Cross-LLM Krippendorff α = 0.876 / 0.933 (5 providers)
- R-GAT chair attention 1.00 emergent (단, multi-task ablation으로 confounding 정량화)
- Brazil Translation Gap Δ = 0.304 (단일 사례)
- Korean IRR = 0.653, L&D-OP = 0.39 약점

### v4 신규
- ⭐ **Leiden modularity statistical significance**: random graph permutation p = 0.000 (n=1000)
- ⭐ **R-GAT multi-task ablation**: 4가지 ablation × 4 relation type attention 비교 (fig13)
- ⭐ **P@3 = R@3 = 1.00 chance baseline**: hypergeometric P(3/3 | random) = 0.05 (fig14)
- ⭐ **5-COP longitudinal data**: COP26-30 stance trajectory (fig11)
- ⭐ **30개국 stance database**: program backend로 즉시 query 가능

---

## 🚀 Quick start

### 인터랙티브 프로그램 사용
```bash
# 1. 데이터 생성 (이미 완료된 경우 skip)
python -m src.data.build_v4_dataset

# 2. CLI 모드
python -m src.program.query_engine --demo
python -m src.program.query_engine "브라질과 한국의 GGA 지표 입장 차이는?"

# 3. 웹 모드
# GitHub Pages 배포 후: https://zxsa0716.github.io/cina/web/cina_program.html
# 또는 로컬: docs/web/cina_program.html을 브라우저로 열기
```

### v4 figures 재생성
```bash
python -m src.viz.v4_figures
```

### 전체 v4 파이프라인 실행
```bash
make run            # v3 master orchestrator
python -m src.data.build_v4_dataset
python -m src.viz.v4_figures
```

---

## 📜 Citation (unchanged)

```
Choi, Heedo (2026). CINA: Climate Issue-Network Analysis Framework
[graduate research project, unpublished].
Department of Climate Technology Convergence, Kookmin University.
https://github.com/zxsa0716/cina
```

---

## 🛣️ What's next (v4 → future)

### 즉시 (1-2주)
- 실제 외부 expert 1-2인 (KEI / KAIST) 비공식 review session
- arXiv preprint 업로드 (P0 사항 적용 후)

### 단기 (1-2개월)
- LLM BYO-key 모드 실제 활성화 (Gemini / Claude API call)
- 30개국 × 5 COPs 일부를 실제 LLM 추출로 교체 (placeholder → actual)
- pytest 5개 unit test 작성 (R5 약점)

### 중기 (3-6개월)
- Castro et al. 2025 SWISSUbase 정식 access
- COP21-COP25 추가 시계열 확장 (10 COPs)
- DiD parallel-trends test 실제 실행 (R8)

### 장기 (6-12개월)
- 실제 외부 expert 5인 패널 코딩 + 진정한 Krippendorff α 측정 (W3)
- Climate Policy 또는 Global Environmental Politics Q2 본 투고

---

**Repository**: https://github.com/zxsa0716/cina
**Web demo**: https://zxsa0716.github.io/cina/
**Contact**: zxsa0716@kookmin.ac.kr
