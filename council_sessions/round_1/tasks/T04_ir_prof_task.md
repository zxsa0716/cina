---
assigned_to: ir-political-professor
round: 1
issued_by: team-lead
issued_at: 2026-04-25
priority: P0
deadline: round_1 종료 전
depends_on: [T02_refinement_task.md]
---

# Task T04 — Round 1 IR / Political Science Critique

## 목적
국제정치학·외교학 교수 시점에서 CINA의 Round 1 산출물을 비판적으로 검토한다. IR 이론 접지, 협상 권력 분석, 연합 동학, 패권 서사 관점에서 다음 4개를 평가한다:
1. CINA 프레임워크의 IR 이론 접지 (`docs/01_theoretical_foundations.md`)
2. Round 1 데이터 정제 결과 (`data_refinement/round_1/REPORT.md`)
3. Stage 2 그래프 분석 설계 (`docs/05_stage2_graph_analysis.md`)
4. 신규성 포지셔닝 (`docs/08_novelty_positioning.md`)

## 사용할 이론 앵커

- **현실주의 / 자유주의 / 구성주의** 균형 비판
- **Regime Complex Theory** (Keohane & Victor 2011) — CINA가 이미 채택. 더 정교화 가능한가?
- **Two-Level Games** (Putnam 1988) — flexibility_signals 추출의 IR 정합성
- **Issue Linkage Theory** (Tollison & Willett, Sebenius) — hypergraph가 진짜 issue linkage 이론을 구현하는가
- **Epistemic Communities** (Haas 1992) — Belém indicators 사례에서 작동 메커니즘
- **Hegemonic Stability / G-X 외교** — 의장국 브라질의 위치
- **Network IR** (Hafner-Burton, Kahler, Montgomery 2009) — CINA의 graph approach가 이 흐름에 어떻게 연결되나

## 구체 산출물

`council_sessions/round_1/ir_political/critique.md`:

### Section 1. 5-Dimension Rubric (1-5)
| Dimension | Score | 핵심 평가 |
|-----------|-------|----------|
| Theoretical grounding | X/5 | IR 이론 접지의 학술 수준 |
| Methodological rigor | X/5 | 협상 분석으로서 정합 |
| Empirical validity | X/5 | COP30 사례 적용 타당성 |
| Policy / strategic relevance | X/5 | 외교 실무 (외교부, MOFA) 적용성 |
| Clarity and reproducibility | X/5 | IR 학계 reviewer 기준 |

### Section 2. 핵심 비판 (Top 3)
각 비판:
- 구체 인용 (CINA 문서의 어느 섹션·문장)
- IR 이론 근거 (저자·연도·핵심 명제)
- 수정 제안 (실행 가능한 형태)

### Section 3. Power 분석 강화 권고
- 의장국 브라질의 dual-role (mediator vs interest) 정량화 방법
- BASIC 내부 분열 vs LMDC 결속의 권력 분석
- AOSIS 도덕적 권위 vs 실질 협상력 격차

### Section 4. policy-science-professor 와의 합의·불일치 예측
- 합의 예상: ...
- 불일치 예상: 정책학자가 "이행" 강조 시 IR은 "권력" 강조
  → 두 관점 모두 CINA에 통합되어야 함

### Section 5. 추가 reference (영어 IR literature 우선)
- *International Organization*, *International Studies Quarterly*, *Global Environmental Politics*
- Network IR 최근 5년 ≥ 3
- Climate diplomacy specific (Bäckstrand, Falkner, Hochstetler) ≥ 2

## 제공된 컨텍스트
- 데이터 정제 결과: `council_sessions/round_1/refinement/professor_input/ir_pack.md`
- CINA 이론 접지: `docs/01_theoretical_foundations.md`
- 신규성: `docs/08_novelty_positioning.md`

## 비판 어조 가이드
- **국제정치학회 reviewer 수준**: 학술 reviewer가 reject할 약점 적극 지적
- **이론 vs 데이터 정합**: 이론 인용만으로는 부족, 어떻게 측정할지까지
- **냉정한 비교**: 기존 IR computational 연구 대비 진짜 새로운가?

## 품질 기준
- [ ] critique.md 2000-4000자 (한국어, IR 용어는 영어 병기)
- [ ] 모든 비판에 IR 이론 reference
- [ ] 5-rubric + 산출 근거
- [ ] 추가 reference ≥ 5개 (영어 학술지)
