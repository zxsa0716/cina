# 📘 CINA API Reference

> **Version**: v2.4.0 (engine) · v5.2-merged (dataset) · v6 (corpus) · v7/v8.3 (embeddings)
> **Last updated**: 2026-05-12

Comprehensive reference for both Python backend modules and browser JavaScript API.

---

## 📑 Contents

- [Python API](#python-api)
  - [Query Engine v2 (`src.program.query_engine_v2`)](#query-engine-v2)
  - [LLM Cache (`src.program.llm_cache`)](#llm-cache)
  - [LLM Stance Extractor (`src.program.llm_stance_extractor`)](#llm-stance-extractor)
  - [Cross-LLM α (`src.eval.cross_llm_alpha`)](#cross-llm-α)
  - [External Coder α (`src.eval.external_coder_alpha`)](#external-coder-α)
  - [Dataset Builders](#dataset-builders)
  - [Reproducibility Certificate](#reproducibility-certificate)
- [Browser JavaScript API (`window.CINA_v2`)](#browser-javascript-api)
- [Data Schemas](#data-schemas)
- [CLI Commands Cheatsheet](#cli-commands-cheatsheet)

---

## 🐍 Python API

### Query Engine v2

`src.program.query_engine_v2`

The main Q&A backend. Loads dataset + corpus + embeddings, parses intent, retrieves, builds response.

#### Top-level functions

```python
from src.program.query_engine_v2 import answer_question, parse_intent

# One-shot Q&A
resp = answer_question("브라질 GGA-IND COP30 입장은?", k=24, seed=42)
print(resp.text)
print(resp.citations)         # list[Citation]
print(resp.methodology)       # Methodology dataclass
```

#### `answer_question(question: str, k: int = 24, seed: int = 42) -> Response`

Main entry. Returns a `Response` dataclass with:

| Field | Type | Description |
|-------|------|-------------|
| `text` | str | human-readable answer |
| `citations` | list[Citation] | evidence citations (max 12) |
| `viz_payload` | dict | structured data for visualisation |
| `intent` | QueryIntent | parsed intent |
| `matched_records` | int | how many records matched |
| `confidence` | float | 0-1 |
| `methodology` | Methodology | reproducibility footer |

#### `parse_intent(question: str) -> QueryIntent`

Heuristic Korean+English intent parser. Returns:
```python
@dataclass
class QueryIntent:
    type: str                  # "lookup"|"compare"|"trend"|"coalition"|"gap"|"recommendation"|"factoid"|"search"
    countries: list[str]
    issues: list[str]
    cop: Optional[str]
    raw_question: str
    relevance_keywords: list[str]
```

#### Retrieval functions

```python
from src.program.query_engine_v2 import (
    retrieve, corpus_search, semantic_search, hybrid_search, corpus_filter_by_context,
)

# Top-k stance records by relevance scoring
records = retrieve(intent, k=24)

# TF-IDF corpus search
hits = corpus_search("voluntary indicators chair", top_k=8)

# Semantic embedding search (requires v7 embeddings)
hits = semantic_search("브라질 의장국 통제", top_k=8, kinds=["corpus_chunk"])

# Hybrid (default α=0.6 semantic + 0.4 keyword)
hits = hybrid_search("L.25E 어구 통제", top_k=8, alpha=0.6)

# Context-based filter (country/issue/cop overlap)
hits = corpus_filter_by_context(intent)
```

---

### LLM Cache

`src.program.llm_cache` — SQLite-backed persistent cache for any LLM call.

```python
from src.program.llm_cache import cached_call, CacheStats

def gemini_call(prompt, key):  # provider-specific
    return ...

# Cache lookup → call if miss → store
response = cached_call(
    provider="gemini",
    model="gemini-2.5-flash-lite",
    prompt=prompt,
    api_key=key,
    call_fn=gemini_call,
    temperature=0.2,
    ttl_days=30,         # cache expiry
    skip_cache=False,
)

# Stats
print(CacheStats.snapshot())   # {hits, misses, hit_rate, writes, errors}
print(CacheStats.db_stats())   # {n_cached, total_lifetime_hits, per_provider}
```

CLI:
```bash
python -m src.program.llm_cache --stats   # show cache size
python -m src.program.llm_cache --clear   # delete all cached responses
```

---

### LLM Stance Extractor

`src.program.llm_stance_extractor` — real LLM stance extraction with corpus grounding.

```python
from src.program.llm_stance_extractor import extract_one, run, load_corpus_text

# Single record
record = extract_one("Brazil", "GGA-IND", "COP30", provider="gemini", api_key="...")

# Batch with checkpoint
n_ok, n_err = run(targets=[("Brazil","GGA-IND","COP30"), ...],
                  provider="gemini", api_key="...", max_n=20, delay_sec=0.6)
```

CLI:
```bash
# Subset
python -m src.program.llm_stance_extractor \
    --provider gemini --countries Brazil,Korea --cops COP30 --max 20

# Full 2,400
python -m src.program.llm_stance_extractor --provider gemini --all

# Resume
python -m src.program.llm_stance_extractor --provider gemini --resume
```

Output: `data/processed/stances_v5_llm.jsonl`

---

### Cross-LLM α

`src.eval.cross_llm_alpha` — measure inter-LLM reliability (paper claim α=0.876/0.933).

```python
from src.eval.cross_llm_alpha import krippendorff_alpha, bias_correct, sample_targets, run

# Pure function: α from matrix [n_units × n_coders]
matrix = [[0.5, 0.52], [-0.3, -0.28]]
alpha = krippendorff_alpha(matrix)         # interval-level α

# Bias correction (per-coder mean centring)
bc_matrix, meta = bias_correct(matrix)
alpha_bc = krippendorff_alpha(bc_matrix)
```

CLI:
```bash
export GEMINI_API_KEY=...
export ANTHROPIC_API_KEY=...
export GROQ_API_KEY=...
python -m src.eval.cross_llm_alpha --n 78 --providers gemini,anthropic,groq
```

---

### External Coder α

`src.eval.external_coder_alpha` — measure real human-coder reliability from CSV exports.

```bash
# After 3 coders use docs/web/coder_tool.html and export CSVs
python -m src.eval.external_coder_alpha \
    --csvs coder_park.csv,coder_lee.csv,coder_kim.csv
```

---

### Dataset Builders

```python
# v5.1 baseline dataset (50 × 8 × 6 = 2,400 records, 125 verified quotes)
python -m src.data.build_v5_dataset

# v6 corpus quantitative CSVs
python -m src.data.build_v6_quantitative

# v6 corpus manifest + TF-IDF search index
python -m src.data.build_v6_corpus_index

# v7 sentence-transformers embeddings
python -m src.data.build_v7_embeddings           # build if stale
python -m src.data.build_v7_embeddings --force   # force rebuild
python -m src.data.build_v7_embeddings --check-stale  # exit 0 fresh, 1 stale

# v8.3 Gemini-aligned embeddings (optional)
export GEMINI_API_KEY=...
python -m src.data.build_v7_embeddings_gemini

# v9.1 merge v5.1 heuristic + v5.2-llm into v5.2-merged
python -m src.data.merge_v5_llm

# Smart rebuild dispatcher
python -m src.data.rebuild_if_stale              # rebuild what's stale
python -m src.data.rebuild_if_stale --check      # report only
python -m src.data.rebuild_if_stale --force      # rebuild everything
```

---

### Reproducibility Certificate

`src.data.build_reproducibility_certificate` — chain hash over all build artefacts.

```bash
python -m src.data.build_reproducibility_certificate         # generate
python -m src.data.build_reproducibility_certificate --verify # compare to stored
```

Output:
- `data/reproducibility_certificate.json` — 58 entries with sha256 + chain hash
- `data/reproducibility_certificate.md` — human-readable summary

---

## 🌐 Browser JavaScript API

Available as `window.CINA_v2.*` after `cina_program_v2.js` is loaded.

```javascript
// Main Q&A entry
const result = await window.CINA_v2.answerQuestion(
  "브라질 GGA-IND COP30 입장은?",
  { mode: "llm", provider: "gemini" }
);
// result.html, .citations, .intent, .confidence, .n_retrieved, .source

// Intent parsing
const intent = window.CINA_v2.parseIntent("AOSIS GGA-IND 추이?");

// BYO LLM key management
window.CINA_v2.setKey("gemini", "AIzaSy...");
window.CINA_v2.getKey("gemini");
window.CINA_v2.clearKey("gemini");
window.CINA_v2.hasAnyKey();
window.CINA_v2.pickFirstAvailableProvider();

// Hybrid α slider (0=keyword, 1=semantic)
window.CINA_v2.setAlpha(0.8);
window.CINA_v2.getAlpha();

// Language toggle
window.CINA_v2.setLang("en");   // or "ko"
window.CINA_v2.getLang();
window.CINA_v2.translate("strong_support");

// Data loading
await window.CINA_v2.loadData();         // 2,400 stance records
await window.CINA_v2.loadCorpus();       // 21-doc manifest + TF-IDF
await window.CINA_v2.loadEmbeddings();   // v7/v8.3 embeddings

// Search functions
const hits = window.CINA_v2.corpusSearch("voluntary indicators", 8);
const sem = await window.CINA_v2.semanticSearch("브라질 통제", 8);
const hyb = await window.CINA_v2.hybridSearch("L.25E 어구", 8);

// History export
window.CINA_v2.exportMarkdown();
window.CINA_v2.exportJSON();
window.CINA_v2.exportBibTeX();
window.CINA_v2.getHistory();
window.CINA_v2.clearHistory();
```

---

## 📄 Data Schemas

### Stance record (`stances_v5.jsonl` and `stances_v5_merged.jsonl`)

```json
{
  "_meta": {
    "doc_id": "v5_COP30_Brazil_GGA-IND",
    "country": "Brazil", "issue": "GGA-IND", "cop": "COP30",
    "iso3": null,
    "extracted_at": "2026-05-09T...",
    "provider": "v5_canonical_extension",
    "k_samples": 5,
    "prompt_version": "stance_extract_v1.3",
    "dataset_version": "5.1.0",
    "source_type": "verified_canonical",
    "country_metadata": {"region": "LatAm", "income": "upper-mid", "ndgain": 65, ...},
    "overlay_history": [...]
  },
  "stance_score": 0.95,
  "stance_score_mean": 0.95,
  "stance_score_std": 0.04,
  "ci_lower_95": 0.87,
  "ci_upper_95": 1.00,
  "stance_category": "strong_support",
  "frame_type": "sovereignty",
  "frame_distribution": {"scientific":0.1, "justice":0.15, "sovereignty":0.45, "security":0.1, "development":0.2},
  "salience_score": 0.85,
  "nato_4axis": {"nodality":0.55, "authority":0.24, "treasure":0.16, "organization":0.30},
  "nato_axis_sum": 1.25,
  "procedural_signals": {"is_chair_role": true, "is_pen_holder": true, "drafts_text_for_issue": true},
  "procedural_composite": 1.0,
  "coalition_membership": {"primary":"G77+China", "all":["G77+China"]},
  "translation_gap_delta": 0.0,
  "domestic_stance_proxy": 1.0,
  "evidence_quote": "[COP30, Brazil] 59 voluntary, non-prescriptive, ...",
  "evidence_location": "§7",
  "evidence_source_doc": "UNFCCC_FCCC_PA_CMA_2025_L25E",
  "confidence": 0.88
}
```

### Corpus manifest record (`data/corpus/manifest.jsonl`)

```json
{
  "path": "data/corpus/unfccc_decisions/COP30_L25E_GGA_indicators.md",
  "doc_id": "UNFCCC_FCCC_PA_CMA_2025_L25E",
  "title": "Belém Adaptation Indicators...",
  "short_title": "L.25E (Belém Adaptation Indicators)",
  "type": "COP_decision_text",
  "cop": "COP30", "country": null,
  "issues_addressed": ["GGA-IND"],
  "language": "en",
  "license": "UN Open License",
  "official_url": "https://unfccc.int/...",
  "adoption_date": "2025-11-21",
  "sha256": "...",
  "size_bytes": 4521,
  "n_tokens": 845,
  "category_dir": "unfccc_decisions"
}
```

### Embedding record (`embeddings_index.json` → `items[]`)

```json
{
  "row": 0,
  "id": "UNFCCC_FCCC_PA_CMA_2025_L25E::chunk_0",
  "kind": "corpus_chunk",
  "doc_id": "UNFCCC_FCCC_PA_CMA_2025_L25E",
  "title": "Belém Adaptation Indicators ...",
  "path": "data/corpus/unfccc_decisions/COP30_L25E_GGA_indicators.md",
  "type": "COP_decision_text",
  "cop": "COP30", "country": null,
  "chunk_idx": 0,
  "text_preview": "FCCC/PA/CMA/2025/L.25E — Belém Adaptation Indicators decision ..."
}
```

---

## 🛠 CLI Commands Cheatsheet

```bash
# Build chain (in order)
python -m src.data.build_v5_dataset                  # 2,400 stance records
python -m src.data.build_v6_quantitative             # 5 CSVs
python -m src.data.build_v6_corpus_index             # manifest + TF-IDF
python -m src.data.build_v7_embeddings               # sBERT embeddings (~5 min)

# Optional
export GEMINI_API_KEY=...
python -m src.data.build_v7_embeddings_gemini        # Gemini-aligned (~10 min)
python -m src.program.llm_stance_extractor --all     # full LLM extraction (~2 days)
python -m src.data.merge_v5_llm                      # overlay merge

# Verification
python -m src.data.rebuild_if_stale --check          # build freshness
python -m src.data.build_reproducibility_certificate --verify  # hash chain
python -m pytest tests/ -v                           # 40 unit tests

# Q&A
python -m src.program.query_engine_v2 --demo
python -m src.program.query_engine_v2 "your question here"

# Krippendorff α
python -m src.eval.cross_llm_alpha --n 78 --providers gemini,anthropic,groq
python -m src.eval.external_coder_alpha --csvs c1.csv,c2.csv,c3.csv
```

---

## 📞 Contact

Heedo Choi (최희도) — Kookmin University Department of Climate Technology Convergence
zxsa0716@kookmin.ac.kr · github.com/zxsa0716/cina
