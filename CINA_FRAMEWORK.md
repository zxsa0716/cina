# CINA: Climate Issue-Network Analysis Framework v2.0

*Master specification document*

---

## 0. Executive Summary (for the reviewer who reads only the first page)

**문제**: 기후 협상은 수백 개 국가·수십 개 이슈·수십 년의 역사를 가진 고차원 의사결정 공간이다. 한 국가의 협상단은 다른 국가의 공식 문서 수백 건을 읽고, 이슈별 연합 구조를 파악하고, 자국 이해관계와의 접점을 식별해야 한다. 현재 이 작업은 대부분 수작업이며, 소규모 개도국 대표단은 정보 비대칭에 시달린다.

**기존 AI 접근의 한계**:
- NegotiateCOP (Germany 2024): 문서 검색·QA에 머무름. 구조 분석 없음.
- RICE-N (Salesforce 2022): 이론 시뮬레이션. 실제 문서·실제 국가 입장 미반영.
- Castro et al. 2025 (Nature Sci Data): 협력/대립 **빈도** 집계. 이슈별 스탠스·전략적 함의 없음.
- Heterogeneous Stance Networks (MDPI 2025): 일반 SNS 스탠스 탐지. 기후외교 고유 구조(다중 이슈, 블록 구조, 이슈 연계) 미고려.

**CINA의 기여**: 원시 협상 문서에서 장관급 전략 브리핑까지 연결하는 **end-to-end 검증 가능 파이프라인**. 이론(regime complexity, two-level games, issue linkage)에 접지하고, 실제 COP30 결과(Belém Adaptation Indicators 59개)에 회고적으로 검증한다.

---

## 1. 이론적 근거 (Theoretical Grounding)

CINA는 4가지 국제관계·환경정치 이론에 기반한다:

### 1.1 Regime Complex Theory (Keohane & Victor, 2011)
기후 거버넌스는 단일 regime이 아니라 UNFCCC, Paris Agreement, Loss and Damage fund, 관련 IO들이 얽힌 "regime complex"다. 이는 이슈별로 다른 규칙·다른 참여자·다른 권력 구조가 공존함을 의미한다. → **함의**: 국가 스탠스는 이슈마다 다르며, 단일 "기후 정책 입장" 벡터로 환원할 수 없다. CINA의 이슈별 분리 모델링의 근거.

### 1.2 Two-Level Games (Putnam, 1988)
협상가는 국제 테이블(Level I)과 국내 정치(Level II)의 교집합 "win-set" 안에서만 합의 가능하다. → **함의**: 국가의 공식 submission은 국내 win-set의 경계를 반영한다. 동일 이슈라도 국가의 국내 제약이 다르면 flexibility signal이 다르게 나타난다. CINA의 `flexibility_signals` 추출의 근거.

### 1.3 Issue Linkage Theory (Tollison & Willett, 1979; Haas 1980)
합의 불가능해 보이는 단일 이슈도 다른 이슈와 묶으면 파레토 개선이 가능하다. → **함의**: 협상 전략의 핵심은 이슈 간 연계(linkage) 식별. CINA의 cross-issue hypergraph 모듈의 근거.

### 1.4 Epistemic Communities (Haas, 1992)
기술적 이슈에서 과학자·전문가 네트워크가 정책 수렴을 유도한다. → **함의**: COP30 Belém Adaptation Indicators 사례에서 "전문가 원안" vs "정치적 재작성"의 divergence는 epistemic community와 정치 블록의 긴장을 보여준다. CINA의 평가 과제: 이 divergence를 구조적으로 예측할 수 있는가?

---

