---
assigned_to: policy-science-professor
round: 3
priority: P0
depends_on:
  - council_sessions/round_3/tasks/T02_refinement_task.md (T02 outputs)
  - council_sessions/round_2/policy_science/critique.md (Round 2 권고 anchor)
  - council_sessions/round_2/synthesis/cross_review.md
inputs:
  - council_sessions/round_3/refinement/professor_input/policy_sci_pack_round3.md (T02 산출)
  - data/processed/uae_belem_indicators.jsonl v2 (kind 분화 후)
  - data/processed/instrument_signals_v2.jsonl (TF-IDF 가중 NATO 4축)
  - data/processed/frame_by_group.csv
  - data/processed/country_features_v2.csv (32→36-dim)
  - data/raw/korean_gov/me_3rd_adaptation_plan_2026.pdf
  - data/raw/korean_gov/kei_2024_08_adaptation_monitoring.pdf
  - src/stage1/prompts/v1_4_extraction.md
deadline: T02 완료 후 24h target
review_tone: 한국정책학회보 / Climate Policy / Global Environmental Change reviewer (revise-not-reject)
---

# T03 — Policy-Science Professor Round 3

## 목적

Round 2 권고 4건의 정밀화 결과를 검증한다: (a) NATO 4축 변별력 회복(Nodality SD 0.36→?), (b) 149 indicator 노이즈 정제 후 진짜 indicator 분포, (c) 키워드 사전 정밀화의 인과 추론 함축, (d) Stage 1 LLM v1.4 prompt가 evidence-based 점수 산출에 충분한가. 동시에 Task E (Implementation Realization Rate) 메트릭을 한국 KEI 모니터링 보고서에 시범 적용한다.

## 구체 산출물

### Section 1. Round 2 권고 정밀화 검증

각 권고 항목마다 (a) Round 2 → Round 3 변화 정량 보고, (b) 정책학적 함의 평가, (c) Round 4 추가 권고 명시:

- [ ] **NATO 4축 SD 변화**: Nodality SD 0.36 → ?
  - discriminating keyword + TF-IDF 가중 적용 후 6 issue × 4 instrument 매트릭스 분포 분산 비교
  - GGA-IND Authority 6.1 → ? (기존 가설 유효성 검증)
  - 통계적 유의성: SD 차이 F-test 또는 Levene 검정
- [ ] **149 indicator → ? indicator (kind=indicator만)**:
  - 진짜 indicator 카운트 (예상 ~109건) 검증
  - 9a/9b/9c/9e thematic target별 진짜 indicator 분포
  - Krippendorff(2019) §11 unit definition 위반 해결 여부
- [ ] **frame_distribution 5범주 활성화**:
  - justice/development 0건 → 새 분포
  - LMDC sovereignty / AOSIS justice / LDC development 분리되었는가
  - 정책학 관점에서 frame이 "의도된 정책수단 선택"의 사전 시그널인가
- [ ] **Stage 1 v1.4 prompt 검토**:
  - Howlett(2019) Ch.5 instrument calibration이 prompt에 충분히 반영되었는가
  - evidence_quote 출력이 정책수단 추론의 근거로 충분한가
  - Round 4 활성화 시 expected output 평가

### Section 2. Implementation Realization Rate (Task E) 메트릭 구체화

Round 2 §4 IRR 정의를 한국 KEI 사례로 시범 적용:

- [ ] **IRR 공식 검증**:
  ```
  IRR_i,t = (Σ_indicator W_k × Realized_k) / (Σ_indicator W_k × Promised_k)
  ```
  - W_k 정량 가중치 (정량 약속=1.0, 정성=0.5)는 reviewer가 받아들일 수 있는가
  - Realized_k 측정 정의 (NDC 갱신 + 예산 + 법령 0/0.5/1)의 ICR (inter-coder reliability) 가능성
- [ ] **한국 제3차 적응강화대책 cross-walk 매트릭스**:
  - 5대 과학기반 적응 영역 (KEI 분류) × GGA 6 핵심 영역 (UAE-Belém 9a-e)
  - 5×6 = 30 셀 매트릭스
  - 각 셀: 한국 NAP 약속 텍스트 + GGA 지표 매핑 + Promised/Realized 점수
  - 출력: `deliverables/korean_nap_gga_crosswalk.csv` + `deliverables/korean_nap_gga_crosswalk_analysis.md`
