# 14. Schema v1.3 — Stage 1 Stance Schema 확장

> Round 1 두 교수 critique 결정적 권고(CR1) 반영. Stage 1 추출 스키마에 정책수단·프레임·현저성·절차권 4축을 추가한다.
>
> **결정**: Heedo 2026-04-25 accept. 적용 시점: Round 2 prompt v1.3.

---

## 1. 추가 필드 4축

### 1.1 `instrument_signals` (정책수단 — Policy-Sci 권고)
NATO 프레임 (Hood 1983; Howlett 2019) 기반 정부 자원 4축:

```json
"instrument_signals": {
  "nodality": ["...evidence quote..."],         // 정보 자원: 데이터 공개·과학 인용·보고 의무
  "authority": ["...evidence quote..."],        // 권한 자원: 의무화·조약·규제·강제력
  "treasure": ["...evidence quote..."],         // 재정 자원: 재원 약속·기금 기여·세제·인센티브
  "organization": ["...evidence quote..."]      // 조직 자원: 신규 기관·전문가 그룹·실무 조직
}
```

각 배열에 0~3개 evidence quote. 단일 stance 내 동일 quote가 여러 축에 등장할 수 있다 (다중 수단 사용 시).

**Why**: 단순 "지지/반대"는 정책 binding force를 평가하지 못함. NATO 분류로 어떤 수단이 약속됐는지 가시화하면, 합의 텍스트의 de facto 강도를 평가할 수 있다 (예: "voluntary, non-prescriptive" Belém Indicators는 nodality만 있고 authority·treasure 부재 → binding force 약함).

### 1.2 `frame_type` (프레이밍 — IR 권고)
협상자가 이슈를 어떤 정치 서사 안에 묶는가:

```json
"frame_type": "scientific" | "justice" | "sovereignty" | "security" | "development" | "mixed"
```

- `scientific`: IPCC 인용·기술적 임계값·과학 합의 강조
- `justice`: 역사적 책임·차별화·도덕적 권위 (AOSIS, LDC 전형)
- `sovereignty`: 국가 능력 맥락·자발성·red line (LMDC 전형)
- `security`: 국가안보·안정·위협 프레임 (소수 사례)
- `development`: 빈곤·산업화·발전권·MoI (BASIC, G77 일반)
- `mixed`: 두 개 이상 동시 (혼성 프레임)

**Why**: 동일 스탠스 점수라도 framing이 다르면 동맹 가능성·brokerage 위치가 다르다. Stage 2 GAT가 frame embedding을 동시 학습하면 Hochstetler & Milkoreit 2014 *Politics & Policy* 가 보고한 framing-coalition co-evolution을 포착 가능.

### 1.3 `salience_score` ∈ [0, 1] (현저성 — IR 권고)
국가가 이슈에 얼마나 정치적 자원을 투입하는가:

```json
"salience_score": 0.85,
"salience_evidence": ["repeated mention", "minister-level statement", "prepared text dedicated paragraph"]
```

지표:
- 텍스트 비중 (해당 이슈에 할애된 단락 수)
- 발언 단위 (장관·기후대사·실무자 — 최고위 = 1.0)
- 입장 변화 (이전 회기 대비 강도 변화)

**Why**: stance_score는 방향, salience는 강도. 두 차원 분리가 spatial voting 모델 (Mas-Colell et al.) 과 정합. 현저성 없는 강한 스탠스는 cheap talk일 수 있다.

### 1.4 `procedural_signals` (절차권 — IR P0 권고)
의장국·co-facilitator 식별을 위한 절차적 권한 시그널:

```json
"procedural_signals": {
  "is_chair_role": false,
  "is_co_facilitator": false,
  "is_pen_holder": false,        // 텍스트 초안 작성 권한
  "drafts_text_for_issue": null  // 어느 이슈에 대해 초안 작성?
}
```

Round 2 정제 단계에서 SBI/SBSTA L-document 메타데이터 (의장단 letter, draft conclusions) 와 cross-reference하여 자동 채움.

**Why**: Belém Adaptation Indicators "Rube Goldberg" 사건의 핵심 메커니즘은 의장국 브라질의 procedural authority. 이 변수 없이는 epistemic_divergence_score가 인과 메커니즘을 설명 못함 (IR 교수 결정적 비판).

