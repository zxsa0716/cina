# Stage 1 LLM Extraction Run Plan (v1.3, Round 4 Ready)

> Round 3 종료 시 H-R3-3 (Stage 1 활성화) Heedo 결정 대기. API key 설정 후 즉시 실행 가능.
>
> **현 상태**: ANTHROPIC_API_KEY 미설정 — 실제 추출 미실행. 본 문서는 prep + 즉시 실행 가능 명령 제공.

---

## 1. 5개 High-Value 시드 문서 (calibration set 토대)

| 우선순위 | 문서 | 위치 | 이슈 | 근거 |
|---------|------|------|------|------|
| 1 | **FCCC/PA/CMA/2025/L.25E** Belém Adaptation Indicators 결정문 최종 | `data/raw/unfccc_submissions/cop30_curated/FCCC_PA_CMA_2025_L25E_final.pdf` | GGA-IND | Round 2 핵심 evidence (Authority 6.1, voluntary 언어) |
| 2 | **Brazilian Plano Clima Sumário Executivo 2024-2035** | `data/raw/round3/Brazilian_Plano_Clima/Brazil_Plano_Clima_Sumario_Executivo_2024_2035.pdf` | MIT-ADAPT, NAPs | Round 3 paradox (국내 vs 국제 instrument-mix translation) |
| 3 | **AOSIS adaptation submission 2024 data gaps** | `data/raw/round3/AOSIS_GGA_submission/AOSIS_adaptation_submission_2024_data_gaps.pdf` | GGA-IND, ADAPT-FIN | frame_type=justice 검증 (norm entrepreneurship) |
| 4 | **LMDC submission on GGA** | `data/raw/round3/LMDC_AILAC_submission/LMDC_submission_on_GGA.pdf` | GGA-IND | frame_type=sovereignty 검증 (CBDR-RC) |
| 5 | **UAE-Belém Indicators Health (9c)** | `data/raw/unfccc_submissions/cop30_curated/UAE_Belem_9c_Health.pdf` | GGA-IND health | 54 indicators 가장 풍부 (validation set) |

총 5 문서. 각 문서에서 추출 대상:
- 5 시드 × 6 이슈 = 30 (country, issue) 조합 (동일 문서 내 다중 국가 언급)
- 또는 5 시드 × 단일 핵심 이슈 = 5 records (calibration 시드)

## 2. v1.3 Prompt (실행 가능 형태)

`src/stage1_extract/extract.py` 내 `load_prompt_v1_3()` 함수로 정의 예정. 본 문서에 텍스트 사양:

### SYSTEM
```
You are a specialized climate diplomacy analyst. Extract a country's stance on a
specific climate negotiation issue from official UNFCCC documents.

Theoretical framework:
- Win-set theory (Putnam 1988, Two-Level Games)
- Within stance, distinguish: key_demands / red_lines / flexibility_signals

Beyond stance direction, classify the country's policy instruments using NATO
framework (Hood 1983; Howlett 2019):
  • nodality (information): data disclosure, scientific citation, reporting duty
  • authority: mandatory rules, treaties, regulations, enforcement
  • treasure: financial commitments, funds, taxes, incentives
  • organization: new institutions, expert groups, working bodies
For each axis, return 0-3 direct quotes from the document.

Classify the dominant frame:
  scientific | justice | sovereignty | security | development | mixed
A frame is the political narrative the country wraps the issue in.

Score salience (0-1): how much political capital the country invests.

Detect procedural authority signals:
  is_chair_role / is_co_facilitator / is_pen_holder
  drafts_text_for_issue: which issue, if any.

Analyst discipline:
1. Cite only direct quotes from the provided document. No paraphrasing in evidence.
2. If the document does not address the issue, return stance_score=0, confidence=0.
3. Use the full [-1, +1] range. Do NOT default to ±0.5.
4. If a country's statement is ambiguous, lower confidence and widen uncertainty.

Output: strict JSON. No markdown, no commentary.
```

