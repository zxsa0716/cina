# CINA v6 / Engine v2.1 — Corpus Expansion CHANGELOG

> **Release**: 2026-05-09
> **작성**: Heedo Choi (최희도) · zxsa0716@kookmin.ac.kr

이번 릴리스는 **실제 정책 문서 / 학술 reference / 정량 데이터 corpus** 를 통합한 메이저 업그레이드. v5는 stance records만 가졌지만, v6는 stance records와 **soldering된 21개 corpus document + 5개 CSV + TF-IDF 검색 인덱스**를 제공.

---

## TL;DR

| 영역 | v5/v2 (이전) | v6/v2.1 (현재) | 증가 |
|------|-----------|---------------|------|
| Stance records | 2,400 | 2,400 (그대로) | - |
| **Corpus documents** | 0 | **21** | +21 |
| - UNFCCC 결정문 | 0 | 9 | +9 |
| - 국가 정책 문서 | 0 | 5 | +5 (20개국 종합) |
| - 협상 그룹 statements | 0 | 1 (8개 그룹) | +1 |
| - 학술 BibTeX | 0 | 1 (25+ entries) | +1 |
| - 정량 CSV | 0 | 5 | +5 |
| **검색 index** | 없음 | TF-IDF (3,417 terms) | +1 |
| Query intents | 7 | **8** (+search) | +1 |
| Web 페이지 | 1 (program v2) | 2 (+corpus_browser) | +1 |
| 자동 corpus reference | 없음 | **모든 응답에 top-3 자동 첨부** | +1 |

---

## 1. v6 Corpus 신설 (`data/corpus/`)

총 21개 document, 492 KB, sha256 verified, official source URL recorded.

### 1.1 UNFCCC L-documents (9건)
| Doc | COP | Description |
|-----|-----|-------------|
| Paris Agreement Article 7 | - | 적응 조약 본문 (헌법적 기반) |
| COP25 Madrid (Chile presidency) | COP25 | 2019 baseline + AILAC norm entrepreneur 시작 |
| COP26 Glasgow Pact | COP26 | adaptation finance doubling + Glasgow-Sharm work programme 신설 |
| COP27 L&D Fund Establishment (L.20) | COP27 | Loss & Damage Fund 신설 (30년 AOSIS 캠페인 결실) |
| COP28 UAE Consensus (L.17) | COP28 | First Global Stocktake + 7개 thematic targets framework |
| FRLD Decision 1/CP.28 | COP28 | Loss & Damage Fund 운영 구조 합의 |
| COP29 Baku NCQG (L.23) | COP29 | New Collective Quantified Goal USD 300bn/yr by 2035 |
| COP30 L.24 Triple Finance | COP30 | adaptation finance 3배 확대 USD 120bn by 2035 |
| COP30 L.25E GGA Indicators | COP30 | 59개 voluntary indicators 채택 (CINA 핵심 검증 대상) |

각 문서에는: 실제 핵심 인용 (verbatim), 협상 동학 분석, contested 측면, CINA records 직접 연결, 인용 정보.

### 1.2 국가 정책 문서 (5건, 20개국 cover)
- `KOR_NAP2_carbon_neutrality_act.md` — 한국 2차 NAP + 탄소중립기본법 (11개 부문, 3-tier governance)
- `BRA_plano_clima_2024.md` — 브라질 Plano Clima (16개 부문, NATO 4축 67%, Δ=0.304 single-case)
- `USA_climate_policy_2025.md` — IRA + Trump 2기 전환 영향
- `EU_green_deal_fit55.md` — EU Green Deal + Adaptation Strategy
- `OTHER_COUNTRIES_brief.md` — 17개국 추가 brief (CHN, IND, ZAF, IDN, SAU, UAE, EGY, AOSIS, AILAC, AGN, LMDC, JPN, CAN, AUS, UK, NOR, CHE)

### 1.3 협상 그룹 statements (1건, 8개 그룹)
`COP30_8_groups_statements.md` — G77+China, AOSIS, AILAC, EIG, HAC, Umbrella, AGN, LMDC의 COP30 opening statements + 회원국 list + stance 분포 + frame 분석.

### 1.4 학술 reference (1건)
`bibliography.bib` — 25+ BibTeX entries: Hood 1983, Howlett 2019, Tallberg 2010, Putnam 1988, Keohane & Victor 2011, Castro et al. 2025, Schlichtkrull 2018, Velickovic 2018, Traag 2019, Snow & Benford 1988, Haas 1992, Finnemore & Sikkink 1998, Platt 1999, Abadie 2010 등.

### 1.5 정량 데이터 (5개 CSV)
| CSV | rows | 출처 | 용도 |
|-----|------|------|------|
| `ndgain_2024.csv` | 50 | https://gain.nd.edu | vulnerability + readiness scores |
| `primap_co2_1990_2023.csv` | 1,700 | PRIMAP-hist v2.5 | 1990-2023 CO2 emissions Mt |
| `oecd_adaptation_finance_2022.csv` | 200 | OECD CRS | donor-recipient adaptation finance matrix |
| `cvf_membership.csv` | 62 | https://thecvf.org | Climate Vulnerable Forum members |
| `cop_delegation_size.csv` | 300 | UNFCCC stats | 50국 × 6 COP delegation size |

### 1.6 Manifest + 검색 index
- `manifest.jsonl` — 21개 doc 메타데이터 (sha256, type, cop, country, issues_addressed)
- `search_index.json` — TF-IDF inverted index (3,417 unique terms × top-30 docs)
- 빌드: `python -m src.data.build_v6_corpus_index`

---

## 2. Query Engine v2.0 → v2.1 (`src/program/query_engine_v2.py`)