- [ ] **KEI 제3차 적응강화대책 중간 모니터링 1차 결과 (2024)**:
  - 제2차 대책(2021-2025) → 제3차 대책(2026-2030) 전환 시 약속 이행 vs 누락 분석
  - 한국 사례 IRR_2025 시범 산출 (제2차 대책 기준)
  - 정책학 학술지 (한국정책학회보 / 한국행정학보) 투고 차원에서 주요 발견 1-2 paragraph

### Section 3. Round 3 Rubric 재평가

Round 2 평점 (3.8/5) 기준으로 Round 3 진척 평가:

| Dimension | Round 2 | Round 3 | 변화 동인 (정밀화 결과 기반) |
|-----------|---------|---------|-------------------------|
| Theoretical grounding | 4.0 | ? | NATO 4축 SD 정상화 + Howlett calibration prompt 명시 |
| Methodological rigor | 3.5 | ? | TF-IDF 가중 적용 + LLM prompt v1.4 ready (호출은 Round 4) |
| Empirical validity | 4.0 | ? | indicator kind 분화 + 한국 NAP cross-walk |
| Policy strategic relevance | 3.0 | ? | KEI cross-walk + Task E 한국 사례 시범 |
| Clarity & reproducibility | 4.5 | ? | Round 3 audit trail 추가 |

목표: 평균 4.0+ (Round 4-5에서 4.5 도달).

### Section 4. 핵심 비판 (Round 3 진척 기반)

Round 3 정밀화 결과가 새 결함을 드러내는지 진단:

- [ ] **C1 (Round 3 신규 또는 잔존)**: 키워드 사전 정밀화로 4축 SD 회복했지만, 정책학 이론적 기반 (Hood NATO 분류)이 충분한가? Salamon(2002) *Tools of Government* 같은 더 정교한 분류 (subsidies, contracts, vouchers, tax expenditures, etc.) 도입이 필요한가
- [ ] **C2**: Stage 1 LLM 활성화 (Round 4) 전에 Stage 2 GAT 학습 가능한가? 현재 점수가 규칙 기반이지만 v2 (TF-IDF 가중)가 GAT 입력으로 충분한 변별력을 보유하는가
- [ ] **C3**: 한국 KEI cross-walk가 30 셀 중 결측 셀이 어느 정도일까. 결측 셀이 50% 이상이면 IRR 측정 불가 → Round 4 추가 데이터 수집 필요

### Section 5. ir-political-professor와의 합의·불일치 예측 (Round 3)

Round 2 §6 합의·불일치 항목 update:

- [ ] 합의 예상: chair_metadata N=67+ 후 인과 추론 가능성, frame_distribution 5범주 활성화의 측정 가능성
- [ ] 불일치 예상: 한국 NAP cross-walk를 IR이 "single-country case"로 약화 평가할 가능성 → 정책학 입장은 "Task E 적용의 first proof"

### Section 6. team-lead 결정 요청

- [ ] D1: Stage 1 LLM 활성화 (Round 4) 시점에 KEI cross-walk 데이터를 LLM input으로 포함할 것인가
- [ ] D2: 한국 KEI 사례를 Track A 브리핑(수업 제출용)에 어느 정도 비중으로 반영할 것인가
- [ ] D3: Salamon(2002) 정책수단 분류 도입 필요 여부

## 품질 기준

- [ ] critique 본문 ≥ 3,000자 (Round 1·2 critique 분량 유지)
- [ ] 5-Dimension Rubric 명시 점수 + 변화 동인
- [ ] 핵심 비판 Top 3 (C1 C2 C3 명시)
- [ ] Reference ≥ 5개 추가 (Round 1·2 합산 13개 + Round 3 5개 = 누적 18개)
- [ ] 한국 KEI cross-walk 매트릭스 5×6 결측셀 ≤ 30%
- [ ] IRR 공식 검증 (W_k, Realized_k 정의 명확화)

## 제공된 컨텍스트

- Round 2 critique 본인 (council_sessions/round_2/policy_science/critique.md)
- Round 2 cross-review (council_sessions/round_2/synthesis/cross_review.md)
- Round 2 quality_gates (council_sessions/round_2/synthesis/quality_gates.json)
- T02 산출물 (정밀화 후 데이터)
- 한국 KEI Working Paper 2024-08 (T01 P0 수집)

## 출력 위치

- Critique: `council_sessions/round_3/policy_science/critique.md`
- Cross-walk: `deliverables/korean_nap_gga_crosswalk.csv` + `deliverables/korean_nap_gga_crosswalk_analysis.md`
- IRR protocol: `docs/16_task_e_irr_protocol.md`
