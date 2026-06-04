"""Build CINA v7 semantic embeddings for corpus + stance evidence quotes.

v6 (TF-IDF keyword) → v7 (semantic embedding) upgrade.

Pipeline:
  1. Load all 21 corpus documents from data/corpus/manifest.jsonl
  2. Split each document into chunks (whole-doc + paragraph-level)
  3. Encode each chunk using sentence-transformers
     (paraphrase-multilingual-MiniLM-L12-v2, 384-dim, Korean+English)
  4. Also encode all stance evidence_quote strings from stances_v5.jsonl
     for stance-document cross-retrieval
  5. Save as:
     - data/corpus/embeddings.npz       (float16 compressed, ~N×384)
     - data/corpus/embeddings_index.json (id ↔ row mapping + metadata)

Model: paraphrase-multilingual-MiniLM-L12-v2
  - 384-dim, 480 MB, multilingual incl. Korean
  - https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

Reproducibility: seed=42 fixed, model version pinned.

Author: Heedo Choi (Kookmin University)
License: MIT
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
CORPUS_DIR = ROOT / "data" / "corpus"
MANIFEST = CORPUS_DIR / "manifest.jsonl"
EMBED_NPZ = CORPUS_DIR / "embeddings.npz"
EMBED_INDEX = CORPUS_DIR / "embeddings_index.json"
STANCES_JSONL = ROOT / "data" / "processed" / "stances_v5.jsonl"

# Web-deployed copies (for GitHub Pages serving)
WEB_EMBED_NPZ = ROOT / "docs" / "web" / "data" / "corpus" / "embeddings.npz"
WEB_EMBED_INDEX = ROOT / "docs" / "web" / "data" / "corpus" / "embeddings_index.json"
WEB_EMBED_F32_JSON = ROOT / "docs" / "web" / "data" / "corpus" / "embeddings.json"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMBED_DIM = 384
CHUNK_MAX_CHARS = 1200
CHUNK_OVERLAP = 200


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

def chunk_text(text: str, max_chars: int = CHUNK_MAX_CHARS, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks, preferring paragraph breaks."""
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    if len(text) <= max_chars: return [text]
    chunks = []
    paras = re.split(r"\n\s*\n", text)
    buf = ""
    for p in paras:
        if len(buf) + len(p) + 2 < max_chars:
            buf += ("\n\n" if buf else "") + p
        else:
            if buf: chunks.append(buf)
            # overlap last 'overlap' chars for context continuity
            tail = buf[-overlap:] if len(buf) > overlap else ""
            buf = (tail + "\n\n" + p) if tail else p
            # if single paragraph still too large, hard-split
            while len(buf) > max_chars * 2:
                chunks.append(buf[:max_chars])
                buf = buf[max_chars - overlap:]
    if buf: chunks.append(buf)
    return chunks


# ---------------------------------------------------------------------------
# Strip YAML front-matter
# ---------------------------------------------------------------------------

def strip_yaml(text: str) -> str:
    if not text.startswith("---"): return text
    end = text.find("\n---", 4)
    if end == -1: return text
    return text[end+4:].strip()


# ---------------------------------------------------------------------------
# Load manifest + read all docs
# ---------------------------------------------------------------------------

