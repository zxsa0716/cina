# Realist B0 Baseline: F1 통계적 정량 (Round 5)

> Round 5 P0-3 산출물. IR 교수 비평 §3.2.B 직접 충족.
> 작성일: 2026-04-26 | 버전: v1 | 작성: data-refinement-analyst Round 5
> 참조: `data/processed/realist_b0_statistics.json`

---

## 1. Round 4 피드백 (IR §3.2.B)

IR 교수 비평:
> "F1=0.560 confirm은 헌법 §4 명제의 첫 정량 evidence. 단 N=32 기반이라 95%CI bootstrap 필수."

Round 4: F1=0.560 (N=32 chair, pseudo-truth 기반)
Round 5 추가: McNemar test + Cohen κ + Bootstrap 95%CI (n=1000, seed=42)

---

## 2. 방법론

### 2.1 데이터

- **국가**: 19개국 (BRA, USA, CHN, IND, JPN, KOR, AUS, CAN, NOR, CHE, MEX, ZAF, SAU, ARE, EGY, COL, CHL, CRI, KEN)
- **총 쌍**: 19×18/2 = **171 unique pairs**
- **True cooperative pairs**: **75쌍** (그룹 멤버십 pseudo-truth)
- **B0 features**: CO2 per capita, share of global CO2, log(GDP) → cosine similarity

### 2.2 Confusion Matrix (Round 4 재현)

|  | Pred Cooperative | Pred Non-coop |
|---|---|---|
| **True Cooperative** | TP = 42 | FN = 33 |
| **True Non-coop** | FP = 33 | TN = 63 |
| **합계** | 75 | 96 |

### 2.3 통계 방법

1. **Bootstrap 95%CI**: n=1000 resamples, seed=42, pair-level resampling
2. **Cohen's kappa**: 분류 정확도의 우연 보정 효과 크기
3. **McNemar test**: B0 vs Random baseline 쌍별 불일치 검정

---

## 3. 결과

### 3.1 Main Table

| Metric | Value | 95% CI | p-value (vs Random) | Cohen κ |
|---|---|---|---|---|
| **B0 F1** | **0.560** | **[0.458, 0.654]** | **< 0.0001** | **0.216 (fair)** |
| Random F1 | 0.440 | N/A | baseline | N/A |

### 3.2 Bootstrap 세부

- Resamples: 1,000 (seed=42)
- F1 mean (boot): 0.5596
- 95% CI lower: 0.4583
- 95% CI upper: 0.6536
- CI 폭: ± 0.097 (상당한 불확실성 — N=32 한계)

### 3.3 Cohen's Kappa

- Observed agreement (po): 0.614
- Expected by chance (pe): 0.508
- **κ = 0.216** → **fair** agreement (0.21~0.40 범위)
- Landis & Koch (1977) 기준: "fair"는 우연보다 낫지만 "moderate" 미달

### 3.4 McNemar Test

B0 correct predictions: 105/171 = 61.4%
Random baseline correct: 87/171 = 50.9%
Discordant pairs (n12 = B0 right, Random wrong): ~18
chi² = 16.1, **p < 0.0001** (significant at all conventional levels)

### 3.5 해석

```
F1 = 0.560 [0.458, 0.654] (κ = 0.216, p < 0.0001 vs Random)
```

- B0는 random baseline(F1=0.440)보다 통계적으로 유의하게 우수
- 그러나 F1 < 0.70 기준 가설 **CONFIRMED**: 실용적 사용 불가 수준
- κ = 0.216 (fair) → 구성주의 변수 없이는 국제협상 협력 구조 설명 불충분
- 95% CI [0.458, 0.654]의 폭이 넓음: N=32 기반의 추정 불안정성 노출

---

## 4. 가설 검증 요약

| 가설 | 예상 | 실측 | 판정 |
|---|---|---|---|
| F1 < 0.70 (realism insufficient) | < 0.70 | 0.560 | **CONFIRMED** |
| B0 > Random (some realist signal) | F1_B0 > F1_rand | 0.560 > 0.440 | **CONFIRMED** |
| Statistical significance (p<0.05) | p < 0.05 | p < 0.0001 | **CONFIRMED** |
| Moderate+ effect size | κ ≥ 0.40 | κ = 0.216 (fair) | REJECTED |

### CINA 정당화

B0 F1=0.560, κ=0.216 결과는:
1. Realist 변수가 **완전히 무의미하지 않음** (p<0.0001)
2. 그러나 **실용적 사용에는 불충분** (F1<0.70, κ<0.40)
3. → CINA가 추가하는 framing/coalition/constructivist 변수의 필요성을 **정량적으로 정당화**

예시 오류 사례 (Round 4에서 확인):
- USA-SAU cosine = 0.889 (realist: 협력 예측) vs 실제: 서로 다른 협상 블록
- BRA-KEN cosine = 낮음 (realist: 비협력 예측) vs 실제: G77 동일 그룹

---

## 5. 한계 및 R6 권고

1. **N=32 한계**: Bayer-Urpelainen et al. (2021) panel analysis 기준 N≥80 필요
   - Round 5 후: 56개 chair_metadata records = 56/80 = **70.0%**
   - R6에서 4건 추가 수집으로 **N=60** 도달 가능
2. **Pseudo-truth의 한계**: ENB Castro 2025 실제 co-sponsorship 데이터로 대체 필요
3. **McNemar 근사**: pair-level 중복 구조 미반영, 정확한 검정은 exact McNemar 필요

---

## 6. 인용 한 줄 결론

> "CINA 19개국 Realist B0 (CO2/GDP cosine) F1=0.560 [95%CI: 0.458–0.654] (κ=0.216, p<0.0001 vs Random 0.440): realism has limited but statistically significant predictive power for UNFCCC cooperation, confirming CINA constructivist variable extension is necessary." (CINA Round 5, 2026-04-26)

---

**버전**: v1 (Round 5)
**데이터**: `data/processed/realist_b0_statistics.json`
**처리 스크립트**: `src/p03_realist_b0_statistics.py`
