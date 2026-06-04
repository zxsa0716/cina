"""pytest fixtures shared across CINA tests."""
from __future__ import annotations
import sys
from pathlib import Path

# Ensure project root is on sys.path so `from src...` works in tests
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


import pytest


@pytest.fixture
def sample_v5_record():
    """Synthetic v5 record for unit tests."""
    return {
        "_meta": {
            "doc_id": "test_record",
            "country": "Brazil", "issue": "GGA-IND", "cop": "COP30",
            "source_type": "verified_canonical",
        },
        "stance_score": 0.95,
        "ci_lower_95": 0.85, "ci_upper_95": 1.00,
        "frame_type": "sovereignty",
        "nato_4axis": {"nodality": 0.55, "authority": 0.20, "treasure": 0.15, "organization": 0.30},
        "procedural_signals": {"is_chair_role": True, "is_pen_holder": True},
        "procedural_composite": 1.0,
        "translation_gap_delta": 0.0,
        "evidence_quote": "[COP30, Brazil] 59 voluntary indicators...",
        "salience_score": 0.85, "confidence": 0.88,
    }


@pytest.fixture
def heuristic_record():
    """Heuristic-extension record (lower priority in merge)."""
    return {
        "_meta": {
            "doc_id": "test_heuristic",
            "country": "Brazil", "issue": "GGA-IND", "cop": "COP30",
            "source_type": "heuristic_extension",
        },
        "stance_score": 0.92,
        "evidence_quote": "(auto-generated placeholder)",
    }


@pytest.fixture
def llm_verified_record():
    """LLM-extracted verified record (highest priority in merge)."""
    return {
        "_meta": {
            "doc_id": "test_llm",
            "country": "Brazil", "issue": "GGA-IND", "cop": "COP30",
            "source_type": "verified_llm",
        },
        "stance_score": 0.94,
        "evidence_quote": "[COP30, Brazil] (LLM-extracted)",
        "evidence_verified": True,
    }
