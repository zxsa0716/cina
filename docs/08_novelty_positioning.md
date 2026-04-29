# 08. Novelty Positioning — 학술적 기여의 정확한 위치

> CINA가 기존 연구의 어디에 위치하며, 왜 **새로운 기여**인가를 명시적으로 논증. 논문의 Introduction과 Discussion에 직접 사용.

## 1. 기존 연구 랜드스케이프 (Related Work)

### 1.1 AI for Climate Negotiations — 최근 5년 주요 연구

| 연구 | 방법 | 도메인 | 주요 산출물 | CINA와의 차이 |
|------|------|--------|------------|-----------|
| **NegotiateCOP** (GIZ, 2024) | RAG (retrieval-augmented generation) | UNFCCC submissions | 문서 시맨틱 검색 + QA | 텍스트 수준, 구조 분석 없음 |
| **RICE-N** (Salesforce, 2022; Zhang et al.) | Multi-agent RL + IAM | 경제·기후 시뮬레이션 | 협상 전략 자가학습 | 이론적; 실제 문서 미사용 |
| **Castro et al. 2025** (Nature Sci Data) | Rule-based + LLM coding of ENB | ENB 1995–2023 | Cooperation/conflict interaction dataset | 빈도 기록; 이슈별 세분화·전략 미지원 |
| **Kammerer & Hickmann 2024** | Manual content analysis + network | HLS 연설 | 국가 간 공동 언급 네트워크 | 수작업; 자동화·예측 불가 |
| **Debus et al. 2024** | LLM-agent coalition modeling | 독일 연정 협상 | LLM이 연정 협상 시뮬레이션 | 국내 정치; 국제 기후 미적용 |
| **Heterogeneous Stance Networks (MDPI 2025)** | LLM+GNN stance classification | 일반 SNS | 스탠스 분류 정확도 향상 | 기후외교 특수성 미반영 |
| **ChatClimate (2023)** | RAG with IPCC | IPCC 문서 QA | 과학 질문 응답 | 과학 사실; 협상 전략 아님 |

### 1.2 방법론 영역별 최신 성과

**Stance Detection with LLMs**:
- ICLR 2025 (Qs0qrvXJ25): LLM-generated synthetic data for stance detection
- 기여점: 합성 데이터로 LLM 출력 안정성 개선
- **CINA와의 차이**: 우리는 합성 데이터가 아니라 실제 UNFCCC 문서, 불확실성 정량화에 초점

**Graph Neural Networks for Political Analysis**:
- Huang et al. 2023: GNN for partisan prediction in congressional voting
- Liu et al. 2024: Temporal GNN for legislative coalition prediction
- **CINA와의 차이**: 국가 × 이슈 이종 구조, 이슈 연계 hypergraph

**Graph-Grounded Generation**:
- SelfCheckGPT, RAGAS 등 hallucination evaluation framework 존재
- **CINA의 새로움**: 텍스트 근거뿐 아니라 **네트워크 구조 근거**까지 claim에 묶음

---

## 2. CINA의 정확한 기여 (Contribution Itemization)

### 2.1 Technical Contributions

**C1. End-to-End Text → Graph → Strategic Brief Pipeline**
- 기후외교 도메인에서 최초로 통합된 파이프라인.
- 기존 도구들은 개별 단계(검색·스탠스·시뮬레이션)만 담당.

**C2. Calibrated LLM Stance Extraction with Uncertainty Quantification**
- Multi-sample (k=5) + Bayesian credible interval + Platt calibration against ENB ground truth.
- 기존 LLM 스탠스 연구는 단일 점 추정이 대부분.

**C3. Heterogeneous Temporal Graph Formulation for Climate Diplomacy**
- Country × Issue × Group 3-type 노드, 5-type 엣지, 시간축.
- 기존 정치 네트워크 분석은 homogeneous (국가-국가) 그래프.

**C4. Cross-Issue Linkage Hypergraph**
- Issue linkage theory (Tollison-Willett 1979)의 첫 계산적 구현.
- Apriori-style motif mining으로 package deal 후보 자동 탐지.

