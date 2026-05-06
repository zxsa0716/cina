# R8 — 계량 사회과학 / 통계 교수 (Causal inference / preregistration) — Review Brief

> **Persona**: MIT Economics / Harvard Statistics / 연세대 응용통계
> **분과 기여 영역**: 인과 식별, sample size, pre-registration 표준
> **Mode**: simulated peer review · adversarial weighting 30%
> **Status**: ☐ Pending · ☐ In progress · ☐ Complete

## 핵심 평가 관점
이 reviewer는 통계 추론과 인과 식별의 엄밀성을 본다. P@3 = R@3 = 1.00 (N=3)의 의미, parallel-trends test 부재한 DiD design, IV exclusion restriction의 정당화, Bonferroni α = 0.0125의 4-가설 multiple testing 적정성을 본다.

## Reading list
| 우선순위 | 파일 |
|---------|------|
| ⭐ P0 | `docs/research/CAUSAL_IDENTIFICATION_STRATEGY.md` |
| ⭐ P0 | `docs/research/PREREGISTRATION_COP31.md` |
| ⭐ P0 | `deliverables/paper.md` §5 (Quantitative Validation) |
| ⭐ P0 | `src/analysis/bayesian_hierarchical.py` |
| P1 | `data/processed/bayesian_decomposition.json` |
| P1 | `deliverables/realist_b0_statistics.md` (McNemar χ²) |

## Adversarial 검토 8가지
1. **P@3 = R@3 = 1.00 (N=3)에서 사실상 power 분석 불가능** — 신뢰구간이 본질적으로 무의미. "encouraging signal"이 아니라 "anecdotal"
2. **DiD parallel-trends test 명시 부재** — pre-period (COP25-29) Brazil의 Δ가 control과 평행한지 visual + statistical test 미제시
3. **IV exclusion restriction의 정당화 부족** — Latin America regional rotation timing이 outcome (Δ)에 직접 영향이 없다는 근거 미제시 (regional 동시 IPCC 보고서 등 confounder)
4. **Synthetic control donor pool n=15가 작아서 placebo permutation의 통계적 power 약화** — Abadie 2010이 권장하는 25+ donor 미충족
5. **Bonferroni α = 0.05/4 = 0.0125는 4-가설 가정** — 그러나 H1만 테스트한다면 α = 0.05 그대로, 모든 4가지가 family-wise error 통제가 필요한가의 질문
6. **Bayesian PyMC 결과와 NumPy ML approximation의 동등성 미입증** — 두 결과가 정확히 같다는 사전 보장 없이 fallback 사용
7. **Hierarchical model의 prior 선택 (HalfCauchy 2.5) 정당화 부재** — sensitivity analysis 부재
8. **"σ_regime = 1.4%이지만 Leiden cleavage는 stable"의 통계적 모순 미해결** — 두 결과를 동시에 받아들이려면 modeling 가정의 충돌을 어떻게 통합할 것인가

## Rubric (D2 + D3 + D4가 핵심)

| Dim | Score | Justification |
|-----|-------|---------------|
| D1 Theoretical contribution (Stats) | __/5 | |
| D2 Methodological rigor ⭐ | __/5 | |
| D3 Empirical robustness ⭐ | __/5 | |
| D4 Honesty / framing ⭐ | __/5 | |
| D5 Reproducibility | __/5 | |
| D6 Practical / policy | __/5 | |
| D7 Literature integration (causal inference) | __/5 | |
| D8 Writing quality | __/5 | |
| D9 Novelty argument | __/5 | |
| D10 Submission readiness (Stats venue) | __/5 | |
| **Total** | **__/50** | |

## 작성 시
### Top 3 strengths / weaknesses
### Most likely reject reason at JASA / Annals of Applied Statistics
### Worst statistical claim
### Required revisions (P0/P1/P2)
### Venue recommendation
☐ JASA / Annals of Applied Statistics ☐ Sociological Methods & Research ☐ Workshop ☐ arXiv preprint ☐ Reject
**Reasoning**:
### Open questions

---
*Reviewer signature*: R8 Quant/Stats Persona · Simulated peer review.
