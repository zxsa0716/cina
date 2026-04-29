---
template_for: data-refinement-analyst
log_type: refinement_session
round: 0
date: YYYY-MM-DD
---

# Refinement Session Log — Round {N}

## 1. Mandate
(team-lead가 발급한 정제 task 인용)

## 2. 입력 인벤토리
- raw 파일 수: N (data/raw 트리)
- manifest entries: M (data/manifest/manifest.jsonl)
- 신규 파일 수 (이번 라운드): K

## 3. 정제 단계

### 3.1 추출
- PDF → 텍스트 (PyMuPDF)
- HTML → 텍스트 + 단락 분리 (BeautifulSoup)
- 추출 실패: N건 (이유 명시)

### 3.2 단락 분할
- paragraphs[] 빌드
- 평균 단락 길이 (tokens): ...
- 너무 짧은 단락 (< 30 tokens) 제거: K건

### 3.3 토픽 자동 태깅
- 1차 키워드 필터 결과: 분포 (GGA-IND: X, ADAPT-FIN: Y, ...)
- 2차 LLM 확인 (claude-haiku): N개 호출, ~$0.01

### 3.4 국가 인식 (NER + 매핑)
- 평균 문서당 언급 국가 수: ...
- Group label normalize: G77, EU, AOSIS, ...

### 3.5 중복·결측
- 중복 (sha256): K건 → 제거
- 결측 metadata: M건 → 보강 시도

## 4. 산출물

- `data/processed/documents.jsonl` 새 entries: N
- 스키마 검증 통과율: X%
- 거부된 레코드: K건 + 이유 분류

## 5. 품질 통계

| 지표 | 값 | 목표 |
|------|-----|------|
| 평균 confidence (토픽 태깅) | 0.X | ≥ 0.8 |
| 단락당 evidence quote 후보 수 | N | ≥ 1 |
| 국가 식별 precision (수동 sample 10) | X% | ≥ 90 |
| stance extraction 준비도 | YES/NO | YES |

## 6. Collector 피드백

(다음 라운드 collector에게 전달할 gap)
- 누락 국가: ...
- 누락 이슈: ...
- 누락 시점: ...
- 부적절한 소스 (스탠스 추출에 정보 부족): ...

## 7. 두 교수에게 전달할 입력 패키지

- `data_refinement/round_{N}/professor_input/policy_sci_pack.md`
- `data_refinement/round_{N}/professor_input/ir_pack.md`

각 패키지에 포함:
- 라운드 정제 결과 요약
- 핵심 인용 5-10개 (각 교수 시점에서 가장 흥미로운)
- 명시적 질문 (정책학자/IR학자에게 묻고 싶은 것)

## 8. team-lead에게 escalation

- (있으면 명시)

## Appendix A. 코드 스냅샷

```bash
python -m src.refine.run --input data/raw --output data/processed --round {N}
```
