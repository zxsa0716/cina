# R4 — 정책학 교수 (Policy Science — Howlett school) — Review (COMPLETE)

> **Persona**: 서울대 행정대학원 / Simon Fraser School of Public Policy / Carleton SPPA
> **Mode**: simulated peer review · adversarial weighting 30%
> **Status**: ✅ Complete · 2026-05-05

---

## 1. Summary judgement

NATO 4축 정책수단(Hood 1983; Howlett 2019; Capano-Howlett-Pritoni 2025)의 LLM 기반 자동 추출은 흥미롭고 정책수단 측정학에 대한 잠재적 기여이지만, **(i) supervised dictionary 또는 manual coding baseline 대비 정량 비교 부재**, **(ii) instrument calibration의 frequency vs intensity 구별 부재**, **(iii) Capano et al. 2025 NATO text-analysis review의 직접 활용 부재**가 정책학 reviewer가 즉시 잡을 약점이다. Translation Gap Δ=0.304는 흥미로운 metric이나, NATO instrument의 calibration 의미가 아닌 단순 token frequency 차이로 환원될 위험이 있다.

## 2. Rubric scores

| Dimension | Score | One-line justification |
|-----------|-------|------------------------|
| D1 Theoretical contribution (Policy Science) | 2.5/5 | NATO 4축 측정 시도는 가치 있으나 instrument theory에 새 contribution은 없음. |
| D2 Methodological rigor ⭐ | 2.0/5 | Supervised baseline 부재 + calibration intensity 미구별 |
| D3 Empirical robustness | 2.5/5 | Brazil 단일 사례 Δ=0.304는 generalisability 약함. |
| D4 Honesty / framing | 4.0/5 | CRITICAL_REVIEW에서 한계 인정 자세 양호. |
| D5 Reproducibility | 4.0/5 | 코드와 schema 공개 우수. |
| D6 Practical / policy | 3.5/5 | 한국 NAP 30-cell crosswalk는 정책학 분석 도구로 활용 가능. |
| D7 Literature integration ⭐ | 2.5/5 | Capano-Howlett-Pritoni 2025 NATO text-analysis review를 reference로만 인용, 직접 활용 부재. |
| D8 Writing quality | 3.5/5 | 정책학 voice로는 양호. |
| D9 Novelty argument | 2.5/5 | "다축 동시 추출"은 NLP 기여, 정책학 자체에 새 발견 없음. |
| D10 Submission readiness (Policy venue) | 2.0/5 | Policy Sciences (Springer) 또는 Policy Studies Journal 본 투고는 시기상조. |

**Total: 27.0/50** · **Average: 2.70/5**

## 3. Top 3 strengths

1. **NATO 4축 LLM 자동 추출은 instrument measurement 자동화에 대한 잠재 기여**. 정책학 분야는 instrument coding이 manual에 의존해 왔는데, scalable 자동 추출은 시계열 / 다국가 비교 정책분석을 가능하게 함.

2. **한국 NAP 30-cell crosswalk (5 분야 × 6 GGA 이슈)는 정책 평가 도구로 활용 가능**. 환경부 차원의 적응대책 자기 평가에 도입 가능.

3. **Translation Gap Δ metric 자체는 정책 instrument 측정학에 새로운 개념**. 단일 사례 결과에 한정되지만, 향후 시계열 / 다국가로 확장 시 chair-mediated divergence 측정의 표준이 될 잠재력 있음.

## 4. Top 3 weaknesses (specific, actionable)

1. **NATO 4축 LLM 추출의 supervised baseline 대비 정량 비교 부재**. Capano et al. (2025) NATO text-analysis review는 dictionary methods, supervised learning, topic models, scaling models 등 다양한 NATO 측정 방법론을 비교하는 메타논문이다. 본 연구는 Capano et al. 2025를 reference 추가했으나, **본인의 LLM zero-shot 방법이 dictionary baseline 대비 (a) precision/recall, (b) coding 일관성, (c) 시간/비용 면에서 어떤 정량적 우위를 갖는지** 측정하지 않았다. 정책학 reviewer는 "왜 dictionary 대신 LLM을 써야 하는가"를 직접 묻는다.

