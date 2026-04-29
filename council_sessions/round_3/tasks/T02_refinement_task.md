---
assigned_to: data-refinement-analyst
round: 3
priority: P0
depends_on:
  - council_sessions/round_3/tasks/T01_collector_task.md (T01 P0 outputs)
  - council_sessions/round_2/synthesis/cross_review.md (CR3.2, CR3.3, CR3.4, CR3.8)
  - council_sessions/round_2/policy_science/critique.md (C1 indicator noise, C3 4축 변별력)
  - council_sessions/round_2/ir_political/critique.md (C2.2 frame_type justice/development)
inputs:
  - data/processed/documents.jsonl (87 docs)
  - data/processed/uae_belem_indicators.jsonl (149 indicators — 31% noise)
  - data/processed/ndc_adaptation_sections.jsonl (39)
  - data/processed/chair_metadata.jsonl (17)
  - data/processed/extraction_targets.jsonl (298)
  - data/processed/refinement_round2_stats.json
  - docs/14_schema_v1_3_changes.md (Stage 1 prompt v1.3 spec)
  - docs/15_stage2_features_v2.md
deadline: T01 완료 후 24h target
---

# T02 — Refinement Round 3

## 목적

Round 2에서 발견된 결정적 결함 4건을 정제 단계에서 잡는다: (a) NATO 4축 변별력 부족(SD 0.36), (b) frame_type justice/development 0건, (c) 149 indicator 31% 노이즈, (d) Stage 1 LLM 미가동 (모든 점수가 규칙 기반). 동시에 Round 3 신규 수집물 (~63 docs)을 schema v1.3로 정제한다.

## 구체 산출물

### P0-A. 149 indicator 노이즈 정제 — `kind` 필드 분화 (CR3.3)

`uae_belem_indicators.jsonl` 정제:

- [ ] **`kind` 필드 추가**: `indicator | toc | header | metadata | misc`
- [ ] 자동 라벨링 규칙:
  - seq < 14 AND text contains `....` (줄임표) AND text length < 150 → `kind=toc`
  - text matches `^(Introduction|Definition|Annex|Table|Figure|Box \d+)` → `kind=header`
  - text contains "Page" or matches `\d+\s*$` (페이지 번호) → `kind=metadata`
  - text length > 200 AND contains 정량 지표 키워드 (e.g., "%", "by 2030", "indicator", "target", "baseline") → `kind=indicator`
  - 기타 → `kind=misc`
- [ ] 수정 후 indicator 진짜 카운트 재산출 (Policy 교수 §3 C1 추정: 9a ~28건, 9b ~35건, 9c ~40건, 9e ~6건 → 총 ~109건 진짜 indicator)
- [ ] 출력: `data/processed/uae_belem_indicators.jsonl` v2 (kind 필드 포함) + `data/processed/uae_belem_indicators_clean.jsonl` (kind=indicator만)
- [ ] 통계: `kind` 분포 + 진짜 indicator 카운트를 `refinement_round3_stats.json`에 기록

### P0-B. NATO 4축 discriminating keyword + TF-IDF (CR3.4)

현재 키워드 사전 정밀화 (Howlett 2019 Ch.5 기반):

- [ ] **현재 사전 광범위 매칭 진단**:
  - "report", "data", "information" → 거의 모든 UNFCCC 문서 매칭 (Nodality 인플레)
  - 진단 로그: `council_sessions/round_3/refinement/keyword_inflation_audit.md`
- [ ] **discriminating keyword 선별** (Hood 2007 + Howlett 2019 calibration):
  - **Nodality (정보)**: "voluntary reporting", "context-specific information", "biennial transparency report", "stocktake", "synthesis report" (단순 "report" 제외)
  - **Authority (규범/권위)**: "shall", "decides", "binding", "obligation", "compliance committee", "facilitative dialogue" (단순 "may" 제외)
  - **Treasure (재원)**: "GCF replenishment", "GEF allocation", "concessional finance", "loss and damage fund", "adaptation finance" (단순 "support" 제외)
  - **Organization (조직)**: "subsidiary body", "committee mandate", "constituted body", "expert group" (단순 "body" 제외)
