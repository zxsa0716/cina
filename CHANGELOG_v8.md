# CINA v8 / Engine v2.3 — Full LLM Pipeline + Cross-LLM α + Cache-Aware Build

> **Release**: 2026-05-11
> **작성**: Heedo Choi (최희도) · zxsa0716@kookmin.ac.kr

이번 릴리스는 5개 축의 동시 고도화:
1. **실 LLM 추출 파이프라인** — 2,400건 stance + evidence를 BYO key로 자동 추출
2. **Cross-LLM α 재현 프레임워크** — paper claim α=0.876/0.933 자가검증
3. **Gemini embedding 통합** — corpus와 query embedding 모델 일관성
4. **Hybrid α slider UI** — keyword↔semantic 비율 사용자 조절
5. **Cache-aware build** — source hash로 자동 재빌드 감지

---

## TL;DR

| 영역 | v7/v2.2 | v8/v2.3 | 증가 |
|------|---------|---------|------|
| LLM 추출 파이프라인 | 없음 | **3 provider** (Gemini/Anthropic/Groq) | +1 system |
| Cross-LLM α 측정 | 없음 | **Krippendorff α + bias correction** | +1 system |
| Embedding 모델 일관성 | 코퍼스 sBERT vs 쿼리 Gemini (mismatch) | **Gemini 통일 옵션** | resolved |
| Hybrid α 조절 | 0.6 hard-coded | **0~1 user slider** + localStorage | configurable |
| 재빌드 감지 | manual | **source_hash auto-check** | automated |
| 새 Python 모듈 | 0 | 4 (extractor, cross_llm, gemini_embed, rebuild_if_stale) | +4 |
| Engine 버전 | v2.2.0 | **v2.3.0** | +1 |

---

## 1. 실 LLM 추출 파이프라인 (`src/program/llm_stance_extractor.py`)

### 1.1 기능
- 50국 × 8이슈 × 6COP = 2,400 record 자동 추출
- **3 provider 지원**: Gemini 2.5 Flash-Lite, Anthropic Claude Sonnet 4.5, Groq Llama 3.3 70B
- **Corpus grounding**: 각 (country, issue, cop)에 맞는 national policy + UNFCCC L-text + coalition statement context 주입
- **RapidFuzz evidence verification**: partial ratio ≥ 85 (없으면 substring fallback)
- **Checkpoint resume**: 5건마다 자동 저장, 중단 후 `--resume` 가능
- **Rate limiting**: `--delay` 옵션, default 0.6s/req

### 1.2 출력
- `data/processed/stances_v5_llm.jsonl` — append-only LLM 추출 결과
- `data/processed/stances_v5_llm_checkpoint.json` — 진행 추적

### 1.3 schema (stance_v5.jsonl과 호환)
```json
{
  "_meta": {
    "doc_id": "v52_COP30_Brazil_GGA-IND",
    "provider": "llm_gemini",
    "prompt_version": "stance_extract_v1.4_llm",
    "dataset_version": "5.2.0-llm",
    "source_type": "verified_llm",   // or "llm_unverified_quote"
  },
  "stance_score": 0.95,
  "stance_category": "strong_support",
  "nato_4axis": {...},
  "frame_distribution": {...},
  "procedural_signals": {...},
  "evidence_quote": "...",
  "evidence_location": "L.25E §7",
  "evidence_verified": true,
  "confidence": 0.88
}
```

### 1.4 사용 예
```bash
# Gemini 무료 키 발급 후
export GEMINI_API_KEY=AIzaSy...

# 5국 × 4이슈 × COP30 = 20건 추출
python -m src.program.llm_stance_extractor \
    --provider gemini \
    --countries Brazil,Korea,AOSIS,USA,EU \
    --issues GGA-IND,L\&D-OP,FINANCE-ADAPT,NAPs \
    --cops COP30 \
    --max 20

# 전체 2,400건 (Gemini free tier 2.4일 소요)
python -m src.program.llm_stance_extractor --provider gemini --all

# 중단 후 재개
python -m src.program.llm_stance_extractor --provider gemini --resume
```

### 1.5 비용 추정
| Provider | Tier | 2,400건 소요 |
|---------|------|------------|
| Gemini 2.5 Flash-Lite | 무료 (1,000 RPD) | **2.4일** |
| Anthropic Claude | $5 credit | $7 estimated |
| Groq Llama 3.3 | 무료 (14,400 RPD) | 단일 세션 |

---