2. **Instrument calibration의 frequency vs intensity 구별 부재**. Howlett (2019) calibration은 instrument의 *intensity* (강도) 측정이고, NATO 4축의 단순 사용 여부 (binary) 또는 frequency (빈도)와 다르다. 예를 들어 Brazil의 Authority axis "shall not create new financial obligations"는 단 1회 등장하지만 그 강도는 매우 강하다. 본 연구의 Δ=0.304는 NATO 축의 frequency 차이를 측정한 것이지 calibration intensity 차이를 측정한 것이 아닐 수 있다. Howlett의 calibration 개념과 본 연구의 측정 사이에 conceptual gap이 있다.

3. **Negative authority "shall NOT" 측정 방법론 정당화 부재**. IRR_Brazil.md는 "negative authority 분리 후 Δ 재산출"이라 명시하지만, **negative authority를 어떻게 자동 검출했는지 (dictionary? LLM zero-shot? manual?)** 본문에 명시되지 않는다. 만일 LLM이 "shall not"의 negative authority를 단순 keyword matching으로 처리했다면, Δ=0.304는 단순 keyword frequency 효과일 가능성을 배제할 수 없다.

## 5. Adversarial finding

### Most likely reject reason at Policy Sciences / Policy Studies Journal

> "본 연구의 NATO 4축 LLM 자동 추출은 흥미로운 시도이나, 정책학 분야에서 NATO 측정의 표준 방법론(dictionary, supervised learning)과의 정량 비교가 부재하다. Howlett (2019) calibration 개념은 instrument intensity를 측정하는 것이고, 본 연구의 측정은 instrument frequency에 가까워 conceptual stretching이 있다. Capano-Howlett-Pritoni (2025) review를 인용했으나 그 framework을 본 연구의 baseline으로 활용한 적용은 없다. Brazil Translation Gap Δ=0.304는 흥미로운 single-case observation이나 calibration theory에 대한 contribution이라기보다 frequency comparison이다."

### Worst sentence/claim in the paper

> (paper.md §3.2) "instrument_signals: {nodality:[...], authority:[...], treasure:[...], organization:[...]}"

→ 이 schema는 4축의 *언급 여부 (binary list)* 만 저장하고, *intensity*나 *operational strength* 신호는 저장하지 않는다. Howlett (2019)의 calibration 개념은 binary signal이 아니라 강도/operational specificity 측정이다.

## 6. Required revisions before submission (priority-ordered)

- **P0 (must fix)**:
  1. NATO 4축 LLM zero-shot 추출 vs supervised dictionary baseline 정량 비교 (precision, recall, F1) 추가
  2. "Calibration intensity" vs "instrument frequency" 구별을 §3 Methodology에서 명시. 본 연구의 측정이 어디에 해당하는지 정확히 표기
  3. Negative authority 자동 검출 방법론 (dictionary? LLM prompt?) 명시. 이를 통해 Δ=0.304가 keyword frequency effect가 아님을 입증
- **P1 (should fix)**:
  1. Capano-Howlett-Pritoni 2025 review의 측정 framework을 본 연구의 비교 baseline으로 통합
  2. Howlett (2019) calibration 정의를 §2 Theoretical Framework에서 직접 인용 + 본 연구의 측정과 정확한 관계 명시
- **P2 (nice to have)**:
  1. 한국 NAP 30-cell crosswalk를 환경부와 사전 검토 후 발표

## 7. Venue recommendation

- ☐ Policy Sciences (Springer) — 본 투고 시기상조
- ☐ Policy Studies Journal — 동일
- ☐ 한국정책학회보 KCI — 단저자 + 정책수단 측정 기여로 가능
- ☑️ Workshop (Policy Sciences Conference, Carleton SPPA workshop)
- ☐ Reject

**Reasoning**: NATO calibration 영역의 표준 방법론과 정량 비교가 가능해진 후 본 투고. 그 전에는 workshop에서 method paper 단계로 발표.

## 8. Open questions for the author

1. NATO 4축 LLM zero-shot 추출이 dictionary baseline 대비 어떤 정량적 우위를 갖는가? Precision/recall 측정 결과가 있는가?
2. Howlett (2019) calibration intensity 개념과 본 연구의 측정은 어떻게 정확히 매핑되는가?
3. Negative authority "shall not" 검출은 LLM이 어떤 prompt로 수행하는가? Keyword matching이 아닌가?

---

*Reviewer signature*: R4 Policy Science Persona (Howlett school)
*Honesty disclosure*: Simulated peer review.
