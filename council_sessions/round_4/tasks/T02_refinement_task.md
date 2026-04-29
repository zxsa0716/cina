---
task_id: T02-Round4
assigned_to: data-refinement-analyst
agent_model: sonnet
round: 4
priority: P0 (L.25 cosine + KOR cross-walk + IRR + realist B0 + Stage 1 LLM trial) + P1 (headline 3-way + mixed composition + NDC chair_role 수정)
depends_on:
  - T01 Round 4 산출물 (chair letters 12+, KOR MOE PDF, realist 4 datasets, NSA 8+ entity, placeholder 4 재수집)
  - council_sessions/round_3/synthesis/cross_review.md (§6 Round 4 핵심 방향)
  - council_sessions/round_3/policy_science/critique.md §4 (KOR cross-walk 5×6 매트릭스), §1.2 (headline_indicator 3-way)
  - council_sessions/round_3/ir_political/critique.md §1 (Tallberg 4 채널), §4.3 (mixed composition), §9 D2 (realist B0 F1)
  - council_sessions/round_3/policy_science/critique.md §1.1 (NDC `is_chair_role=true` 라벨 오류)
  - data/processed/refinement_round3_stats.json
  - Heedo 결정 H-R3-3 (Stage 1 LLM 사전 승인)
deadline: T01 완료 후 48시간
---

# T02 Round 4 — data-refinement-analyst 작업 지시

## 0. 목적

T01 Round 4 신규 데이터 (chair letters 12+ / KOR MOE PDF / realist 4 datasets / NSA 8+ entity / placeholder 4)를 정제하여 documents.jsonl + chair_metadata.jsonl 확장 + country_features_v2.csv 통합. 동시에 Round 3 잔존 결함 5건 (L.25 cosine 미산출 / KOR cross-walk 부재 / IRR 미산출 / Stage 1 LLM 미가동 / NDC chair_role 라벨 오류) 모두 처리.

## 1. 산출물 (Deliverables)

### 1.1 P0 — L.25 advance→final sBERT cosine diff (양교수 공통 P0, Tallberg formula control 첫 정량 검증)

**입력**:
- `data/processed/documents.jsonl` 중 `FCCC/PA/CMA/2025/L.25` 관련 문서 (advance + final 2개 버전 분리 추출)
- 만약 advance 버전이 없으면 cop30_curated 또는 round4_curated에서 `cma2025_07a01a_advance.pdf`/`L25_advance.pdf` 식별

**처리**:
1. paragraph-level 분할 (각 paragraph ID 부여)
2. sBERT (`sentence-transformers/all-MiniLM-L6-v2` 또는 `paraphrase-multilingual-MiniLM-L12-v2`) embedding 산출
3. paragraph alignment (advance vs final) — fuzzy match via cosine similarity > 0.7 threshold
4. 매칭된 paragraph pair에 cosine_similarity 산출
5. Top-N (가장 변화 큰 10 paragraph) 식별 + 텍스트 diff 추출

**산출물**:
- `data/processed/L25_drafting_diff.jsonl` (paragraph_id, advance_text, final_text, cosine_sim, change_magnitude, frame_advance, frame_final)
- `docs/research_logs/L25_drafting_diff.md` — 분석 로그 (top-10 변경 paragraph 인용 + Tallberg formula control 해석)
- 통계: 평균 cosine sim, 변화율 분포, frame_type 변환 사례 (예: justice → mixed)

**검증**: IR critique §1.1 "(ii) formula control 채널 검증" — chair가 advance에서 final로 paragraph를 어떻게 수정했는가의 첫 정량 evidence.

### 1.2 P0 — `deliverables/korean_nap_gga_crosswalk.csv` (5×6 매트릭스)

**입력**:
- T01 Round 4 KOR MOE 적응대책 PDF 본문
- KEI 정책보고서 2024-04 (한국 5대 영역 분류 표준)
- `data/processed/uae_belem_indicators.jsonl` (110 records, 9a-e 분류)

**스키마** (Policy critique §4):

| 한국 영역 \ GGA | 9a Water | 9b Food | 9c Health | 9d Eco | 9e Infra | Cross-cut |
|---|---|---|---|---|---|---|
| 1. 물관리 | ●HIGH | ◐MED | ○LOW | ◐MED | ◐MED | ◐MED |
| 2. 산림·생태계 | ◐MED | ◐MED | ○LOW | ●HIGH | ○LOW | ◐MED |
| 3. 농수산 | ◐MED | ●HIGH | ○LOW | ◐MED | ○LOW | ◐MED |
| 4. 보건 | ○LOW | ○LOW | ●HIGH | ○LOW | ○LOW | ◐MED |
| 5. 산업·인프라 | ◐MED | ○LOW | ○LOW | ○LOW | ●HIGH | ◐MED |

**산출물**:
- `deliverables/korean_nap_gga_crosswalk.csv` (실제 한국 적응대책 본문에서 evidence quote 인용 + 30 셀 모두 채움)
- evidence_traceability JSON: 각 셀의 ●/◐/○ 판정 근거 paragraph 인용
- T03 Policy 교수에게 검증 요청

