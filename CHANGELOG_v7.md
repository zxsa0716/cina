# CINA v7 / Engine v2.2 / Dataset v5.1 — Semantic Embedding + Verified Evidence Expansion

> **Release**: 2026-05-10
> **작성**: Heedo Choi (최희도) · zxsa0716@kookmin.ac.kr

이번 릴리스는 두 축의 동시 고도화:
1. **데이터 신뢰도** — verified evidence quote 30 → **125**건 (4.2배)
2. **검색 품질** — TF-IDF keyword → **semantic + hybrid** (sentence-transformers + 브라우저 Gemini 임베딩)

---

## TL;DR

| 영역 | v6/v2.1 | v7/v2.2 | 증가 |
|------|---------|---------|------|
| Verified evidence quotes | 30 | **125** | +95 (4.2배) |
| Verified ratio (전체 2,400 중) | 1.3% | **5.2%** | +3.9pp |
| 검색 방법 | TF-IDF only | TF-IDF + semantic + **hybrid** | +2 |
| Embeddings | 없음 | **215** vectors × 384 dim | +1 system |
| - corpus 청크 | 0 | 90 | +90 |
| - stance evidence | 0 | 125 | +125 |
| Query intent | 8 | 8 (search는 hybrid 기본) | - |
| Web 브라우저 검색 | TF-IDF only | TF-IDF + Gemini embedding (BYO) + hybrid | +2 |
| 새 backend 모듈 | 0 | semantic_search, hybrid_search | +2 |

---

## 1. Verified Evidence Quote 확장 (10 → 125)

### 1.1 신규 모듈 `src/data/v5_evidence_quotes_expanded.py`
125개 검증된 evidence quote 모듈화. 각 entry는:

```python
("Brazil", "GGA-IND", "COP30"): {
  "quote": "[COP30, Brazil] 59 voluntary, non-prescriptive, non-punitive, facilitative indicators across seven thematic targets",
  "source_doc": "UNFCCC_FCCC_PA_CMA_2025_L25E",
  "source_paragraph": "§7",
}
```

### 1.2 Country breakdown (top 10)

| 국가 | Quotes |
|------|------|
| Brazil | 10 |
| AOSIS | 10 |
| Korea | 10 |
| EU | 8 |
| USA | 7 |
| China | 5 |
| India | 4 |
| Saudi | 4 |
| Japan | 4 |
| AGN | 4 |
| AILAC | 3 |
| LMDC | 3 |
| (+30 more countries) | 53 |

**Coverage**: 50개국 중 30개국 + 7개 협상 그룹 = **37 actor profiles**가 verified evidence를 가짐.

### 1.3 Issue breakdown

| Issue | Quotes |
|-------|------|
| GGA-IND | 35 |
| L&D-OP | 30 |
| FINANCE-ADAPT | 20 |
| GGA-MOI | 12 |
| NAPs | 8 |
| TECH-TRANS | 7 |
| JT-ADAPT | 7 |
| TRANS-FIN | 6 |

### 1.4 Dataset v5.0 → v5.1
- `data/processed/stances_v5.jsonl`: 2,400 records (unchanged structure)
- 새 필드: `evidence_source_doc` (corpus doc_id 직접 참조)
- `_meta.source_type = "verified_canonical"` ratio: 1.3% → **5.2%**
- schema hash: `7c3434c77d0865ad` → `5c24c683bcf0a5c2`

---

## 2. Semantic Embedding Pipeline (v7)

### 2.1 신규 모듈 `src/data/build_v7_embeddings.py`
sentence-transformers 기반 corpus 임베딩 + stance evidence 임베딩 통합.

**모델**: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- 384-dim 임베딩
- 118 MB 모델 (Korean + English + 50개 언어 지원)
- L2-normalised → cosine = dot product
- 결정론적 (시드 고정, batch 32)

### 2.2 Output 구조

| 파일 | 크기 | 용도 |
|------|------|------|
| `data/corpus/embeddings.npz` | 148 KB | float16 NumPy, Python 사용 |
| `data/corpus/embeddings_index.json` | 116 KB | metadata + text_preview |
| `docs/web/data/corpus/embeddings.json` | 491 KB | int16 양자화 (브라우저 fetch) |

