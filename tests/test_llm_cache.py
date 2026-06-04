"""Unit tests for v9.2 LLM cache."""
import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def tmp_cache(monkeypatch):
    """Redirect cache DB to a temp file for test isolation."""
    import src.program.llm_cache as cache_mod
    with tempfile.TemporaryDirectory() as td:
        monkeypatch.setattr(cache_mod, "DB", Path(td) / "test.sqlite")
        cache_mod.CacheStats.reset()
        yield cache_mod


class TestLLMCache:
    def test_cache_miss_then_hit(self, tmp_cache):
        cache_mod = tmp_cache
        calls = []
        def dummy(prompt, key):
            calls.append(prompt); return f"resp_{prompt[:5]}"

        r1 = cache_mod.cached_call("gemini", "test-model", "hello world", "k", dummy)
        r2 = cache_mod.cached_call("gemini", "test-model", "hello world", "k", dummy)
        assert r1 == r2
        assert len(calls) == 1   # only first call executed

    def test_different_temperature_different_cache(self, tmp_cache):
        cache_mod = tmp_cache
        calls = []
        def dummy(prompt, key):
            calls.append(prompt); return "x"
        cache_mod.cached_call("p", "m", "q", "k", dummy, temperature=0.1)
        cache_mod.cached_call("p", "m", "q", "k", dummy, temperature=0.2)
        assert len(calls) == 2

    def test_stats_snapshot(self, tmp_cache):
        cache_mod = tmp_cache
        def dummy(prompt, key): return "ok"
        cache_mod.cached_call("p", "m", "a", "k", dummy)
        cache_mod.cached_call("p", "m", "a", "k", dummy)
        s = cache_mod.CacheStats.snapshot()
        assert s["hits"] == 1
        assert s["misses"] == 1
        assert s["hit_rate"] == 0.5

    def test_skip_cache_flag(self, tmp_cache):
        cache_mod = tmp_cache
        calls = []
        def dummy(prompt, key): calls.append(prompt); return "x"
        cache_mod.cached_call("p", "m", "q", "k", dummy)
        cache_mod.cached_call("p", "m", "q", "k", dummy, skip_cache=True)
        assert len(calls) == 2

    def test_db_stats(self, tmp_cache):
        cache_mod = tmp_cache
        def dummy(prompt, key): return "x"
        cache_mod.cached_call("gemini", "m1", "q1", "k", dummy)
        cache_mod.cached_call("anthropic", "m2", "q2", "k", dummy)
        s = cache_mod.CacheStats.db_stats()
        assert s["n_cached"] == 2
        assert "gemini" in s["per_provider"]
        assert "anthropic" in s["per_provider"]