**왜 P0**: Track A 가속 + 한국 첫 NAP IRR 정량화 사례 (KEI/KIEP 미산출 영역) + Policy critique 4.08 → 4.20 결정 dimension.

### 1.3 P0 — IRR_Korea_2025 시범 정량화

**입력**:
- 1.2 산출 cross-walk
- KEI WP 2024-08 (제2차 적응대책 92개 세부과제 모니터링)

**공식**:
```
IRR_Korea_2025 = Σ_(k in 한국 5영역) [W_k × Realized_k] / Σ_(k) [W_k × Promised_k]

Promised_k: 제2차 적응대책 (2021-2025) 92개 세부과제
Realized_k: 2024 중간 모니터링 1차 결과 (정량 0.5-1.0, 정성 0.0-0.5)
W_k: cross-walk 셀 가중치 (●HIGH=1.0, ◐MED=0.6, ○LOW=0.3)
```

**산출물**:
- `data/processed/IRR_Korea_2025.json` (영역별 분자/분모, 최종 IRR, 신뢰구간)
- 예상 결과: IRR ≈ 0.62-0.68
- T03 Policy 교수 검증 요청

### 1.4 P0 — Realist baseline B0 country_features_v2.csv 통합 + F1 측정

**입력**: T01 Round 4 4 datasets (WB GDP, SIPRI MILEX, COW alliances, OWID CO2)

**처리**:
1. ISO3 join — CINA 20국 + AOSIS·LDC = 36+ 국가
2. 4 features 생성:
   - GDP_pc (USD, 2024)
   - MILEX_pct_GDP (2024)
   - alliance_count (2012 cutoff)
   - CO2_cumulative_per_capita (1850-2024, OWID)
3. 결측 imputation (median by group: AOSIS / LDC / G77 / Annex I)
4. country_features_v2.csv 산출

**B0 단독 F1 측정** (IR critique §9 D2):
- target task: stance prediction (해당 국가가 GGA-IND voluntary vs binding 지지하는가)
- baseline: Logistic Regression 4 features만
- ground truth: chair_metadata + party_submission frame_type
- Round 3 corpus 80% train + 20% test, 5-fold CV
- 기록: F1 macro, F1 weighted, ROC-AUC, confusion matrix

**3 시나리오 Discussion 대응**:
- F1 < 80%: CINA novelty 강화 — "realist 단독으로는 stance 설명 부족"
- F1 80-90%: incremental 위치 — "CINA가 +N pp 추가"
- F1 ≥ 90%: Drezner (2007) "power asymmetry explains all" 가설 → Discussion 재구성

**산출물**:
- `data/processed/country_features_v2.csv`
- `data/processed/realist_b0_eval.json` (F1 + 3 시나리오 대응 권고)

### 1.5 P0 — Stage 1 LLM trial run (CR3.6 H-R3-3 accept)

**Heedo 사전 승인**: ANTHROPIC_API_KEY 설정 + prompt v1.4 + 5건 highest-priority docs trial.

**5건 highest-priority docs**:
1. L.25 final (FCCC/PA/CMA/2025/L.25)
2. AOSIS_SCF (round3_curated-87e79f4af3e3)
3. LMDC_GGA (round3_curated-cfdd2faec536)
4. Brazil Plano Clima Sumário Executivo (round3_curated-8a2f2dbfb372)
5. ENB COP30 daily report (가장 긴 paragraph 포함)

**Stage 1 prompt v1.4** (`docs/14_schema_v1_3_changes.md` 기반 + LLM evidence_quote 강화):
- 입력: paragraph
- 출력: stance_dict (NATO 4축 + frame_type + salience + procedural + evidence_quote)
- temperature: 0.0 (재현성)
- seed: 42
- 모델: claude-3-5-sonnet (or claude-opus-4 if approved)

**산출물**:
- `data/processed/stage1_llm_trial_5docs.jsonl` (paragraph-level stance + evidence_quote)
- `data/processed/stage1_llm_trial_stats.json` (paragraph 처리 수, 평균 evidence_quote 길이, frame_type 분포 vs rule-based)
- `docs/research_logs/stage1_llm_trial_round4.md` — 분석 로그 + rule-based vs LLM 일치율 (Cohen κ)
- 비용 보고: 실제 API 호출 비용 ($)

**검증**: rule-based 분류와의 Cohen κ ≥ 0.6이면 일치 양호. 미달 시 prompt 수정 권고.

### 1.6 P1 — headline_indicator 3-way 재분류 + ICR Cohen κ ≥ 0.7 (Policy §1.2)

**입력**: `data/processed/uae_belem_indicators.jsonl` 110 records 중 headline_indicator 83건

**3 sub-kind**:
- `substantive_indicator`: 실제 측정 대상 (예: "Significantly reducing climate-induced water scarcity")
- `procedural_header`: 보고서 섹션 헤더 (예: "Recommendations for next steps after SB62")
- `table_label`: 표 라벨 (예: "directly relevant |")

