# 🎓 CINA Pre-Submission Evaluation Session — Master Design

> **목적**: 논문 투고 전 10명 분야 교수의 비판적 사전 심사를 모사하여, CINA 프로젝트(코드·데이터·논문 초안·웹사이트·산출물 일체)의 강·약점을 다각도로 진단하고 투고 전 수정 우선순위를 도출.
>
> **세션 형식**: 시뮬레이션 peer review. 각 교수는 자기 분야 lens로만 critique; 다른 분야는 의도적으로 평가하지 않음. Aggregator(저자)가 마지막에 합의안 도출.
>
> **작성일**: 2026-05-05
> **저자**: 최희도 (Heedo Choi) · 국민대학교 대학원 기후기술융합학과

---

## 0. 평가 대상물 (review package)

각 교수는 다음 자료에 모두 접근 가능하다.

| # | 자료 | 위치 |
|---|-----|-----|
| 1 | 학술 페이퍼 초안 | [`deliverables/paper.md`](../../deliverables/paper.md) (3,500+ 단어, 28 references) |
| 2 | 한국어/영문 장관급 브리핑 | [`deliverables/ministerial_briefing_{ko,en}.md`](../../deliverables/) |
| 3 | Phase 5 평가 보고서 | [`deliverables/evaluation_report.md`](../../deliverables/evaluation_report.md) |
| 4 | 정량 검증 보고서 6종 | [`deliverables/IRR_Korea.md`, `IRR_Brazil.md`, ...](../../deliverables/) |
| 5 | 자체 비판 평가 | [`docs/research/CRITICAL_REVIEW.md`](../research/CRITICAL_REVIEW.md) |
| 6 | 학술 고도화 로드맵 | [`docs/research/METHODOLOGY_ADVANCEMENT_ROADMAP.md`](../research/METHODOLOGY_ADVANCEMENT_ROADMAP.md) |
| 7 | OSF-style 사전 등록 | [`docs/research/PREREGISTRATION_COP31.md`](../research/PREREGISTRATION_COP31.md) |
| 8 | 인과 식별 전략 | [`docs/research/CAUSAL_IDENTIFICATION_STRATEGY.md`](../research/CAUSAL_IDENTIFICATION_STRATEGY.md) |
| 9 | 코드 (master pipeline + R-GAT + Bayesian + Cross-LLM) | [`src/`](../../src/) |
| 10 | Figure 10장 + 5 페이지 인터랙티브 웹 | [`docs/web/`](../../docs/web/) |
| 11 | 공개 데이터 샘플 8종 | [`data/sample/`](../../data/sample/) |
| 12 | 자동 실행 보고서 | [`RUN_REPORT.md`](../../RUN_REPORT.md) |

---

## 1. 10명 평가자 profile (분야별 lens 분리)

| # | 평가자 | 분야 / 가상 소속 | Primary lens | 약점 포착 가능성 |
|---|-------|---------------|------------|-------------|
| **R1** | **기후과학자** | IPCC AR6 WGII Lead Author급 | 과학적 정확성, IPCC 정렬, 적응 영역 substantive 정확성 | 지표 해석 오류, 기후 메커니즘 부재 |
| **R2** | **국제정치학 (IR) 교수** | regime complex / Two-Level Games 전문가 | 이론적 엄밀성, IR 문헌 정렬 | 이론-측정 정합성, over-claim |
| **R3** | **외교학 (Diplomacy) 교수** | 전직 협상 실무 + 학계 | 협상 실무 적합성, 정책 권고의 현장성 | 권고가 실제 외교부 SOP에 부합하는가 |
| **R4** | **정책학 (Policy Studies) 교수** | Howlett / NATO 4축 정책수단 calibration | 정책 도구 분류 정확성, instrument calibration 이론 | NATO 4축 자동 분류의 reliability |
| **R5** | **NLP / LLM 연구자** | stance detection / political text analysis 전문 | LLM 평가 방법론, 베이스라인, ablation 통계 | n 작음, 단일 시점, p-hacking risk |
| **R6** | **GNN / 그래프 학습 전문가** | R-GAT / heterogeneous GNN 전문 | 그래프 모델 정확성, attention 해석성, ablation | "emergent attention 1.00" 주장의 robustness |
| **R7** | **계량방법론 / 인과추론 전문가** | DiD / synthetic control / IV / Bayesian inference | 인과 식별, 표본 크기, 통계 추론 타당성 | n=98 / N=3 / σ_regime 1.4% 모순 |
| **R8** | **한국 외교부 정책자문관** | 실무 (현직 또는 전직) | 한국 stance 묘사 정확성, 권고의 actionability, 정치적 현실성 | 한국 입장 점수의 실제 부합성 |
| **R9** | **학술 출판 편집위원** | *Global Environmental Change* 또는 *Climate Policy* 편집위원급 | 투고 매체 적합성, scope vs depth, contribution sharpening | "어디 학술지에 fit하는가" 정확 진단 |
| **R10** | **연구 윤리 / 재현성 전문가** | computational social science 재현성 운동 | 데이터 윤리, IRB, 재현성, 정직 보고 | 시뮬레이션 패널 disclosure, LLM bias |