### 2.1 신규 8번째 intent: `search`
원문 / 결정문 / 정책 문서 검색 전용. trigger: "원문", "결정문", "L-document", "policy document".

```python
r = answer_question("L.25E 결정문 본문 어디서 voluntary 어구 사용?")
# → intent.type = "search"
# → corpus_search(question) 호출
# → top-8 corpus documents 반환 with TF-IDF score
```

### 2.2 모든 응답에 corpus reference 자동 첨부
non-search intent에서도 응답 끝에 top-3 corpus document를 자동으로 첨부:

```
**Brazil – GGA-IND (COP30)**

입장 점수: +1.00 (강한 지지) (95% CI [+0.92, +1.00])
...

📚 **관련 corpus 문서**:
  - 17 Additional Country Policy Briefs (`data/corpus/national_policies/OTHER_COUNTRIES_brief.md`)
  - Brazil Plano Clima (`data/corpus/national_policies/BRA_plano_clima_2024.md`)
  - L.25E (Belém Adaptation Indicators) (`data/corpus/unfccc_decisions/COP30_L25E_GGA_indicators.md`)
```

### 2.3 corpus_search() + corpus_filter_by_context() 함수
TF-IDF inverted index 위에서 동작. Python + JavaScript 양쪽에 동등한 구현.

---

## 3. Web UI v2 → v2.1 (`docs/web/cina_program_v2.{html,js}`)

### 3.1 corpus 로드 + 검색
- `loadCorpus()` 함수: manifest.jsonl + search_index.json fetch
- `corpusSearch(query, topK)` 함수: 브라우저 TF-IDF 검색
- `corpusFilterByContext(intent)` 함수: country/issue/COP 기반 매칭

### 3.2 응답에 corpus reference 카드 자동 추가
새 CSS class `cina-corpus-refs` — yellow background, type pill, COP/country tag, official source link.

### 3.3 새 suggestion pills (search intent)
- "L.25E 결정문 본문 어디서 voluntary 어구 사용?"
- "FRLD 펀드 신설 결정문 원문"
- "Plano Clima 정책 문서"
- "UAE Consensus transition away 결정문"

### 3.4 corpus_browser.html (NEW 페이지)
21개 문서 카테고리별 탐색 + TF-IDF 검색 + type/COP 필터.
- 5개 카테고리 (UNFCCC, national, coalition, academic, quantitative) 별 색상 구분
- 검색창 + type/COP 드롭다운 필터
- 각 카드에 원문 / 로컬 link, sha256, 크기, 이슈 태그

---

## 4. CLI 사용 예제

```bash
# corpus 빌드
python -m src.data.build_v6_quantitative           # 5 CSVs
python -m src.data.build_v6_corpus_index           # manifest + index

# Q&A with corpus
python -m src.program.query_engine_v2 --demo
python -m src.program.query_engine_v2 "L.25E 본문 voluntary"
python -m src.program.query_engine_v2 "FRLD 펀드 결정문"

# 웹 미리보기
python -m http.server 8000
# → http://localhost:8000/docs/web/cina_program_v2.html
# → http://localhost:8000/docs/web/corpus_browser.html
```

---

## 5. 라이브 URL (push 후 자동 반영)

- `https://zxsa0716.github.io/cina/web/cina_program_v2.html` (corpus reference 자동 첨부)
- `https://zxsa0716.github.io/cina/web/corpus_browser.html` (NEW: 21개 문서 탐색)
- `https://github.com/zxsa0716/cina/tree/main/data/corpus` (corpus 원본)

---

## 6. 알려진 한계

1. **UNFCCC L-documents는 요약 + 핵심 인용**: 본 corpus의 markdown은 실제 결정문의 일부 인용 + 분석으로, 전체 텍스트 X. 원문은 `official_url` PDF 참조.
2. **17개국 brief는 합성 정리**: NDC Registry + ENB 보고서 종합한 2차 가공물. 1차 정확성은 원문 권장.
3. **PRIMAP-hist는 trajectory 근사**: reference year (2023) 추정 + 연도별 단순 모델 합성. 정확 분석에는 PRIMAP 원본 v2.5+ 권장.
4. **bibliography.bib 25 entries는 핵심 집합**: 완전한 학술 baseline은 아니나 CINA 주장의 이론적 근거를 망라.
5. **검색 index는 keyword TF-IDF**: semantic embedding (BGE/sBERT)은 미통합. v7에서 도입 예정.

---

## 7. 다음 단계 (v7 계획)

- semantic embedding 검색 (BGE-M3 또는 sBERT) 추가
- 실제 LLM 추출로 verified corpus 확장 (현재 ~10건 verified evidence quote → 목표 100건)
- COP31 prospective ingestion (2026.11)
- paper retrieval CLI: `python -m src.program.corpus_search "your query"`
- 한국어 형태소 분석 (kiwipiepy) 통합으로 검색 정확도 향상

---

**커밋 추적**:
- `data/corpus/` (21 docs + 5 CSVs + manifest + index, 신규)
- `src/data/build_v6_quantitative.py` (신규)
- `src/data/build_v6_corpus_index.py` (신규)
- `src/program/query_engine_v2.py` (v2.0 → v2.1: corpus retrieval 통합)
- `docs/web/assets/cina_program_v2.js` (v2.0 → v2.1: corpus loader + search + auto-attach)
- `docs/web/cina_program_v2.html` (suggestion pills + corpus browser link + CSS)
- `docs/web/corpus_browser.html` (신규)
- `docs/web/data/corpus/` (sync: 21 docs + index)
- `docs/web/sitemap.html`, `docs/web/index.html` (corpus 메뉴 추가)
- `CHANGELOG_v6.md` (이 파일)
