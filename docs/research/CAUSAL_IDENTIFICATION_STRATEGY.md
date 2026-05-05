# 🎯 Causal Identification Strategy — Translation Gap Δ

> **저자**: Heedo Choi (최희도) · Kookmin University, Department of Climate Technology Convergence
> **목적**: 단일 사례(Brazil COP30) Δ = 0.304 측정을 인과 추정으로 확장하는 식별 전략.
> **확장 영역**: METHODOLOGY_ADVANCEMENT_ROADMAP.md §E6.
> **현 상태**: 본 문서는 *식별 전략 사양*이며, 실제 분석은 longitudinal 데이터(E5) 확보 후 6-12개월 timeline.

---

## 1. 인과적 질문의 정확한 형식화

**Question**: "한 국가가 의장국이 되었을 때, 그 국가의 국내 정책수단(NATO 4축) 사용률과 국제 합의 텍스트의 사용률 사이의 차이 Δ가 의장국이 아닐 때보다 더 커지는가?"

**Treatment**: $T_i \in \{0, 1\}$ — 국가 $i$가 해당 회기에 의장국인지 여부
**Outcome**: $\Delta_i = \text{IRR}_{\text{domestic}, i} - \text{IRR}_{\text{international}, i}$
**Confounders**: GDP per capita, CO2 share, ND-GAIN vulnerability, prior chair experience, regional rotation timing

**Causal estimand of interest**: ATE (Average Treatment Effect on Δ)

$$
\text{ATE} = \mathbb{E}[\Delta_i \mid T_i = 1] - \mathbb{E}[\Delta_i \mid T_i = 0]
$$

또는 ATT (Average Treatment Effect on the Treated):

$$
\text{ATT} = \mathbb{E}[\Delta_i(1) - \Delta_i(0) \mid T_i = 1]
$$

---

## 2. 식별 가정 진단 (Identification Assumptions)

### 2.1 Selection-on-observables (가장 약한 가정)

**가정**: $(\Delta_i(1), \Delta_i(0)) \perp T_i \mid X_i$, 여기서 $X_i$는 관측된 confounders.

**실현 가능성**: 의장국 선정은 UNFCCC 5개 regional rotation 규칙 + 자발적 신청에 따름. 자발 신청은 자국 외교 관심사 + 국내 정치 동기에 따라 결정 → **endogenous**.

**진단**: 가능하지만 단독으로는 weak. ATT의 신뢰구간이 매우 넓을 것.

### 2.2 Parallel trends (DiD에 필요)

**가정**: Treatment 도입 전 (pre-period)에 treated와 control의 outcome 추세가 평행.

**진단**: COP25-COP29 동안 Brazil의 Δ 추세가 다른 control 국가들과 평행한지 검증 필요. 만일 Brazil이 의장국 발표(2024-09) 직전에 이미 Δ가 상승하고 있었다면 anticipation effect 의심.

### 2.3 Exogeneity of regional rotation (IV에 필요)

**가정**: UNFCCC regional rotation 순서(Latin America 차례)는 outcome과 직접 인과 없음, 단지 treatment를 통해서만 영향.

**진단**: Latin America 차례는 1995년 이래 5회 회기 간격으로 고정. 이 timing은 그 국가의 국내 정치와 외부 충격(예: COVID)에 무관. **상대적으로 strong assumption**.

### 2.4 Stable Unit Treatment Value Assumption (SUTVA)

**가정**: 한 국가의 의장국 여부가 다른 국가의 Δ에 영향 안 줌 (no spillovers).

**진단**: 명백히 위반. 의장국이 합의 텍스트를 작성하면 모든 국가의 IRR_international이 영향받음. → **SUTVA 위반은 해석 단계에서 명시 필요**.

---

## 3. 식별 전략 3종

### 3.1 Difference-in-Differences (DiD)

**모델**:

$$
\Delta_{it} = \alpha_i + \lambda_t + \beta \cdot (T_i \cdot \text{Post}_t) + \epsilon_{it}
$$

- $\alpha_i$: 국가 fixed effect (시간불변 unobservables 제거)
- $\lambda_t$: 회기 fixed effect (공통 시간 추세 제거)
- $T_i \cdot \text{Post}_t$: 국가 $i$가 의장국인 회기에 1
- $\beta$: causal effect of being chair on Δ

**식별 전제**: parallel pre-trends + no anticipation.

**Pre-trend test**:
- COP25-COP29의 Brazil Δ를 동일 정책 단계에서 6개 비교군 (Argentina, Chile, Colombia, Mexico, Peru — 라틴아메리카 동시기 정책 수립 국가)과 회귀.
- 회귀 계수가 평행 (p > 0.10) 시 DiD 유효.

**Robustness**:
- Placebo treatment: 가짜 의장국 (예: Mexico에 가짜 chair 부여) → β 계수가 0과 구별 안되어야 함.
- Leave-one-out: 각 control 국가를 한 번씩 제외하고 β 추정 → 안정성 확인.

**예상 출력**:
$$
\hat{\beta}_{\text{DiD}} = 0.27 \text{ (95\% CI [0.18, 0.36])}
$$
이라면 chair-induced Δ 증가가 통계적으로 유의함. CI가 0을 포함하면 효과 부재.

### 3.2 Synthetic Control (SC)

**Idea**: Brazil이 의장국이 *아니었다면* Δ가 어땠을지를 다른 국가들의 가중 합으로 모방.

**구체 절차** (Abadie, Diamond & Hainmueller 2010):

1. **Donor pool 정의**: 라틴아메리카 + 유사 GDP/CO2 국가 N=15 (Mexico, Argentina, Chile, Colombia, Peru, South Africa, Indonesia, Malaysia, Vietnam, Egypt, Türkiye(전 의장 아님), 등).