---

## 2. 평가 dimension (모든 reviewer 공통 5개 axis + 분야별 추가)

각 평가자는 **5점 척도** (1 매우 부족 → 5 우수)로 다음 5개 공통 axis를 채점한 뒤, 분야별 1–2개 추가 axis를 병행 평가.

### 공통 axis

| Axis | 정의 | 예시 평가 |
|------|-----|---------|
| **A1. 과학적 정확성** | 측정·계산·결과의 substantive 정확성 | 지표 정의가 학술적으로 표준에 부합하는가 |
| **A2. 방법론적 엄밀성** | 통계 추론·식별 가정·재현성 | 표본 크기, 신뢰구간, 가정의 명시성 |
| **A3. 이론적 정초** | IR/정책학/NLP 이론과의 연결 | 사용 이론의 적합성과 정확성 |
| **A4. 정직성·자기 비판** | 한계 인정, over-claim 부재, 시뮬레이션 vs 실측 분리 | "first quantitative measurement" 등 표현 |
| **A5. 실용성·임팩트** | 외교부·학계가 실제로 사용 가능한가 | 권고의 실행 가능성, 베이스라인 대비 차별점 |

### 분야별 추가 axis

| 평가자 | 추가 axis |
|-------|---------|
| R1 기후과학 | A6. IPCC AR6 적응 챕터 정렬 |
| R2 IR | A6. IR theory 정렬 / A7. Power dynamics 처리 |
| R3 외교 | A6. 외교부 SOP 부합 / A7. Talking points의 진정성 |
| R4 정책 | A6. NATO 4축 분류의 신뢰도 |
| R5 NLP | A6. Stance detection benchmark / A7. Statistical power |
| R6 GNN | A6. R-GAT architecture 적합성 / A7. Attention interpretability |
| R7 계량 | A6. 인과 식별의 타당성 / A7. multiple-comparison correction |
| R8 외교부 | A6. 한국 입장 묘사의 사실 부합 / A7. Political feasibility |
| R9 편집위원 | A6. 투고 venue 적합성 / A7. 분량·구조 적정성 |
| R10 윤리 | A6. 재현성 / A7. Honest reporting / A8. IRB·데이터 사용 |

---

## 3. 평가 산출물 (per reviewer)

각 reviewer는 다음 8개 항목을 채워 [`docs/peer_review/individual_reviews/Rxx_<영역>.md`](individual_reviews/) 형식으로 제출.

```yaml
reviewer_id: R{1-10}
reviewer_field: <분야>
reviewer_proxy_affiliation: <가상 소속>
review_date: 2026-05-05

# Section 1: 짧은 요약 (3 문장)
short_summary: |
  ...

# Section 2: 강점 (3-5개, bullet, 각각 한 줄)
strengths:
  - ...
  - ...

# Section 3: 약점 (3-5개, bullet, 각각 한 줄)
weaknesses:
  - ...
  - ...

# Section 4: 분야별 detailed critique (300-600 단어)
detailed_critique: |
  ...

# Section 5: 5개 axis 점수 (1-5)
scores:
  A1_scientific_accuracy: <int>
  A2_methodological_rigor: <int>
  A3_theoretical_grounding: <int>
  A4_honesty_self_criticism: <int>
  A5_practicality_impact: <int>
  # 분야별 추가 axis
  A6_<discipline_specific>: <int>

# Section 6: Top 3 action items (저자가 받아야 할 가장 중요한 수정 사항)
top_3_action_items:
  - priority: high|medium|low
    item: ...
    estimated_effort: <weeks>

# Section 7: 최종 의사결정
recommendation:
  decision: <Accept | Minor revision | Major revision | Reject>
  target_venue_assessment: <어느 학술지/워크숍에 fit한지>
  conditions_for_acceptance: |
    ...

# Section 8: 자유 의견 (저자에게 직접 전하고 싶은 말)
free_comments: |
  ...
```

---

## 4. Aggregation protocol — 10명의 평가를 어떻게 합치나

10개의 review가 모두 채워지면 다음 알고리즘으로 합의안 도출:

### 4.1 점수 집계

- 5개 공통 axis별로 **10명의 점수 평균** 산출
- 각 axis에서 **분산** 측정 (분산이 크면 reviewer 사이 불일치)
- 분산 ≥ 1.0인 axis는 의견 갈림 → 본문에서 별도 토론 권장

