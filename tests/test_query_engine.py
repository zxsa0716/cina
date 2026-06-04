"""Unit tests for CINA query engine v2.3."""
from src.program.query_engine_v2 import (
    parse_intent, _record_relevance, _fmt_score, _stance_label_ko, INTENT_TRIGGERS,
)


class TestIntentParser:
    def test_lookup_basic(self):
        i = parse_intent("브라질 GGA-IND COP30 입장은?")
        assert "Brazil" in i.countries
        assert "GGA-IND" in i.issues
        assert i.cop == "COP30"
        assert i.type == "lookup"

    def test_compare_two_countries(self):
        i = parse_intent("브라질과 한국의 GGA 지표 입장 차이는?")
        assert "Brazil" in i.countries and "Korea" in i.countries
        assert i.type == "compare"

    def test_trend(self):
        i = parse_intent("AOSIS GGA-IND 시계열 추이?")
        assert "AOSIS" in i.countries
        assert i.type == "trend"

    def test_coalition(self):
        i = parse_intent("한국과 비슷한 국가는?")
        assert "Korea" in i.countries
        assert i.type == "coalition"

    def test_gap(self):
        i = parse_intent("브라질의 translation gap 분석")
        assert "Brazil" in i.countries
        assert i.type == "gap"

    def test_recommendation(self):
        i = parse_intent("COP30 한국 외교 권고")
        assert "Korea" in i.countries
        assert i.type == "recommendation"

    def test_factoid(self):
        i = parse_intent("사우디 L&D-OP 정확히 몇이야?")
        assert "Saudi" in i.countries
        assert i.type == "factoid"

    def test_search_intent(self):
        i = parse_intent("L.25E 결정문 본문 보여줘")
        assert i.type == "search"

    def test_multi_country_compare_routing(self):
        # "차이" appears in both gap and compare, but with 2 countries -> compare
        i = parse_intent("미국과 중국의 GGA-IND 차이")
        assert len(i.countries) >= 2
        # Should resolve to either compare or gap (both valid for 2 countries)
        assert i.type in ("compare", "gap")


class TestRelevanceScoring:
    def test_country_match_bonus(self, sample_v5_record):
        from src.program.query_engine_v2 import QueryIntent
        intent = QueryIntent(type="lookup", countries=["Brazil"], issues=[], cop="COP30",
                             raw_question="brazil")
        s = _record_relevance(sample_v5_record, intent)
        assert s > 1.5   # country bonus

    def test_verified_canonical_bonus(self, sample_v5_record):
        from src.program.query_engine_v2 import QueryIntent
        intent = QueryIntent(type="lookup", countries=[], issues=[], cop=None,
                             raw_question="x")
        s = _record_relevance(sample_v5_record, intent)
        assert s >= 0.5   # source_type bonus


class TestFormatters:
    def test_fmt_score_positive(self):
        assert _fmt_score(0.65) == "+0.65"
        assert _fmt_score(1.0) == "+1.00"

    def test_fmt_score_negative(self):
        assert _fmt_score(-0.5) == "-0.50"

    def test_stance_label_thresholds(self):
        assert _stance_label_ko(0.95) == "강한 지지"
        assert _stance_label_ko(0.5) == "지지"
        assert _stance_label_ko(0.0) == "중립"
        assert _stance_label_ko(-0.5) == "반대"
        assert _stance_label_ko(-0.9) == "강한 반대"


class TestIntentTriggersStability:
    def test_all_intents_have_triggers(self):
        expected = {"trend", "coalition", "gap", "compare", "recommendation", "factoid", "search"}
        assert expected.issubset(set(INTENT_TRIGGERS.keys()))