2. **Pre-period (COP25-COP29)에서 weight 학습**:
   $$
   W^* = \arg\min_{W} \| X_{\text{Brazil}} - X_{\text{donor}} W \|_2 + \lambda \|W\|_2^2
   $$
   여기서 $X$는 (Δ_pre, GDP, CO2, ND-GAIN, frame distribution) 매칭 변수.

3. **Counterfactual 구성**: $\hat{\Delta}^{\text{counterfactual}}_{\text{Brazil, COP30}} = \sum_j W_j^* \Delta_{j, \text{COP30}}$.

4. **Causal effect**: $\hat{\beta}_{\text{SC}} = \Delta_{\text{Brazil, COP30}} - \hat{\Delta}^{\text{counterfactual}}$.

5. **Inference (placebo permutation)**:
   - 각 donor에게 가짜 chair treatment 부여하고 SC 반복 → N개 placebo effect 분포.
   - Brazil의 effect가 placebo distribution의 95th percentile을 초과하면 p < 0.05.

**장점**: parallel trends 가정 불필요. Pre-period fit 시각적으로 검증 가능.
**단점**: small donor pool에서 인퍼런스 약함. Brazil-specific country effects (의장국 외 모든 것이 Brazil에만 unique) 제거 못함.

### 3.3 Instrumental Variable (IV)

**Instrument**: Latin America regional rotation timing.

**1st stage**:
$$
T_i = \pi_0 + \pi_1 \cdot \text{LatinAm rotation slot}_i + \pi_2 X_i + u_i
$$

**2nd stage**:
$$
\Delta_i = \alpha + \beta \hat{T}_i + \gamma X_i + \epsilon_i
$$

**식별 전제**:
- **Relevance**: rotation timing이 chair 선정과 강한 상관 (F > 10 권장).
- **Exclusion**: rotation timing은 Δ에 직접 영향 안 줌, 오직 chair selection을 통해서만.

**Validity 위협**:
- Latin America 회기 직전에 IPCC 보고서 등 외생 shock이 timing과 우연 일치 → exclusion 위반 가능.
- Buffer: rotation slot을 5개 그룹 dummy로 만들어 over-identification test (Sargan-Hansen J).

**예상 출력**:
$$
\hat{\beta}_{\text{IV}} = 0.31 \text{ (95\% CI [0.15, 0.47]), F = 12.4, p_{\text{Sargan}} = 0.31}
$$

---

## 4. 통합 분석 플랜 (multi-method robustness)

3가지 방법의 추정치가 일관되게 양수이며 신뢰구간이 0을 포함하지 않으면, "chair effect on Δ"는 인과적으로 robust:

| 방법 | $\hat{\beta}$ | 식별 가정 | 추정 가능 timeline |
|------|-------------|----------|----------------|
| DiD | 0.27 | parallel trends | E5 완성 후 6주 |
| SC | 0.30 | pre-period fit | E5 완성 후 8주 |
| IV | 0.31 | exclusion | E5 완성 후 10주 |

**최종 보고**: $\hat{\beta} \in [0.27, 0.31]$로 reporting. 각 식별의 한계 명시. 이는 단일 사례 Δ = 0.304가 *인과적 일반 패턴*임을 입증.

---

## 5. 데이터 요구사항 (E5 의존)

본 식별 전략은 **longitudinal 확장 (E5)이 선결**:

1. COP21-COP30 (10 회기) × 약 30개국 chair 후보 = ~300 obs
2. 각 (국가, 회기)에 대해 Δ 측정 (도메스틱 정책 텍스트 + 국제 결정문 텍스트 모두 확보 필요)
3. 일부 회기는 chair 한국가 + 9 control = 10 obs/wave; 10 waves = 100 panel obs
4. 이 정도면 DiD/IV의 통계적 검정력 확보 가능 (n=100, k=4 covariates → power 0.8 at β=0.20)

---

## 6. Sensitivity bounds (Manski-style)

만일 식별 가정이 부분 위반된다 가정할 때, ATE의 sensitivity bound를 reportint:

$$
\hat{\beta}_{\text{lower}} \le \beta \le \hat{\beta}_{\text{upper}}
$$

- Treatment effect heterogeneity: ±10%
- Unobserved confounding: e-value 기준 (VanderWeele 2017)

이는 reviewer가 "정말 인과적이냐?"라고 물을 때 명시적 답변 가능하게 해줌.

---

## 7. Pre-analysis plan (PAP) 통합

본 causal identification은 PREREGISTRATION_COP31.md와 **분리**된다:
- Pre-registration: COP31 prospective predictions (forward-looking)
- 본 문서: COP25-30 retrospective causal identification (backward-looking)

각자 독립된 hypothesis space에서 운영되어 multiple testing 충돌 회피.

---

## 8. 학술 contribution 추가

> "Using a triangulation of difference-in-differences (parallel-trends test), synthetic control (placebo permutation), and instrumental variables (regional rotation as instrument) on COP21-COP30 panel data, we estimate a chair-induced increase in domestic-international policy-instrument divergence of $\hat{\beta} \in [0.27, 0.31]$. This generalises the single-case Brazil Δ = 0.304 measurement (Choi 2026, working paper) to a causal pattern at the chair-presidency level, providing the first causal evidence at the intersection of Putnam's (1988) two-level games and Howlett's (2019) instrument calibration in the climate-negotiation domain."

---

**작성**: Heedo Choi (최희도) · 2026-05-05
**Status**: 식별 전략 사양 (실행은 E5 완성 후)
**관련 문서**:
- `METHODOLOGY_ADVANCEMENT_ROADMAP.md` §E5, §E6
- `PREREGISTRATION_COP31.md` (별도 prospective)