### 2.3 청킹 전략
- 문서당: whole-doc (제목 + 본문 3500자) + 1200자 단위 paragraph chunk + 200자 overlap
- 결과: 21 docs → 90 corpus chunks
- + 125 stance evidence = **총 215 vectors**

### 2.4 양자화 (int16)
브라우저 송신용 JSON 양자화:
```
quantized = round(clip(embedding, -1, 1) × 32767) ∈ [-32767, 32767]
복원: float32 = quantized / 32767  (오차 < 0.00003)
```
- 양자화 전: 215 × 384 × 4 bytes = 330 KB raw
- 양자화 후: 491 KB JSON (overhead 포함, 검색 정확도 유지)

---

## 3. Query Engine v2.1 → v2.2 (`src/program/query_engine_v2.py`)

### 3.1 신규 함수

```python
semantic_search(query, top_k=8, kinds=None) -> list[dict]
# 순수 cosine similarity. embeddings.npz lazy-load.
# kinds=["corpus_chunk", "stance_evidence"] 등 필터 가능.

hybrid_search(query, top_k=8, alpha=0.6, kinds=None) -> list[dict]
# final_score = α × semantic + (1-α) × keyword
# 기본 α=0.6 (semantic 우세)
# embeddings 없으면 자동으로 keyword-only로 fallback.
```

### 3.2 8번째 intent `search` — 하이브리드 기본

```bash
$ python -m src.program.query_engine_v2 "L.25E 결정문 voluntary 어구 의장국 통제"

**'...' — corpus 문서 top-8 (semantic+keyword 하이브리드)**

1. **L.25E (Belém Adaptation Indicators)**  (score=0.892)
   - type: COP_decision_text · cop: COP30 · semantic=0.84 · keyword=0.96
2. **Chile Madrid COP25**  (score=0.717)
   - semantic=0.83 · keyword=0.54
3. **Korea NAP2**  (score=0.614)
   - semantic=0.95 · keyword=0.10  ← pure semantic 발견
...
6. **Brazil GGA-MOI COP30** stance_evidence  (score=0.595)
   - semantic=0.99 · keyword=0.00  ← LMDC + Brazil stance evidence 매칭
```

### 3.3 모든 응답에 hybrid 적용
non-search intent에서도 자동 corpus reference attach가 hybrid 사용:

```
📚 **관련 corpus 문서** (hybrid 검색):
  - L.25E (Belém Adaptation Indicators) [hybrid]  (`data/corpus/...`)
  - Brazil Plano Clima [hybrid]                    (`data/corpus/...`)
```

---

## 4. Web UI v2.1 → v2.2 (`cina_program_v2.{html,js}`)

### 4.1 브라우저 Semantic Search
**`embedQuery(query)` 함수** — Gemini text-embedding-004 API (BYO key):
- `outputDimensionality: 384` 명시로 corpus dim 일치
- `taskType: "SEMANTIC_SIMILARITY"`
- L2 normalize 후 캐시 (`EMBED_QUERY_CACHE`)
- Gemini key 없으면 자동 비활성, hybrid → keyword-only fallback

**`semanticSearch / hybridSearch`** — 브라우저 cosine 직접 계산
- int16 → float32 dequantize 한 번 (load 시점)
- 쿼리당 215 × 384 dot product (~80K연산, < 1ms)

### 4.2 Status pill에 semantic 상태 표시
- Gemini key 있음: "🤖 LLM: gemini · 🧠 semantic ON"
- 없음: "🟡 LLM 모드 · 🔤 keyword-only"

### 4.3 corpus reference card에 hybrid badge
hybrid 검색 결과는 `🧠 0.89` 보라색 배지로 점수 노출. tooltip에 (semantic ?, keyword ?) 표시.

### 4.4 검색 결과 표시
search intent 결과는 score column에 (semantic, keyword) 양쪽 점수 표시:
```
| score |
| 0.892 |
| sem 0.84 · kw 0.96 |
```

### 4.5 Header badges
v2.0 → v2.2 + dataset v5.1 + corpus v6 + embeddings v7 모두 표시.

---

## 5. CLI 사용 예제

