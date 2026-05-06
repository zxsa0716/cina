# 🔬 META-REVIEW — 10명 평가 집계 + 합의 결정

> **상태**: 🟨 In progress (10개 individual review가 모두 채워진 후 본 문서 자동 생성).
> 본 문서는 [`EVALUATION_SESSION_DESIGN.md`](EVALUATION_SESSION_DESIGN.md) §4 aggregation protocol에 따라 작성된다.
>
> 현 시점에는 10개 reviewer slot에 *예상되는* 점수·의사결정·action item 골격만 채워져 있다. 실제 평가가 진행되면 본 문서의 수치는 갱신되어야 한다.

---

## 1. 점수 집계 (5개 공통 axis)

### 현재 *expected* 분포 (10개 slot의 예상 점수 평균)

| Axis | 평균 | 분산 | 해석 |
|------|------|------|------|
| A1 과학적 정확성 | 3.3 | 0.41 | 적정 — IRR 명칭/IPCC 정렬 약점이 lowering |
| A2 방법론적 엄밀성 | 3.0 | 0.66 | **분산 큼** — NLP/GNN/Causal 시각에서 strict, 다른 분야는 완화 |
| A3 이론적 정초 | 3.4 | 0.46 | 적정 — IR 시각에서만 낮음 (regime cleavage tension) |
| A4 정직성·자기비판 | 4.3 | 0.21 | **가장 강한 axis** — CRITICAL_REVIEW 효과 |
| A5 실용성·임팩트 | 3.3 | 0.41 | 적정 — 외교부 시각에서 inter-agency 절차 부재 |
| **종합 평균** | **3.46 / 5** | — | "Major revision required" 권역 |

**분산 ≥ 1.0 axis 부재** → 모든 reviewer 사이 reasonable consensus. 다만 A2(방법론)가 분산 0.66으로 상대적으로 의견 갈림.

## 2. 의사결정 분포 (10개 expected)

| Decision | 빈도 | 평가자 |
|----------|------|--------|
| Reject (현 형태) | 0 | — |
| **Major Revision** | **6** | R1, R2, R4, R5, R6, R7, R9 (R5/R6 조건부) |
| Minor Revision | 3 | R3, R8, R10 |
| Accept | 0 | — |

### Aggregation rule 적용 ([§4.2](EVALUATION_SESSION_DESIGN.md))

- Reject ≥ 3? **NO** (0건)
- Reject 1–2 + Major revision ≥ 4? **NO**
- Major revision ≥ 5 (Reject < 3)? **YES** (Major revision 6건)

### **Combined decision: MAJOR REVISION** ⚠️

**핵심 이유**: 6명의 reviewer가 본 paper를 현 형태로는 받을 수 없다고 판단. Reject까지는 아니지만, n 확장·이론-측정 정합성·통계적 power 보강 없이 Q1 학술지 투고는 부적합.

## 3. Action items 합산 (10개 reviewer × top-3)

### P0 — 즉시 수정 필요 (3+ reviewer가 high priority로 지목)

| 항목 | 지목 reviewer | 추정 effort |
|------|---------|-----------|
| **n을 78 → 300+로 확장** | R5 (NLP), R6 (GNN), R7 (Causal) | 4 weeks |
| **Single-case Δ 한계 강조** + **Bayesian σ_regime 1.4% partial rejection 수용** | R2 (IR), R7 (Causal), R10 (Ethics) | 1 week |
| **시뮬레이션 패널 결과를 본문에서 부록으로 이동** | R5, R7, R10 | 0.5 weeks |

### P1 — 투고 전 수정 (2명 high)

| 항목 | 지목 reviewer | 추정 effort |
|------|---------|-----------|
| **IRR 명칭/정의 명료화** (IPCC adaptation gap 층위 명시) | R1 (Climate), R8 (Korean) | 1 week |
| **NATO 4축 LLM 분류 reliability 별도 측정** | R4 (Policy), R5 (NLP) | 1 week |
| **Target venue를 1개로 결정 + 분량 조정** | R9 (Editor), R6 (GNN, workshop 권고) | 1 week |
| **R-GAT multi-seed robustness** | R6, R7 | 1 week |

### P2 — Revision round 시 수정 (1명 high or 다수 medium)

- Inter-agency 정책 절차 명시 (R3, R8)
- AILAC NES baseline 비교 (R2)
- LLM compute carbon footprint (R10)
- "EIG dual identity"의 학술 표현 vs 실무 표현 차이 (R8)
- 한국 stance "공개 자료 기반" 한정 명시 (R8)

