"""CINA v8.3 — Gemini-based corpus embedding (model consistency).

v7 used sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2) for
corpus embedding, while browser queries went through Gemini's text-embedding-004.
Cross-model mismatch can lose ~5% semantic similarity.

This script re-embeds the SAME corpus using Gemini text-embedding-004
(outputDimensionality: 384, matching the existing browser query path).
Output: embeddings_gemini.npz / embeddings_gemini_index.json.

Query engine v2.3 prefers this Gemini-aligned embedding when present.

Usage:
  export GEMINI_API_KEY=...
  python -m src.data.build_v7_embeddings_gemini

Rate limits (Gemini text-embedding-004 free tier):
  - 1,500 RPM, 100 RPD (free) — we have 215 items, fits in 1 day
  - Pro tier: unlimited

Cost: free for our 215-chunk corpus.

Author: Heedo Choi (Kookmin University)
License: MIT
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
CORPUS = ROOT / "data" / "corpus"

# Output (parallel to v7 sentence-transformers outputs)
EMBED_GEMINI_NPZ   = CORPUS / "embeddings_gemini.npz"
EMBED_GEMINI_INDEX = CORPUS / "embeddings_gemini_index.json"
WEB_EMBED_GEMINI_JSON = ROOT / "docs" / "web" / "data" / "corpus" / "embeddings_gemini.json"

# Reuse v7 chunking + manifest loading + source-hash logic
from src.data.build_v7_embeddings import (
    chunk_text, strip_yaml, load_manifest, load_stance_evidence,
    CHUNK_MAX_CHARS, CHUNK_OVERLAP,
    compute_source_hash,
)

GEMINI_MODEL = "text-embedding-004"
GEMINI_DIM   = 384


# ===========================================================================
# Gemini embedding API
# ===========================================================================

def gemini_embed(text: str, api_key: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list[float]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:embedContent?key={api_key}"
    body = json.dumps({
        "content": {"parts": [{"text": text}]},
        "outputDimensionality": GEMINI_DIM,
        "taskType": task_type,
    }).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    for retry in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                j = json.loads(r.read())
            vec = j.get("embedding", {}).get("values", [])
            if not vec: raise RuntimeError("empty vector")
            # L2 normalise
            n = math.sqrt(sum(v*v for v in vec)) or 1
            return [v / n for v in vec]
        except urllib.error.HTTPError as e:
            if e.code == 429 and retry < 2:
                wait = 2 ** retry
                print(f"  [retry] HTTP 429 wait {wait}s")
                time.sleep(wait)
                continue
            raise

import math


# ===========================================================================
# Build (reuses v7 chunking)
# ===========================================================================

def build_gemini_embeddings(api_key: str, max_n: int | None = None, delay_sec: float = 0.05):
    manifest = load_manifest()
    print(f"[v8.3 gemini] {len(manifest)} corpus documents")
    stance_evidence = load_stance_evidence(limit=None)
    print(f"[v8.3 gemini] {len(stance_evidence)} stance evidence records")

    items = []
    for doc in manifest:
        path = ROOT / doc["path"]
        if not path.exists(): continue
        raw = path.read_text(encoding="utf-8", errors="ignore")
        body = strip_yaml(raw) if path.suffix == ".md" else raw[:8000]
        # Whole-doc
        whole = (doc.get("title", "") + "\n\n" + body)[:3500]
        items.append({
            "id": f"{doc['doc_id']}::whole", "kind": "corpus_whole",
            "doc_id": doc["doc_id"], "title": doc.get("title", ""),
            "path": doc["path"], "type": doc.get("type", "?"),
            "cop": doc.get("cop"), "country": doc.get("country"),
            "language": doc.get("language", "en"), "chunk_idx": None, "text": whole,
        })
        for i, ch in enumerate(chunk_text(body)):
            items.append({
                "id": f"{doc['doc_id']}::chunk_{i}", "kind": "corpus_chunk",
                "doc_id": doc["doc_id"], "title": doc.get("title", ""),
                "path": doc["path"], "type": doc.get("type", "?"),
                "cop": doc.get("cop"), "country": doc.get("country"),
                "language": doc.get("language", "en"), "chunk_idx": i,
                "text": ch[:CHUNK_MAX_CHARS],
            })
    for s in stance_evidence:
        items.append({
            "id": s["id"], "kind": s["kind"], "doc_id": s["doc_id"],
            "title": f"{s['country']} {s['issue']} {s['cop']}",
            "path": "stances_v5.jsonl", "type": "stance_evidence",
            "cop": s["cop"], "country": s["country"], "language": "en",
            "chunk_idx": None, "text": s["text"],
            "stance_score": s["stance"], "source_type": s["source_type"],
        })

    if max_n: items = items[:max_n]
    print(f"[v8.3 gemini] embedding {len(items)} items via {GEMINI_MODEL}")

    embeddings = np.zeros((len(items), GEMINI_DIM), dtype=np.float32)
    t_start = time.time()
    for k, it in enumerate(items):
        vec = gemini_embed(it["text"], api_key)
        embeddings[k] = vec
        if (k + 1) % 20 == 0:
            elapsed = time.time() - t_start
            eta = elapsed / (k + 1) * (len(items) - k - 1)
            print(f"  [{k+1}/{len(items)}] ETA {eta/60:.1f} min")
        time.sleep(delay_sec)
    print(f"[v8.3 gemini] done in {(time.time()-t_start)/60:.1f} min. shape={embeddings.shape}")
    return embeddings, items


def save_gemini(embeddings: np.ndarray, items: list[dict]):
    # NPZ float16
    np.savez_compressed(EMBED_GEMINI_NPZ, embeddings=embeddings.astype(np.float16))
    print(f"[v8.3 gemini] {EMBED_GEMINI_NPZ}: {EMBED_GEMINI_NPZ.stat().st_size//1024} KB")

    meta = {
        "version": "v8.3.0", "model_name": GEMINI_MODEL, "model_dim": GEMINI_DIM,
        "n_items": int(embeddings.shape[0]),
        "n_corpus_chunks":   sum(1 for it in items if it["kind"].startswith("corpus")),
        "n_stance_evidence": sum(1 for it in items if it["kind"] == "stance_evidence"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_hash": compute_source_hash(),
        "items": [
            {k: v for k, v in it.items() if k != "text"} | {"row": i, "text_preview": it["text"][:240]}
            for i, it in enumerate(items)
        ],
    }
    EMBED_GEMINI_INDEX.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    print(f"[v8.3 gemini] {EMBED_GEMINI_INDEX}: {EMBED_GEMINI_INDEX.stat().st_size//1024} KB")

    # Web int16 quant
    WEB_EMBED_GEMINI_JSON.parent.mkdir(parents=True, exist_ok=True)
    q = (np.clip(embeddings, -1, 1) * 32767).astype(np.int16)
    web_obj = {
        "version": "v8.3.0", "model": GEMINI_MODEL,
        "dim": GEMINI_DIM, "n": int(embeddings.shape[0]),
        "quant": "int16/32767",
        "ids": [it["id"] for it in items],
        "embeddings": q.tolist(),
    }
    WEB_EMBED_GEMINI_JSON.write_text(json.dumps(web_obj), encoding="utf-8")
    print(f"[v8.3 gemini] {WEB_EMBED_GEMINI_JSON}: {WEB_EMBED_GEMINI_JSON.stat().st_size//1024} KB")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try: sys.stdout.reconfigure(encoding="utf-8")
        except: pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=None,
                    help="limit number of items (debug)")
    ap.add_argument("--delay", type=float, default=0.05,
                    help="sec between API calls (Gemini free tier = 1500 RPM ≈ 0.04s)")
    args = ap.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not set. Get at https://aistudio.google.com/apikey")
        sys.exit(1)

    emb, items = build_gemini_embeddings(api_key, max_n=args.max, delay_sec=args.delay)
    save_gemini(emb, items)
    print(f"\n[v8.3 gemini] done. {emb.shape[0]} embeddings via Gemini text-embedding-004 (model-aligned with browser query path).")


if __name__ == "__main__":
    main()
