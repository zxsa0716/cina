---
name: stance-extractor
description: UNFCCC·NDC·ENB 문서에서 국가·이슈별 스탠스를 구조화 JSON으로 추출. Multi-sample(k=5) + Bayesian credible interval + Platt calibration. 할루시네이션 방지를 위해 evidence_quote를 모든 레코드에 강제. Stage 1 파이프라인의 워크호스.
---

# Stance Extractor Skill

## 언제 이 skill을 호출하는가

- "스탠스 추출해줘"
- "이 문서에서 브라질이 GGA에 대해 뭐라 했는지 뽑아줘"
- `cina-orchestrator` 가 Phase B에서 자동 위임

## 입력·출력 스키마

### Input
- 문서 집합: `data/raw/` 의 .pdf/.html/.txt
- 국가 목록: 기본 20개국 (CINA_FRAMEWORK §3.1)
- 이슈 목록: {GGA-IND, ADAPT-FIN, L&D-OP, NAPs, MIT-ADAPT, JT-ADAPT}
- Config: `temperature=0.3, k_samples=5, calibration_path=data/calibration/platt.pkl`

### Output
- `data/processed/stances.jsonl` — 각 라인은 [docs/03_data_architecture.md §4의 Stance Schema] 준수

## 작업 절차

### 1. 문서 로딩 & 토픽 필터링
- PDF → text (PyMuPDF)
- 키워드 기반 토픽 1차 필터 (adaptation, GGA, finance, loss, NAP, just transition)
- LLM 2차 확인 ("이 문서는 다음 이슈 중 어느 것을 주로 다루나?")

### 2. (국가, 이슈) 조합 구성
각 이슈별로 관련 문서 subset 추출. 국가는 문서의 `authors` 필드로 결정.

### 3. LLM 추출 (k=5 샘플)
[docs/04_stage1_stance_extraction.md §2] 프롬프트 사용.
- model: `Codex-opus-4-7`
- temperature: 0.3
- response_format: JSON schema 강제
- 5회 병렬 호출

### 4. 집계 & Bayesian CI
```python
from scipy.stats import beta
rescaled = [(s + 1) / 2 for s in sample_scores]  # [0,1] 스케일
alpha_post = 1 + sum(rescaled) * 5
beta_post = 1 + (5 - sum(rescaled)) * 5
ci_low_01, ci_up_01 = beta.ppf([0.025, 0.975], alpha_post, beta_post)
ci_low = ci_low_01 * 2 - 1
ci_up = ci_up_01 * 2 - 1
```

### 5. Platt Calibration
`data/calibration/platt.pkl` 이 있으면 loading하여 raw → calibrated 변환.
없으면 `data/calibration/expert_coded_stances_sample.csv` 로 학습.

### 6. Evidence Verification
각 `evidence_quote`에 대해:
- 원문에서 fuzzy match (ratio ≥ 0.85)
- 미통과 quote는 record에서 제거, warning 로그
- 모든 quote 제거 시 → stance_score=0, confidence=0 으로 설정

### 7. 로그 & 아티팩트
- `data/llm_logs/{date}/stage1_extraction.jsonl` — 모든 LLM 호출
- `data/processed/stances.jsonl` — 집계된 최종 스탠스
- `data/processed/stance_extraction_stats.json` — 실행 통계

## 프롬프트 관리

- 프롬프트 버전: `v1.2` (현재). 변경 시 `{v1.3}` 로 증가.
- 프롬프트 파일: `src/stage1_extract/prompts/v1.2/system.txt, user_template.txt, few_shots.json`
- 모든 stance 레코드는 `prompt_version` 필드로 역추적 가능

## 품질 자동 점검

실행 후 다음을 자동 리포트:
- Confidence 분포 (mean, std, histogram)
- CI width 분포 (ci_upper - ci_lower)
- Evidence quote 밀도 (stance당 평균 quote 수)
- 이슈별 커버리지 (국가 × 이슈 조합 중 비공란 비율)

기준 미달 시 Heedo에게 alert:
- Mean confidence < 0.6 → "프롬프트 개선 필요"
- CI width > 0.5 → "샘플 수 k 증가 고려"
- Evidence density < 1.5 → "문서 품질 점검"

## 의존성

MCP:
- `anthropic` (LLM 호출)
- `filesystem` (로그·결과 저장)

Python 라이브러리:
- `anthropic`, `PyMuPDF`, `scipy`, `scikit-learn`, `pandas`

## 계산 비용 추정

- 20국 × 6이슈 × 5샘플 = 600 LLM calls
- 평균 input tokens ~2000, output tokens ~500
- Codex Opus 4.7 기준: ~$25–40 per full run
- 병렬 호출 시 소요 시간 ~15–30분
