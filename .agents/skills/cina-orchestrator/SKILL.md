---
name: cina-orchestrator
description: CINA 파이프라인 전체를 조율하는 오케스트레이터. Heedo가 "CINA 돌려"나 "브리핑 생성해"라고 할 때 자동 호출. Stage 0→1→2→3 전체 흐름을 관장하고, 각 단계별 세부 skill(stance-extractor, graph-analyst, briefing-composer, evidence-validator)에 위임한다. 수업 제출물과 논문 draft 두 트랙을 구분해 처리.
---

# CINA Orchestrator Skill

## 언제 이 skill을 호출하는가

다음 패턴을 Heedo가 표현할 때:
- "CINA 파이프라인 돌려줘"
- "브리핑 만들어줘" / "장관 보고서 생성"
- "브라질 COP30 분석 시작"
- "Stage 1부터 돌려" / "전체 실행"

## 전체 흐름

### Phase A. 사전 점검
1. `data/raw/` 에 UNFCCC 문서가 있는지 확인. 없으면 `src/collect/run.py` 실행.
2. `data/calibration/expert_coded_stances_sample.csv` 확인. 없으면 Heedo에게 수동 코딩 세트 요청.
3. `.Codex/logs/cina_runs.jsonl` 에 이번 실행 메타데이터 기록.

### Phase B. Stage 1 (스탠스 추출) — `stance-extractor` skill에 위임
- Input: `data/raw/`의 모든 문서
- 각 (국가, 이슈) 조합에 대해 5-sample 추출 + calibration
- Output: `data/processed/stances.jsonl`
- 성공 기준: 주요 20개국 × 6 이슈 = 120 조합 중 ≥ 100개 비공란 추출

### Phase C. Stage 2 (그래프 분석) — `graph-analyst` skill에 위임
- Input: `data/processed/stances.jsonl` + `data/raw/castro_2025/`
- HeteroData 그래프 구축 → R-GAT 학습 → Community / Centrality / Hypergraph 분석
- Output: `data/processed/graph_analysis.json`
- 성공 기준: 각 이슈별 최소 2개 커뮤니티 탐지

### Phase D. Stage 3 (브리핑 생성) — `briefing-composer` skill에 위임
- Input: `data/processed/graph_analysis.json` + `data/processed/stances.jsonl`
- 섹션별 생성 + `evidence-validator` skill로 검증
- Output: `deliverables/ministerial_briefing.md`, `deliverables/ministerial_briefing_en.md`
- 성공 기준: 모든 factual claim에 evidence citation 존재

### Phase E. 사후 처리
1. Evidence Traceability Table 자동 생성 → Appendix A에 추가
2. `deliverables/run_report_{timestamp}.md` 생성 (실행 통계)
3. Heedo에게 변경 사항 요약 제시

## 두 트랙 (Course Assignment vs Paper Draft) 구분

| 트랙 | Output 위치 | 언어 | 섹션 추가 |
|------|------------|------|-----------|
| 수업 제출 | `deliverables/ministerial_briefing.md` | 한국어 | 수업 요건 체크리스트 |
| 논문 draft | `docs/paper_draft/` | 영어 | Methodology 크로스레퍼런스 |

Heedo의 요청에 "수업용", "제출용"이 있으면 수업 트랙, "논문", "paper"이 있으면 논문 트랙. 불명확하면 양쪽 다.

## 에러 처리

- Stage N 실패 → 로그에 기록 후 이전 단계 산출물 retain
- LLM rate limit → exponential backoff (1, 2, 4, 8초)
- 동일 실행 내 retry ≥ 3 시 fail-fast

## 재현성 요구

매 실행마다 다음을 `data/runs/{timestamp}/` 에 기록:
- `config.yaml`: 모든 파라미터
- `prompts_v.txt`: 사용된 프롬프트 버전
- `model_versions.json`: LLM/GNN 버전
- `random_seeds.json`: 모든 seed
- `requirements_snapshot.txt`: pip freeze 결과

## Heedo에게 진척 보고

각 Phase 완료 시 한 줄 요약 + 핵심 수치:
```
Phase B 완료: 20국 × 6이슈 = 118/120 스탠스 추출, 평균 confidence 0.82, MAE(vs expert) 0.24
```

Phase 전체 완료 후:
```
CINA 실행 완료. 총 소요 47분, LLM 비용 $31, 브리핑 8,400자.
- 가장 confident한 발견: GGA-IND에서 남아공의 bridge centrality (0.34)
- 가장 확인 필요한 주장: BRA의 epistemic divergence risk 0.62 (expert 검증 권장)
```

## 의존성

다른 skill 4개:
- `stance-extractor`
- `graph-analyst`
- `briefing-composer`
- `evidence-validator`

MCP:
- `filesystem` (data/, deliverables/ 접근)
- `fetch` (UNFCCC·IISD 문서)
- `anthropic` (LLM 호출)

## 품질 게이트 (각 Phase 완료 전 자동 검증)

| 게이트 | Phase | 기준 |
|--------|-------|------|
| Data Coverage | A | 20국 × 6이슈 조합의 ≥ 80% 문서 확보 |
| Calibration Fit | B | Platt scaling ECE ≤ 0.10 |
| Graph Connectivity | C | 단일 connected component |
| Evidence Grounding | D | 모든 claim ≥ 1 evidence |

게이트 통과 못하면 다음 phase 진입 차단, Heedo에게 alert.