---

## 2. 전체 v1.3 스키마

```json
{
  "stance_id": "...",
  "country": "Brazil",
  "iso3": "BRA",
  "issue": "GGA-IND",
  "issue_description": "...",
  "cop_session": "COP30",
  "date_context": "2025-11-10",

  // v1.2 — 그대로 유지
  "stance_score_raw_samples": [...],
  "stance_score_mean": 0.65,
  "stance_score_std": 0.05,
  "stance_score_calibrated": 0.58,
  "ci_lower_95": 0.48,
  "ci_upper_95": 0.74,
  "stance_category": "conditional_support",
  "key_demands": [...],
  "red_lines": [...],
  "flexibility_signals": [...],
  "evidence_quotes": [...],
  "epistemic_alignment": {...},

  // v1.3 — NEW
  "instrument_signals": {
    "nodality": [...],
    "authority": [...],
    "treasure": [...],
    "organization": [...]
  },
  "frame_type": "mixed",
  "frame_components": ["scientific", "development"],
  "salience_score": 0.85,
  "salience_evidence": [...],
  "procedural_signals": {
    "is_chair_role": true,
    "is_co_facilitator": false,
    "is_pen_holder": true,
    "drafts_text_for_issue": "GGA-IND"
  },

  "extraction_metadata": {
    ...,
    "prompt_version": "v1.3"  // ← 변경
  }
}
```

---

## 3. 프롬프트 v1.3 변경점

`docs/04_stage1_stance_extraction.md §2` 의 SYSTEM 프롬프트에 다음 단락 추가:

```
Beyond stance direction (key_demands/red_lines/flexibility_signals), classify the
country's policy instruments using NATO framework (Hood 1983; Howlett 2019):
  • nodality (information): data disclosure, scientific citation, reporting duty
  • authority: mandatory rules, treaties, regulations, enforcement
  • treasure: financial commitments, funds, taxes, incentives
  • organization: new institutions, expert groups, working bodies
For each axis, return 0-3 direct quotes from the document. A single quote may
appear in multiple axes if it invokes multiple instruments.

Classify the dominant frame:
  scientific | justice | sovereignty | security | development | mixed
A frame is the political narrative the country wraps the issue in.

Score salience (0-1): how much political capital the country invests.
Use: paragraph share, speaker level, dedicated text, vs cheap talk.

Detect procedural authority signals:
  is_chair_role / is_co_facilitator / is_pen_holder (drafts text)
  drafts_text_for_issue: which issue, if any, the country drafts text for.
These are observable from L-document headers, presidency letters, and
co-facilitator announcements.
```

---

## 4. 영향 범위

| 영역 | 변경 |
|------|------|
| `src/schemas.py` | `Stance` 모델 4 필드 추가 |
| `src/stage1_extract/extract.py` | `load_prompt_v1_3()` 함수 추가, schema validation 강화 |
| `src/data/identifiers.py` | `FRAME_TYPES` 상수 추가 |
| `data/processed/documents.jsonl` | refinement v2 단계에서 procedural metadata 사전 채움 |
| `docs/04_stage1_stance_extraction.md` | v1.3 prompt 텍스트 업데이트 |
| `docs/05_stage2_graph_analysis.md` | country_features에 chair_status 추가 (별도 문서 15) |

---

## 5. 평가 방법론 변경 (Task E 신설)

`docs/07_evaluation_protocol.md` 에 Task E (Implementation Realization Rate) 추가:

> COP 합의 (예: Belém Adaptation Indicators) 채택 24개월 후, 합의문이 약속한 정책수단(instrument_signals)이 실제 국가 NDC 또는 NAP 업데이트에 반영되었는지 측정.
> CINA Stage 1이 추출한 instrument_signals와 사후 NDC/NAP를 비교 → realization rate ∈ [0, 1].
> 이 task는 Heedo 헌법 §1 (논문감) 강화에 결정적: 정책학회 reviewer가 "AI가 협상을 분석하는 건 봤다, 실제 정책 결과까지 예측하나?" 질문에 답.

---

## 6. 변경 이력

- 2026-04-25: v1.3 초안 작성. Heedo 결정 HEEDO-1 accept 후 시행. Round 2 prompt 적용 예정.