- [ ] **TF-IDF 가중**: corpus 87 docs 대상 TF-IDF 산출, 일반어(IDF<2.0) penalty
- [ ] **새 점수 산출 후 재분포**:
  - 표준편차 검증: Nodality SD ≥ 0.6 (현재 0.36) 목표
  - 6 issue × 4 instrument 매트릭스 재산출
  - GGA-IND Authority 점수 재산출 (현재 6.1 — discriminating 사전 적용 시 더 분리될 가능성)
- [ ] 출력: `data/processed/instrument_signals_v2.jsonl` (per-doc 4축 점수 + TF-IDF 가중 + evidence_quote 후보)
- [ ] 통계: `refinement_round3_stats.json`의 `instrument_totals_v2` + `instrument_by_issue_v2` 매트릭스

### P0-C. frame_type 5범주 모두 활성화 — rhetorical signature (CR3.2)

현재 frame_distribution: `mixed 24, sovereignty 5, scientific 51, justice 0, development 0`. 두 카테고리 0건 해결:

- [ ] **justice frame keyword expansion** (IR 교수 §3 C2.2 기반):
  - "equity", "CBDR-RC", "common but differentiated", "historical responsibility", "polluter pays", "fair share", "loss and damage", "climate-vulnerable", "1.5 to stay alive", "right to development" (justice 맥락)
  - rhetorical signature: "those least responsible", "front lines of climate", "moral obligation"
- [ ] **development frame keyword expansion**:
  - "right to development", "development space", "policy space", "domestic priorities", "poverty eradication", "sustainable development priorities"
  - rhetorical signature: "developmental needs", "national circumstances and capabilities", "common but differentiated responsibilities and respective capabilities" (LMDC sovereignty와 분리: development는 G77+China/LDC 맥락)
- [ ] **재추출 후 그룹별 frame distribution table**:
  - (group × frame) contingency table — group: BASIC, LMDC, AOSIS, AILAC, LDC, EIG, Umbrella, EU, HAC, African, Arab, Amazon
  - Pearson χ² test 보고
  - 출력: `data/processed/frame_by_group.csv` + `refinement_round3_stats.json`
- [ ] 검증 기준:
  - AOSIS frame_type = justice 또는 mixed(justice 우세) 비율 ≥ 60%
  - LDC frame_type = development 또는 justice 비율 ≥ 50%
  - LMDC frame_type = sovereignty 우세
  - 위 3개 모두 만족 → IR 교수 §5.2 검증 완료

### P0-D. Stage 1 LLM 활성화 prep (CR3.8 + Round 4 P0)

Round 4 P0 활성화를 위한 prep:

- [ ] **ANTHROPIC_API_KEY 환경 변수 점검** (점검만, 호출 안 함)
- [ ] **Stage 1 prompt v1.4 작성**:
  - Hood NATO 4축 + frame_type 5범주 + salience_score + procedural_signals 모두 evidence_quote 출력
  - rhetorical signature instruction (justice/development 분리 명시)
  - discriminating keyword 사전을 prompt context에 포함
  - JSON schema strict mode
  - seed = 42 (재현성)
  - temperature = 0.0
  - 출력: `src/stage1/prompts/v1_4_extraction.md`
- [ ] **extraction_targets.jsonl 우선순위 부여**:
  - 현재 298 targets → priority 1 (highest-value 5 docs), priority 2 (~30 docs), priority 3 (나머지)
  - priority 1 5 docs:
    1. FCCC/PA/CMA/2025/L.25E_final (`cop30_curated-f569...` — GGA 최종 결정문)
    2. AOSIS submission 1건 (Round 3 수집 후 highest-priority)
    3. LMDC submission 1건 (Round 3 수집 후 highest-priority)
    4. Plano Clima Sumário Executivo (`brazilian_gov-...`)
    5. ENB COP30 summary (`enb_curated-...`)
  - 출력: `data/processed/extraction_targets.jsonl` v2 (priority 필드 추가)
- [ ] **비용 추정**: 5 docs × ~50K input tokens × $3/MTok + ~10K output × $15/MTok ≈ **$5-10/trial**
- [ ] **거버넌스 노트**: Heedo HEEDO-4 결정 필요 (Round 2 LEAD_REPORT에 명시)