**C5. Graph-Grounded Generation (GGG)**
- 일반 RAG (텍스트 근거) + 구조 근거 (centrality, cluster ID).
- Claim-by-claim evidence traceability table.

**C6. Epistemic Divergence Prediction**
- 전문가 원안 vs 정치적 재작성 간 거리를 **사전** 예측.
- COP30 Belém Adaptation Indicators 사례에 실증.

### 2.2 Empirical Contributions

**C7. COP30 Retrospective Validation Benchmark**
- COP30 사전 데이터 + 사후 결과 쌍으로 구성된 공개 벤치마크.
- 4-task suite (스탠스·연합·결과·브리핑 품질).

**C8. CINA-Brazil-COP30 Dataset**
- 브라질 × 6 적응 이슈 × 2015–2025 스탠스 텐서 + 그래프.
- Expert-coded calibration set (n=50).

### 2.3 Theoretical Contributions

**C9. Computational Operationalization of Two-Level Games**
- win-set 개념을 `flexibility_signals` + `red_lines` 추출로 실체화.

**C10. Regime Complex Theory × Graph Representation**
- Keohane-Victor의 regime complex를 이종 그래프로 형식화.

---

## 3. "Why Now" Argument

### 3.1 기술적 성숙
- **LLM 능력**: structured output (JSON mode), tool use, long-context (200K+) 모두 2024–2025에 실용 수준 도달
- **HGNN 라이브러리**: PyTorch Geometric의 HeteroData가 2024에 안정화
- **Calibration 인프라**: Bayesian stance calibration 방법론이 최근 수렴

### 3.2 데이터 성숙
- Castro et al. 2025 ENB 데이터셋 공개로 ground truth 접근 가능
- NegotiateCOP의 UNFCCC 색인 덕에 문서 접근 API 존재
- COP30 종료 직후라 회고 검증 적기

### 3.3 정책 수요
- 소규모 개도국 대표단의 정보 비대칭 해소는 UNFCCC의 공식 Action agenda (Adaptation Community 2024)
- EU·미국이 AI 정책 분석 도구에 투자 증가

---

## 4. Target Venue별 포지셔닝

### 4.1 Nature Climate Change / Global Environmental Change (Primary)
- **메시지**: "AI 방법론이 기후 외교 의사결정에 제공하는 새로운 분석 층위"
- **강조점**: Policy relevance, retrospective validation, implications for small delegations
- **Figure 1**: 파이프라인 + COP30 실제 사례
- **Discussion**: Climate governance literature (Keohane, Bäckstrand)에 대한 기여

### 4.2 NeurIPS Climate Change AI Workshop (Technical)
- **메시지**: "Heterogeneous GNN + LLM pipeline with uncertainty quantification"
- **강조점**: 방법론 신규성, ablation, 재현성
- **주요 실험**: Task A (calibration), Ablation
- **Bonus**: Challenge track에서 open benchmark 제출

### 4.3 Climate Policy (Policy)
- **메시지**: "브라질 의장국 COP30 사례 분석: AI가 포착한 연합 역학"
- **강조점**: Case study narrative, policy recommendation
- **Figure**: Coalition map, package deal opportunities

### 4.4 Nature Scientific Data (Dataset track)
- **메시지**: "CINA-Brazil-COP30: open dataset for climate negotiation analysis"
- **강조점**: Data architecture, reproducibility, 공개

---

## 5. 경쟁 도구와의 직접 비교

### 5.1 vs NegotiateCOP
| 측면 | NegotiateCOP | CINA |
|------|-------------|------|
| 용도 | 문서 검색 + QA | 구조 분석 + 전략 브리핑 |
| 출력 | 텍스트 답변 | 정량 분석 + 브리핑 |
| 스탠스 | 없음 | Country × Issue × 불확실성 |
| 연합 | 없음 | 이슈별 커뮤니티 탐지 |
| 시간 | 최신 검색 | 시계열 분석 |
| 사용자 | 소규모 대표단 | 전략 담당자 |

