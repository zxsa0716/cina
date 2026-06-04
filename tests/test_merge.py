"""Unit tests for v5.2 overlay merge (v9.1)."""
from src.data.merge_v5_llm import merge_records, PRIORITY, src_of, key_of


class TestMergePolicy:
    def test_llm_verified_beats_canonical(self, sample_v5_record, llm_verified_record):
        # Same (country, issue, cop); LLM verified should win
        merged, audit = merge_records([sample_v5_record], [llm_verified_record])
        assert len(merged) == 1
        assert src_of(merged[0]) == "verified_llm"
        assert merged[0]["stance_score"] == 0.94    # llm value, not heuristic

    def test_canonical_beats_heuristic(self, sample_v5_record, heuristic_record):
        merged, _ = merge_records([sample_v5_record, heuristic_record], [])
        # Both targets have same key, canonical wins
        assert len(merged) == 1
        assert src_of(merged[0]) == "verified_canonical"

    def test_priority_ordering(self):
        assert PRIORITY["verified_llm"] < PRIORITY["verified_canonical"]
        assert PRIORITY["verified_canonical"] < PRIORITY["llm_unverified_quote"]
        assert PRIORITY["llm_unverified_quote"] < PRIORITY["heuristic_extension"]

    def test_overlay_history_recorded(self, sample_v5_record, llm_verified_record):
        merged, _ = merge_records([sample_v5_record], [llm_verified_record])
        h = merged[0]["_meta"]["overlay_history"]
        kept = [e for e in h if e["kept"]]
        dropped = [e for e in h if not e["kept"]]
        assert len(kept) == 1
        assert len(dropped) == 1
        assert kept[0]["source_type"] == "verified_llm"
        assert dropped[0]["source_type"] == "verified_canonical"

    def test_audit_kept_counts(self, sample_v5_record, heuristic_record):
        merged, audit = merge_records([sample_v5_record, heuristic_record], [])
        assert audit["kept_counts"].get("kept_verified_canonical") == 1
        assert audit["n_total"] == 1   # only 1 key, the lower-priority dropped

    def test_no_overlap_keeps_both(self):
        r1 = {"_meta": {"country": "Brazil", "issue": "GGA-IND", "cop": "COP30",
                        "source_type": "heuristic_extension"}, "stance_score": 0.5}
        r2 = {"_meta": {"country": "Korea", "issue": "L&D-OP", "cop": "COP30",
                        "source_type": "verified_llm"}, "stance_score": 0.4}
        merged, audit = merge_records([r1], [r2])
        assert len(merged) == 2
        assert audit["n_overlay_events"] == 0


class TestKeyOf:
    def test_key_extracted_correctly(self, sample_v5_record):
        assert key_of(sample_v5_record) == ("Brazil", "GGA-IND", "COP30")
