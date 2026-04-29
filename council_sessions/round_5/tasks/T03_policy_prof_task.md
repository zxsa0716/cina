---
assigned_to: policy-science-professor
agent_model: opus
round: 5
priority: P0
depends_on:
  - council_sessions/round_5/refinement/professor_input/policy_sci_pack_round5.md
  - council_sessions/round_5/tasks/T02_refinement_task.md (P0-2 산출 필수)
  - council_sessions/round_5/tasks/T01_collector_task.md (P0-3 KEI WP 5건)
  - council_sessions/round_4/policy_science/critique.md (R4 baseline 4.38)
deadline: Round 5 cross-review 작성 전
---

## 목적

Round 4 critique C1·C2 후속 검증. T02 R5 P0-2 산출 (Brazilian negative Authority 분리 후 IRR_intl 재계산) 결과를 정책학적으로 재해석하고, T01 R5 P0-3 산출 (KEI WP 5건 가중치 reference)을 통해 IRR_Korea 가중치의 외부 정합성을 평가한다. Round 5 dual review에서 Policy 점수를 4.38 → 4.55+ 도약시키기 위한 핵심 라운드.

---

## 구체 산출물 (P0)

### P0-1. Brazilian Δ_revised 정책학적 재평가 (C1 후속)

- [ ] T02 R5 P0-2 산출 (`data/processed/irr_brazilian_translation_gap_v2.json`) 정독
- [ ] 두 시나리오 정책학 해석:
  - 시나리오 A (Δ=0.269, negative 미분리): "instrument inflation" 해석 — Brazilian dual-role 의장국이 의도적으로 voluntary 조항 삽입으로 Δ 측정값을 과대평가
  - 시나리오 B (Δ_revised, negative 분리): "true translation gap" — 순수 promise-realization 격차
- [ ] Howlett(2019) instrument calibration 이론 + Tosun & Workman(2017) instrument translation 문헌과 cross-walk
- [ ] **결정적 판단**: 어느 시나리오가 정책학적으로 더 타당한가? Brazilian dual-role의 strategic ambiguity 가설(IR critique §2.3)과 충돌·보완 관계 명시
- [ ] 학술 기여 framing: "negative Authority 분리는 IRR 산식 v2.0 업그레이드의 첫 정량 검증" — Global Environmental Change reviewer가 받아들일 framing 제시

### P0-2. IRR_Korea 가중치 외부 정합성 평가 (C2 후속)

- [ ] T01 R5 P0-3 산출 (`data/raw/round5/kei_wp_series/WEIGHTING_REFERENCE.md`) 정독
- [ ] CINA 가중치 (Authority 0.35 / Treasure 0.25 / Nodality 0.20 / Organization 0.20)와 KEI WP 5건 가중치 비교 표 작성
- [ ] 정합성 score: (a) 동일 (b) 유사 (±5%) (c) 차이 있음 (>10%) (d) 상이 (>20%)
- [ ] 차이 시 정당성 분석:
  - CINA가 GGA 적응 맥락 특화 가중치라 KEI 일반 NAP과 다를 수 있음 → 학술 차별화 가능
  - 또는 외부 정합성 부재 → R6 KEI 명수정 박사 직접 협의 필수
- [ ] **권고**: D-R5-2 (KEI 외부 협의 시점) 결정 입력 — Round 6 우선 또는 Round 7 연기

### P0-3. Korean L&D-OP 0.390 약점 → 수업 brief 권고

- [ ] IRR_Korea_2025 6 dim 중 L&D-OP 0.390 최약점 → 환경부 적응대책 L&D 항목 부재 evidence
- [ ] 한국 환경부 장관 brief 권고 3건 작성:
  - 단기 (2026년): COP31 전 L&D Operational Entity 관련 input 정식 발신
  - 중기 (2026-2027): 한국 NAP 차기 update에 L&D 항목 신설
  - 장기 (2028~): 한국 NAP IRR 정기 측정 → KEI 협력 인프라
- [ ] `deliverables/track_a_korean_brief_round5.md` 신설 또는 update

### P0-4. 5-Dim 자기평가 + Round 6 권고

- [ ] 5-Dim 점수 self-rate (R4 4.38 baseline):
  - Theoretical (R4 4.5)
  - Methodological (R4 4.0)
  - Empirical (R4 4.4)
  - Policy strategic (R4 4.3)
  - Reproducibility (R4 4.7)
- [ ] mean ≥ 4.55 목표 (NeurIPS CCAI accept threshold)
- [ ] Round 6 권고 P0/P1 list (3-5건)
- [ ] team-lead 결정 필요 사안 (D-R6-x) 0-3건

---

## 품질 기준

- [ ] 모든 주장에 evidence 인용 (T02 산출 또는 KEI WP 원문)
- [ ] 두 시나리오 framing이 reviewer에게 방어 가능
- [ ] L&D-OP 권고 3건이 실무 외교부·환경부 적용 가능
- [ ] 5-Dim 점수 변동 시 정량 근거 명시 (어느 산출이 +0.X 영향)

---

## 제공된 컨텍스트

### Round 4 critique 자기 진술 (요약)
- Combined 5-Dim mean 4.38, Theoretical 4.5 / Methodological 4.0 / Empirical 4.4 / Policy strategic 4.3 (핵심 도약) / Reproducibility 4.7
- 핵심 비판 C1 (Brazilian Δ negative Authority 분리), C2 (IRR_Korea 가중치 외부 정합성)
- team-lead 결정 요청 5건: D-R5-1 ~ D-R5-5

### IR critique cross-reference
- IR §2.3 Brazilian dual-role strategic ambiguity 해석 (Policy C1과 보완 관계)
- IR §3.1.D KEI 협의보다 internal validity 우선 (Policy C2와 우선순위 차이)

### Round 4 cross-review §4 (team-lead 권고)
- D-R5-1: A (분리 + dual-framing 보고)
- D-R5-2: B (Round 6 KEI 협의)
- D-R5-3: A (Plano Clima 분기, D-R4-1 잔여)
- D-R5-4: A (수업 brief 직접 활용)
- D-R5-5: L.25 pre-crystallized formula 단일 채택

---

## 출력 위치

- `council_sessions/round_5/policy_science/critique.md`
- `deliverables/track_a_korean_brief_round5.md` (신설 또는 update)