### USER (template)
```
Country: {country}
Issue: {issue_label} — {issue_description}

Document excerpt:
=== DOC START ===
{paragraphs_joined}
=== DOC END ===
Source document ID: {doc_id}
Pre-detected procedural metadata (from refinement): {procedural_pre}

Extract the country's stance per v1.3 schema. Respond with JSON only:
{{
  "country": "...",
  "issue": "...",
  "stance_score": <number in [-1, 1]>,
  "stance_category": "<one of: strong_support, support, conditional_support, neutral_or_silent, oppose, strong_oppose>",
  "key_demands": ["..."],
  "red_lines": ["..."],
  "flexibility_signals": ["..."],
  "evidence_quotes": [{{"quote": "...", "source_doc_id": "...", "paragraph": <int>}}],
  "confidence": <number in [0, 1]>,
  "reasoning": "...",
  
  "instrument_signals": {{
    "nodality": ["..."],
    "authority": ["..."],
    "treasure": ["..."],
    "organization": ["..."]
  }},
  "frame_type": "<scientific|justice|sovereignty|security|development|mixed>",
  "frame_components": ["..."],
  "salience_score": <number in [0, 1]>,
  "salience_evidence": ["..."],
  "procedural_signals": {{
    "is_chair_role": <bool>,
    "is_co_facilitator": <bool>,
    "is_pen_holder": <bool>,
    "drafts_text_for_issue": "<issue_code or null>"
  }}
}}
```

## 3. 실행 명령 (Heedo가 API key 설정 후)

```bash
# 1. API key 설정
export ANTHROPIC_API_KEY=sk-ant-...    # bash
$env:ANTHROPIC_API_KEY="sk-ant-..."    # PowerShell

# 2. 파이프라인 실행 (Stage 1만)
python -m src.pipeline \
  --country Brazil \
  --cop 30 \
  --sector adaptation \
  --language ko \
  --raw-dir data/raw/unfccc_submissions/cop30_curated \
  --output deliverables/ \
  --stages 1

# 또는 5 시드 문서만 한정 추출 (calibration set 빌드)
python -m src.stage1_extract.run_calibration \
  --seed-docs deliverables/stage1_extraction_run_plan.md \
  --output data/processed/stances_seed_v1_3.jsonl \
  --k-samples 5 \
  --temperature 0.3
```

## 4. 예상 산출물

- `data/processed/stances_seed_v1_3.jsonl` — 5 시드 × 6 이슈 = 30 records (또는 시드당 핵심 이슈 1개 = 5 records)
- 각 record:
  - stance_score (calibrated, CI 95%)
  - instrument_signals 4축 (각 축 0-3 quotes)
  - frame_type + salience
  - procedural_signals (is_pen_holder, drafts_for)
- 비용: ~$5-8 (Opus 4.7, k=5, 5 시드, 평균 1500 input + 800 output tokens)

## 5. Calibration 후속 작업

Stage 1 시드 추출 완료 후:
1. Heedo + 1명 (가능시 지도교수)이 50 (country, issue) sample을 expert coding
2. Platt scaling MLE 추정 — 보정 함수 학습
3. CI coverage ≥ 90% 검증
4. 전체 corpus (114 documents, ~120 country-issue pairs) 추출 — 비용 ~$30-40

## 6. Round 4-5 통합 시점

- Round 4 T02 (refinement): Stage 1 LLM 가동 후 정제 결과를 v1.3 schema에 통합
- Round 4 T01 (collector): historical chair letters 추가 → procedural_signals 정확도 향상
- Round 5 (estimated): Stage 2 R-GAT 학습 시작 (chair_status + drafts_text edge 모두 활성화)

## 7. 헌법 정합

- ✓ §4 LLM-GNN-LLM 신규성 회복 — Round 1-3은 rule-based, Stage 1 LLM 가동으로 첫 LLM 단계 실증
- ✓ HEEDO-1 scope expansion — Task E 정량화 데이터 입력 가속
- ✓ 양 교수 R3 권고 직접 대응

---

**상태**: Ready (API key only). Heedo 결정 H-R3-3 대기 중.
**다음 액션**: Heedo가 `ANTHROPIC_API_KEY` 설정 + `python -m src.pipeline --stages 1` 실행
**예상 시간**: 5 시드 추출 ~10분, 전체 corpus ~1시간
**예상 비용**: 시드 ~$5-8, 전체 ~$30-40