→ **CINA ≠ NegotiateCOP의 대체**. NegotiateCOP를 **상위 레이어**로 사용 (Stage 0.5 데이터 접근).

### 5.2 vs Castro et al. 2025
| 측면 | Castro 2025 | CINA |
|------|------------|------|
| 데이터 | ENB 1995–2023 | UNFCCC submission + ENB + NDC |
| 분석 단위 | 국가 쌍 협력/대립 | 국가 × 이슈 스탠스 |
| 출력 | 데이터셋 | 분석 + 브리핑 |
| 방법 | Rule-based coding | LLM extraction + GNN |
| 기여 | Ground truth | Predictive framework |

→ **CINA는 Castro 2025를 ground truth로 사용**. Castro의 데이터가 없었다면 CINA 평가 불가능.

### 5.3 vs RICE-N
| 측면 | RICE-N | CINA |
|------|--------|------|
| 접근 | MARL simulation | Data-driven analysis |
| 국가 모델 | IAM + reward shaping | 실제 submission 기반 |
| 이슈 | 감축 중심 | 적응 전체 |
| 검증 | 이론적 | 회고적 empirical |

→ **CINA는 실증적 보완**. RICE-N의 균형 해는 CINA의 구조적 예측과 교차검증 가능.

---

## 6. 예상 비판과 대응

### 비판 1: "LLM 기반 추출은 편향적이다"
**대응**: Calibration protocol (Section 4 in docs/04) + expert-coded validation set + transparent uncertainty reporting.

### 비판 2: "COP30 데이터로만 검증하면 일반화 어렵다"
**대응**: 2차 검증을 COP31 (Turkey, 2026) 에 실시간 적용. Prospective validation도 준비 (Phase 4).

### 비판 3: "Hypergraph motif mining은 over-fitting 위험"
**대응**: Min_support threshold를 Castro 2025 데이터로 calibrate. Null model 비교 (random permutation).

### 비판 4: "장관급 브리핑은 기밀 영역이라 실제 영향력 측정 어렵다"
**대응**: Expert evaluation으로 proxy. Future work로 실제 대표단 사용 파일럿 제안.

### 비판 5: "전문가 원안 vs 정치적 재작성은 규범적 판단"
**대응**: "전문가 원안"은 2024–2025 SBI expert meeting report의 공식 텍스트로 정의. 해석 여지 축소.

---

## 7. 윤리적 고려

### 7.1 이중 사용 우려
CINA는 개도국 대표단의 정보 격차 해소를 목표하지만, 선진국이 도구를 선점해 협상력 격차 확대에 악용될 가능성도 있다.

**완화책**:
- 오픈 소스 공개
- 사용 윤리 가이드라인 (CINA Code of Use) 첨부
- 개도국 대표단 파일럿 우선

### 7.2 데이터 편향
UNFCCC 공식 문서는 정부 언어이므로, 실제 시민사회·기업·취약 커뮤니티 입장은 반영되지 않는다. 이 한계를 limitations section에 명시.

### 7.3 자동 전략 브리핑의 위험
"장관급 브리핑"이 사람의 판단을 대체하는 것이 아니라 **보조**임을 강조. 최종 결정은 인간 전문가가 내림.

---

## 8. 한 문장 요약 (elevator pitch)

> CINA는 UNFCCC 문서에서 장관급 전략 브리핑까지 연결되는 최초의 end-to-end AI 파이프라인으로, 기후외교에 특화된 이종·시간 그래프를 통해 이슈별 연합 역학과 이슈 연계 기회를 구조적으로 탐지하고, 모든 주장을 텍스트 인용과 네트워크 지표 양쪽에 동시에 접지한다. COP30 Belém Adaptation Indicators 합의에 회고적으로 검증하여, 단순 문서 QA나 경제 시뮬레이션이 제공하지 못하는 **전략적 통찰의 자동 생성**이라는 새로운 분석 층위를 열었다.

---

## 다음 문서
- [09_ministerial_briefing_template.md](09_ministerial_briefing_template.md)
