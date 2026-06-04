# 🏁 CINA — Final System Status

> **Sign-off**: 2026-05-13
> **Author**: Heedo Choi (최희도) · zxsa0716@kookmin.ac.kr
> **Status**: ✅ **PRODUCTION-COMPLETE** — 5-stage build chain + cache + tests + CI + cert + i18n

CINA(Climate Issue-Network Analysis) 시스템이 production-grade 완성 상태에 도달했습니다.
본 문서는 시스템 전체의 sign-off 보고서.

---

## 📊 At-a-glance

| 지표 | 값 |
|------|------|
| **총 코드 라인** | ~5,500 (Python) + ~3,500 (JS) + ~1,500 (HTML/CSS) |
| **Python 모듈** | 18 |
| **Web 페이지** | 5 (index, program, corpus, coder, sitemap) |
| **Unit tests** | 40 / 40 pass (21s) |
| **CI jobs** | 4 (pytest, freshness, cert, integrity) |
| **Stance records** | 2,400 (50국 × 8이슈 × 6 COP) |
| **Verified evidence** | 125 verified_canonical (5.2%) |
| **Corpus documents** | 21 (9 UNFCCC + 5 national + 1 coalition + 1 bib + 5 CSVs) |
| **Embeddings** | 215 (90 corpus + 125 stance, 384-dim) |
| **Engine 버전** | v2.4.0 |
| **Dataset 버전** | v5.2-merged |
| **Reproducibility chain** | 58 entries SHA-256 chain |

---

## 🧩 System Architecture (5-layer)

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 5 — User-facing Web (docs/web/)                          │
│  index.html · cina_program_v2.html · corpus_browser.html        │
│  coder_tool.html · sitemap.html                                 │
│  🇰🇷↔🇬🇧 i18n · α slider · BYO LLM · IndexedDB cache             │
└─────────────────────────────────────────────────────────────────┘
                              ▲
┌─────────────────────────────────────────────────────────────────┐
│  Layer 4 — Query Engine v2.4 (src/program/)                     │
│  query_engine_v2.py  (8 intents, hybrid search, methodology)    │
│  llm_stance_extractor.py · llm_cache.py (SQLite TTL 30d)        │
└─────────────────────────────────────────────────────────────────┘
                              ▲
┌─────────────────────────────────────────────────────────────────┐
│  Layer 3 — Eval & Reproducibility (src/eval/, src/data/)        │
│  cross_llm_alpha.py (Krippendorff α + bias correction)          │
│  external_coder_alpha.py (real-coder CSV aggregator)            │
│  build_reproducibility_certificate.py (chain hash, 58 entries)  │
│  rebuild_if_stale.py (cache-aware dispatcher)                   │
└─────────────────────────────────────────────────────────────────┘
                              ▲
┌─────────────────────────────────────────────────────────────────┐
│  Layer 2 — Builders (src/data/)                                 │
│  build_v5_dataset.py + v5_evidence_quotes_expanded.py (125)     │
│  build_v6_corpus_index.py + build_v6_quantitative.py            │
│  build_v7_embeddings.py + build_v7_embeddings_gemini.py         │
│  merge_v5_llm.py (overlay precedence + audit log)               │
└─────────────────────────────────────────────────────────────────┘
                              ▲
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1 — Source Data (data/)                                  │
│  processed/stances_v5*.jsonl  (heuristic + LLM + merged)        │
│  corpus/{unfccc, national, coalition, academic, quantitative}   │
│  corpus/embeddings.{npz,json} · search_index.json · manifest    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Complete Feature Matrix

### Data
- ✅ 50 countries × 8 issues × 6 COPs = **2,400 stance records**
- ✅ **125 verified canonical** quotes (corpus-anchored)
- ✅ **22-field schema** per record (CI, NATO 4-axis, frame distribution, coalition, Δ)
- ✅ **v5.2-merged overlay**: verified_llm > verified_canonical > heuristic
- ✅ Deterministic seed=42, schema hash tracking

### Corpus (v6)
- ✅ 9 UNFCCC L-documents (Paris Art.7, COP25-COP30, FRLD)
- ✅ 5 national policy documents (KOR, BRA, USA, EU + 17국 brief)
- ✅ 1 coalition statement (G77, AOSIS, AILAC, EIG, HAC, Umbrella, AGN, LMDC)
- ✅ 25+ BibTeX entries
- ✅ 5 quantitative CSVs (ND-GAIN, PRIMAP CO2, OECD finance, CVF, COP delegation)
- ✅ TF-IDF inverted index (3,417 terms)
- ✅ SHA-256 manifest per document

### Embeddings (v7/v8.3)
- ✅ sentence-transformers paraphrase-multilingual-MiniLM-L12-v2 (384-dim)
- ✅ Gemini text-embedding-004 옵션 (모델 일관성)
- ✅ 215 vectors (90 corpus + 125 stance evidence)
- ✅ int16 양자화 (3.3x 압축)
- ✅ Cache-aware build (source hash invalidation)

### Query Engine (v2.4)
- ✅ **8 intents**: lookup, compare, trend, coalition, gap, recommendation, factoid, search
- ✅ **Hybrid search** (TF-IDF + semantic, α slider)
- ✅ **95% CI display** per stance
- ✅ **Multi-record citations** (up to 12)
- ✅ **Methodology footer** with hash for reproducibility
- ✅ Auto-attach corpus references to all responses
- ✅ v5.2-merged 우선 로드