### P0-E. 신규 Round 3 수집물 정제 (~63 docs)

T01 P0 산출물 schema v1.3 정제:

- [ ] **Historical presidency letters 50건**: chair_metadata 자동 검출 → 17 → **목표 67+**
  - `is_pen_holder=True` 자동 라벨 (procedural_phrases 포함 시)
  - `chair_country` (Fabius FRA, Sharma GBR, Al Jaber ARE, Babayev AZE, etc.) 부착
  - `co_facilitator` 자동 검출
  - `host_session` (cop21~cop29) 부착
- [ ] **Realist baseline 4 dataset**: country_features 32-dim → 36-dim 확장
  - `gdp_log_2024`, `co2_cum_log_1850_2024`, `milex_pct_gdp_2024`, `alliance_count_cow`
  - 출력: `data/processed/country_features_v2.csv` (CINA 20국)
- [ ] **Korean MOE NAP + KEI Working Paper**: documents.jsonl에 추가
  - 한국어 paragraph extraction
  - 정책 수단 (NATO 4축) Korean keyword 사전 적용

### P1-A. JT-ADAPT 비국가 행위자 노드 정제 (CR3.5)

T01 P1-A 산출물 처리:

- [ ] documents.jsonl에 비국가 행위자 entity (COICA, APIB, ITUC, CAN, WWF) 노드 추가
- [ ] 새 필드: `actor_type` ∈ `state | non_state | indigenous | union | ngo | igo`
- [ ] JT-ADAPT 이슈에서 비국가 행위자 frame_type 분포 산출

### P1-B. SAU/AOSIS/LMDC formal submission 정제

T01 P1-B 산출물 처리:

- [ ] manifest entry → documents.jsonl 정제
- [ ] group_frequency 업데이트 (LMDC 2 → ?, SAU under-detected 보강)

## 품질 기준

- [ ] schema_pass_rate ≥ 95% (Round 2 95.2% 유지/향상)
- [ ] documents.jsonl 87 → **목표 150+**
- [ ] uae_belem_indicators v2: kind 분포 명시, kind=indicator만 진짜 카운트 보고
- [ ] frame_distribution: 5범주 모두 nonzero (justice ≥ 5, development ≥ 5)
- [ ] instrument_signals: Nodality SD ≥ 0.6
- [ ] chair_metadata: 17 → 67+
- [ ] country_features: 32-dim → 36-dim
- [ ] processing_version: `round3-v1.4-prep` (Stage 1 LLM 미가동, prompt v1.4 정의됨)
- [ ] audit trail: 모든 변환 단계 로그 + rejected_reasons 명시

## 제공된 컨텍스트

- Round 2 cross-review CR3.2~CR3.4, CR3.8 (council_sessions/round_2/synthesis/cross_review.md)
- Policy 교수 §3 C1 (149 indicator 31% 노이즈 진단), §3 C3 (Nodality SD 0.36)
- IR 교수 §3 C2.2 (frame_type justice/development 0건), §5.2 (그룹별 frame contingency)
- 기존 schema v1.3 spec (docs/14_schema_v1_3_changes.md)

## 출력 위치

- Processed data: `data/processed/{documents,uae_belem_indicators,instrument_signals_v2,frame_by_group,country_features_v2}.{jsonl,csv}`
- 통계: `data/processed/refinement_round3_stats.json`
- Prompt: `src/stage1/prompts/v1_4_extraction.md`
- Audit: `council_sessions/round_3/refinement/keyword_inflation_audit.md`
- 교수 input pack:
  - `council_sessions/round_3/refinement/professor_input/policy_sci_pack_round3.md`
  - `council_sessions/round_3/refinement/professor_input/ir_pack_round3.md`

## 예상 시간

- P0-A indicator kind 분화: 2h (rule-based)
- P0-B NATO 4축 정밀화: 4h (사전 작성 + TF-IDF 산출 + 재점수)
- P0-C frame_type rhetorical signature: 3h
- P0-D LLM prep (호출 없음): 2h
- P0-E 신규 정제: 4h
- P1: 3h
- 총 ~18h (T01 완료 후 24h 내 가능)