## 2. 파이프라인 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                   INPUT LAYER                                │
│  UNFCCC Submissions (공식 입장문)                           │
│  NDCs (국가 감축·적응 계획)                                 │
│  ENB Summaries (IISD 일일 요약, 1995–)                     │
│  Castro et al. 2025 Dataset (interaction ground truth)      │
└────────────────┬────────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 1: CALIBRATED STANCE EXTRACTION (LLM)                │
│                                                              │
│  • Multi-sample generation (T=0.3, n=5) per (country,issue) │
│  • Structured output: stance score ∈ [−1,+1] with           │
│    Bayesian credible interval + evidence quotes             │
│  • Calibration: Platt scaling against ENB-coded interactions│
│                                                              │
│  Output: Stance Tensor S ∈ R^{N×I×3}                        │
│    (N=countries, I=issues, 3=score/lower/upper)             │
└────────────────┬────────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 2: HETEROGENEOUS TEMPORAL GAT                        │
│                                                              │
│  Node types:                                                │
│    • Country (N ≈ 195)                                      │
│    • Issue (I ≈ 6 for adaptation sector)                    │
│    • Negotiation group (G ≈ 12: G77, EU, AOSIS, …)          │
│                                                              │
│  Edge types:                                                │
│    • Country—Issue (stance, weight = stance_score)          │
│    • Country—Country (historical cooperation from Castro)   │
│    • Country—Group (membership)                             │
│    • Temporal: time-varying edge weights (2015–2025)        │
│                                                              │
│  Model: Heterogeneous Graph Attention Network (R-GAT)       │
│    • Attention weights α ∈ [0,1] per edge                   │
│    • Trained for: (a) coalition prediction,                 │
│                   (b) outcome prediction                    │
│                                                              │
│  Analysis outputs:                                          │
│    1. Community detection (Leiden) per issue                │
│    2. Betweenness centrality → bridge countries             │
│    3. Cross-issue hypergraph (3+ nodes as hyperedges)       │
│    4. Attention heatmap as XAI artifact                     │
└────────────────┬────────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 3: GRAPH-GROUNDED BRIEFING GENERATION (LLM)          │
│                                                              │
│  Input: structured analysis JSON from Stage 2 + evidence    │
│                                                              │
│  Generation constraints:                                    │
│    • Every claim must cite ≥1 evidence_quote AND            │
│      ≥1 structural fact (centrality, cluster ID, etc.)      │
│    • Output follows fixed ministerial brief template:       │
│      1. Situation / 2. Coalition map / 3. Leverage          │
│      4. Package deals / 5. Red lines / 6. Recommendation    │
│                                                              │
│  Hallucination prevention: assertion ↔ evidence table       │
└────────────────┬────────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT: Ministerial Strategic Briefing                     │
│                                                              │
│  + Interactive dashboard (React + D3)                       │
│  + Reproducibility bundle (code + data + prompts)           │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 대상 사례: 브라질 × COP30 × 적응

### 3.1 왜 브라질인가
- **의장국**: COP30(벨렘, 2025.11)의 의장국으로서 모든 이슈를 조율하는 위치
- **구조적 특이성**: G77 회원이면서 BASIC(Brazil-South Africa-India-China) 멤버, 동시에 Amazon 생태계로 적응·산림 이슈에 독특한 입지
- **검증 가치**: 의장국은 이슈별로 포지션이 달라지므로 CINA의 이슈별 스탠스 분리 능력을 가장 강하게 테스트

### 3.2 왜 적응(Adaptation) 섹터인가
- **실제 COP30 핵심 쟁점**: Global Goal on Adaptation 지표 합의가 COP30 최대 성과이자 논쟁점
- **데이터 풍부**: UAE–Belém 2년 프로그램(COP28 결정 11/CMA.5)으로 2024–2025 기간 submission이 집중됨
- **Rube Goldberg 사건**: 브라질 의장국이 전문가 제안을 재작성한 59-indicator 합의는 CINA의 구조적 예측력을 시험하는 완벽한 ground truth

### 3.3 적응 섹터 내 하위 이슈 (I=6)
COP30 공식 의제 기반:

| 약어 | 이슈 | 핵심 쟁점 |
|------|------|----------|
| GGA-IND | Global Goal on Adaptation indicators | 수량적·정성적, 선택/필수, 능력 맥락 |
| ADAPT-FIN | Adaptation finance | 2025년까지 2배→2035년까지 3배 (실제 합의) |
| L&D-OP | Loss and Damage Fund 운영 | 기여 의무국, 접근성 |
| NAPs | National Adaptation Plans 이행 | 보고 주기, 기술 이전 |
| MIT-ADAPT | 감축-적응 연계 | synergy vs trade-off |
| JT-ADAPT | Just Transition 내 적응 | 취약계층 보호 조항 |

---

## 4. 평가 프로토콜 (Evaluation)

### 4.1 회고적 검증 (Retrospective Validation)
COP30 종료 이후 실제 결과(합의 텍스트)가 공개되었으므로, CINA를 **pre-COP30 문서만으로** 훈련/추론한 뒤 예측과 실제를 비교한다.

**Task A — 스탠스 정확도**:
- Metric: Country × Issue 스탠스 점수 vs 전문가 수작업 코딩 (n=50 샘플)
- 지표: Spearman ρ, Krippendorff's α, 신뢰구간 coverage