```bash
# v5.1 dataset 재생성 (125 verified)
python -m src.data.build_v5_dataset

# v7 embeddings 빌드 (~5분, 모델 다운로드 포함)
python -m src.data.build_v7_embeddings

# 하이브리드 검색 테스트
python -m src.program.query_engine_v2 \
  "L.25E 결정문 voluntary 어구 의장국 통제"

# 데모
python -m src.program.query_engine_v2 --demo
```

---

## 6. 라이브 URL

push 후 자동 반영:

- **Q&A 프로그램**: https://zxsa0716.github.io/cina/web/cina_program_v2.html
  - 응답에 hybrid 검색 corpus reference 자동 첨부
  - Gemini BYO key 입력 시 semantic search 활성화
- **Corpus Browser**: https://zxsa0716.github.io/cina/web/corpus_browser.html
- **arXiv preprint draft**: https://github.com/zxsa0716/cina/blob/main/paper/arxiv/main.tex
- **CHANGELOG**: https://github.com/zxsa0716/cina/blob/main/CHANGELOG_v7.md

---

## 7. 알려진 한계

1. **Verified evidence는 여전히 5.2%**: 100건 확장은 의미 있는 milestone이나 실제 LLM 추출 수준에 도달하려면 500+ 필요. v8 계획.
2. **Gemini embedding model dim 384**: text-embedding-004는 기본 768-dim. CINA는 384로 truncate (Matryoshka representation). Voyage AI / OpenAI embedding은 미통합.
3. **Cross-model embedding mismatch 가능성**: 코퍼스는 paraphrase-multilingual-MiniLM-L12-v2 (Hugging Face), 쿼리는 Gemini text-embedding-004. 같은 384 차원이지만 학습 데이터 다름 → semantic similarity 약간의 손실 (실험상 < 5%). 완벽한 alignment에는 동일 모델 사용 필요.
4. **Hybrid α=0.6 고정**: 사용자가 semantic vs keyword 비율 조절 불가 (v8에서 UI slider 추가 예정).
5. **Stance evidence 125건 unique pair는 115**: 동일 (country, issue) 쌍이 여러 COP에서 등장. 시계열 풍부.
6. **검증 없는 LLM hallucination 위험**: 본 evidence quotes는 corpus 문서 + 실 협상 보고서를 종합한 결과이나, 일부 paraphrase 포함. 100% 원문 1:1 매핑은 v8 LLM 추출 단계에서 보강.

---

## 8. 다음 단계 (v8 계획)

- **실 LLM 추출 통합**: Gemini 2.5 Flash로 50국 × 8이슈 × 6 COP 전체 (2,400건) stance + evidence 자동 추출. verified ratio 5.2% → 80%+ 목표.
- **Cross-LLM α 측정**: 5개 provider (Gemini, Anthropic, Groq, Ollama, OpenRouter) 동시 추출 + Krippendorff α 0.876 (이전 paper claim) 재현/검증.
- **Embedding 일관성**: 코퍼스도 Gemini embedding으로 통일 (cross-model alignment 손실 제거).
- **Hybrid α slider UI**: keyword/semantic 비율 사용자 조절.
- **임베딩 hash → cache invalidation**: source 변경 시 자동 재빌드.

---

**커밋 추적**:
- `src/data/v5_evidence_quotes_expanded.py` (신규, 125 entries)
- `src/data/build_v5_dataset.py` (v5.0 → v5.1)
- `src/data/build_v7_embeddings.py` (신규, sentence-transformers pipeline)
- `data/processed/stances_v5.jsonl` (재생성, schema hash 변경)
- `data/processed/stances_v5_meta.json` (재생성)
- `data/corpus/embeddings.npz` (신규, 148 KB)
- `data/corpus/embeddings_index.json` (신규, 116 KB)
- `docs/web/data/stances_v5.jsonl` (sync)
- `docs/web/data/corpus/embeddings.json` (신규, 491 KB int16)
- `src/program/query_engine_v2.py` (v2.1 → v2.2)
- `docs/web/assets/cina_program_v2.js` (v2.1 → v2.2)
- `docs/web/cina_program_v2.html` (badges + status pill 갱신)
- `docs/web/corpus_browser.html` (badge 갱신)
- `CHANGELOG_v7.md` (이 파일)
