---
name: briefing-composer
description: Stage 2 분석 결과를 장관급 전략 브리핑으로 변환. 고정 템플릿(docs/09) 따라 섹션별 LLM 생성. 모든 claim에 텍스트 인용과 구조적 근거를 강제하는 Graph-Grounded Generation. Stage 3 담당.
---

# Briefing Composer Skill

## 언제 이 skill을 호출하는가

- "브리핑 써줘"
- "장관 보고서 생성"
- "최종 문서 작성"
- `cina-orchestrator`가 Phase D에서 자동 위임

## 입력·출력

### Input
- `data/processed/graph_analysis.json` — Stage 2 출력
- `data/processed/stances.jsonl` — evidence quotes 원천
- Config:
```yaml
focal_country: "Brazil"
cop: 30
sector: "adaptation"
language: "ko"   # or "en"
template_path: "docs/09_ministerial_briefing_template.md"
max_words_per_section: 600
temperature: 0.2
```

### Output
- `deliverables/ministerial_briefing.md` (한국어)
- `deliverables/ministerial_briefing_en.md` (영어, 언어별 실행)
- `deliverables/evidence_table.csv`
- `deliverables/briefing_metadata.json`

## 작업 절차

### 1. 템플릿 파싱
`docs/09_ministerial_briefing_template.md` 의 섹션 구조를 AST로 파싱:
- §1 Situation
- §2 Coalition Map
- §3 Leverage
- §4 Package Deals
- §5 Red Lines & Risks
- §6 Recommendations
- §7 Scenarios

### 2. Analysis → Section 매핑
각 섹션마다 필요한 분석 필드 추출:
```python
section_inputs = {
    "§1": {"stances_focal": filter_stances(focal=focal_country)},
    "§2": {"communities": analysis["issue_communities"]},
    "§3": {"bridge": analysis["bridge_countries"], "centrality": analysis["centralities"]},
    "§4": {"hyperedges": analysis["cross_issue_hyperedges"]},
    "§5": {"divergence": analysis["epistemic_divergence"], "red_lines": extract_red_lines(focal)},
    "§6": {"all": analysis, "focal": focal_country},
    "§7": {"all": analysis, "scenarios_model": compute_scenarios(analysis)},
}
```

### 3. 섹션별 LLM 생성
각 섹션에 대해:
1. `docs/06_stage3_briefing_generation.md §3.1` 프롬프트 사용
2. evidence_quotes를 context로 제공 (시맨틱 관련 top-K만)
3. JSON 출력: {content: "...", citations: [...]}
4. 생성 후 `evidence-validator` skill 호출

### 4. Evidence Verification Loop
```python
for section in sections:
    for attempt in range(3):
        draft = generate_section(section)
        unverified = evidence_validator.check(draft)
        if not unverified:
            break
        else:
            prompt += f"\nPrevious draft had unverified claims: {unverified}. Regenerate."
    if unverified:
        # 최후 수단: 해당 claim 제거
        draft = remove_unverified_claims(draft, unverified)
        log_warning(section, unverified)
```

### 5. Executive Summary 생성
모든 섹션 완성 후:
- Input: 각 섹션 첫 단락 + 권고 bullet들
- Output: 5개 bullet, 각 30단어 이내
- 프롬프트: "Synthesize the core takeaway. Maximum 5 bullets, 30 words each."

### 6. Evidence Table 자동 생성
`docs/06 §5` 방식:
```python
rows = []
for cid, cite in enumerate(all_citations):
    rows.append({
        "Claim ID": f"C{cid:03d}",
        "Sentence": cite["sentence"][:200],
        "Evidence Quote": cite["evidence_quote"][:200],
        "Source": cite["source_doc_id"],
        "Structural Fact": cite.get("structural_fact", "-"),
        "Confidence": cite["confidence"],
    })
pd.DataFrame(rows).to_csv("deliverables/evidence_table.csv")
```

### 7. 메타데이터 기록
`deliverables/briefing_metadata.json`:
```json
{
  "generated_at": "2026-05-15T18:00:00Z",
  "focal_country": "Brazil",
  "cop": 30,
  "sector": "adaptation",
  "total_sections": 7,
  "word_count": 8420,
  "claims_verified": 142,
  "claims_unverified": 3,
  "evidence_citations": 187,
  "generation_time_sec": 412,
  "llm_cost_usd": 3.8
}
```

## 언어 모드

- `language: "ko"`: 한국어 출력. 외교부 보고 문체.
- `language: "en"`: 영어 출력. Academic policy brief 문체. 논문 appendix 용.
- 모든 숫자·이름은 동일. 언어 변환만 다름.

## 스타일 준수

[docs/06 §4] 언어 스타일 가이드 엄격 적용:
- 감정 표현 금지
- 과도한 확신 금지 (CI width에 따라 "강한 증거로", "잠정적 시사" 구별)
- actionable verb로 권고 시작

## 할루시네이션 방지 게이트

생성된 각 문장에 대해:
1. 숫자 등장 → analysis_json / stances.jsonl 에서 검색 매치 필수
2. 국가명 등장 → 해당 국가 스탠스 존재 확인
3. 이슈명 등장 → 이슈 코드 유효성 확인

실패 시 → `evidence-validator` skill이 재생성 요청

## 품질 점검

실행 후 리포트:
- 섹션별 단어 수
- 인용 밀도 (단어 100개당 citation)
- 불확실성 언어 사용률 (CI 기반)
- 할루시네이션 의심 case (low confidence + high specificity)

## 의존성

- `stance-extractor` (upstream)
- `graph-analyst` (upstream)
- `evidence-validator` (downstream)

MCP:
- `anthropic` (LLM 호출)
- `filesystem` (템플릿·출력)

## 비용·시간

- 섹션당 LLM 호출 3~5회 (생성 + 재검증)
- 총 30–50 호출
- 비용 ~$2–5 per briefing
- 시간 ~5–10분
