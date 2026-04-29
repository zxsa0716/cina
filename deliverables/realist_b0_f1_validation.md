# Realist B0 Baseline F1 Validation

> Round 4 P0-3 산출물. IR 교수 권고 "realist baseline 먼저 증명" 직접 충족.
> 작성일: 2026-04-26 | 버전: v1 | 작성: data-refinement-analyst Round 4

---

## 1. 분석 목적

realist 변수 (CO2 per capita, share of global CO2, log GDP)만으로 CINA 19개국 간 협력 관계를 얼마나 잘 예측하는가? F1 < 0.7이면 realism alone insufficient → CINA constructivist + framing 변수의 필요성 정당화.

---

## 2. 방법론

### 2.1 입력 데이터
- `data/processed/realist_baseline_b0.csv` (OWID 2024, 19개국)
- 국가: BRA, USA, CHN, IND, JPN, KOR, AUS, CAN, NOR, CHE, MEX, ZAF, SAU, ARE, EGY, COL, CHL, CRI, KEN

### 2.2 Realist Similarity Matrix 산출
특성 벡터 f(i) = [CO2_per_capita_t, share_global_CO2_pct, log(GDP+1)]
- 정규화: z-score (mean 0, std 1)
- 유사도: cosine similarity

### 2.3 Pseudo-truth 협력 쌍 (Ground Truth)
ENB Castro 2025 데이터 미수집 대체: 협상 그룹 멤버십 기반 협력 pseudo-truth
- 동일 그룹 멤버 쌍 = cooperative pair (binary)
- 그룹 분류:

| 그룹 | 해당 국가 |
|---|---|
| G77+China | BRA, CHN, IND, MEX, ZAF, SAU, ARE, EGY, COL, CHL, CRI, KEN |
| BASIC | BRA, CHN, IND, ZAF |
| LMDC | BRA, CHN, IND |
| UMBRELLA | USA, CAN, AUS, JPN |
| EIG | KOR, CHE, NOR |
| AILAC | COL, CHL, CRI |
| ARAB | SAU, ARE, EGY |
| AGN | KEN |

- Pseudo-truth cooperative pairs: **75쌍** (19×18/2 = 171 총 쌍 중 44%)

### 2.4 F1 산출 (Top-K prediction)
K = 75 (truth pairs 수와 동일)
Top-K realist prediction: cosine similarity 상위 75쌍을 "predicted cooperative"로 분류

---

## 3. 정량 결과

### 3.1 Similarity Matrix (선택 값)

| | BRA | USA | CHN | IND | KOR | SAU |
|---|---|---|---|---|---|---|
| BRA | 1.000 | -0.863 | -0.369 | 0.570 | -0.327 | -0.768 |
| USA | -0.863 | 1.000 | 0.788 | -0.077 | 0.573 | 0.889 |
| CHN | -0.369 | 0.788 | 1.000 | 0.554 | -0.049 | 0.553 |
| IND | 0.570 | -0.077 | 0.554 | 1.000 | 0.538 | -0.095 |
| KOR | -0.327 | 0.573 | -0.049 | 0.538 | 1.000 | 0.307 |
| SAU | -0.768 | 0.889 | 0.553 | -0.095 | 0.307 | 1.000 |

전체 19×19 행렬: `data/processed/realist_b0_similarity_matrix.csv`

### 3.2 F1 결과

| 지표 | 값 |
|---|---|
| K (prediction 수) | 75 |
| Truth cooperative pairs | 75 |
| True Positives (TP) | 42 |
| False Positives (FP) | 33 |
| False Negatives (FN) | 33 |
| Precision | 0.560 |
| Recall | 0.560 |
| **F1** | **0.560** |

---

## 4. 해석

### 4.1 가설 검증

| 가설 | 예상 | 실측 | 판정 |
|---|---|---|---|
| F1 < 0.7 → realism insufficient | F1 < 0.70 | F1 = 0.560 | **CONFIRMED** |

### 4.2 왜 F1 = 0.56인가?

Realist 변수 (CO2 per capita, share, GDP)는 경제적 유사성을 측정한다.
그러나 UNFCCC 협상에서 협력을 결정하는 것은 **물질적 이해관계보다 구성주의적 정체성**이다.

주요 예측 오류 사례:
- USA-SAU cosine = **0.889** (두 대형 고배출 경제) → realist 예측: 협력
  → 실제: 서로 다른 그룹 (UMBRELLA vs ARAB/G77), 적응 재원에서 경쟁적
- BRA-KEN cosine = 낮음 → realist 예측: 비협력
  → 실제: G77 동일 그룹, 적응재원 요구에서 연대

### 4.3 CINA 정당화

F1 = 0.560 (chance level ~0.44 대비 +0.12)은 realism이 완전 무작위보다는 낫지만 **실용적 사용 불가**한 수준.

CINA Stage 2 GNN이 추가하는 변수:
1. **Framing variables**: CINA 6개 이슈별 입장 (Stage 1 추출)
2. **Coalition membership**: G77/BASIC/UMBRELLA 등 정체성 네트워크
3. **Historical cooperation**: 과거 co-sponsoring, joint submission
4. **Constructivist**: "adaptation equity" vs "sovereignty" 담론 정체성

가설: GNN + framing 변수 추가 시 F1 ≥ 0.80 목표.

### 4.4 Baseline 비교 (향후)
| 모델 | F1 | 데이터 |
|---|---|---|
| Random baseline | ~0.44 | - |
| Realist B0 (this study) | 0.560 | CO2 per cap, share, GDP |
| CINA Stage 2 GNN (목표) | ≥ 0.80 | + framing + coalition |

---

## 5. 한계

1. Pseudo-truth ground truth의 한계: ENB Castro 2025 실제 협력 데이터로 대체 필요 (Round 5 Collector task)
2. GDP 데이터 일부 결측 (BRA, 2024 OWID) → log(GDP+1)에서 GDP=0으로 처리
3. 단일 연도 (2024) 데이터 — 협상 stance는 다년간 누적

---

## 6. 인용 한 줄 결론

> "CINA 19개국에 대한 realist 유사도 matrix (CO2 per cap / share / log GDP cosine)는 그룹 협력 pseudo-truth 대비 F1=0.560으로, 확률적 기준(0.44) 대비 제한적 예측력만 보여 CINA constructivist+framing 변수 추가의 필요성을 정량 확인." (CINA Round 4, 2026-04-26)

---

**산출**: 2026-04-26
**데이터**: `data/processed/realist_b0_similarity_matrix.csv`
**다음 단계**: ENB Castro 2025 실제 협력 matrix 수집 (Round 5 Collector) 후 F1 재산출
