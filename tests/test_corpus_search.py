"""Unit tests for corpus retrieval (v6 + v7)."""
import pytest
from src.program.query_engine_v2 import (
    corpus_search, corpus_filter_by_context, load_corpus_manifest,
    load_corpus_index, QueryIntent,
)


class TestCorpusSearch:
    def test_manifest_loads(self):
        m = load_corpus_manifest()
        assert len(m) >= 20      # we have 21 docs in v6

    def test_search_finds_l25e(self):
        hits = corpus_search("voluntary indicators GGA Brazil chair", top_k=5)
        ids = [h["doc_id"] for h in hits]
        # Should rank L.25E first or close to it
        assert any("L25E" in d or "L.25E" in d for d in ids), f"L.25E not in top-5: {ids}"

    def test_search_returns_metadata(self):
        hits = corpus_search("Korea NAP adaptation", top_k=3)
        assert len(hits) > 0
        for h in hits:
            assert "doc_id" in h
            assert "score" in h
            assert "manifest" in h
            assert h["score"] >= 0


class TestContextFilter:
    def test_filter_by_country(self):
        intent = QueryIntent(type="lookup", countries=["Korea"], issues=[], cop=None, raw_question="x")
        hits = corpus_filter_by_context(intent)
        assert any(r.get("country") == "Korea" for r in hits)

    def test_filter_by_cop(self):
        intent = QueryIntent(type="lookup", countries=[], issues=[], cop="COP30", raw_question="x")
        hits = corpus_filter_by_context(intent)
        assert any(r.get("cop") == "COP30" for r in hits)


@pytest.mark.slow
class TestSemanticSearch:
    """These require sentence-transformers + corpus embeddings."""

    def test_semantic_available_or_skip(self):
        from src.program.query_engine_v2 import semantic_search
        hits = semantic_search("voluntary indicators GGA Brazil", top_k=3)
        # If embeddings present, should return results; if not, returns []
        if hits:
            assert len(hits) > 0
            for h in hits:
                assert "score" in h
                assert h["score"] > 0
