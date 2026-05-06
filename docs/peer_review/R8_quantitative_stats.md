# R8 — 계량 사회과학 / 통계 교수 (Causal inference / preregistration) — Review (COMPLETE)

> **Persona**: MIT Economics / Harvard Statistics / 연세대 응용통계
> **Mode**: simulated peer review · adversarial weighting 30%
> **Status**: ✅ Complete · 2026-05-05

---

## 1. Summary judgement

본 연구는 OSF-style pre-registration 시도, Bayesian variance decomposition, DiD/SC/IV identification strategy 문서화 등 통계학 분야 best practice의 부분 채택을 보이지만, **(i) P@3=R@3=1.00 (N=3)에서 사실상 power 분석 불가능**, **(ii) DiD parallel-trends test 명시 부재**, **(iii) IV exclusion restriction 정당화 부족**, **(iv) Bonferroni α=0.0125의 multiple testing scope 불명확**, **(v) Bayesian PyMC와 NumPy ML approximation의 동등성 미입증** 등 통계학 reviewer가 즉시 잡을 5가지 P0 결함이 있다. 통계 venue (JASA, Annals of Applied Statistics) 본 투고는 무리이며, longitudinal extension 후 재고려 권장.

## 2. Rubric scores

| Dimension | Score | One-line justification |
|-----------|-------|------------------------|
| D1 Theoretical contribution (Stats) | 2.0/5 | 통계 method 자체에 새 기여 없음. |
| D2 Methodological rigor ⭐ | 1.5/5 | DiD parallel-trends test 부재 + IV justification 약함 + multiple testing scope 모호. |
| D3 Empirical robustness ⭐ | 1.0/5 | N=3에서 P@3=1.00은 binomial(3, 0.5) 가정하에 1/8 = 0.125 확률로 chance에서도 발생. |
| D4 Honesty / framing ⭐ | 4.5/5 | "small sample, encouraging signal" 표현은 정직. CRITICAL_REVIEW.md 자기 비판 우수. |
| D5 Reproducibility | 4.0/5 | PyMC 코드 + NumPy fallback 모두 공개. |
| D6 Practical / policy | 1.5/5 | 통계 분과는 정책 응용 부차적. |
| D7 Literature integration (causal inference) | 2.0/5 | Imbens-Rubin, Abadie 2010 인용은 했으나 최근 DiD literature (Roth 2024 etc.) 미인용. |
| D8 Writing quality | 3.0/5 | 통계 voice 표준이나 statistical claim 정확성 약함. |
| D9 Novelty argument | 2.5/5 | Δ metric 자체는 신선하나 통계학 기여라기보다는 measurement contribution. |
| D10 Submission readiness (Stats venue) | 1.5/5 | JASA / Annals of Applied Statistics는 desk reject 위험. |

**Total: 23.5/50** · **Average: 2.35/5**

## 3. Top 3 strengths

1. **OSF-style pre-registration 시도는 사회과학 표준 reproducibility framework의 자발적 채택**. 4개 falsifiable hypothesis + Bonferroni-corrected α + code freeze date 명시는 ASA 권장사항에 부합.

2. **DiD/SC/IV 3-method triangulation strategy 문서화 (CAUSAL_IDENTIFICATION_STRATEGY.md)는 인과 식별 학술 표준의 채택**. 단일 method의 unique identifying assumption이 위반될 때 cross-method robustness check를 제안한 것은 모범적.

3. **Bayesian variance decomposition을 PyMC + NumPy ML fallback dual implementation으로 제공한 것은 reproducibility의 우수 사례**. 단, 두 결과의 동등성 미입증 한계는 별도.

## 4. Top 3 weaknesses (specific, actionable)

1. **P@3=R@3=1.00 (N=3)의 통계적 의미 불충분 정당화**. 6개 issue 중 3개 contested 정확 예측은 random chance (binomial test) 하에서도 C(3,3)/C(6,3) = 1/20 = 0.05 확률로 발생한다. paper.md는 "small-sample, encouraging signal"로 약화는 했지만, **N=3에서 power 분석이 사실상 불가능하다는 점, 그리고 random chance 대비 p=0.05 정도라는 점**을 명시해야 한다. 현재는 abstract에서 P@3=1.00이 강조되는데, 이는 mid-tier reviewer에게는 "왜 이렇게 약한 evidence를 abstract에 강조하는가" 의문을 제기한다.

2. **DiD parallel-trends test 명시 부재**. CAUSAL_IDENTIFICATION_STRATEGY.md는 "Pre-trend test: COP25-COP28 동안 Δ_Brazil 추세가 control 그룹과 평행한지 검증 필요"라고 언급하지만, 실제 시계열 데이터가 없어 미실행. DiD의 핵심 가정 (parallel pre-trends)이 미검증인 상태에서 hypothetical $\hat{\beta}$ 추정치를 제시하는 것은 method paper 표준에 미달. 권장: longitudinal data 확보 후 실제 parallel-trends test 결과를 paper에 포함하거나, 또는 본 strategy 문서는 paper에서 future work로 분리.