### LLM Integration
- ✅ **3 providers**: Gemini, Anthropic, Groq (BYO key)
- ✅ **Stance extraction pipeline** (full 2,400-record run via --all)
- ✅ **Checkpoint resume**
- ✅ **Persistent SQLite cache** (Python) + **IndexedDB cache** (Browser)
- ✅ TTL 30 days, hit_count tracking, --stats / --clear CLI
- ✅ Multi-turn memory in browser (last 5 turns to prompt)
- ✅ Theoretical grounding (Hood/Howlett/Tallberg/Putnam) enforced

### Web UI (v2.4)
- ✅ **🇰🇷 한국어 ↔ 🇬🇧 EN i18n** (data-i18n + JS auto-update)
- ✅ All HTML labels + builder responses + status pill i18n-aware
- ✅ Inline SVG charts (CI bar, NATO 4-axis bar, sparkline, gap bar)
- ✅ Mini chart toolbox: svgSparkline, svgNatoBar, svgHBars, svgCIBar
- ✅ Citation panel (expandable)
- ✅ Export: Markdown / JSON / BibTeX
- ✅ α slider (keyword↔semantic 비율)
- ✅ Cache stats display + clear button
- ✅ Mobile-responsive

### Evaluation
- ✅ **Krippendorff α framework** (interval + bias correction)
- ✅ **Cross-LLM α** measurement script (5-provider)
- ✅ **External coder tool** (web form + CSV aggregator)
- ✅ Hypergeometric chance baseline
- ✅ 1000-run permutation test for modularity

### Testing & CI
- ✅ **40 pytest tests** (21s, 100% pass)
  - 17 query engine, 7 alpha, 7 merge, 6 corpus, 5 cache
- ✅ pytest.ini with slow/network/llm markers
- ✅ **GitHub Actions workflow** (4 jobs: tests + freshness + cert + integrity)
- ✅ conftest.py fixtures

### Reproducibility
- ✅ **58-entry SHA-256 chain hash certificate**
- ✅ Categories: dataset / corpus / embeddings / scripts / tests / docs
- ✅ `--verify` mode for external validators
- ✅ Cache invalidation across all build stages

### Documentation
- ✅ `docs/api/README.md` — ~600 lines API reference
- ✅ `CHANGELOG_v5.md` ~ `CHANGELOG_v10.md` (6 versions)
- ✅ `data/corpus/README.md` — corpus overview
- ✅ `CLAUDE.md` — project context

---

## 🚀 Live Entry Points

### Web (GitHub Pages, 자동 빌드 1-2분)

| URL | 기능 |
|-----|------|
| https://zxsa0716.github.io/cina/ | 메인 랜딩 |
| https://zxsa0716.github.io/cina/web/cina_program_v2.html | Q&A v2.4 (i18n + cache + α slider) |
| https://zxsa0716.github.io/cina/web/corpus_browser.html | Corpus 21-doc explorer |
| https://zxsa0716.github.io/cina/web/coder_tool.html | External coder input form |
| https://zxsa0716.github.io/cina/web/sitemap.html | Sitemap |

### Python (CLI)

```bash
# Q&A (full pipeline)
python -m src.program.query_engine_v2 "your question"
python -m src.program.query_engine_v2 --demo

# Build chain (cache-aware)
python -m src.data.rebuild_if_stale          # rebuild stale only
python -m src.data.rebuild_if_stale --check  # report only

# Real LLM extraction (BYO key)
export GEMINI_API_KEY=...
python -m src.program.llm_stance_extractor --provider gemini --all
python -m src.data.merge_v5_llm              # overlay merge

# Evaluation
python -m src.eval.cross_llm_alpha --n 78 --providers gemini,anthropic,groq
python -m src.eval.external_coder_alpha --csvs c1.csv,c2.csv,c3.csv

# Reproducibility
python -m src.data.build_reproducibility_certificate
python -m src.data.build_reproducibility_certificate --verify

# Tests
python -m pytest tests/ -v
```

---

## 📈 Version History

| Version | 주요 contribution |
|---------|-------------------|
| **v4.1** | BYO LLM activation + 900 records + 4 figures |
| **v5.0** | 2,400 records + 7-intent engine + 50국 + 8 이슈 |
| **v5.1** | 125 verified evidence quotes (10 → 125) |
| **v5.2** | LLM overlay merge policy |
| **v6.0** | 21-document corpus + TF-IDF search + auto-attach |
| **v7.0** | Semantic embeddings (sentence-transformers, 215 vectors) |
| **v8.0** | LLM extraction pipeline + Cross-LLM α + Gemini embed + α slider + cache-aware build |
| **v9.0** | Overlay merge + SQLite cache + 40 pytest + CI + cert + i18n + API docs |
| **v10.0** | IndexedDB browser cache + full i18n coverage + system completion |

---

## 🎯 Outstanding Items (optional v11+)

이 항목들은 시스템 완성을 막지 않으나 향후 가능한 확장:

- 실제 KEI/KAIST/MOFA 외부 코더 3명에게 coder_tool 배포 후 α 측정
- arXiv preprint 실제 업로드 (paper/arxiv/ 패키지 완성됨)
- COP31 prospective ingestion (2026.11)
- semantic embedding cross-model alignment (Voyage AI / OpenAI 추가)
- Persistent LLM cache → server-side shared cache (현재는 per-user)

---

## 📞 Contact

Heedo Choi (최희도)
국민대학교 일반대학원 기후기술융합학과
zxsa0716@kookmin.ac.kr
https://github.com/zxsa0716/cina

---

# 🏁 끝.

5-layer architecture, 18 Python modules, 5 web pages, 40 unit tests passing,
4-job CI, 58-entry reproducibility certificate, bilingual UI, IndexedDB cache,
hybrid semantic+keyword search, SQLite LLM cache, deterministic build chain.

시스템 완성.
