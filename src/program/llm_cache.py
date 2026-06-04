"""CINA v9.2 — Persistent LLM cache (SQLite-backed).

Hashes (provider, model, temperature, prompt) → cached response. Survives
across runs; idempotent on identical inputs. Used by:
  - llm_stance_extractor (2,400-record extraction)
  - cross_llm_alpha (multi-provider parallel)
  - query_engine_v2 LLM mode (browser-side BYO falls outside this scope)

Cost savings: ~99% on resumed/repeated runs.

API:
  from src.program.llm_cache import cached_call, CacheStats

  def call_fn(prompt, key): ...  # provider-specific (gemini, anthropic, groq)

  resp = cached_call(
      provider="gemini",
      model="gemini-2.5-flash-lite",
      prompt=prompt,
      api_key=key,
      call_fn=call_fn,
      temperature=0.2,
      ttl_days=30,   # cache expiry
  )

  print(CacheStats.snapshot())  # {hits: N, misses: M, hit_rate: 0.xx}

Schema:
  cache(hash TEXT PRIMARY KEY, provider TEXT, model TEXT, temperature REAL,
        prompt_preview TEXT, response TEXT, created_at TEXT, hit_count INTEGER)
  stats(key TEXT PRIMARY KEY, value INTEGER)  -- hits, misses

Author: Heedo Choi (Kookmin University)
License: MIT
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent.parent
CACHE_DIR = ROOT / "data" / "llm_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
DB = CACHE_DIR / "llm_responses.sqlite"

# In-memory hit counters for this process
_STATS = {"hits": 0, "misses": 0, "writes": 0, "errors": 0}


def _connect() -> sqlite3.Connection:
    con = sqlite3.connect(str(DB), timeout=10)
    con.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            hash TEXT PRIMARY KEY,
            provider TEXT NOT NULL,
            model TEXT NOT NULL,
            temperature REAL,
            prompt_preview TEXT,
            response TEXT NOT NULL,
            created_at TEXT NOT NULL,
            hit_count INTEGER DEFAULT 0
        )
    """)
    con.execute("CREATE INDEX IF NOT EXISTS idx_provider ON cache(provider)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_created ON cache(created_at)")
    con.commit()
    return con


def _hash(provider: str, model: str, temperature: float, prompt: str) -> str:
    h = hashlib.sha256()
    h.update(provider.encode())
    h.update(b"|")
    h.update(model.encode())
    h.update(b"|")
    h.update(f"{temperature:.4f}".encode())
    h.update(b"|")
    h.update(prompt.encode())
    return h.hexdigest()


def lookup(provider: str, model: str, temperature: float, prompt: str,
           ttl_days: int = 30) -> str | None:
    """Return cached response if present and not expired."""
    try:
        con = _connect()
        h = _hash(provider, model, temperature, prompt)
        row = con.execute(
            "SELECT response, created_at FROM cache WHERE hash = ?", (h,)
        ).fetchone()
        if row is None:
            _STATS["misses"] += 1
            con.close()
            return None
        response, created_at = row
        if ttl_days > 0:
            ct = datetime.fromisoformat(created_at)
            if (datetime.now(timezone.utc) - ct).days > ttl_days:
                _STATS["misses"] += 1
                con.close()
                return None
        # Increment hit count
        con.execute("UPDATE cache SET hit_count = hit_count + 1 WHERE hash = ?", (h,))
        con.commit()
        con.close()
        _STATS["hits"] += 1
        return response
    except Exception as e:
        _STATS["errors"] += 1
        return None


def store(provider: str, model: str, temperature: float, prompt: str, response: str):
    """Write response to cache (idempotent on hash collision)."""
    try:
        con = _connect()
        h = _hash(provider, model, temperature, prompt)
        con.execute("""
            INSERT OR REPLACE INTO cache (hash, provider, model, temperature, prompt_preview, response, created_at, hit_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT hit_count FROM cache WHERE hash = ?), 0))
        """, (h, provider, model, temperature, prompt[:200], response,
              datetime.now(timezone.utc).isoformat(), h))
        con.commit()
        con.close()
        _STATS["writes"] += 1
    except Exception as e:
        _STATS["errors"] += 1


def cached_call(provider: str, model: str, prompt: str, api_key: str,
                call_fn: Callable[[str, str], str],
                temperature: float = 0.2, ttl_days: int = 30,
                skip_cache: bool = False) -> str:
    """Lookup-then-call. Returns cached response if hit, else calls + stores."""
    if not skip_cache:
        cached = lookup(provider, model, temperature, prompt, ttl_days=ttl_days)
        if cached is not None: return cached
    response = call_fn(prompt, api_key)
    store(provider, model, temperature, prompt, response)
    return response


# ===========================================================================
# Stats
# ===========================================================================

class CacheStats:
    @staticmethod
    def snapshot() -> dict:
        total = _STATS["hits"] + _STATS["misses"]
        return {
            "hits":     _STATS["hits"],
            "misses":   _STATS["misses"],
            "writes":   _STATS["writes"],
            "errors":   _STATS["errors"],
            "total":    total,
            "hit_rate": (_STATS["hits"] / total) if total else 0.0,
        }

    @staticmethod
    def reset():
        for k in _STATS: _STATS[k] = 0

    @staticmethod
    def db_stats() -> dict:
        try:
            con = _connect()
            n = con.execute("SELECT COUNT(*) FROM cache").fetchone()[0]
            sum_hits = con.execute("SELECT SUM(hit_count) FROM cache").fetchone()[0] or 0
            per_provider = dict(con.execute(
                "SELECT provider, COUNT(*) FROM cache GROUP BY provider"
            ).fetchall())
            con.close()
            return {"n_cached": n, "total_lifetime_hits": int(sum_hits), "per_provider": per_provider}
        except Exception:
            return {"n_cached": 0, "total_lifetime_hits": 0, "per_provider": {}}


# ===========================================================================
# CLI
# ===========================================================================

if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        try: sys.stdout.reconfigure(encoding="utf-8")
        except: pass
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true", help="print cache DB stats")
    ap.add_argument("--clear", action="store_true", help="clear all cached responses")
    args = ap.parse_args()
    if args.clear:
        if DB.exists(): DB.unlink()
        print("[v9.2 cache] cleared")
    if args.stats or not args.clear:
        s = CacheStats.db_stats()
        print(json.dumps(s, indent=2))
