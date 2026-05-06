# R7 — Causal Inference / Quantitative Methodology Reviewer 슬롯

```yaml
reviewer_id: R7
reviewer_field: Causal Inference / DiD-SC-IV / Bayesian Hierarchical Models
reviewer_proxy_affiliation: 가상 — *Journal of Econometrics* / *Political Analysis* 평가
review_date: <to be filled>
status: ⬜ EMPTY
```

## 책임 영역

- DiD / Synthetic Control / IV 식별 가정의 타당성
- Bayesian 3-level model의 prior choice + posterior diagnostics
- Translation Gap Δ = 0.304의 통계적 유의성 (single case)
- P@3 = R@3 = 1.00의 통계적 의미
- Multiple-comparison correction (Bonferroni α = 0.0125)
- Sample size 적합성

## 예상 강점

- Pre-registration with Bonferroni correction은 multiple-testing 처리의 표준
- DiD/SC/IV triangulation strategy는 single-method bias 회피의 valid 접근
- Bayesian 분산 분해는 Leiden 결과를 보완하는 좋은 시도

## 예상 약점

- **결정적**: Δ = 0.304는 "단일 의장국, 단일 시점, 단일 결정문" sample. Standard error 측정 불가. 통계적 유의성 검정 자체가 부재 — "0.304"가 "0.0"과 통계적으로 다른지 보증할 수 없음
- Bayesian 분산 분해 결과 σ_regime/σ_total² = 1.4%는 effect size로는 negligible. 본문은 이를 "transparent tension reporting"으로 처리하지만, 실제로는 Leiden cleavage 가설이 본 데이터에서 *기각*되는 결과로 해석 가능
- DiD/SC/IV 식별 전략은 "longitudinal extension 후 가능"으로 미실시. 즉 *현재* 단계의 paper.md에는 인과 추정이 없고 *전략 사양*만 있음. Causal claim 자체를 paper에서 제거하거나 "future work"로 명확히 해야 함
- σ_country = 54%는 country-level random effect 우세인데, 이는 IR 분야의 표준 결과 (countries differ a lot). 새로운 발견이 아님
- "P@3 = R@3 = 1.00" 통계적 의미: 6개 issue 중 3개를 정확히 맞출 확률 (random) = C(3,3)/C(6,3) = 1/20 = 0.05. 그러나 N=3 single trial에서 1.00은 단일 시도의 결과이지 분포에서의 측정이 아님. McNemar test 또는 binomial test 부재.

## 예상 점수

```yaml
A1_scientific_accuracy: 3
A2_methodological_rigor: 2     # Single-case Δ + N=3 P@3 의 통계 약함
A3_theoretical_grounding: 4
A4_honesty_self_criticism: 4
A5_practicality_impact: 3
A6_causal_identification_validity: 3   # 전략은 좋으나 실시 부재
A7_multiple_comparison_correction: 4   # Pre-reg는 valid
```

## 예상 top-3 action items

```yaml
- priority: high
  item: |
    "Δ = 0.304"의 single-case 한계를 paper §4.4에서 더 강하게 표시.
    Standard error/CI 부재를 명시. "Causal interpretation은 longitudinal
    extension (E5) + DiD/SC/IV (E6)에서만 가능"을 §7 Future Work에서
    재강조.
  estimated_effort: 0.5 weeks

- priority: high
  item: |
    Bayesian 분산 분해 결과를 Leiden cleavage 가설의 *partial rejection*
    으로 honest framing. σ_regime 1.4%는 horizontal cleavage가
    formal-group cleavage보다 *작음*을 의미. 본문 §4.2의 "consistent with"
    표현을 "in tension with"로 변경.
  estimated_effort: 0.5 weeks

- priority: high
  item: |
    P@3 = R@3 = 1.00에 대한 binomial test 또는 Wilson score 95% CI
    [0.29, 1.00] 명시. "Encouraging single-trial signal"이라는 honest
    표현 유지.
  estimated_effort: 0.3 weeks
```

## 예상 의사결정

```yaml
recommendation:
  decision: Major Revision
  target_venue_assessment: |
    Political Analysis 적합 (statistical methodology 강조). Journal of
    Econometrics 무리 (causal claim 미실시). NeurIPS CCAI Workshop 가능.
    Causal identification은 향후 longitudinal extension 후 별도 paper로
    분리하는 것이 학술적으로 합리적.
  conditions_for_acceptance: |
    1. Δ single-case 한계 강조
    2. Bayesian 결과를 partial rejection으로 honest framing
    3. P@3 binomial test 추가
```

---

**Status**: ⬜ Empty template.