**Task B — 연합 탐지**:
- Metric: CINA 추출 커뮤니티 vs ENB-coded 협력 패턴 (Castro et al. 2025)
- 지표: Normalized Mutual Information, Coalition F1@k

**Task C — 결과 예측**:
- Metric: 합의된 59 indicators 중 CINA가 예측한 핵심 분열 지점과 실제 분열 지점의 일치율
- 지표: Precision@10, Recall@10 on contested indicators

**Task D — 브리핑 품질 (Expert Eval)**:
- Rubric: 정확성(facts cited), 전략적 통찰(non-trivial insights), 가독성, 할루시네이션
- 평가자: 기후 협상 경험자 3인 블라인드 비교 (CINA vs GPT-5 zero-shot vs 인간 작성)
- 지표: 5점 척도 mean + inter-rater reliability

### 4.2 Baseline
- **B1**: Keyword + 감성분석 기반 스탠스 추출
- **B2**: BERT fine-tuned on Castro et al. 2025 cooperation labels
- **B3**: NegotiateCOP의 QA 답변을 인간 코더가 구조화
- **B4**: GPT-5 zero-shot 브리핑 (그래프 분석 없이)

### 4.3 Ablation
- A1: Stage 1만 (그래프 없이 LLM만)
- A2: Stage 1+2만 (브리핑 없이 대시보드만)
- A3: Full pipeline (CINA)
- A4: Full + 전문가 피드백 루프 (human-in-the-loop)

---

## 5. 수업 제출물 vs 논문 산출물 매핑

| 수업 과제 요구 | CINA 산출물 | 파일 |
|--------------|-------------|------|
| 국가 선정 근거 | 브라질 의장국 선정 분석 | `deliverables/country_selection.md` |
| COP 중점 아젠다 | 적응 섹터 6개 이슈 매트릭스 | `deliverables/agenda_matrix.md` |
| 각국/그룹 스탠스 | CINA Stage 2 연합 맵 | `deliverables/coalition_map.md` |
| 장관급 브리핑 | Stage 3 자동 생성 브리핑 | `deliverables/ministerial_briefing.md` |

| 논문 장 | CINA 산출물 | 파일 |
|-------|-------------|------|
| Introduction | 기존 도구의 한계 | `docs/08_novelty_positioning.md` |
| Related Work | 문헌 정리 | `docs/01_theoretical_foundations.md` |
| Methodology | 3단계 파이프라인 | `docs/02_methodology.md` ~ `06_*` |
| Evaluation | 4-task 평가 | `docs/07_evaluation_protocol.md` |
| Discussion | 한계와 정책 함의 | `docs/08_novelty_positioning.md` |

---

## 6. 로드맵

| Phase | 기간 | 목표 | 주요 산출물 |
|-------|------|-----|------------|
| 0 | 현재 | 프레임워크 문서화 | 본 문서 + `docs/` 전체 |
| 1 | +2주 | 데이터 수집 + Stage 1 프롬프트 v1 | `data/raw/`, `src/stage1_extract/` |
| 2 | +4주 | 그래프 구축 + GAT 학습 | `src/stage2_graph/`, 연합 맵 |
| 3 | +6주 | 브리핑 생성 + expert eval | `deliverables/`, eval report |
| 4 | +8주 | 수업 제출 + 논문 v1 draft | 제출 완료 + arXiv preprint |

---

## 7. 위험 요소와 대응

| 위험 | 대응 |
|------|------|
| UNFCCC 문서 접근 제약 | NegotiateCOP API + IISD ENB 공개 데이터 사용 |
| LLM 스탠스 추출 신뢰도 | Multi-sample + Bayesian calibration + 전문가 검증 세트 |
| 그래프 데이터 희소성 | Castro et al. 2025 interaction 데이터로 prior 제공 |
| 할루시네이션 | Evidence grounding 강제 (인용 없는 claim 필터링) |
| 정치적 민감성 | 최종 브리핑은 공개 소스만 사용, 기밀 정보 포함 안 함 |

---

## 8. 이 문서를 Claude가 어떻게 쓰는가

이 `CINA_FRAMEWORK.md`는 프로젝트의 **헌법 문서**이다. 변경 시:
1. 변경 근거를 Heedo와 명시적으로 합의한다.
2. 변경된 section의 관련 `docs/*.md`를 함께 업데이트한다.
3. 이 문서의 date-stamped change log를 갱신한다 (`## 9. Change Log`).

## 9. Change Log

- 2026-04-24: v2.0 초기 작성. COP30 retrospective validation framing 채택. Heedo와 합의.
