# CINA v9 / Engine v2.4 — System Hardening: merge + cache + tests + CI + cert + i18n

> **Release**: 2026-05-12
> **작성**: Heedo Choi (최희도) · zxsa0716@kookmin.ac.kr

이번 릴리스는 **시스템 인프라 통째 고도화** — 단순 기능 추가가 아닌 production-grade 인프라:
1. v5.2 overlay merge 정책
2. SQLite persistent LLM cache
3. 외부 코더 Krippendorff α 도구
4. Pytest 40 테스트
5. GitHub Actions CI workflow
6. Reproducibility certificate (chain hash)
7. i18n (한국어/영어 UI 토글)
8. API documentation

---

## TL;DR

| 영역 | v8/v2.3 | v9/v2.4 | 증가 |
|------|---------|---------|------|
| Merge 정책 | 없음 | **overlay precedence + audit log** | +1 system |
| LLM cache | 없음 | **SQLite, all providers, TTL** | +1 system |
| Real-coder tool | 없음 | **web form + CSV export + α aggregator** | +1 tool |
| Test 인프라 | 0 | **40 pytest** (5 modules, 21초) | +40 |
| CI workflow | 없음 | **4-job GitHub Actions** | +1 system |
| Reproducibility cert | 없음 | **chain hash (58 entries)** | +1 system |
| i18n | 한국어 only | **ko/en 토글** | +1 lang |
| API docs | 없음 | **포괄 reference** | +1 doc |
| Engine 버전 | v2.3.0 | **v2.4.0** | +1 |

---

## 1. v5.2 Overlay Merge (`src/data/merge_v5_llm.py`)

### 1.1 우선순위 정책
```
verified_llm > verified_canonical > llm_unverified_quote > heuristic_extension
```

### 1.2 머지 결과 (현재 상태)
```
heuristic=2400  llm=0
result: 2400 records  verified_ratio: 5.2%
overlay events: 0
kept counts:
   kept_heuristic_extension: 2275
   kept_verified_canonical: 125
```

(LLM 추출 데이터 추가되면 `verified_llm` 우선순위가 자동 반영)

### 1.3 Audit log
각 머지된 record는 `_meta.overlay_history`에 어떤 source가 dropped됐는지 기록.

### 1.4 출력
- `data/processed/stances_v5_merged.jsonl` — canonical 서빙 dataset
- `data/processed/stances_v5_merged_meta.json` — metadata
- `data/processed/stances_v5_merged_audit.json` — kept/dropped 통계

---

## 2. Persistent LLM Cache (`src/program/llm_cache.py`)

### 2.1 SQLite 백엔드
- 키: `sha256(provider | model | temperature | prompt)`
- TTL: 기본 30일
- 자동 hit_count 증가

### 2.2 통합 지점
- `llm_stance_extractor.extract_one()` — 2,400건 추출 시 ~99% 캐시 절감
- `cross_llm_alpha.extract_one()` — 다중 provider 측정 시 동일 prompt 재사용
- Future: query_engine_v2 LLM 모드 (브라우저는 별도)

### 2.3 사용 예
```python
from src.program.llm_cache import cached_call, CacheStats

response = cached_call(
    provider="gemini", model="gemini-2.5-flash-lite",
    prompt=prompt, api_key=key, call_fn=fn,
    temperature=0.2, ttl_days=30,
)
print(CacheStats.snapshot())   # {hits, misses, hit_rate, writes, errors}
```

### 2.4 CLI
```bash
python -m src.program.llm_cache --stats
python -m src.program.llm_cache --clear
```

---

## 3. External Coder Krippendorff Tool

### 3.1 Web form (`docs/web/coder_tool.html`)
- Coder 등록 (id, 소속, 전문 분야)
- 결정론적 sample (seed=42, n=20 default)
- 입력: stance (-1~+1), frame (5-class), NATO 4-axis (slider 4개), confidence, evidence quote
- LocalStorage 자동 저장 + CSV/JSON export