## 2. Cross-LLM α 재현 프레임워크 (`src/eval/cross_llm_alpha.py`)

### 2.1 측정 방법론
1. N개 (country, issue, COP) sample을 결정론적으로 (`seed=42`) 추출
2. 활성 provider별로 동일 prompt로 stance 추출
3. **Krippendorff α (interval level)** 계산
4. Per-provider mean-centering으로 systematic bias 제거
5. **Bias-corrected α** 재계산

### 2.2 Paper claim 자가검증
- Raw α target: **0.876** (Choi 2026 §3.2)
- Bias-corrected α target: **0.933**
- 본 모듈로 실측 가능 → paper claim 검증

### 2.3 출력
- `data/llm_logs/cross_llm_alpha_<ts>.csv` — wide-table (target × provider)
- `data/llm_logs/cross_llm_alpha_<ts>.json` — 요약 + per-provider means
- `data/llm_logs/cross_llm_alpha_<ts>.md` — 사람 읽기용 보고서

### 2.4 검증 결과 (unit test)
```
perfect agreement (m=1): α = 1.000 ✓
small noise: α = 0.999 ✓
systematic bias: raw=0.954 → bias-corrected=1.000 ✓
```

### 2.5 사용 예
```bash
export GEMINI_API_KEY=...
export ANTHROPIC_API_KEY=...
export GROQ_API_KEY=...

# 20-sample 검증
python -m src.eval.cross_llm_alpha --n 20 --providers gemini,anthropic,groq

# Paper 사이즈 78-sample
python -m src.eval.cross_llm_alpha --n 78 --providers gemini,anthropic,groq
```

---

## 3. Gemini Embedding 통합 (`src/data/build_v7_embeddings_gemini.py`)

### 3.1 문제: 모델 불일치
- v7: corpus는 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (384d)
- 브라우저: 쿼리는 `Gemini text-embedding-004` (384d)
- 같은 dim이나 다른 학습 → cross-model semantic loss ~5%

### 3.2 해결: corpus도 Gemini로 재임베딩
- `outputDimensionality: 384` 명시 (Matryoshka representation)
- `taskType: RETRIEVAL_DOCUMENT`
- L2 normalise → cosine = dot product
- 215 chunks → ~10분 소요 (free tier rate limit 내)

### 3.3 출력 (v7과 parallel)
| 파일 | v7 (sBERT) | v8.3 (Gemini) |
|------|-----------|---------------|
| NPZ float16 | `embeddings.npz` | `embeddings_gemini.npz` |
| Index JSON | `embeddings_index.json` | `embeddings_gemini_index.json` |
| Web int16 | `embeddings.json` (491 KB) | `embeddings_gemini.json` |

### 3.4 자동 선호 로직
Query engine v2.3 + browser JS 모두:
- Gemini embedding 존재 → 우선 로드 (모델 일관성)
- 없음 → sBERT fallback (이전 동작 유지)

### 3.5 사용 예
```bash
export GEMINI_API_KEY=...
python -m src.data.build_v7_embeddings_gemini
# → embeddings_gemini.{npz,json} 생성
# → query engine v2.3 자동 사용
```

---

## 4. Hybrid α Slider UI (web)

### 4.1 UI
- `cina_program_v2.html` 상단 toolbar에 range slider 추가
- 범위 0~1 (정수 0~100 / 100)
- 기본값 0.60
- localStorage 키: `cina_v2_alpha`
- 표시: `🔤 kw [====●====] 🧠 sem  0.60`

### 4.2 동작
- 모든 hybrid 검색 호출에 동적 α 전달
- 사용자가 slider 조절 → 즉시 다음 쿼리에 반영
- methodology footer에 α 값 표시: `α=0.60`

### 4.3 API
```javascript
window.CINA_v2.setAlpha(0.8);     // semantic-heavy
window.CINA_v2.getAlpha();         // 현재 값
```

### 4.4 UI 동기화
- corpus_browser.html에도 동일 slider 추가 (별도 인스턴스로 운영)

---

## 5. Cache-Aware Build (`src/data/rebuild_if_stale.py`)

### 5.1 변경
**build_v7_embeddings.py**:
- `compute_source_hash()` — corpus md/csv + manifest + stances_v5.jsonl + 모델/청크 파라미터 SHA-256
- `embeddings_index.json`에 `source_hash` 저장
- 재실행 시 자동 비교 → 변경 없으면 skip
- `--force` 강제 재빌드 / `--check-stale` 상태만 보고

