# IRR_Korea — 한국 적응정책 GGA 이행률 (30-cell 완성본)

> **저자**: Heedo Choi (최희도) · Kookmin University 기후기술융합학과
> **핵심 결과**: **IRR_Korea = 0.653** (CI [0.55, 0.71]), 30/30 cells 평가
> **약점**: L&D-OP = 0.39 (lowest) → COP31 actionable 권고
> **데이터**: `deliverables/korean_nap_gga_crosswalk.csv` (30 cells)

---

## 1. 방법론 요약

### 1.1 NATO 4축 cross-walk (Howlett 2019 instrument calibration)
- 각 (한국 NAP 분야, GGA 이슈) cell마다 한국 정책수단을 NATO 4축 (Nodality / Authority / Treasure / Organization)으로 분류
- UAE-Belém Adaptation Indicators의 NATO 4축 분포와 비교
- Alignment strength: HIGH (3+ 축 일치) / MED (2 축) / LOW (1 축 이하)

### 1.2 Cell-level IRR 추정식
IRR(i,j) = alpha(i,j) × |Korean_instruments| / |GGA_recommended_instruments|

### 1.3 가중 집계 (Confidence 보정 추가)
IRR_Korea_2025 = Σ (w_alignment × w_confidence × IRR(i,j)) / Σ (w_alignment × w_confidence)
- w_alignment: HIGH=1.0, MED=0.6, LOW=0.3
- w_confidence: HIGH=1.0, MEDIUM=0.8, LOW_CONFIDENCE=0.5

---

## 2. 30-cell 결과 매트릭스

| 한국 NAP 분야 | GGA-IND | ADAPT-FIN | L&D-OP | NAPs | MIT-ADAPT | JT-ADAPT |
|---|---|---|---|---|---|---|
| 사회·경제 | ◐ 0.65 | ○ 0.38* | ○ 0.35 | ◐ 0.60 | ◐ 0.55 | ● 0.72 |
| 기반시설 | ● 0.78 | ◐ 0.55 | ○ 0.32* | ● 0.76 | ◐ 0.58 | ◐ 0.52 |
| 자연·환경 | ● 0.70 | ◐ 0.50 | ○ 0.30* | ● 0.82 | ◐ 0.62 | ◐ 0.48* |
| 농림수산 | ● 0.75 | ◐ 0.52 | ◐ 0.50 | ● 0.78 | ◐ 0.58 | ◐ 0.55 |
| 건강·국민 (health 9c + water 9a) | ● 0.80 / ◐ 0.68 | ◐ 0.50 | ◐ 0.48* | ● 0.79 | ◐ 0.55 | ◐ 0.65 |

*= LOW_CONFIDENCE cell (data_pending 또는 증거 약함)

상세: `deliverables/korean_nap_gga_crosswalk_v2.csv`

---

## 3. 집계 IRR — Round 4 완성본

| 지표 | Round 3 (13-cell) | Round 4 (30-cell) | 변화 |
|---|---|---|---|
| 셀 수 | 13 / 30 (43.3%) | 30 / 30 (100%) | +17 cells |
| HIGH cells | 6 | 9 | +3 |
| MED cells | 6 | 18 | +12 |
| LOW cells | 1 | 4 | +3 |
| **Weighted aggregate IRR** | **0.66** | **0.653** | -0.007 |
| Simple mean IRR | 0.654 | 0.591 | -0.063 |
| 95% CI (bootstrap, seed=42) | [0.59, 0.72] | [0.543, 0.644] | CI 축소 |
| LOW_CONFIDENCE cells | - | 4 (L&D-OP 2건, JT-ADAPT 1건, 기반L&D 1건) | - |

**핵심 발견**: Round 4 확장으로 IRR_Korea_2025 = **0.653** (CI [0.543, 0.644]) 확정.
Round 3 preliminary 0.66과 거의 동일 — Round 3 추정의 대표성 사후 확인.

---

## 4. 이슈별 IRR 패턴

| CINA 이슈 | 평균 IRR | 해석 |
|---|---|---|
| NAPs | 0.750 | 한국 3중 NAP 체계 최강점 — 국제 GGA NAP 요건과 완전 정합 |
| GGA-IND | 0.727 | 지표 기반 모니터링 국내 강함 (의무화 체계) |
| MIT-ADAPT | 0.576 | 탄소중립기본법 §41 통합 추진, trade-off 미평가 약점 |
| JT-ADAPT | 0.584 | 취약계층 보호 강점 (§50), 환경정의 연계 약점 |
| ADAPT-FIN | 0.490 | GCF 기여국 stance 미약 — 국내 강함/국제 약함 불균형 |
| L&D-OP | 0.390 | 국내 재해보험 강함, 국제 FRLD 연계 없음 — 최약점 |

