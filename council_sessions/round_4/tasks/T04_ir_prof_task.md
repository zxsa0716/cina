---
task_id: T04-Round4
assigned_to: ir-political-professor
agent_model: opus
round: 4
priority: P0
depends_on:
  - T01 Round 4 산출물 (chair letters 12+, NSA 8+ entity)
  - T02 Round 4 산출물 (chair_metadata 80+, L25_drafting_diff, country_features_v2.csv, realist_b0_eval, mixed_frame_composition)
  - council_sessions/round_3/ir_political/critique.md (anchor 4.13/5)
  - council_sessions/round_3/synthesis/cross_review.md (§1.2 D-R3-1 chair 충분성, D-R3-2 Plano Clima)
  - Heedo 결정 D-R4-1 (Plano Clima 챕터 분기 vs 통합)
deadline: T02 완료 후 48시간
---

# T04 Round 4 — ir-political-professor 작업 지시

## 0. 목적

Round 3에서 IR 4.13/5 도달. Round 4 목표 **4.40+** — Methodological 3.7 → 4.2 (+0.5) + Empirical 3.8 → 4.3 (+0.5). 결정 dimension은 **chair_metadata N≥80 panel 분석 + 에너지 수출국 의장 가설 검증 + realist B0 F1 결과 대응**.

## 1. 산출물 (Deliverables)

### 1.1 P0 — chair_metadata N≥80 후 Bayer-Urpelainen panel 분석 가능성 검증

**입력**: T02 Round 4 §1.9 산출 chair_metadata.jsonl 80+ records, COP_coverage ≥ 10

**검증 질문**:

1. **N과 COP_coverage 통계적 충분성**:
   - Bayer-Urpelainen (2013, *ISQ* 57) 패널 분석 minimum: N>100, COP_coverage ≥ 10
   - 80 records가 "panel regression 가능" 임계인가, 아니면 "case study + descriptive"에 머무르는가?
   - 자유도 계산: T02 산출 chair_metadata에서 unique chair × COP × frame_type 셀 수 = ?
   - **권고**: N=80에서 panel 분석이 합리적이면 즉시 진행, 미달이면 Round 5 추가 수집 우선순위

2. **counterfactual baseline 충분성** (R3 §3.2 D-R3-1 IR 부정적 해석):
   - 비-BASIC 비-산유국 의장 (FRA, FJI, UK, CHL) baseline ≥ 6 records 충족?
   - 산유국 의장 (UAE, AZE, EGY, POL coal) baseline ≥ 8 records 충족?
   - t-test 또는 Cohen's d 산출 가능?

3. **Tallberg 4 채널 자동 식별률** (Round 3 §1.3):
   - Round 3에서 (i) info asym 4건, (ii) formula control 6건, (iii) brokerage 4건, (iv) agenda-shaping 2건
   - Round 4 chair +12 records 추가 후 4 채널 모두 N≥10 도달?
   - SBI/SBSTA opening plenary minutes 추가 수집되었는가? (T01 §1.6)

**산출물**:
- `council_sessions/round_4/ir_political/chair_panel_validation.md`
- 권고 (1) panel regression 즉시 진행 / (2) Round 5 N≥150 추가 수집 후 진행 / (3) case-study limit으로 제출

### 1.2 P0 — "에너지 수출국 의장 3연속" 가설 검증 평가

**입력**: T01 + T02 chair_metadata 80+ records (UAE/AZE/BRA + COP21~27 historical)

**가설**: COP28(UAE) → COP29(AZE) → COP30(BRA)의 연속 3개 의장국이 모두 에너지 수출국/자원 보유국이라는 사실이 GGA의 voluntary + soft-law 귀결에 구조적 영향을 주었는가?

**Round 3 §3.1 4 이론 옵션 재검토**:

| 이론 | Round 3 검증 가능성 | Round 4 검증 가능성 (N=80 후) |
|------|---------------------|--------------------------------|
| Sebenius (1983) negotiation arithmetic | 부분 (N=3) | **검증 가능** (UAE/AZE letter mit:adapt 비율 vs 비-산유국 의장 baseline) |
| Steinberg (2002) presidency as agenda-setter | 불가 (counterfactual 부재) | **부분 검증** (FRA/UK/CHL baseline 추가 시 KS-test 가능) |
| Hochstetler (2012) BASIC chair-host paradox | 가능 (R3 가시화) | **확장 검증** (BRA + 추가 BASIC 의장 baseline) |
| Falkner (2016) climate hegemon thesis | 부분 | **검증 가능** (5 COP letter panel — Glasgow→Sharm→Dubai→Baku→Belém) |

**검증 질문**:
1. Round 4 chair_metadata N=80에서 4 이론 중 검증 *가능* 단계와 *불가능* 단계 명확화
2. 검증 결과가 "에너지 수출국 의장 효과 statistically significant (p<0.05)" 또는 "spurious correlation"
3. 결과에 따라 NeurIPS CCAI 워크숍 paper의 핵심 finding 후보 가능?

**산출물**:
- `council_sessions/round_4/ir_political/energy_chair_hypothesis_test.md`
- 4 이론별 검증 결과 + 통계 reporting (p-value, effect size, 신뢰구간)
- 권고: paper 핵심 finding 채택 / Discussion section 가설 / Round 5 N≥150 후 재검증

### 1.3 P0 — Realist B0 F1 ≥ 90% 검증 + Discussion 대응 전략

**입력**: T02 Round 4 §1.4 산출 realist_b0_eval.json (F1 + 3 시나리오)

**3 시나리오 대응 전략 작성**:

#### Case 1: F1 < 80% — CINA novelty 강화

- 권고: CINA 핵심 contribution = "realist 단독으로는 stance 설명 부족. frame_type + chair_metadata가 incremental +N pp 추가"
- paper Discussion §결정성: "CINA의 정교한 GAT + frame variable이 realist baseline보다 유의미"
- target reviewer: International Organization, GEC

#### Case 2: F1 80-90% — incremental 위치

- 권고: CINA contribution = "realist이 80-90% 설명. CINA frame_type이 +N pp 추가 (예: +5pp). 단 incremental 정량화 명확"
- paper Discussion: "incremental contribution이지만 frame mechanism 설명력 (causal interpretability) 추가"
- target reviewer: GEP, Climate Policy

#### Case 3: F1 ≥ 90% — Drezner (2007) "power asymmetry explains all"

- **Critical**: CINA novelty 위협 (R3 IR §9 D2 명시)
- 권고: paper 재구성 — CINA를 "stance prediction" task가 아닌 "**explanation + interpretability**" task로 재배치
- Drezner 2007 인용 + "power asymmetry explains stance, frame_type explains *justification*" 분리 framing
- target reviewer: GEP, NeurIPS CCAI (XAI angle)

**산출물**:
- `council_sessions/round_4/ir_political/realist_b0_discussion_strategy.md`
- 실제 F1 값에 따라 채택 시나리오 명시 + paper Discussion 1-2 페이지 초안

### 1.4 P0 — L.25 advance→final cosine diff 분석 (Tallberg formula control 정량 검증)

**입력**: T02 Round 4 §1.1 산출 L25_drafting_diff.jsonl + L25_drafting_diff.md

**검증 질문**:
1. **변화 magnitude**: 평균 cosine sim 분포가 어떻게 분포되는가? (cosine sim < 0.5 paragraph 비율)
2. **Tallberg formula control 가설**: chair (BRA Corrêa do Lago)가 advance → final로 paragraph를 어떻게 수정했는가? Top-10 변경 paragraph가 sovereignty 또는 voluntary 언어 강화 방향?
3. **frame_type 변환**: advance에서 justice였던 paragraph가 final에서 mixed/sovereignty로 변경된 사례 N건?

**산출물**:
- `council_sessions/round_4/ir_political/l25_formula_control_analysis.md`
- Tallberg (2010) 4 채널 중 (ii) formula control의 첫 정량 evidence

### 1.5 P0 — Plano Clima 분석 docs/16 구조 결정 입력 (Heedo D-R4-1 응답)