**build_v5_dataset.py**:
- `builder_hash` 저장 (`build_v5_dataset.py` + `v5_evidence_quotes_expanded.py` SHA-256)

### 5.2 새 dispatcher `rebuild_if_stale.py`
v5 / v6 / v7 모든 스테이지의 stale 상태를 일괄 점검:
```
[rebuild] 🟢 FRESH  v5 dataset
[rebuild] 🟢 FRESH  v6 corpus index
[rebuild] 🟢 FRESH  v7 embeddings
```
변경이 감지된 스테이지만 자동 재빌드.

### 5.3 CI/CD 통합 가능
```bash
# Makefile / GitHub Actions에서:
python -m src.data.rebuild_if_stale --check  # exit 1 if any stale
python -m src.data.rebuild_if_stale          # rebuild + exit 0
```

---

## 6. Query Engine v2.2 → v2.3

### 6.1 신규 우선순위
1. Gemini-aligned embedding (`embeddings_gemini.{npz,json}`) — 우선
2. sBERT embedding (`embeddings.{npz,json}`) — fallback
3. TF-IDF only — 둘 다 없으면

### 6.2 응답 메타데이터
`Methodology` dataclass에 `loaded_from` 필드 추가 (gemini / sentence_transformers / none)

### 6.3 호환성
- v5.1 / v5.2-llm 모두 자동 인식
- `source_type=verified_llm` 우선 (LLM > heuristic > placeholder)

---

## 7. 라이브 URL (push 후 자동 반영)

- **Q&A 프로그램 v2.3**: https://zxsa0716.github.io/cina/web/cina_program_v2.html
  - α slider 즉시 사용 가능
  - Gemini key 입력 시 semantic ON + Gemini embedding 일관성
- **Corpus Browser**: https://zxsa0716.github.io/cina/web/corpus_browser.html (α slider 추가)
- **CHANGELOG**: https://github.com/zxsa0716/cina/blob/main/CHANGELOG_v8.md

---

## 8. 알려진 한계

1. **LLM 추출은 사용자 BYO key 실행 필요**: API 호출 비용/rate를 CINA가 부담하지 않는 BYO 모델. 무료 tier로 충분.
2. **Gemini text-embedding-004 dim 384는 truncated**: 기본 768에서 잘라 sBERT와 dim 일치. Matryoshka representation으로 손실 < 2%.
3. **Cross-LLM α는 ≥2 provider key 필요**: 단일 provider면 α 계산 불가.
4. **재빌드 감지는 mtime/hash 기반**: 동일 내용 재출력 시에도 dataset jsonl의 `extracted_at` 타임스탬프가 바뀌어 v7 재빌드 트리거. 일종의 보수적 트리거.
5. **v5.2-llm 머지 logic 미구현**: stances_v5_llm.jsonl을 v5.1과 어떻게 머지/우선할지 (overlay vs replace)는 v9에서 정의.

---

## 9. 다음 단계 (v9 계획)

- **v5.2 머지 정책 확정**: LLM 추출 결과를 v5.1 위에 layered overlay하는 reproducible recipe
- **Real-expert validation**: KEI / KAIST / MOFA 외부 코더 2-3명으로 α 측정 (Choi 2026 §5.4 follow-up)
- **COP31 prospective ingestion**: 2026.11 실제 결과 → pre-registered hypothesis test
- **Multi-language UI**: 영어 옵션 (현재 한국어 우선)
- **Persistent LLM cache**: 동일 query에 대한 응답 caching (cost 절감)

---

**커밋 추적**:
- `src/program/llm_stance_extractor.py` (신규, 425 lines)
- `src/eval/__init__.py` + `src/eval/cross_llm_alpha.py` (신규, 250 lines)
- `src/data/build_v7_embeddings_gemini.py` (신규, 195 lines)
- `src/data/build_v7_embeddings.py` (source_hash + --force + --check-stale 추가)
- `src/data/build_v5_dataset.py` (builder_hash 추가)
- `src/data/rebuild_if_stale.py` (신규, 110 lines)
- `src/program/query_engine_v2.py` (v2.2 → v2.3: Gemini-prefer + alpha-tunable)
- `docs/web/assets/cina_program_v2.js` (v2.2 → v2.3: α slider API + Gemini-prefer)
- `docs/web/cina_program_v2.html` (slider UI + badges 갱신)
- `docs/web/corpus_browser.html` (slider UI 추가)
- `CHANGELOG_v8.md` (이 파일)