**처리**:
1. LLM v1.4로 9a Water 41건 시범 재분류 (Stage 1 LLM trial과 동일 API 사용)
2. 외부 코더 (모의: 두 번째 LLM run with different temperature 0.3) 30건 무작위 더블 코딩
3. Cohen κ 산출 (target ≥ 0.7)

**산출물**:
- `data/processed/uae_belem_indicators_v2.jsonl` (3-way kind 재분류)
- `data/processed/icr_cohen_kappa_round4.json`
- 9a Water 결과를 9b/9c/9d/9e에 확장 적용 (Round 5)

### 1.7 P1 — mixed frame 37건 internal composition (IR §4.3)

**처리**: mixed로 분류된 37건 각각에 component breakdown 산출 (예: justice 60% + sovereignty 40%)

**산출물**:
- `data/processed/mixed_frame_composition.jsonl` (doc_id, mixed_components: {justice: 0.6, sovereignty: 0.4, ...})
- 통계: 평균 component count, brokerage 가설 vs 노이즈 가설 분리 evidence

### 1.8 P1 — NDC chair_role 라벨 오류 수정 (Policy §1.1)

**문제**: `chair_metadata.jsonl` NDC 50건 중 `presidency_country` null인데 `is_chair_role=true`로 라벨링된 건 다수 존재

**처리**: NDC 문서는 일괄 `is_chair_role=false` 또는 `null`로 회귀, 의장국 라벨은 cop30_curated/round4_curated의 actual chair_communication에 한정

**산출물**:
- `data/processed/chair_metadata.jsonl` 수정 (Round 4 v1.5)
- 통계: 라벨 수정 전후 분포 비교

### 1.9 신규 manifest + collector_feedback

**처리**: T01 신규 50+건 정제 → documents.jsonl 확장
- target: 114 → **160+** (T01 +52, 일부 reject 가능)
- 신규 chair_metadata 12+건 통합 → 80+

**산출물**:
- `data/processed/documents.jsonl` 확장
- `data/processed/refinement_round4_stats.json` (cr4_compliance 블록 포함)
- `council_sessions/round_4/refinement/REPORT.md`
- `council_sessions/round_4/refinement/collector_feedback_round4.md` (Round 5 권고)
- `council_sessions/round_4/refinement/professor_input/{policy_sci, ir}_pack_round4.md`

## 2. 품질 기준 (Acceptance Criteria)

- [ ] documents.jsonl 114 → 160+ records
- [ ] chair_metadata.jsonl 32 → 80+ records, COP_coverage ≥ 10
- [ ] L25_drafting_diff.jsonl 산출 (top-10 paragraph 변경 식별)
- [ ] korean_nap_gga_crosswalk.csv 30 셀 모두 채움 + evidence_traceability
- [ ] IRR_Korea_2025.json 산출 (예상 0.62-0.68)
- [ ] country_features_v2.csv 산출 + realist B0 F1 측정 보고
- [ ] stage1_llm_trial_5docs.jsonl 산출 (5건 trial run, Cohen κ vs rule-based 보고)
- [ ] uae_belem_indicators_v2.jsonl (9a Water 41건 3-way 재분류 + Cohen κ ≥ 0.7)
- [ ] mixed_frame_composition.jsonl 37건 component breakdown
- [ ] chair_metadata NDC 라벨 수정 후 정합성 회복

## 3. 제공된 컨텍스트

### 3.1 Round 3 산출물
- `data/processed/refinement_round3_stats.json` — cr3_compliance 5/5 met
- `data/processed/uae_belem_indicators.jsonl` — 110 records (kind 분화 완료)
- `data/processed/chair_metadata.jsonl` — 32 records (NDC 라벨 오류 잔존)
- `data/processed/non_state_actor_signals.jsonl` — 20 records / 4 entity

### 3.2 Heedo 결정
- H-R3-1 Task E IRR accept → docs/07 §11 신설 + IRR_Korea_2025 시범 산출 (1.3)
- H-R3-2 비국가 행위자 JT-ADAPT 한정 accept → mixed_frame_composition (1.7)
- H-R3-3 Stage 1 LLM 사전 승인 → ANTHROPIC_API_KEY 설정 후 5건 trial (1.5)

### 3.3 양 교수 critique 핵심 잔존 우려
- Policy §1.1: NDC 50건 chair_role 라벨 오류 (Round 4 즉시 수정)
- Policy §1.2: headline_indicator 내부 false-positive 20-30% (3-way 재분류)
- IR §9 D2: realist B0 F1 ≥ 90% 시 CINA novelty 위협 (즉시 검증)
- IR §9 D3: L.25 cosine diff (4시간 작업, 즉시 산출)
- IR §4.3: mixed frame 37건 component breakdown

## 4. 보고

### 4.1 형식
`council_sessions/round_4/refinement/REPORT.md`:
- 1.1~1.9 각 산출물별 결과 요약
- cr4_compliance 블록
- 새 gap (Round 5 권고)

### 4.2 인계
- T03 Policy 교수에게: korean_nap_gga_crosswalk.csv + IRR_Korea_2025.json
- T04 IR 교수에게: chair_metadata 80+ + L25_drafting_diff + realist_b0_eval

---

*— team-lead, 2026-04-26*