3. **Bonferroni α=0.0125의 multiple testing scope 불명확**. 4 hypothesis (H1-H4) 모두 family-wise error 통제 필요인지, 아니면 H1 (contested set continuity)만 primary endpoint이고 H2-H4는 secondary인지 명시 부재. Primary/secondary 구별이 있다면 α 분배가 다르다 (예: Hochberg, Holm-Bonferroni). 또한 H1의 |overlap| ≥ 2 임계치는 binomial 분포상 p ≈ 0.5인데 (chance가 충분히 가능), 이는 strong test가 아님.

## 5. Adversarial finding

### Most likely reject reason at JASA / Annals of Applied Statistics

> "본 연구의 통계적 backbone은 (i) N=3 contested issue 예측에서 P@3=R@3=1.00이 binomial 분포상 chance에서 p≈0.05 확률로 발생 가능한 수준임에도 abstract에서 강조되고, (ii) DiD/SC/IV identification strategy는 longitudinal data 부재로 어떠한 실제 추정도 보고되지 않은 strategy paper이고, (iii) Bayesian PyMC와 NumPy ML fallback의 동등성이 입증되지 않은 채 같은 결과로 보고되며, (iv) Bonferroni α=0.0125의 family-wise error 통제 scope가 모호하다. 통계학 분과 venue 본 투고는 desk reject 가능성이 높다. 적용 영역의 method paper로 reframe하여 application venue에서 발표 권장."

### Worst statistical claim

> (paper.md Abstract) "CINA correctly identifies 3 of 3 contested issues from stance variance alone (Task C; small-sample, encouraging signal)."

→ Binomial(3, 0.5)에서 3/3 정확 = 1/8 = 0.125 확률. 또는 6개 issue 중 3개를 무작위 선택해서 3개 다 contested set에 속할 확률 = C(3,3)/C(6,3) = 1/20 = 0.05. 어느 baseline 가정 하에서도 "encouraging signal"은 over-statement이고, 정확히는 "consistent with chance, requires prospective validation"이다.

## 6. Required revisions before submission (priority-ordered)

- **P0 (must fix)**:
  1. P@3=R@3=1.00 결과에 random chance baseline (binomial 또는 hypergeometric)과의 비교 + p-value 명시. Abstract에서 강조 약화 (현재 "novel" tier로 표시됨)
  2. CAUSAL_IDENTIFICATION_STRATEGY.md를 paper.md "future work" §7로 이전 또는 별도 strategy paper로 분리. 실제 추정 없이 strategy만으로 paper.md §5에 포함시키지 않음
  3. Bonferroni α=0.0125의 multiple testing scope 명시 (H1만 primary? 모두 family-wise?)
  4. Bayesian PyMC와 NumPy ML fallback의 numerical 동등성 sanity check 결과 추가
- **P1 (should fix)**:
  1. PREREGISTRATION_COP31의 OSF 실제 등록 (현재 GitHub만)
  2. Bayesian hierarchical 모델의 prior sensitivity analysis (HalfCauchy 2.5 vs LogNormal 등)
  3. Roth (2024) 또는 Callaway-Sant'Anna 2021 등 최근 DiD literature 인용
- **P2 (nice to have)**:
  1. Power analysis simulation: COP31 prospective validation에서 어느 sample size에서 어떤 effect를 detect 가능한지
  2. Bayesian model의 LOO / WAIC 비교 (3-level vs 2-level)

## 7. Venue recommendation

- ☐ JASA / Annals of Applied Statistics
- ☐ Sociological Methods & Research
- ☑️ Workshop (NeurIPS CCAI / ASA Government Statistics)
- ☑️ arXiv preprint
- ☐ Reject

**Reasoning**: 통계 분과 venue 본 투고는 위 P0 + 실제 longitudinal data + 실제 인과 추정 후. 현 단계는 method strategy paper로 arXiv preprint + workshop 발표가 적정.

## 8. Open questions for the author

1. P@3=R@3=1.00의 random chance baseline은 무엇으로 정의하는가? Binomial vs hypergeometric vs other?
2. CAUSAL_IDENTIFICATION_STRATEGY는 longitudinal data 확보 전에 paper.md에 포함될 것인가, 별도 strategy paper로 분리될 것인가?
3. Bonferroni α=0.0125는 4개 hypothesis 모두 family-wise error 통제인가, H1 primary + H2-H4 secondary인가?
4. PyMC와 NumPy ML fallback의 numerical 동등성 sanity check 결과가 있는가?

---

*Reviewer signature*: R8 Quant/Stats Persona (MIT Econ / Harvard Stats)
*Honesty disclosure*: Simulated peer review.