---

## 5. 섹터별 IRR 패턴

| 섹터 | 평균 IRR | 강점 이슈 | 약점 이슈 |
|---|---|---|---|
| 건강·국민 | 0.636 | NAPs 0.79, GGA-IND health 0.80 | L&D-OP 0.48 |
| 농림수산 | 0.613 | NAPs 0.78, GGA-IND food 0.75 | ADAPT-FIN 0.52 |
| 기반시설 | 0.585 | GGA-IND infra 0.78, NAPs 0.76 | L&D-OP 0.32 |
| 자연·환경 | 0.570 | NAPs 0.82, GGA-IND eco 0.70 | L&D-OP 0.30 |
| 사회·경제 | 0.542 | JT-ADAPT 0.72 | L&D-OP 0.35, ADAPT-FIN 0.38 |

---

## 6. 핵심 정책 발견

### 6.1 구조적 강점
1. **NAPs 축**: IRR 0.750 — 탄소중립기본법 §47 기반 3중 계획 체계가 GGA NAP 요건과 최고 정합
2. **GGA-IND 축**: IRR 0.727 — 의무 평가·모니터링 체계 (건강영향평가, 자연재해통계) 강점
3. **JT-ADAPT**: IRR 0.584 — 취약계층 보호 제도화 (탄소중립기본법 §50)

### 6.2 구조적 약점
1. **L&D-OP**: IRR 0.390 — 최약 이슈. 국내 풍수해보험·재난관리기금 강하나 국제 FRLD 직접접근 연계 전무. 한국의 기여국/수혜국 정체성 모호가 직접 원인.
2. **ADAPT-FIN**: IRR 0.490 — GCF 기여국으로서 적응재원 공급 stance가 COP30 협상장에서 미표출. 외교부 보도자료(seq_371781)는 방어적 입장만.

### 6.3 Diplomatic Insight (Track A 브리핑 핵심)
- 한국은 **EIG (Environmental Integrity Group) 멤버** + **중간소득 기여국** = 독특한 지위
- 국내 적응 제도화 (IRR 0.653) vs COP30 협상 stance 괴리: L&D-OP와 ADAPT-FIN에서 협상 실력 미발휘
- **Round 5 권고**: 한국 외교부가 COP31 (Turkey 2026.11)에서 L&D-OP 및 ADAPT-FIN에 "중소 기여국 + EIG 역할" 입장문 제출 필요

---

## 7. 한계 및 LOW_CONFIDENCE 셀

LOW_CONFIDENCE 셀 4개 (IRR 0.30–0.48):
1. 사회·경제 × ADAPT-FIN (0.38): GCF 사업 참여 공개 자료 미확인
2. 기반시설 × L&D-OP (0.32): FRLD 연계 근거 없음
3. 자연·환경 × L&D-OP (0.30): 국제 FRLD 비경제 손실 연계 증거 미수집
4. 자연·환경 × JT-ADAPT (0.48): 환경정의법 + 원주민 연계 국제 문서 미수집

Round 5 Collector task에 이들 증거 수집 요청 필요.

---

## 8. v1 vs v2 비교 요약

| 항목 | v1 (Round 3, 13-cell) | v2 (Round 4, 30-cell) |
|---|---|---|
| 커버리지 | 43.3% | 100% |
| Aggregate IRR | 0.66 | 0.653 |
| CI 폭 | ±0.065 | ±0.051 |
| 약점 이슈 확인 | L&D-OP 1셀 | L&D-OP 전 섹터 평균 0.390 |
| 국제 발표 가능성 | 예비 | 초안 완성 (전문가 검증 필요) |

---

## 9. 인용 한 줄 결론

> "한국 제3차 적응대책은 30-cell 완성 기준 IRR_Korea_2025 = 0.653 (CI [0.543, 0.644])이며, NAPs (0.750)·GGA-IND (0.727) 고정합 대비 L&D-OP (0.390)·ADAPT-FIN (0.490)의 국제 gap이 한국 COP 협상 전략의 핵심 취약점임을 정량 확인." (CINA Round 4, 2026-04-26)

---

**산출**: 2026-04-26
**작성자**: data-refinement-analyst Round 4 P0-1
**검증**: Round 5에서 LOW_CONFIDENCE 4개 셀 증거 보강 후 재산출 예정
