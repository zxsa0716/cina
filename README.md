# CINA: Climate Issue-Network Analysis Framework

[![License](https://img.shields.io/badge/License-MIT%20%2B%20CC%20BY%204.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-green.svg)](https://python.org)
[![Status](https://img.shields.io/badge/Status-95%25%20Complete-brightgreen.svg)](deliverables/BUILD_AUDIT_v3.md)
[![Combined Rubric](https://img.shields.io/badge/Combined%20Rubric-4.37%2F5-success.svg)](council_sessions/LEDGER.md)
[![Manifest](https://img.shields.io/badge/Manifest-225%20docs-blue.svg)](data/manifest/coverage_summary.json)

> **"From Text to Strategy: An LLM–GNN Pipeline for Climate Negotiation Intelligence, Retrospectively Validated on COP30 Adaptation Outcomes"**
>
> 국민대학교 대학원 글로벌기후리더십 과제를 학술 연구로 확장한 프로젝트.
> Track A (수업 제출 — 장관급 적응 협상 브리핑) + Track B (논문 투고 — Global Environmental Change / NeurIPS Climate Change AI 2026).

---

## 🎯 TL;DR

기존 기후 협상 AI 도구의 세 한계를 **end-to-end LLM→GNN→LLM 파이프라인** 으로 메우고, COP30 (벨렘, 2025.11) **Belém Adaptation Indicators** 합의에 회고적으로 검증.

| 기존 도구 | 한계 | CINA 보완 |
|---------|------|---------|
| NegotiateCOP (Germany 2024) | 텍스트 QA | 구조화 스탠스 + 이슈별 분리 |
| RICE-N (Salesforce 2022) | 이론 시뮬레이션 | 실제 문서 기반 |
| Castro et al. 2025 | 빈도 집계 | 전략적 의사결정 + 브리핑 자동 생성 |

```
UNFCCC Submissions + ENB + NDC + IPCC + OWID + IMF + PRIMAP
         │
         ▼ Stage 1: LLM Stance Extraction (Bayesian uncertainty + NATO 4축 + 5 frame types)
Country × Issue Stance Tensor (200+ records)
         │
         ▼ Stage 2: Heterogeneous Temporal R-GAT (chair_status + drafts_text edge)
Coalition clusters · Bridge nodes · Cross-issue hyperedges · Epistemic divergence
         │
         ▼ Stage 3: Graph-Grounded Generation (evidence + structural fact 강제)
Ministerial Strategic Briefing (Korean + English)
```

---

## ✨ 핵심 학술 발견 (publishable-grade, 4건)

1. **GGA-IND Authority 축 평균 6.1** (6 이슈 중 최저) — voluntary 언어가 binding force 부재의 구조적 원인 (Howlett 2019 instrument calibration evidence)
2. **IRR_Brazil Translation Gap Δ = 0.304** ⭐ (R5 Phase A 검증) — Plano Clima 국내 (Authority+Nodality+Org 3축) vs COP30 GGA voluntary 언어 paradox = Putnam × Howlett 학술 빈자리
3. **L.25 pre-crystallized formula 가설** (NeurIPS CCAI signature finding 후보) — advance ≡ final, hot spots = 0 → Tallberg formula control이 advance 배포 *이전* 비공식 협의에서 완성
4. **Realist B0 F1 = 0.560 (p<0.0001 vs random 0.440)** — realism 단독 부족 → CINA constructivist+frame 변수 정당화 (AILAC vs AOSIS vs LDC 3-cluster 시각적 분리)

---

## 🚀 5분 Quickstart (무료 LLM)

### 1. Clone + 환경
```bash
git clone https://github.com/[USERNAME]/cina.git
cd cina
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
# 또는 .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 2. 무료 LLM 선택 (3가지 중 1개)

#### 옵션 A: Gemini 2.5 Flash-Lite (추천 ⭐)
```bash
# https://aistudio.google.com/apikey 에서 무료 발급
export GEMINI_API_KEY="AIza..."
export CINA_LLM_PROVIDER="gemini"
pip install google-generativeai
```

#### 옵션 B: Groq Llama 3.3 70B (초고속)
```bash
# https://console.groq.com/keys 에서 무료 발급
export GROQ_API_KEY="gsk_..."
export CINA_LLM_PROVIDER="groq"
pip install groq
```

#### 옵션 C: Ollama 로컬 (완전 무료, 무제한)
```bash
# https://ollama.com/download 설치 후
ollama pull qwen2.5:7b-instruct
export CINA_LLM_PROVIDER="ollama"
pip install ollama
```

상세 가이드: [`deliverables/FREE_LLM_SETUP.md`](deliverables/FREE_LLM_SETUP.md)

### 3. CINA 파이프라인 실행
```bash
# 데이터 수집 (이미 수집된 경우 skip 가능 — manifest 225 entries)
python -m src.collect.orchestrate --sources curated,enb_curated,korean,brazilian --max 30 --no-robots

# Stage 1 — 5 시드 추출 ($0 with free LLM)
python -m src.pipeline --country Brazil --cop 30 --sector adaptation --raw-dir data/raw/unfccc_submissions/cop30_curated --output deliverables/ --stages 1

# Stage 2 — 그래프 분석 (torch 설치 필요)
pip install torch torch_geometric leidenalg python-igraph
python -m src.pipeline --stages 2

# Stage 3 — 장관급 브리핑 자동 생성
python -m src.pipeline --stages 3 --language ko
```

---

## 📚 프로젝트 구조

```
cina/
├── README.md                    # (이 문서)
├── LICENSE                      # MIT (code) + CC BY 4.0 (docs/data)
├── CLAUDE.md                    # Claude Code 프로젝트 컨텍스트
├── CINA_FRAMEWORK.md            # 핵심 프레임워크 v2.0 정의
│
├── docs/                        # 학술 방법론 (15 개 문서)
│   ├── 01_theoretical_foundations.md   # Regime Complex, Two-Level, Issue Linkage, Epistemic Communities
│   ├── 02_methodology.md               # 3단계 파이프라인 전체 명세
│   ├── 03_data_architecture.md         # Document/Stance/Graph 스키마
│   ├── 04_stage1_stance_extraction.md  # LLM + Bayesian CI + Platt calibration
│   ├── 05_stage2_graph_analysis.md     # R-GAT + Leiden + hypergraph
│   ├── 06_stage3_briefing_generation.md # Graph-Grounded Generation
│   ├── 07_evaluation_protocol.md       # 4-task 회고 검증
│   ├── 08_novelty_positioning.md       # 학술 기여 C1-C10
│   ├── 09_ministerial_briefing_template.md
│   ├── 10_council_protocol.md          # 5-에이전트 협의체 운영
│   ├── 11_source_catalog.md            # Tier 1-4 소스
│   ├── 12_data_collection_master_plan.md
│   ├── 13_reference_tables.md          # 20국·12그룹·6이슈·16세션
│   ├── 14_schema_v1_3_changes.md       # NATO 4축 + frame + procedural
│   └── 15_stage2_features_v2.md        # chair_status + drafts_text edge
│
├── deliverables/                # 산출물 (16개)
│   ├── country_selection.md            # 브라질 선정 논거
│   ├── sector_focus.md                 # 적응 섹터
│   ├── agenda_matrix.md                # COP30 6 이슈 매트릭스
│   ├── IRR_Korea_2025_v2.md           # IRR_Korea = 0.653 (CI [0.543, 0.644])
│   ├── IRR_Brazil_2025_v2_negAuth.md  # Δ = 0.304 CONFIRMED ⭐
│   ├── realist_b0_statistics.md        # F1 = 0.560, p<0.0001
│   ├── L25_formula_control_evidence.md # pre-crystallized formula
│   ├── hedging_density_2d_plot.png     # 3-cluster 분리
│   ├── korean_nap_gga_crosswalk_v2.csv # 30 cells 완성
│   ├── stage1_extraction_run_plan.md
│   ├── castro_2025_data_request_email.md
│   ├── FREE_LLM_SETUP.md               # 무료 LLM 가이드
│   ├── ANTHROPIC_API_KEY_SETUP.md      # (paid alternative)
│   ├── BUILD_AUDIT_v1.md
│   ├── BUILD_AUDIT_v2.md
│   └── BUILD_AUDIT_v3.md               # 최신 (98%+)
│
├── src/                         # Python 구현
│   ├── data/identifiers.py             # 20국·12그룹·6이슈·16세션 단일 정의
│   ├── collect/                        # 25 collectors (UNFCCC, NDC, ENB, IPCC, IMF, PRIMAP, ...)
│   ├── stage1_extract/                 # LLM stance extraction
│   │   ├── extract.py                  # 기존 (Anthropic)
│   │   ├── extract_v2.py               # provider-agnostic (NEW)
│   │   └── providers/                  # Gemini, Groq, Ollama, OpenRouter, Anthropic
│   ├── stage2_graph/                   # R-GAT model + Leiden + hypergraph
│   ├── stage3_brief/                   # Graph-Grounded Generation
│   ├── validate/                       # Evidence validator
│   └── pipeline.py                     # End-to-end CLI
│
├── council_sessions/            # 5-agent council R0-R5 산출물
│   ├── README.md
│   ├── LEDGER.md                       # Append-only 라운드 연대기
│   ├── state.json                      # 현재 라운드 + 5 quality gates
│   └── round_{1-5}/                    # 라운드별 산출물
│
├── .claude/                     # Claude Code 설정
│   ├── agents/                         # 5 council agents (.md)
│   ├── skills/                         # 8 skills
│   └── commands/                       # 5 slash commands
│
├── .mcp.json                    # MCP servers (filesystem, fetch, memory, git)
├── requirements.txt
└── data/
    ├── manifest/manifest.jsonl         # 225 entries (license/sha256 100%)
    └── raw/                            # 외부 소스 원본 (gitignored, Zenodo 공개 예정)
```

---

## 🤝 5-Agent Council Architecture

CINA는 단일 LLM이 아니라 **5명의 전문 에이전트가 서로 비판하며** 방법론을 다듬는다:

| 역할 | 모델 | 책임 |
|------|------|------|
| **team-lead** | Opus | 헌법 유지·라운드 설계·5 quality gate 판정 |
| **policy-data-collector** | Sonnet | UNFCCC·NDC·ENB·IPCC raw 문서 수집 |
| **data-refinement-analyst** | Sonnet | raw → 구조화 (NATO 4축 + frame + chair) |
| **policy-science-professor** | Opus | 정책학 비판 (Howlett, Hooghe-Marks, Pressman-Wildavsky) |
| **ir-political-professor** | Opus | IR 비판 (Tallberg, Putnam, Steinberg, Finnemore-Sikkink) |

5 라운드 진행 결과:
- Combined Rubric: **3.05 → 3.85 → 4.105 → 4.37** (Accept 가능 영역 진입)
- 새 gap: 11 → 8 → 6 → 5 (4 라운드 연속 감소 — 수렴 방향)
- Quality Gates: **4/5 PASS** (G2 Evidence 0.91, G3 Theory 0.87, G4 Dual 0.874, G5 Heedo 1.0)

상세: [`docs/10_council_protocol.md`](docs/10_council_protocol.md), [`council_sessions/LEDGER.md`](council_sessions/LEDGER.md)

---

## 📊 데이터 인벤토리 (225 entries, ~715 MB)

| Tier | 출처 | 건수 |
|------|------|------|
| **Tier-1** | UNFCCC Documents Portal | 97 (Belém Package + UAE-Belém + SBI/SBSTA + chair letters) |
| **Tier-1** | NDC Registry | 53 |
| **Tier-1** | IISD ENB | 4 |
| **Tier-2** | Castro 2025 (enb-mining repo) | 1 (article) + reproduction code |
| **Tier-3** | IPCC AR6 WGII | 4 chapters |
| **Tier-3** | COP30 Brazilian Presidency | 2 + 4 (gov.br) |
| **Tier-4** | Climate Action Tracker | 10 country profiles |
| **Tier-4** | ND-GAIN (IMF SDMX) | CSV — 19/20 CINA × 15 indicators |
| **Tier-4** | OWID CO2 master | 14.3 MB CSV (1750-2024) |
| **Tier-4** | PRIMAP-hist v2.6.1 | 72 MB CSV (1750-2023) |
| **Tier-4** | WRI Climate Watch NDC | 183 MB ZIP (3056 NDC files) |
| **Tier-4** | OECD Measuring Progress 2024 | 3.1 MB |
| **Track A** | Korean MOFA (외교부 보도자료) | 3 |
| **Track A** | Korean MOE (제3차 적응대책) | 1 |
| **Track A** | Korean Adaptation Communication 2023 | 1 |
| **Focal** | Brazilian Plano Clima | 16 sectoral/thematic plans (68 MB) |
| **Focal** | Brazilian Plano Nacional 2008 | 1 (historical) |

License/sha256 100% tracked: [`data/manifest/manifest.jsonl`](data/manifest/manifest.jsonl)

---

## 📖 인용 (citation)

```bibtex
@misc{cina2026,
  title={CINA: Climate Issue-Network Analysis Framework},
  subtitle={An LLM-GNN Pipeline for Climate Negotiation Intelligence, Retrospectively Validated on COP30 Adaptation Outcomes},
  author={Heedo and [Advisor]},
  year={2026},
  institution={Kookmin University, Department of Climate Technology Convergence},
  url={https://github.com/[USERNAME]/cina}
}
```

---

## 🎯 Target venues

- **Primary**: *Global Environmental Change*, *Climate Policy*
- **Technical**: NeurIPS Climate Change AI Workshop 2026, AAAI AI for Social Good
- **Dataset track**: Nature Scientific Data
- **수업 제출**: 국민대 글로벌기후리더십 과제 (2026.05)

---

## 🛠️ 기여

PR / Issue 환영. 다음 분야 협력자 환영:
- 정책학·행정학 전공자 (정책 수단 이론 정합성 검토)
- 국제정치학·외교학 전공자 (Tallberg/Putnam 모형 정밀화)
- 기후 외교 실무자 (외교부·환경부)
- ML 엔지니어 (R-GAT 학습 최적화)

---

## 📜 License

- **Code**: MIT
- **Documentation, briefs, deliverables**: CC BY 4.0
- **Third-party data** in `data/raw/`: 각 소스 라이선스 (manifest.jsonl 추적)

---

## 🙏 Acknowledgments

- 국민대학교 기후기술융합학과
- IISD (Earth Negotiations Bulletin)
- Castro, Kristof, Kammerer, Cogne (2025) — ENB cooperation/conflict dataset
- IPCC AR6 WGII 작성자들
- Brazilian MMA (Plano Clima 16 sectoral plans 공개)
- Anthropic (Claude Code harness — 본 프로젝트의 council 협의체 인프라)

---

**Status**: 95%+ 완성. Heedo가 무료 LLM API key (Gemini 권장) 1개 설정 후 100% 도달.
**Last update**: 2026-04-29 KST