### 4.2 의사결정 합산 규칙

| 의사결정 분포 | 합의 결정 |
|------------|---------|
| Reject ≥ 3명 | **Major Reject** — 본격 재구축 권고 |
| Reject 1–2명 + Major revision ≥ 4명 | **Major Revision Required** |
| Major revision ≥ 5명 (Reject < 3) | **Major Revision** |
| Minor revision 다수 + Major revision ≤ 4 | **Minor Revision** |
| Accept ≥ 3 + 나머지 Minor revision | **Conditional Accept** |

### 4.3 Action item 우선순위

10명의 top_3_action_items를 합쳐 **우선순위 매트릭스**:
- 동일 또는 유사 항목이 **3명 이상에게 high priority**로 지목 → "P0 (즉시 수정)"
- 2명에게 high → "P1 (투고 전 수정)"
- 1명에게 high 또는 다수에게 medium → "P2 (revision round 시 수정)"

### 4.4 Target venue 합의

10명이 각자 제시한 적합 venue의 빈도 분포를 보고 **top-3 venue**를 final recommendation으로 선정.

---

## 5. 시뮬레이션 운영 규칙 (anti-flattery)

본 평가는 "AI가 자기 작품을 칭찬하는" 함정에 빠지지 않도록 다음 규칙을 따른다.

1. **각 reviewer는 분야별 lens를 엄격히 유지**한다. 다른 분야의 강점을 변호하지 않는다.
2. **Reject 또는 Major revision 결정이 1–3명에서 나오는 것이 정상**이다. 모두가 Accept를 주는 평가는 신뢰성 없는 평가이다.
3. **약점을 숨기지 않는다**. 시뮬레이션 패널·n=98·단일 사례 Δ·sigma_regime 1.4% 모순 등은 모든 reviewer가 어떤 식으로든 언급해야 한다.
4. **이론-측정 정합성**을 깐깐히 점검한다. "Tallberg 4채널을 검증했다"는 주장은 실제 R-GAT attention이 4채널 모두를 찾았는지로 평가되어야 한다.
5. **Honest reframing의 일관성**을 점검한다. 본문 어디에도 abstract와 모순되는 over-claim이 남아 있지 않아야 한다.
6. **분량과 분석 깊이의 비례**를 점검한다. 짧은 contribution을 길게 늘이거나, 큰 주장에 분석이 얇은 곳이 있다면 지적한다.

---

## 6. 평가 진행 순서 (recommended)

| Round | 활동 | 산출물 |
|-------|-----|-------|
| Round 1 | 10명 reviewer 동시 평가 (분야별 lens 독립 적용) | 10개 individual review |
| Round 2 | Aggregator가 점수·의사결정·action item 집계 | `META_REVIEW.md` |
| Round 3 | 충돌하는 review 사이 cross-rebuttal (선택) | `CROSS_DEBATE.md` |
| Round 4 | 최종 합의안 + revision plan | `FINAL_VERDICT.md` + `REVISION_PLAN.md` |

저자는 Round 4의 revision plan에 따라 paper.md / 코드 / 데이터를 수정한 후, 투고 전 최종 자기 점검을 거친다.

---

## 7. 본 세션의 한계

- 본 평가는 **실제 외부 reviewer 섭외**가 아닌 **시뮬레이션**이며, 실제 peer review를 대체할 수 없다.
- 그러나 시뮬레이션 reviewer가 self-bias를 의도적으로 도입(분야별 lens 분리, Reject 확률 보장)함으로써 자체 비판의 사각지대를 부분적으로 줄일 수 있다.
- 실제 학술지 투고 시에는 본 시뮬레이션 결과를 cover letter에 언급하지 않는 것이 일반적이다 (피어 리뷰 표준 우회 의심 받을 수 있음). 단, 본 결과는 저자가 내부 revision plan에 활용 가능.

---

## 8. 다음 단계

본 design 문서가 승인되면 다음 단계로 진행:

1. **10명 individual review 작성** (`docs/peer_review/individual_reviews/R01_climate.md` 등)
2. **META_REVIEW 집계**
3. **REVISION_PLAN 도출**
4. 저자의 paper / 코드 / docs 수정
5. 투고 (NeurIPS CCAI 2026 Workshop 또는 한국정책학회보 우선)

---

**작성**: 2026-05-05
**저자**: 최희도 (Heedo Choi) · zxsa0716@kookmin.ac.kr
**관련 문서**: [`CRITICAL_REVIEW.md`](../research/CRITICAL_REVIEW.md), [`METHODOLOGY_ADVANCEMENT_ROADMAP.md`](../research/METHODOLOGY_ADVANCEMENT_ROADMAP.md)