### 3.2 Aggregator (`src/eval/external_coder_alpha.py`)
- 다중 코더 CSV → Krippendorff α (raw + bias-corrected)
- 결과: `data/llm_logs/external_alpha_<ts>.{json,md}`

### 3.3 사용 흐름
1. 3명 외부 전문가 (예: KEI, KAIST, MOFA)에게 `coder_tool.html` URL 전달
2. 각 코더가 20-78 samples 입력 → CSV 다운로드
3. `python -m src.eval.external_coder_alpha --csvs ...` 실행
4. Paper claim α=0.876 / 0.933 자가검증

---

## 4. Pytest Infrastructure (40 tests, 21s)

### 4.1 테스트 파일
| 파일 | 테스트 수 | 영역 |
|------|---------|------|
| `tests/test_query_engine.py` | 17 | intent parsing, relevance scoring, formatters |
| `tests/test_alpha.py` | 7 | Krippendorff α, bias correction |
| `tests/test_merge.py` | 7 | overlay precedence, audit, no-overlap |
| `tests/test_corpus_search.py` | 6 | corpus_search, context filter, semantic |
| `tests/test_llm_cache.py` | 5 | hit/miss, skip_cache, temp differentiation, stats |

### 4.2 마커
- `@pytest.mark.slow` — sentence-transformers 로드 필요
- `@pytest.mark.network` — fetch 호출 필요
- `@pytest.mark.llm` — LLM API key 필요

CI에서 `-m "not slow and not network and not llm"`으로 빠른 검증.

### 4.3 결과
```
40 passed in 21.25s
```

---

## 5. GitHub Actions CI (`.github_workflows_to_install_manually/cina_v9_ci.yml`)

### 5.1 4-job pipeline

1. **unit-tests** — pytest fast path
2. **build-freshness** — `rebuild_if_stale --check`
3. **reproducibility** — chain hash 생성 + artifact upload
4. **corpus-integrity** — manifest sha256 검증

### 5.2 Trigger
- push / pull_request to main
- workflow_dispatch (수동)

### 5.3 설치
```bash
mkdir -p .github/workflows
cp .github_workflows_to_install_manually/cina_v9_ci.yml .github/workflows/
git add .github/workflows && git commit -m "Enable CI" && git push
```

(PAT with `workflow` scope 필요)

---

## 6. Reproducibility Certificate

### 6.1 chain hash
58 entries (모든 build artefact + 소스 코드 + 문서) SHA-256 chain hash:
```
b869015d5f88625263796daf21db3d486f0eae5468fb0a1a6be22e8d8a199a4d
```

### 6.2 카테고리
| 카테고리 | 파일 수 |
|----------|--------|
| v5_dataset | 2 |
| v6_corpus_index | 3 |
| v6_corpus_documents | 10 |
| v6_corpus_csvs | 5 |
| v6_corpus_bib | 1 |
| v7_embeddings | 4 |
| build_scripts | 8 |
| engine_scripts | 3 |
| eval_scripts | 2 |
| test_suite | 5 |
| changelogs | ~9 |
| documentation | ~6 |

### 6.3 외부 검증
```bash
git clone https://github.com/zxsa0716/cina
cd cina
python -m src.data.build_reproducibility_certificate
# chain hash 비교
```

### 6.4 출력
- `data/reproducibility_certificate.json` — 58 entries + 체인
- `data/reproducibility_certificate.md` — 사람이 읽기용 요약

---

## 7. i18n (한국어/영어 UI)

### 7.1 web JS i18n 모듈
`I18N` 객체에 50+ string 키 매핑. `t(key)` 함수로 lookup.

### 7.2 UI 토글
헤더 toolbar에 `🇰🇷 한국어 | 🇬🇧 EN` 버튼. localStorage `cina_v2_lang` 저장.

### 7.3 영어 응답 예시
```
**Brazil – GGA-IND (COP30)**
Stance score: +1.00 (strong support) (95% CI [+0.92, +1.00])
Dominant frame: sovereignty
NATO 4-axis: N=0.55 A=0.24 T=0.16 O=0.30
Procedural authority: chair, pen-holder (composite=1.00)
```

