# AGENTS.md — CINA Project Context

이 폴더는 국민대학교 대학원 "글로벌기후리더십" 수업(2026-1학기)의 과제에서 출발하여, **논문 투고 가능한 AI 방법론 연구**로 확장된 CINA(Climate Issue-Network Analysis) 프로젝트의 작업 공간입니다.

## 1. 프로젝트 정체성

- **수업 과제 요건**: 특정 국가/섹터를 선정해 주무부처 장관급 COP 협상 브리핑 작성
- **확장 목표**: 단순 AI-작성 리포트가 아닌, LLM→GNN→LLM 3단 파이프라인으로 구성된 **재현 가능한 방법론**을 구축하고 이를 COP30 적응 협상(2025.11)에 회고적으로 검증하여 논문화
- **대상**: 국가=브라질(COP30 의장국), 섹터=적응(Adaptation), 검증 사건=Belém Adaptation Indicators (59개 지표 합의)
- **두 트랙**:
  - **Track A**: 2026년 5월 수업 제출용 장관급 브리핑 문서 (`deliverables/`)
  - **Track B**: NeurIPS Climate Change AI 워크숍 / Global Environmental Change 투고용 방법론 논문 (`docs/`)

## 2. 이 폴더의 구조

```
리더쉽/
├── AGENTS.md                    # (이 문서) 프로젝트 컨텍스트
├── README.md                    # 프로젝트 개요
├── CINA_FRAMEWORK.md            # 핵심 프레임워크 정의 문서
├── docs/                        # 방법론 상세 (논문 draft의 구성요소)
│   ├── 01_theoretical_foundations.md
│   ├── 02_methodology.md
│   ├── 03_data_architecture.md
│   ├── 04_stage1_stance_extraction.md
│   ├── 05_stage2_graph_analysis.md
│   ├── 06_stage3_briefing_generation.md
│   ├── 07_evaluation_protocol.md
│   ├── 08_novelty_positioning.md
│   └── 09_ministerial_briefing_template.md
├── deliverables/                # 수업 제출물
│   ├── country_selection.md
│   └── sector_focus.md
├── src/                         # Python 파이프라인 구현 스캐폴드
├── data/                        # 데이터 디렉토리 (원시/가공)
├── .Codex/
│   ├── skills/                  # 파이프라인 단계별 Codex skill
│   └── settings.json
├── .mcp.json                    # MCP 서버 설정
└── 원시 강의자료 PDF            # 교수 공지 자료
```

## 3. 작업 원칙

### 3.1 학술적 엄밀성
- 모든 방법론적 주장은 (a) 기존 연구의 구체적 한계 인용 + (b) 이론적 근거 + (c) 평가 프로토콜을 동반해야 한다.
- 비교 대상 baseline: Castro et al. 2025 (ENB dataset), NegotiateCOP RAG, MDPI 2025 heterogeneous stance networks, 단순 BERT fine-tuning.
- 모든 claim은 원문 인용(evidence_quote)으로 grounding 된다.

### 3.2 재현 가능성
- 모든 LLM 호출은 프롬프트 버전, temperature, seed를 기록한다.
- 모든 그래프 분석은 NetworkX/PyTorch Geometric 코드로 재현 가능해야 한다.
- 데이터 수집 스크립트는 UNFCCC 공식 포털과 IISD ENB를 소스로 한다.

### 3.3 Heedo의 기존 연구 전문성 활용
- GAT(Graph Attention Networks) 기반 모델링 → Stage 2에서 핵심 방법론
- XAI (Explainable AI) → 모든 단계에서 결정 근거를 노출
- IPCC AR6 Hazard-Exposure-Vulnerability 프레임워크 → 적응 섹터 이슈 분류 기준

## 4. 현재 단계

**Phase 0 (완료)**: 프레임워크 설계 및 문서 골격
**Phase 1 (진행)**: 데이터 수집 및 Stage 1 프롬프트 엔지니어링
**Phase 2**: GNN 모델 학습 + 평가
**Phase 3**: 브리핑 생성 및 expert evaluation
**Phase 4**: 수업 제출 + 논문 draft 완성

## 5. 작업 시 주의사항

- 수업 과제 제출은 **2026년 5월 마감** (확인 필요). 이 날짜를 넘기지 않도록 수업용 산출물(`deliverables/`)은 논문 draft와 독립적으로 먼저 완성한다.
- 모든 문서는 한국어·영어 병기가 아니라 한국어 우선. 논문용 영문 전환은 Phase 4에서 일괄 처리.
- 원시 PDF(`기후리더_*.pdf`)에는 교수 공지와 수업 프레임이 있으므로, 과제 요건 해석 시 반드시 참조한다.

## 6. 주요 참조 링크

- NegotiateCOP (독일정부 UNFCCC RAG): https://negotiatecop.org/
- UNFCCC Submission Portal: https://unfccc.int/documents
- IISD ENB: https://enb.iisd.org/
- Castro et al. 2025 (ENB dataset): https://www.nature.com/articles/s41597-025-06262-4
- COP30 공식: https://cop30.br/en