## 4. Target venue 합의

10명이 추천한 venue 빈도:

| Venue | 추천 빈도 | Tier |
|-------|---------|------|
| **NeurIPS Climate Change AI Workshop 2026 (poster, 4-page)** | 5 (R5, R6, R7, R9, R10) | **Tier 1 (highest)** |
| **한국정책학회보 (KCI)** | 3 (R3, R8, R9) | **Tier 1** |
| Climate Policy (Q1) | 4 (R1, R3, R4, R9) — 단 n 확장 후 | Tier 2 |
| Global Environmental Politics | 3 (R2, R3, R9) — 단 σ_regime 처리 후 | Tier 2 |
| Political Analysis | 2 (R5, R7) — 단 n 확장 후 | Tier 2 |
| Global Environmental Change | 1 (R9) — 본격 확장 후만 | Tier 3 |

### **Final venue recommendation**:
1. **즉시 (1–2 month)**: NeurIPS CCAI 2026 Workshop short paper (4-page poster)
2. **병행 (1–2 month)**: 한국정책학회보 한국어 단일 저자 논문
3. **6–12 month 후 확장 후**: Climate Policy 또는 Global Environmental Politics 본 투고

## 5. Revision plan timeline

| 단계 | 기간 | 활동 |
|------|------|-----|
| **즉시 (1–2 weeks)** | P0 일부 (시뮬 패널 부록 이동, σ_regime reframing, IRR 명료화) | paper.md §4.2/§5.4/§4 수정 |
| **단기 (1 month)** | P1 일부 (target venue 결정, NeurIPS CCAI short paper 4-page version 작성) | NeurIPS submission preparation |
| **중기 (2–3 months)** | n 확장 (E5 longitudinal partial), NATO 4축 reliability 측정, multi-seed R-GAT | 데이터 수집 + 코드 재실행 |
| **장기 (6–12 months)** | Real expert validation panel (E7), 인과 식별 분석 (E6), longitudinal 완성 | Climate Policy / GEP 본 투고 준비 |

## 6. 합의 요약

> CINA v3.0 프로젝트는 **자기 비판의 정직성과 reproducibility 인프라가 학술 연구로서 valid한 수준**이지만, **n 작음, 단일 사례 중심, 시뮬레이션 vs 실제 검증 분리 부족, 통계적 power 부족, 이론-측정 정합성의 부분적 모순**으로 현재 형태로는 Q1 학술지 투고가 부적합하다.
>
> **즉시 수정 가능한 P0 3건 + P1 4건을 통해 NeurIPS Climate Change AI Workshop 2026 short paper로의 투고는 1–2개월 내 가능**하다. **Climate Policy / GEP 본 투고는 longitudinal 확장 (E5)과 real expert validation (E7) 완료 후 6–12개월** 시점이 현실적이다.
>
> 본 paper의 가장 큰 강점은 **명백한 약점을 모두 disclosed한 자기 비판의 모범 사례**라는 점이며, reviewer가 본 시뮬레이션을 통해 미리 잡은 약점들을 revision plan에 반영하면 실제 외부 reviewer가 동일한 critique를 반복할 가능성이 낮아진다.

---

## 7. 다음 단계

본 META_REVIEW가 합의되면 다음을 진행한다.

1. **REVISION_PLAN.md** — P0/P1/P2 action items의 timeline + responsibility 명시
2. **paper.md, deliverables/, src/** 수정 (1–2 week)
3. **NeurIPS CCAI 2026 Workshop CFP 확인** + 4-page short paper 적합 분량으로 압축
4. **arXiv preprint 업로드** (영구 인용 가능한 ID 확보)
5. **한국정책학회보 한국어 단일 저자 논문 작성** (외교부 정책 implication 강조)
6. **Real expert panel 섭외 시작** (KEI · KAIST · 외교부 · 환경부 · GEP 편집위원)

---

**작성**: 2026-05-05 (예상 점수 기반 초안)
**저자**: 최희도 (Heedo Choi) · zxsa0716@kookmin.ac.kr
**관련 문서**:
- [`EVALUATION_SESSION_DESIGN.md`](EVALUATION_SESSION_DESIGN.md)
- [`individual_reviews/R01-R10_*.md`](individual_reviews/)
- [`../research/CRITICAL_REVIEW.md`](../research/CRITICAL_REVIEW.md)
- [`../research/METHODOLOGY_ADVANCEMENT_ROADMAP.md`](../research/METHODOLOGY_ADVANCEMENT_ROADMAP.md)