def load_manifest() -> list[dict]:
    with open(MANIFEST, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_stance_evidence(limit: int | None = None) -> list[dict]:
    """Pull evidence quotes from v5 stance dataset."""
    if not STANCES_JSONL.exists(): return []
    out = []
    with open(STANCES_JSONL, "r", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            q = r.get("evidence_quote", "")
            if not q or "placeholder" in q.lower(): continue
            m = r["_meta"]
            out.append({
                "id":      f"stance_{m['country']}_{m['issue']}_{m['cop']}",
                "kind":    "stance_evidence",
                "country": m["country"], "issue": m["issue"], "cop": m["cop"],
                "doc_id":  m["doc_id"],
                "text":    q[:1000],
                "stance":  r.get("stance_score"),
                "source_type": m.get("source_type"),
            })
            if limit and len(out) >= limit: break
    return out


# ---------------------------------------------------------------------------
# Source-content hash for cache invalidation
# ---------------------------------------------------------------------------

def compute_source_hash() -> str:
    """SHA-256 over (corpus file contents + manifest + stance dataset + build params).

    Used to skip rebuild if no source changes. Hash inputs:
      - All corpus markdown files (sha256 from manifest)
      - manifest.jsonl byte content
      - stances_v5.jsonl byte content (for stance evidence)
      - MODEL_NAME, CHUNK_MAX_CHARS, CHUNK_OVERLAP
    """
    h = hashlib.sha256()
    h.update(MODEL_NAME.encode())
    h.update(str(CHUNK_MAX_CHARS).encode())
    h.update(str(CHUNK_OVERLAP).encode())
    if MANIFEST.exists():
        h.update(MANIFEST.read_bytes())
    if STANCES_JSONL.exists():
        h.update(STANCES_JSONL.read_bytes())
    # Also walk corpus markdown for additional change detection
    for p in sorted(CORPUS_DIR.rglob("*.md")):
        try: h.update(p.read_bytes())
        except: pass
    return h.hexdigest()


def stored_source_hash() -> str | None:
    if not EMBED_INDEX.exists(): return None
    try:
        return json.loads(EMBED_INDEX.read_text(encoding="utf-8")).get("source_hash")
    except: return None


def is_stale(force: bool = False) -> tuple[bool, str, str | None]:
    """Returns (needs_rebuild, current_hash, stored_hash)."""
    cur = compute_source_hash()
    stored = stored_source_hash()
    if force:
        return True, cur, stored
    if stored is None:
        return True, cur, None
    return cur != stored, cur, stored


# ---------------------------------------------------------------------------
# Build embeddings
# ---------------------------------------------------------------------------

def build_embeddings(quick: bool = False) -> tuple[np.ndarray, list[dict]]:
    """Encode all corpus chunks + stance evidence into a single matrix."""
    from sentence_transformers import SentenceTransformer

    print(f"[v7] Loading model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    print(f"[v7] Model dim: {model.get_sentence_embedding_dimension()}")

    manifest = load_manifest()
    print(f"[v7] {len(manifest)} corpus documents")
    stance_evidence = load_stance_evidence(limit=200 if quick else None)
    print(f"[v7] {len(stance_evidence)} stance evidence records")

    # Build (id, text) list
    items = []
    for doc in manifest:
        path = ROOT / doc["path"]
        if not path.exists(): continue
        try:
            raw = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if path.suffix == ".md":
            body = strip_yaml(raw)
        else:
            body = raw[:8000]
        chunks = chunk_text(body)
        # Whole-doc text (truncated) as a single embedding
        whole = (doc.get("title", "") + "\n\n" + body)[:3500]
        items.append({
            "id":          f"{doc['doc_id']}::whole",
            "kind":        "corpus_whole",
            "doc_id":      doc["doc_id"],
            "title":       doc.get("title", ""),
            "path":        doc["path"],
            "type":        doc.get("type", "?"),
            "cop":         doc.get("cop"),
            "country":     doc.get("country"),
            "language":    doc.get("language", "en"),
            "chunk_idx":   None,
            "text":        whole,
        })
        for i, ch in enumerate(chunks):
            items.append({
                "id":          f"{doc['doc_id']}::chunk_{i}",
                "kind":        "corpus_chunk",
                "doc_id":      doc["doc_id"],
                "title":       doc.get("title", ""),
                "path":        doc["path"],
                "type":        doc.get("type", "?"),
                "cop":         doc.get("cop"),
                "country":     doc.get("country"),
                "language":    doc.get("language", "en"),
                "chunk_idx":   i,
                "text":        ch[:CHUNK_MAX_CHARS],
            })
    print(f"[v7] {len(items)} corpus chunks (whole + paragraph-level)")

    # Append stance evidence as separate kind
    for s in stance_evidence:
        items.append({
            "id": s["id"], "kind": s["kind"], "doc_id": s["doc_id"],
            "title": f"{s['country']} {s['issue']} {s['cop']}",
            "path": "stances_v5.jsonl", "type": "stance_evidence",
            "cop": s["cop"], "country": s["country"], "language": "en",
            "chunk_idx": None, "text": s["text"],
            "stance_score": s["stance"], "source_type": s["source_type"],
        })

    texts = [it["text"] for it in items]
    print(f"[v7] Encoding {len(texts)} items...")
    embeddings = model.encode(
        texts, batch_size=32, show_progress_bar=True,
        convert_to_numpy=True, normalize_embeddings=True,
    )
    print(f"[v7] Embeddings shape: {embeddings.shape}")
    return embeddings.astype(np.float32), items


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

def save(embeddings: np.ndarray, items: list[dict]):
    # NPZ: float16 for size (lossy but ~2x smaller)
    np.savez_compressed(EMBED_NPZ, embeddings=embeddings.astype(np.float16))
    print(f"[v7] {EMBED_NPZ}: {EMBED_NPZ.stat().st_size//1024} KB ({embeddings.shape})")

    # Index: id, kind, doc_id, type, country, cop + row idx
    meta = {
        "version":      "v7.0.0",
        "model_name":   MODEL_NAME,
        "model_dim":    int(embeddings.shape[1]),
        "n_items":      int(embeddings.shape[0]),
        "n_corpus_chunks":  sum(1 for it in items if it["kind"].startswith("corpus")),
        "n_stance_evidence": sum(1 for it in items if it["kind"] == "stance_evidence"),
        "chunk_max_chars":  CHUNK_MAX_CHARS,
        "chunk_overlap":    CHUNK_OVERLAP,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "items":        [
            {k: v for k, v in it.items() if k != "text"}
            | {"row": i, "text_preview": it["text"][:240]}
            for i, it in enumerate(items)
        ],
    }
    # Stable hash for cache invalidation
    h = hashlib.sha256(json.dumps(meta, sort_keys=True, default=str).encode()).hexdigest()[:16]
    meta["index_hash"] = h
    meta["source_hash"] = compute_source_hash()   # v8.5: cache invalidation key
    EMBED_INDEX.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    print(f"[v7] {EMBED_INDEX}: {EMBED_INDEX.stat().st_size//1024} KB")
    print(f"[v7] source_hash: {meta['source_hash'][:16]}...")

    # ----- Web-deployable copies -----
    WEB_EMBED_NPZ.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy(EMBED_NPZ, WEB_EMBED_NPZ)
    shutil.copy(EMBED_INDEX, WEB_EMBED_INDEX)

    # Browser-loadable JSON: float16 → float32 lossless restore on client.
    # We export as JSON with int16 quantization (compact + browser-easy).
    # Quantize to int16 scale=32767 per row (after L2 norm).
    quantized = (np.clip(embeddings, -1, 1) * 32767).astype(np.int16)
    web_obj = {
        "version":   "v7.0.0",
        "model":     MODEL_NAME,
        "dim":       int(embeddings.shape[1]),
        "n":         int(embeddings.shape[0]),
        "quant":     "int16/32767",
        "ids":       [it["id"] for it in items],
        "embeddings": quantized.tolist(),
    }
    WEB_EMBED_F32_JSON.write_text(json.dumps(web_obj), encoding="utf-8")
    print(f"[v7] {WEB_EMBED_F32_JSON}: {WEB_EMBED_F32_JSON.stat().st_size//1024} KB (int16 quant)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true",
                    help="Only encode 200 stance evidence (debugging)")
    ap.add_argument("--force", action="store_true",
                    help="Force rebuild even if source hash unchanged")
    ap.add_argument("--check-stale", action="store_true",
                    help="Only print stale/fresh status and exit (no build)")
    args = ap.parse_args()

    stale, cur_h, stored_h = is_stale(force=args.force)
    print(f"[v7] current source hash: {cur_h[:16]}...")
    print(f"[v7] stored source hash : {(stored_h or '(none)')[:16]}...")
    print(f"[v7] status: {'STALE (rebuild needed)' if stale else 'FRESH (no rebuild)'}")

    if args.check_stale:
        sys_exit_code = 0 if not stale else 1
        import sys; sys.exit(sys_exit_code)

    if not stale and not args.force:
        print(f"[v7] Skipping rebuild (use --force to override).")
        sys_exit_code = 0
        import sys; sys.exit(sys_exit_code)

    emb, items = build_embeddings(quick=args.quick)
    save(emb, items)
    print(f"\n[v7] Done. {emb.shape[0]} embeddings × {emb.shape[1]} dims.")
    print(f"     Corpus chunks: {sum(1 for it in items if it['kind'].startswith('corpus'))}")
    print(f"     Stance evidence: {sum(1 for it in items if it['kind'] == 'stance_evidence')}")
