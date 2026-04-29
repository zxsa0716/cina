# 07. Evaluation Protocol — 평가 설계

> CINA가 "정말로 작동하는가"를 입증하는 평가 설계. 회고적 검증(retrospective validation)을 중심으로, 4개 task에서 baseline 대비 개선을 측정.

## 1. 평가 철학

### 1.1 왜 회고적 검증인가
COP30(2025.11)이 이미 종료되었고 Belém Adaptation Indicators 59개 합의가 공개된 지금, **사전 문서(COP28~29 submission)만으로** CINA를 훈련/추론한 뒤 COP30 결과를 얼마나 예측하는지를 측정할 수 있다. 이는 전형적인 held-out 시간 validation이다.

### 1.2 평가 단위
- Task A: 스탠스 정확도 (Country × Issue)
- Task B: 연합 탐지 (이슈별 클러스터링)
- Task C: 결과 예측 (합의 텍스트의 분열/타협 지점)
- Task D: 브리핑 품질 (expert 평가)

---

## 2. Task A — 스탠스 정확도

### 2.1 Ground Truth 구축
- **Source**: COP30 이전(2025.10)까지의 UNFCCC 공식 submission 및 ENB 요약에서 $n=50$ (국가, 이슈) 쌍을 층화 샘플링
  - 20개 주요 참여국 × 6 이슈 = 120개 조합 중 50개
  - 층화: stance 분포가 양극단에 치우치지 않도록
- **Coding**: Heedo + 기후 전공자 1명 (가능 시 지도교수)이 독립 코딩
- **라벨**: stance score ∈ [−1, +1] 연속값 + stance category (6단계)
- **동의도**: Krippendorff's α ≥ 0.7 목표 (계속 < 0.7이면 rubric 조정 후 재코딩)

### 2.2 평가 메트릭
| Metric | 정의 | 목표 |
|--------|-----|------|
| Spearman ρ | 예측 vs 정답 순위 상관 | ≥ 0.6 |
| MAE | 연속값 절대오차 평균 | ≤ 0.25 |
| Category F1 | 6단계 분류 F1 (macro) | ≥ 0.55 |
| CI coverage | 95% CI가 정답 포함하는 비율 | ≥ 0.90 |

### 2.3 Baseline
- **B1**: VADER 감성분석
- **B2**: DistilBERT fine-tuned on Castro 2025 cooperation labels
- **B3**: GPT-5 zero-shot (동일 프롬프트, single sample)
- **B4**: CINA w/o calibration (raw LLM)
- **B5**: CINA w/o multi-sampling (single sample + calibration)

### 2.4 통계적 검정
Paired bootstrap (n=1000) 으로 Spearman ρ 차이의 95% CI 산출. 유의한 개선 여부 판단.

---

## 3. Task B — 연합 탐지

### 3.1 Ground Truth
- Castro et al. 2025 ENB 데이터에서 COP30 시점 **cooperation cluster** 추출
- 또는 IISD의 공식 협상 그룹 membership을 pseudo-ground-truth로 사용

### 3.2 Metric
| Metric | 정의 |
|--------|-----|
| NMI (Normalized Mutual Information) | 예측 클러스터와 정답 클러스터의 유사도 |
| ARI (Adjusted Rand Index) | 쌍 기반 일치도 |
| Modularity | 예측 클러스터의 내부 응집도 |
| Coalition F1@k | 상위 k개 주요 연합의 F1 |

### 3.3 Baseline
- **B1**: 공식 negotiation group 그대로 사용 (G77, EU, AOSIS, ...)
- **B2**: Stage 1 스탠스만으로 k-means (no GNN)
- **B3**: Castro 2025 cooperation matrix에서 Louvain

CINA가 B1보다 낫다 = "이슈별로 공식 그룹이 쪼개지는 실질 연합을 탐지한다"
CINA가 B2보다 낫다 = "GNN이 단순 스탠스 벡터를 넘어 상호작용 구조를 포착한다"

---

## 4. Task C — 결과 예측

### 4.1 핵심 질문
CINA가 COP30 사전 데이터만으로 **59개 Belém Indicators의 합의 구조**를 어디까지 예측할 수 있었나?

### 4.2 Ground Truth
- COP30 최종 결정문 텍스트 (cop30.br 공식)
- IISD 분석: 어떤 indicator가 contentious했는지, 어떤 그룹이 주도/저항했는지

### 4.3 하위 task
**C-1. Contested Issue Prediction**:
- Input: 사전 스탠스 텐서 + 그래프
- Target: 59 indicators 중 합의 과정에서 "논쟁적"이었던 indicator 집합
- Metric: Precision@10, Recall@10

**C-2. Coalition-Outcome Attribution**:
- Input: Stage 2 커뮤니티
- Target: 최종 합의문에서 각 블록의 관철율 (wins/demands)
- Metric: Kendall's τ between predicted power and actual wins

**C-3. Epistemic Divergence Prediction**:
- Input: Stage 2 epistemic_divergence score
- Target: 전문가 원안 vs 최종 합의 간 거리 (인간 코더가 평가)
- Metric: Correlation coefficient

