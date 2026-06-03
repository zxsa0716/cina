---
name: evidence-validator
description: 생성된 브리핑 문장마다 (텍스트 인용, 구조적 근거) 두 축의 grounding을 검증. 할루시네이션·수치 조작·없는 국가 언급을 자동 탐지. CINA의 credibility 보증 skill.
---

# Evidence Validator Skill

## 언제 이 skill을 호출하는가

- `briefing-composer`가 섹션 생성 후 자동 위임
- Heedo가 "이 주장 검증해줘"라고 할 때
- 최종 문서 공개 전 반드시 1회 실행

## 입력·출력

### Input
- `draft_text`: 검증할 텍스트 (섹션 또는 전체 브리핑)
- `evidence_base`: `data/processed/stances.jsonl` 및 원시 문서
- `analysis`: `data/processed/graph_analysis.json`

### Output
- `verified_claims`: list of {sentence, evidence, structural_fact, confidence}
- `unverified_claims`: list of {sentence, reason}
- `verification_report.md`: 요약 리포트

## 검증 룰 (Cascade)

### Rule 1. 숫자 주장 (Numeric Claims)
숫자가 포함된 문장:
- 예: "남아공 betweenness는 0.34", "3개 블록으로 분열", "59개 지표 채택"
- 검증: analysis_json, stances.jsonl, 외부 공식 소스에서 해당 숫자 직접 검색
- 미통과: `unverified`

### Rule 2. 국가/이슈 언급
- 문장에 등장한 국가명이 stance 추출 대상에 있는지 확인
- 이슈 코드 (GGA-IND 등)가 유효한지 확인
- 없으면 `unverified`

### Rule 3. 인용문 검증
evidence_quote 인용 시:
- 원문에서 fuzzy match ratio ≥ 0.85
- 출처 문서 ID가 `documents.jsonl`에 존재
- 단락 번호가 유효 범위

### Rule 4. 구조적 근거
"브릿지 국가", "허브", "cluster" 같은 표현:
- `analysis_json`의 해당 필드 존재 확인
- 수치가 일치하는지 확인

### Rule 5. 인과·전략 주장
"...에 의해 ...가 예상된다", "...를 수용하면..." 같은 문장:
- 적어도 한 개의 structural_fact + 한 개의 evidence_quote 동반
- 둘 다 없으면 `unverified`

### Rule 6. 시점 일관성
날짜·COP 회기 언급이 분석 범위와 일치:
- COP30 이전 데이터로 COP30 결과 예측 주장 허용
- COP31 결과를 확정적 기술하면 `unverified`

### Rule 7. 불확실성 표시
CI width > 0.4 인 스탠스에 대한 주장:
- "strong", "definitely", "clearly" 같은 확신 어휘 사용 시 → `warning`
- "likely", "may", "appears" 사용 시 → pass

## 출력 형식

### `verification_report.md`

```markdown
# Verification Report

**Draft**: {section or file}
**Verified at**: 2026-05-15T18:30Z
**Validator version**: v1.1

## Summary
- Total sentences: 142
- Verified: 138 (97.2%)
- Unverified: 3 (2.1%)
- Warnings: 1

## Unverified Claims (must fix)
### U001. "브라질의 Amazon 전략이 적응 섹터 합의를 주도했다"
- Reason: No structural fact linking Amazon strategy to negotiation outcome
- Suggested action: Remove claim or add Stage 2 analysis evidence

### U002. ...

## Warnings (recommended review)
### W001. "COP30에서 분명 성공했다"
- Reason: Over-confident language ("분명") while CI width was 0.52
- Suggested softening: "COP30에서 성과를 얻었다" or similar

## Details per rule
[각 rule 별 pass/fail 분포]
```

## 재생성 피드백

Unverified claim 발견 시 `briefing-composer` 에 regeneration 요청:
```
Revised prompt addition:
"Your previous draft contained these unverified claims:
  - [U001 sentence]
  - [U002 sentence]
Regenerate removing or adequately citing these claims."
```

최대 3회 재생성. 그 이후에도 실패하면:
- 자동 제거 (soft fail)
- 경고와 함께 brief metadata에 기록

## 할루시네이션 카테고리별 통계

각 실행 후 다음 수집:
- Fabricated numbers (rule 1 fail)
- Non-existent actors (rule 2 fail)
- Misquoted sources (rule 3 fail)
- Orphan structural claims (rule 4 fail)
- Unsupported strategic claims (rule 5 fail)

장기 추적으로 프롬프트·모델·데이터 개선 방향 가이드.

## 의존성

Python:
- `rapidfuzz` (fuzzy matching)
- `jsonschema` (구조 검증)
- `re` (regex 기반 숫자 추출)

MCP:
- `filesystem` (소스 문서 접근)

## 호출 패턴

```python
from evidence_validator import validate

unverified = validate(
    draft_text=section_text,
    evidence_base=load_stances(),
    analysis=load_analysis(),
    strict=True,
)
```

## 품질 기준

- False positive rate (잘못 unverified 판정) < 5%
- False negative rate (할루시네이션 놓침) < 2%
- Spot check: 매 10번 실행마다 수동 검토 세트 점검
