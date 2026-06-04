// CINA v10.1 — Browser-side IndexedDB LLM cache (mirror of Python llm_cache.py)
//
// Caches BYO LLM responses by sha256(provider | model | temp | prompt).
// Survives across browser sessions. TTL 30 days default.
// Per-session stats (hits/misses/hit_rate).
//
// Public API (window.CINA_LLMCache):
//   await window.CINA_LLMCache.cachedCall(provider, model, prompt, key, callFn, opts)
//   await window.CINA_LLMCache.stats()        // { hits, misses, total, hit_rate, n_cached }
//   await window.CINA_LLMCache.clear()        // wipes entire cache
//   window.CINA_LLMCache.snapshot()           // session-only stats (sync)
//
// Author: Heedo Choi · MIT
// =====================================================================

(function () {
  "use strict";

  const DB_NAME = "cina_llm_cache_v1";
  const STORE   = "responses";
  const DB_VERSION = 1;

  // Session counters
  const _STATS = { hits: 0, misses: 0, writes: 0, errors: 0 };

  // ============ Open / migrate DB ============
  let _dbPromise = null;
  function openDB() {
    if (_dbPromise) return _dbPromise;
    _dbPromise = new Promise((resolve, reject) => {
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = (e) => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains(STORE)) {
          const os = db.createObjectStore(STORE, { keyPath: "hash" });
          os.createIndex("provider", "provider", { unique: false });
          os.createIndex("created_at", "created_at", { unique: false });
        }
      };
      req.onsuccess = (e) => resolve(e.target.result);
      req.onerror   = (e) => reject(e.target.error);
    });
    return _dbPromise;
  }

  // ============ Hashing (SHA-256) ============
  async function sha256(text) {
    const buf = new TextEncoder().encode(text);
    const hash = await crypto.subtle.digest("SHA-256", buf);
    return Array.from(new Uint8Array(hash))
      .map(b => b.toString(16).padStart(2, "0")).join("");
  }
  async function makeKey(provider, model, temperature, prompt) {
    return await sha256(`${provider}|${model}|${temperature.toFixed(4)}|${prompt}`);
  }

  // ============ Lookup / Store ============
  async function lookup(provider, model, temperature, prompt, ttlDays = 30) {
    try {
      const db = await openDB();
      const key = await makeKey(provider, model, temperature, prompt);
      return await new Promise((resolve, reject) => {
        const tx = db.transaction(STORE, "readwrite");
        const os = tx.objectStore(STORE);
        const req = os.get(key);
        req.onsuccess = () => {
          const row = req.result;
          if (!row) { _STATS.misses++; resolve(null); return; }
          if (ttlDays > 0) {
            const age = (Date.now() - row.created_at_ms) / 86400000;
            if (age > ttlDays) { _STATS.misses++; resolve(null); return; }
          }
          row.hit_count = (row.hit_count || 0) + 1;
          os.put(row);
          _STATS.hits++;
          resolve(row.response);
        };
        req.onerror = () => { _STATS.errors++; resolve(null); };
      });
    } catch (e) {
      console.warn("[CINA cache] lookup error:", e);
      _STATS.errors++;
      return null;
    }
  }

  async function store(provider, model, temperature, prompt, response) {
    try {
      const db = await openDB();
      const key = await makeKey(provider, model, temperature, prompt);
      await new Promise((resolve, reject) => {
        const tx = db.transaction(STORE, "readwrite");
        const os = tx.objectStore(STORE);
        const row = {
          hash:           key,
          provider, model, temperature,
          prompt_preview: prompt.slice(0, 200),
          response,
          created_at_ms:  Date.now(),
          created_at:     new Date().toISOString(),
          hit_count:      0,
        };
        const req = os.put(row);
        req.onsuccess = () => { _STATS.writes++; resolve(); };
        req.onerror   = () => { _STATS.errors++; resolve(); };
      });
    } catch (e) {
      console.warn("[CINA cache] store error:", e);
      _STATS.errors++;
    }
  }

  // ============ Wrap call ============
  async function cachedCall(provider, model, prompt, apiKey, callFn,
                            { temperature = 0.3, ttlDays = 30, skipCache = false } = {}) {
    if (!skipCache) {
      const cached = await lookup(provider, model, temperature, prompt, ttlDays);
      if (cached !== null) return cached;
    }
    const response = await callFn(prompt, apiKey);
    await store(provider, model, temperature, prompt, response);
    return response;
  }

  // ============ Stats ============
  async function stats() {
    try {
      const db = await openDB();
      const n = await new Promise((resolve, reject) => {
        const tx = db.transaction(STORE, "readonly");
        const req = tx.objectStore(STORE).count();
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => resolve(0);
      });
      const total = _STATS.hits + _STATS.misses;
      return {
        ..._STATS,
        total,
        hit_rate: total ? _STATS.hits / total : 0,
        n_cached: n,
      };
    } catch { return {..._STATS, n_cached: 0, total: 0, hit_rate: 0}; }
  }

  function snapshot() {
    const total = _STATS.hits + _STATS.misses;
    return {
      ..._STATS, total,
      hit_rate: total ? _STATS.hits / total : 0,
    };
  }

  async function clear() {
    try {
      const db = await openDB();
      await new Promise((resolve, reject) => {
        const tx = db.transaction(STORE, "readwrite");
        const req = tx.objectStore(STORE).clear();
        req.onsuccess = () => resolve();
        req.onerror   = () => reject();
      });
      for (const k of Object.keys(_STATS)) _STATS[k] = 0;
      console.log("[CINA cache] cleared");
    } catch (e) { console.warn("[CINA cache] clear error:", e); }
  }

  // ============ Cleanup expired ============
  async function purgeExpired(ttlDays = 30) {
    try {
      const db = await openDB();
      const cutoff = Date.now() - ttlDays * 86400000;
      await new Promise((resolve) => {
        const tx = db.transaction(STORE, "readwrite");
        const os = tx.objectStore(STORE);
        const idx = os.index("created_at");
        const req = idx.openCursor();
        let n = 0;
        req.onsuccess = (e) => {
          const cur = e.target.result;
          if (!cur) { console.log(`[CINA cache] purged ${n} expired entries`); resolve(); return; }
          if (cur.value.created_at_ms < cutoff) { cur.delete(); n++; }
          cur.continue();
        };
        req.onerror = () => resolve();
      });
    } catch (e) { console.warn("[CINA cache] purge error:", e); }
  }

  // ============ Public API ============
  window.CINA_LLMCache = {
    cachedCall, lookup, store, stats, snapshot, clear, purgeExpired,
    VERSION: "v10.1.0",
  };
  console.log("[CINA cache] v10.1 IndexedDB LLM cache loaded");
})();