### 7.4 API
```javascript
window.CINA_v2.setLang("en");
window.CINA_v2.translate("strong_support");  // → "strong support"
```

---

## 8. API Documentation (`docs/api/README.md`)

포괄 reference (~600 lines):
- Python API (8개 모듈 + 사용 예)
- Browser JS API (`window.CINA_v2.*` 전체 메서드)
- Data schemas (stance record / corpus manifest / embedding record)
- CLI commands cheatsheet
- Build chain dependency 다이어그램

---

## 9. Query Engine v2.3 → v2.4

### 9.1 변경
- Dataset 우선순위: `stances_v5_merged.jsonl` > `stances_v5.jsonl` (자동 prefer)
- 모든 응답 i18n-aware (한국어/영어 즉시 전환)
- LLM cache 통합 (extractor + alpha framework)

### 9.2 호환성
- v5.1 / v5.2-merged 모두 자동 인식
- 기존 코드 변경 없음

---

## 10. 라이브 URL (push 후 자동 반영)

- **Q&A v2.4**: https://zxsa0716.github.io/cina/web/cina_program_v2.html
  - 🇰🇷/🇬🇧 언어 토글 추가
  - α slider + Gemini embedding (기존)
- **Corpus Browser**: https://zxsa0716.github.io/cina/web/corpus_browser.html
- **Coder Tool (NEW)**: https://zxsa0716.github.io/cina/web/coder_tool.html
- **API docs (NEW)**: https://github.com/zxsa0716/cina/blob/main/docs/api/README.md
- **Reproducibility cert (NEW)**: https://github.com/zxsa0716/cina/blob/main/data/reproducibility_certificate.md

---

## 11. 알려진 한계

1. **v5.2-merged는 LLM 추출 데이터 없으면 v5.1과 동일**: 사용자가 LLM 추출 실행해야 차이가 발생.
2. **i18n 커버리지는 응답 템플릿만**: navigation/header text는 한국어 고정 (HTML 직접 변경 필요).
3. **CI workflow는 manual install 필요**: PAT `workflow` scope 제약.
4. **Reproducibility cert는 cert 자체 제외**: cert 갱신 시 chain hash 자동 변경 (정상 동작).
5. **External coder tool은 sample 크기 5-78 제한**: 더 큰 sample은 sample 모듈 수정 필요.

---

## 12. 다음 단계 (v10 계획)

- **Real expert validation 실행**: KEI/KAIST/MOFA 3명에게 coder_tool 배포 후 실제 α 측정
- **LLM cache 통합 query engine**: 브라우저 BYO 호출에도 cache 적용
- **i18n HTML 텍스트 커버**: navigation/title도 영어 옵션
- **arXiv preprint 제출**: paper/arxiv/ 패키지를 실제 arXiv에 업로드
- **COP31 prospective ingestion 준비**: 2026.11 결과 사전 등록 hypothesis 확정

---

**커밋 추적**:
- `src/data/merge_v5_llm.py` (신규, 175 lines)
- `src/program/llm_cache.py` (신규, 175 lines)
- `src/eval/external_coder_alpha.py` (신규, 110 lines)
- `src/data/build_reproducibility_certificate.py` (신규, 170 lines)
- `src/program/llm_stance_extractor.py` (cache integration)
- `src/eval/cross_llm_alpha.py` (cache integration)
- `src/program/query_engine_v2.py` (i18n hooks, lang toggle)
- `docs/web/coder_tool.html` (신규, 400 lines)
- `docs/web/cina_program_v2.html` (lang toggle UI + badges)
- `docs/web/sitemap.html` (Coder link)
- `docs/web/assets/cina_program_v2.js` (v2.3 → v2.4, i18n + lang API)
- `docs/api/README.md` (신규, ~600 lines)
- `tests/conftest.py`, `tests/test_*.py` (신규, 5 files / 40 tests)
- `pytest.ini` (신규)
- `.github_workflows_to_install_manually/cina_v9_ci.yml` (신규)
- `data/reproducibility_certificate.{json,md}` (신규)
- `CHANGELOG_v9.md` (이 파일)