### 4.4 핵심 서사
만약 CINA가 "GGA-IND 이슈에서 브라질 의장국 주도의 정치적 재작성 가능성 높음"을 사전 flag했다면, 그것은 단순히 LLM이 submission을 요약한 수준을 훨씬 넘는 **구조적 통찰**이다. 이 하나의 성공 사례가 논문의 핵심 contribution 스토리.

---

## 5. Task D — 브리핑 품질 (Expert Evaluation)

### 5.1 설계
- CINA 브리핑 vs 3개 baseline 브리핑 (blind comparison)
  - **B1**: GPT-5 zero-shot 브리핑 (그래프 없이)
  - **B2**: NegotiateCOP 검색 결과를 수작업 정리
  - **B3**: 인간 작성 (Heedo가 동일 데이터로 직접 작성)
- 평가자: 기후 협상 경험자 3인 (예: KEI, KAIST 녹색기술정책 전공자, 환경부 재직자 후보)
- 평가 방식: 1~5점 Likert rubric, 블라인드 (브리핑 출처 익명화)

### 5.2 Rubric (5 dimensions)
1. **Factual accuracy**: 인용 출처가 실제로 해당 내용인가
2. **Strategic insight**: 자명하지 않은 구조적 통찰이 있는가
3. **Actionability**: 권고가 실행 가능한가
4. **Readability**: 장관급 독자에게 적합한가
5. **Uncertainty handling**: 불확실성이 적절히 표시되었는가

### 5.3 Inter-rater reliability
- Krippendorff's α (per dimension)
- 5인 이상 확보 시 ICC도 보고
- α < 0.5 인 dimension은 rubric 재정의 후 재평가

### 5.4 Supplementary metric: 할루시네이션 rate
각 브리핑의 모든 factual claim을 독립 검증자가 체크. "해당 문서에 없는 주장"의 비율을 측정. CINA ≤ 1%, baseline ≥ 5%를 가설로.

---

## 6. Ablation Study

CINA의 각 요소가 얼마나 기여하는지:

| Variant | 변경 | 측정 |
|---------|------|-----|
| A0 (full) | CINA 전체 | baseline |
| A1 | Stage 2 그래프 없이 Stage 3로 바로 | coalition accuracy 감소 확인 |
| A2 | Stage 1 calibration 제거 | stance MAE 변화 |
| A3 | Stage 1 multi-sample 제거 (k=1) | CI coverage 감소 |
| A4 | Stage 3 evidence grounding 강제 해제 | 할루시네이션율 증가 |
| A5 | Cross-issue hypergraph 제거 | package deal 탐지 누락 |

---

## 7. 실험 일정

| Week | 작업 |
|------|------|
| 1 | Calibration set 구축 (n=50 expert coding) |
| 2 | Task A 실행 (Stage 1 on COP30 pre-data) |
| 3 | Task B 실행 (Stage 2 학습·커뮤니티) |
| 4 | Task C 실행 (post-COP30 결과와 비교) |
| 5 | Task D 준비 (expert 평가자 섭외, 브리핑 생성) |
| 6 | Task D 실행 (expert eval) |
| 7 | 통계 분석 + Ablation |
| 8 | 논문 figure/table 작성 |

---

## 8. 보고 방식 (Results Section 예상 구조)

### 8.1 Figure 1: 전체 파이프라인 diagram

### 8.2 Table 1: Task A results
| Method | Spearman ρ | MAE | Cat F1 | CI coverage |
|--------|-----------|-----|--------|-------------|
| B1 VADER | 0.21 | 0.54 | 0.28 | — |
| B2 BERT | 0.45 | 0.36 | 0.41 | — |
| B3 GPT-5 zs | 0.52 | 0.31 | 0.47 | — |
| B4 CINA no-cal | 0.58 | 0.28 | 0.51 | 0.61 |
| B5 CINA k=1 | 0.57 | 0.29 | 0.50 | 0.44 |
| **CINA full** | **0.64** | **0.24** | **0.58** | **0.92** |

### 8.3 Figure 2: Coalition map comparison (official vs CINA-detected)

### 8.4 Table 2: Task C contested issue prediction

### 8.5 Figure 3: Expert evaluation radar chart (5 dimensions)

### 8.6 Table 3: Ablation results

---

## 9. 결과 해석 가이드

### 9.1 CINA가 baseline보다 **명확히 나은** 영역이 있어야 할 것
- Uncertainty quantification (CI coverage)
- 이슈별 분리된 연합 탐지
- Evidence traceability
- Cross-issue linkage 탐지

### 9.2 CINA가 **비교 가능한** 수준일 것
- 단일 국가 스탠스 분류 (단순 BERT도 잘함)

### 9.3 CINA가 **약점**일 수 있는 영역
- 실시간 업데이트 (NegotiateCOP 같은 production 시스템이 유리)
- 자연어 생성 유창성 (순수 LLM 베이스라인과 비교)

이 약점을 논문 discussion에 솔직하게 서술.

---

## 10. 통계적 검정 요약

- Task A, C: Paired bootstrap (n=1000)
- Task B: Permutation test (n=1000) on NMI
- Task D: Wilcoxon signed-rank test (per dimension)
- 다중 비교 보정: Benjamini-Hochberg (FDR < 0.05)

---

## 다음 문서
- [08_novelty_positioning.md](08_novelty_positioning.md) — 논문 contribution positioning