**Heedo D-R4-1 옵션** (Round 3 cross-review §8):
- A. 분기 (`docs/15_two_level_instrument_translation.md` Policy + `docs/16_chair_brokerage_game.md` IR)
- B. 통합 (`docs/15_brazil_dual_role_analysis.md` 단일 챕터)
- C. Round 5 결정 연기

**IR 입장 명확화**:
- 옵션 A 채택 시 IR 챕터 (`docs/16_chair_brokerage_game.md`) 목차 5절 초안
- Tallberg (2010) chair power 4 채널 + Hochstetler (2012) BASIC paradox + Falkner (2016) climate hegemon 통합 분석 frame
- BRA presidency letter + Plano Clima Vol II + L.25 cosine diff를 game-theoretic equilibrium 분석에 통합

**산출물**:
- `council_sessions/round_4/ir_political/plano_clima_chapter_input.md`
- 옵션 A 권고 시 chapter outline 1-2 페이지

### 1.6 P0 — 5-Dimension Rubric 재평가 (Round 3 → Round 4)

**입력**:
- T01 Round 4 chair letters + NSA 8+ entity
- T02 Round 4 chair_metadata 80+, L25 cosine, country_features_v2, mixed_composition
- Stage 1 LLM trial 결과

**재평가 dimensions**:

| Dimension | R3 | R4 expected | 동인 |
|-----------|----|-------------|------|
| Theoretical | 4.3 | 4.5? | Indigenous epistemic community 노드 NSA 8+로 Hooghe-Marks Type II 정당화 강화 + Plano Clima 분석 |
| Methodological | 3.7 | 4.2? | chair N=80 panel 가능 + L.25 cosine + Tallberg 4 채널 모두 N≥10 + Stage 1 LLM 가동 |
| Empirical | 3.8 | 4.3? | chair_metadata 32→80 (Bayer-Urpelainen threshold 도달) + NSA 20→40+ |
| Policy strategic | 4.3 | 4.4? | 에너지 수출국 의장 가설 검증 + realist B0 Discussion 전략 |
| Reproducibility | 4.5 | 4.7? | cr4_compliance + L25 cosine seed 기록 + Stage 1 LLM seed/temp |

**산출물**: `council_sessions/round_4/ir_political/critique.md` 본문 통합

### 1.7 P1 — Round 4 결정적 비판 Top 3 (Round 5 권고)

Round 3 critique §"Round 3 핵심 비판 Top 3" + Round 4 신규 발견 합산.

**산출물**: critique.md §"Round 4 핵심 비판 Top 3" 절

## 2. 품질 기준

- [ ] 6 deliverable 모두 산출 (1.1 + 1.2 + 1.3 + 1.4 + 1.5 + 1.6)
- [ ] critique.md 5-Dim Rubric 재평가 (목표 4.40+)
- [ ] 에너지 수출국 의장 가설 검증 결과 명확
- [ ] realist B0 F1 결과에 따른 Discussion 전략 1 시나리오 채택
- [ ] D-R4-1 Heedo 결정 입력 명확

## 3. 제공된 컨텍스트

- `council_sessions/round_3/ir_political/critique.md` (4.13/5 anchor)
- `council_sessions/round_3/synthesis/cross_review.md` (§1.2 D-R3-1, D-R3-2)
- `council_sessions/round_3/refinement/professor_input/ir_pack_round3.md`
- `data/processed/chair_metadata.jsonl` (T02 산출 후 80+ records)
- `data/processed/L25_drafting_diff.jsonl`
- `data/processed/realist_b0_eval.json`
- `data/processed/mixed_frame_composition.jsonl`

## 4. 보고

### 4.1 형식
`council_sessions/round_4/ir_political/critique.md` (Round 3와 동일 구조 + 1.1~1.7 통합)

### 4.2 Policy 교수와의 합의·불일치 예측 (§7 절)
- D-R3-1 chair 충분성 — Round 4에서 합의 가능?
- D-R3-2 Plano Clima 분석 정점 — 옵션 A 분기 합의?
- D-R3-3 NSA 옵션 A+C 하이브리드 — Round 5 R-GAT 학습 시 ablation 비교

---

*— team-lead, 2026-04-26*
