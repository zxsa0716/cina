---
assigned_to: policy-data-collector
round: 1
issued_by: team-lead
issued_at: 2026-04-25
priority: P0
deadline: round_1 종료 전
depends_on: []
---

# Task T01 — Round 1 Foundation Collection

## 목적
CINA Round 1의 데이터 토대를 구축한다. Tier-P0 소스 5개에서 핵심 문서를 수집하고, 모든 파일에 표준 메타데이터·sha256·라이선스를 첨부한다.

## 구체 산출물

- [ ] `data/raw/cop30_official/` — Belém Package + GGA 결정문 + presidency letters (목표 ≥ 5건)
- [ ] `data/raw/castro_2025/` — Castro et al. 2025 Nature Sci Data 본문 + supplementary CSV (목표 1건)
- [ ] `data/raw/ipcc_ar6/wg2/` — AR6 WGII Ch.1, 16, 17, 18 PDFs (목표 4건)
- [ ] `data/raw/unfccc_submissions/cop30/` — 적응 토픽 (1136) 필터로 최소 20건
- [ ] `data/raw/enb_summaries/cop30/` — COP30 ENB 일일 발행 (목표 ≥ 10건)
- [ ] `data/raw/ndcs/{ISO3}/` — 코어 7개국 NDC: BRA, EU, USA, CHN, IND, ZAF, SAU (각 최신 1건)
- [ ] `data/manifest/manifest.jsonl` — 모든 수집물 등록
- [ ] `data/manifest/coverage_summary.json` — 커버리지 요약

## 실행 명령

```bash
# 1. (먼저) 안전한 소스부터
python -m src.collect.orchestrate --sources cop30,castro,ipcc --max 20

# 2. NDC 코어 7개국
python -m src.collect.orchestrate --sources ndc --countries "Brazil,European Union,United States,China,India,South Africa,Saudi Arabia"

# 3. UNFCCC submission (rate limit 조심)
python -m src.collect.orchestrate --sources unfccc --topic adaptation --max 30

# 4. ENB COP30 (User-Agent 헤더 필수)
python -m src.collect.orchestrate --sources enb --event cop30 --max 15
```

## 품질 기준 (이 task 통과 조건)

- [ ] manifest 총 entries ≥ 50
- [ ] sha256 충돌·중복 0건 (자동 dedupe로 차단)
- [ ] 모든 파일에 `.meta.json` 동봉
- [ ] coverage_summary.json 생성, countries ≥ 7, sessions ≥ 1
- [ ] 실패 URL은 `data/runs/collect_*/summary.json` 에 기록 (중도 종료 X)

## 제공된 컨텍스트

- 카탈로그: [docs/11_source_catalog.md](../../../docs/11_source_catalog.md)
- 마스터플랜: [docs/12_data_collection_master_plan.md](../../../docs/12_data_collection_master_plan.md)
- 식별자 표준: [docs/13_reference_tables.md](../../../docs/13_reference_tables.md)
- 코드: `src/collect/orchestrate.py` + `src/collect/{unfccc,iisd_enb,ndc_registry,cop30_official,castro_2025,ipcc_ar6}.py`

## 산출물 보고

라운드 종료 시 다음을 작성:
- `council_sessions/round_1/data_collection/REPORT.md` (논문체, 1-2 pages)
- `council_sessions/round_1/data_collection/manifest_diff.jsonl` (이번 라운드에 추가된 entries만)
- `council_sessions/round_1/data_collection/issues_log.md` (실패·차단·결정 사항)

## 이번 라운드 특별 주의

1. **ENB는 User-Agent 헤더가 없으면 403** — `CinaHttpClient`가 처리하지만 차단 시 `--no-robots` 옵션 시도
2. **Castro et al. 2025 supplement 위치는 Figshare 또는 Springer static-content** — 링크가 두 가지 패턴 모두 가능
3. **UNFCCC `f[0]=topic:1136` 필터는 페이지네이션 필요** — `max_pages=5`로 충분치 않으면 늘려라
4. **모든 다운로드 후 sha256 무결성 검증** — `manifest.py` 가 자동 처리

## 다음 단계
- 완료 후 `data-refinement-analyst` (Task T02) 가 처리
- 두 교수 (T03, T04) 가 동시 검토
