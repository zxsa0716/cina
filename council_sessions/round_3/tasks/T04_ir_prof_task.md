---
assigned_to: ir-political-professor
round: 3
priority: P0
depends_on:
  - council_sessions/round_3/tasks/T01_collector_task.md (T01 historical chair data)
  - council_sessions/round_3/tasks/T02_refinement_task.md (T02 frame_distribution 5범주, chair_metadata 67+)
  - council_sessions/round_2/ir_political/critique.md (Round 2 권고 anchor)
  - council_sessions/round_2/synthesis/cross_review.md
inputs:
  - council_sessions/round_3/refinement/professor_input/ir_pack_round3.md (T02 산출)
  - data/processed/chair_metadata.jsonl v2 (17 → 67+)
  - data/processed/frame_by_group.csv (group × frame contingency)
  - data/processed/instrument_signals_v2.jsonl
  - data/processed/country_features_v2.csv (realist baseline 포함)
  - data/raw/baseline/{wb_gdp_2024,owid_co2_cumulative,sipri_milex_2024,cow_alliances_v4_1}.{json,csv,xlsx}
  - data/raw/unfccc/historical_presidency/* (COP21~COP29 letters)
deadline: T02 완료 후 24h target
review_tone: International Organization / ISQ reviewer (revise-not-reject)
---

# T04 — IR / Political-Science Professor Round 3

## 목적

Round 2 §3 핵심 비판 3건의 정밀화 결과를 검증한다: (a) chair_metadata N=17 → 67+ 후 인과 추론 수준 도달 여부, (b) frame_type 5범주 모두 활성화 후 AOSIS·LDC norm entrepreneurship visibility, (c) 비-BASIC vs BASIC 의장국 counterfactual baseline 가능성. 동시에 Tallberg 4 채널 모두 측정 가능한지 검증하고, R-GAT drafts_text edge ablation 가능성을 평가한다.

## 구체 산출물

### Section 1. chair_metadata N≥67 후 인과 추론 수준 검증

Round 2 C2.1 (N=17 인과 추론 불가) 해결 여부 진단:

- [ ] **샘플 사이즈 확장 검증**:
  - chair_metadata 17 → 67+ (목표). 실제 N 확인
  - COP21~COP30 분포: COP당 records 수 균형 (단일 COP over-concentration 회피)
  - Bayer & Urpelainen(2013, ISQ) 기준 N>100 기준선 비교
- [ ] **Tallberg 4 채널 모두 측정 가능성**:
  - (i) Information asymmetry: secretariat informational note (FCCC/CP/.../INF) — 17 → ?
  - (ii) Process / formula control: "Draft decision -/CMA." 패턴 — 4 → ?
  - (iii) Brokerage: co_facilitator=True — 3 → ?
  - (iv) Agenda-shaping: "proposed under agenda item" — 2 → ?
  - 채널 (i) 잡혔는가 (Round 2 critique §1.1 가장 약한 채널)
- [ ] **counterfactual baseline 1 (chair-level)**:
  - COP21 Fabius (FRA, EU/Umbrella) chair language vs COP30 Lago (BRA, BASIC) chair language
  - sovereignty/voluntary frame 비율 t-test 또는 Cohen's d
  - 비-BASIC 의장 (Fabius, Sharma, Schmidt) vs BASIC 의장 (Lago) 분리 통계 검증
- [ ] **L.25 advance→final cosine diff 산출**:
  - sBERT embedding으로 advance(`d763`) → final(`f569`) cosine similarity
  - 가설: cosine > 0.85 → chair-driven (formula control)
  - COP29 Baku decision의 advance→final cosine과 비교 (counterfactual baseline 2)

### Section 2. frame_type 5범주 분포 균형 검증

Round 2 C2.2 (justice/development 0건) 해결 여부:

- [ ] **frame_distribution 변화**: scientific 51 / mixed 24 / sovereignty 5 / **justice 0** / **development 0** → 새 분포
  - 5범주 모두 nonzero
  - justice ≥ 5건, development ≥ 5건 (T02 P0-C 목표)
- [ ] **그룹별 frame contingency table 분석**:
  - data/processed/frame_by_group.csv 직접 검토
  - Pearson χ² test 보고
  - Cohen's d (effect size)
  - LMDC (sovereignty 우세) vs AOSIS (justice 우세) vs LDC (development 우세) 분리 검증
  - **검증 통과 기준** (IR 교수 §5.2):
    - AOSIS frame_type = justice 또는 mixed(justice 우세) ≥ 60%
    - LDC frame_type = development 또는 justice ≥ 50%
    - LMDC frame_type = sovereignty 우세
- [ ] **Finnemore-Sikkink norm life cycle 단계 매핑**:
  - 현재 corpus가 어느 단계 (emergence / cascade / internalization)에 위치하는가
  - AOSIS의 "1.5 to stay alive" rhetorical signature 검출 여부
  - Allan(2019) GEP "1.5°C as norm" 가설 정합성

### Section 3. R-GAT drafts_text edge ablation 가능성 평가

Round 2 §1.3 (N=17 attention overfit) 해결 여부:

- [ ] **drafts_text edge type N 검증**:
  - 17 → 67+ 후 R-GAT 학습 가능성
  - Schlichtkrull et al.(2018) R-GAT 기준 edge type별 attention head 학습에 충분한가
  - Kinne(2018, ISQ) Defense Cooperation Agreement network N≥100 기준 vs 현재 N
- [ ] **edge type ablation 통계 검증 가능성**:
  - drafts_text edge 포함 vs 제거 → F1 차이 보고 가능한가
  - K-fold cross-validation 설계 가능한가
- [ ] **Round 4-5 GAT 학습 prep 권고**:
  - country_features_v2 (36-dim) + chair_status edge + drafts_text edge
  - baseline B0 (realist GAT, GDP+CO2+Mil+Alliance만) vs B1 (CINA full)
  - 두 baseline 차이가 통계적으로 유의한지 평가 protocol

### Section 4. Realist baseline B0 평가 prep

T01 P0-B 수집 데이터 검토:

- [ ] **country_features_v2.csv 32-dim → 36-dim 검증**:
  - GDP_log_2024, CO2_cum_log_1850-2024, milex_pct_gdp, alliance_count_cow
  - CINA 20국 모두 결측 없음
  - ISO3 join 정확
- [ ] **realist baseline B0 평가 메트릭**:
  - 가설: realist 변수만으로 stance 예측 → 80% 이하 F1 (CINA 전체 변수 ≥ 90% F1 필요)
  - 만약 realist 변수만으로 90% 이상 예측 → CINA novelty 약화 위험
- [ ] **Drezner(2007) 권력 비대칭 가설 검증**:
  - GDP+military 합산 high-power 국가가 voluntary/non-prescriptive 결정문 frame을 더 선호하는가
  - Hochstetler(2012) BASIC chair-host paradox 정량 시그널

### Section 5. Round 3 Rubric 재평가

Round 2 평점 (3.9/5) 기준으로 Round 3 진척 평가:

| Dimension | Round 2 | Round 3 | 변화 동인 |
|-----------|--------:|--------:|---------|
| Theoretical grounding | 4.0 | ? | frame 5범주 활성화 + Tallberg 4 채널 측정 가능 |
| Methodological rigor | 3.5 | ? | counterfactual baseline 1·2 산출 + R-GAT ablation prep |
| Empirical validity | 3.5 | ? | chair_metadata 67+ + advance→final diff |
| Policy strategic relevance | 4.0 | ? | realist baseline 추가 |
| Clarity & reproducibility | 4.5 | ? | ICR 인프라 추가 |

목표: 평균 4.2+ (Round 4-5에서 4.5 도달).

### Section 6. 핵심 비판 (Round 3 진척 기반)

Round 3 정밀화 결과가 새 결함을 드러내는지 진단:

- [ ] **C1 (Round 3)**: chair_metadata N=67이 여전히 quantitative inference에 부족한가? Bayer-Urpelainen 2013 N>100과 비교
- [ ] **C2**: frame_type 5범주 활성화 후, 이 분류가 *causal mechanism*인지 *descriptive label*인지 식별 가능한가. Process tracing (Beach-Pedersen 2019) 적용 가능 여부
- [ ] **C3**: realist baseline B0이 너무 강하게 예측하면 CINA novelty 위협. 이 위험을 어떻게 분석으로 다룰 것인가

### Section 7. policy-science-professor와의 합의·불일치 예측 (Round 3)

- [ ] 합의 예상: chair_metadata 67+ 후 인과 추론 가능성, frame_distribution 5범주 활성화
- [ ] 불일치 예상: 정책학자가 "한국 KEI cross-walk"를 강조 → IR은 "single-country case 약화 평가"
- [ ] 통합: KEI cross-walk를 IR 측에서 "domestic implementation politics" lens로 재해석 (Putnam 1988 two-level games)

### Section 8. team-lead 결정 요청

- [ ] D1: chair_metadata N=67이 충분치 않다면 Round 4 추가 수집 필요한가 (UNFCCC informational notes)
- [ ] D2: realist baseline B0 평가 시 Round 5 GAT 학습 데이터 분할 (train/val/test) 어떻게 할지
- [ ] D3: Castro et al. 2025 supplementary academic email contact (Round 1 D5 미해결, HEEDO-7) 진척 여부

## 품질 기준

- [ ] critique 본문 ≥ 3,000자
- [ ] 5-Dimension Rubric 명시 점수
- [ ] Round 3 핵심 비판 Top 3 (C1 C2 C3)
- [ ] Reference ≥ 5개 추가 (Round 1·2 합산 18개 + Round 3 5개 = 누적 23개)
- [ ] frame_by_group contingency 검증 + χ² test 결과 보고
- [ ] L.25 advance→final cosine 정량 보고
- [ ] counterfactual baseline 1 (비-BASIC vs BASIC) t-test or Cohen's d 보고

## 제공된 컨텍스트

- Round 2 critique 본인 (council_sessions/round_2/ir_political/critique.md)
- Round 2 cross-review (council_sessions/round_2/synthesis/cross_review.md)
- Round 2 quality_gates (council_sessions/round_2/synthesis/quality_gates.json)
- T01 historical chair data + T02 정밀화 후 데이터
- realist baseline 4 datasets

## 출력 위치

- Critique: `council_sessions/round_3/ir_political/critique.md`
- Counterfactual analysis: `council_sessions/round_3/ir_political/counterfactual_baseline.md`
- R-GAT ablation prep: `docs/17_rgat_edge_ablation_protocol.md`
