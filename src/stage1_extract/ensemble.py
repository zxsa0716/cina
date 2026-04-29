"""Multi-LLM ensemble for Stage 1 stance extraction.

3-LLM 역할 분담 (Heedo의 모든 무료 backend 활용):

    Role 1 — "Fast Scanner" (Gemini 2.5 Flash-Lite)
        가장 빠르고 generous free tier (1000 RPD).
        첫 pass: 문서가 해당 이슈를 다루는지, 핵심 단락 어디인지 빠르게 판정.
        Output: relevance_score, key_paragraphs[], preliminary_stance.

    Role 2 — "Primary Extractor" (Groq Llama 3.3 70B)
        가장 빠른 inference (280+ tok/sec). JSON mode 강함.
        본격 추출: NATO 4축 + frame_type + salience + procedural_signals.
        Output: full v1.3 stance schema.

    Role 3 — "Privacy Validator" (Ollama Gemma 4 / local)
        로컬, zero-cost, 무제한, 데이터 외부 유출 0.
        Cross-check: Groq 결과 검증 + 보수적 fallback score.
        Output: validation_score, disagreements[], consensus_flag.

Ensemble 합의:
    - 3개 LLM의 stance_score 평균 + 표준편차 계산
    - std < 0.15 → 합의 (high confidence)
    - 0.15 ≤ std < 0.35 → partial agreement (Groq 우선)
    - std ≥ 0.35 → disagreement (human review flag)

이는 Krippendorff's alpha (cross-rater reliability) 의 LLM 간 proxy로 작동.
"""
from __future__ import annotations

import json
import logging
import os
import statistics
import time
from datetime import datetime, timezone
from typing import Any

from .providers import get_provider

logger = logging.getLogger(__name__)


SYSTEM_FAST_SCANNER = """You are a fast climate diplomacy first-pass scanner.

Goal: quickly assess if a document addresses a specific climate negotiation issue
for a specific country, and identify the most relevant paragraphs.

Output strict JSON:
{
  "relevance_score": float in [0, 1],   // does this doc address country×issue?
  "key_paragraph_indicators": [string], // 3-5 sentences/phrases most relevant
  "preliminary_stance": float in [-1, 1], // quick rough estimate
  "confidence": float in [0, 1]
}

Be fast and concise."""


SYSTEM_PRIMARY_EXTRACTOR = """You are a climate diplomacy analyst extracting structured stance from UNFCCC documents.

Output strict JSON v1.3 schema:
{
  "stance_score": float in [-1, 1],
  "stance_category": "strong_support|support|conditional_support|neutral_or_silent|oppose|strong_oppose",
  "key_demands": [string],
  "red_lines": [string],
  "flexibility_signals": [string],
  "evidence_quotes": [{"quote": string, "location": string}],
  "frame_type": "scientific|justice|sovereignty|security|development|mixed",
  "instrument_signals": {
    "nodality": [string],
    "authority": [string],
    "treasure": [string],
    "organization": [string]
  },
  "salience_score": float in [0, 1],
  "procedural_signals": {
    "is_chair_role": bool,
    "is_pen_holder": bool,
    "drafts_text_for_issue": string|null
  },
  "confidence": float in [0, 1],
  "reasoning": string
}

Cite ONLY direct quotes (no paraphrasing). Use the full [-1, +1] range."""


SYSTEM_PRIVACY_VALIDATOR = """You are a privacy-first cross-validator for climate diplomacy stance extraction.

Given an extraction by another LLM, validate:
1. Does the stance_score match the evidence_quotes provided?
2. Are there hallucinated facts (numbers, country names, programs) not in the doc?
3. Is the frame_type classification reasonable?

Output strict JSON:
{
  "validation_stance_score": float in [-1, 1],   // your independent estimate
  "agreement_with_primary": float in [0, 1],     // how much you agree
  "disagreements": [string],                      // specific issues
  "hallucination_flags": [string],                // suspected fabrications
  "confidence": float in [0, 1]
}

Be conservative. Lower scores when uncertain."""


def role_fast_scanner(
    text: str, country: str, issue: str, issue_desc: str
) -> dict | None:
    """Gemini Flash-Lite first pass."""
    try:
        provider = get_provider("gemini", temperature=0.2, max_tokens=600)
    except Exception as exc:
        logger.warning("Gemini unavailable for scanner role: %s", exc)
        return None

    user = f"""Country: {country}
Issue: {issue} - {issue_desc}

Document excerpt (first 4000 chars):
{text[:4000]}

Quickly assess relevance and preliminary stance. JSON only."""

    try:
        resp = provider.complete(SYSTEM_FAST_SCANNER, user, json_schema={"type": "object"})
        return resp.parse_json(strict=False)
    except Exception as exc:
        logger.warning("Scanner role failed: %s", exc)
        return None


def role_primary_extractor(
    text: str, country: str, issue: str, issue_desc: str, doc_id: str,
) -> dict | None:
    """Groq Llama 3.3 70B full extraction."""
    try:
        provider = get_provider("groq", temperature=0.3, max_tokens=2000)
    except Exception as exc:
        logger.warning("Groq unavailable for primary role: %s", exc)
        return None

    user = f"""Country: {country}
Issue: {issue} - {issue_desc}

Document:
=== START ===
{text[:8000]}
=== END ===
Source: {doc_id}

Extract full stance per v1.3 schema. JSON only."""

    try:
        resp = provider.complete(SYSTEM_PRIMARY_EXTRACTOR, user, json_schema={"type": "object"})
        return resp.parse_json(strict=False)
    except Exception as exc:
        logger.warning("Primary role failed: %s", exc)
        return None


def role_privacy_validator(
    text: str,
    country: str,
    issue: str,
    primary_extraction: dict,
) -> dict | None:
    """Ollama Gemma 4 local validation."""
    try:
        provider = get_provider("ollama", temperature=0.2, max_tokens=800)
        # Use installed model
        provider.model = os.environ.get("OLLAMA_MODEL", "gemma4:latest")
    except Exception as exc:
        logger.warning("Ollama unavailable for validator role: %s", exc)
        return None

    primary_json = json.dumps(primary_extraction, ensure_ascii=False, indent=2)[:2000]
    user = f"""Country: {country}
Issue: {issue}

Document excerpt (first 4000 chars):
{text[:4000]}

Primary LLM extraction:
{primary_json}

Validate: does evidence support stance_score? Any hallucinations? JSON only."""

    try:
        resp = provider.complete(SYSTEM_PRIVACY_VALIDATOR, user, json_schema={"type": "object"})
        return resp.parse_json(strict=False)
    except Exception as exc:
        logger.warning("Validator role failed: %s", exc)
        return None


def ensemble_extract(
    text: str,
    country: str,
    issue: str,
    issue_desc: str,
    doc_id: str,
) -> dict:
    """Run 3-LLM ensemble extraction with consensus."""
    started = time.time()

    # Role 1: Fast Scanner
    scan = role_fast_scanner(text, country, issue, issue_desc)
    time.sleep(0.3)

    # Role 2: Primary Extractor (depends on relevance)
    primary = None
    if scan and scan.get("relevance_score", 0.5) >= 0.3:
        primary = role_primary_extractor(text, country, issue, issue_desc, doc_id)
    elif scan:
        # Low relevance — placeholder primary
        primary = {
            "stance_score": 0.0,
            "stance_category": "neutral_or_silent",
            "key_demands": [],
            "red_lines": [],
            "flexibility_signals": [],
            "evidence_quotes": [],
            "frame_type": "scientific",
            "instrument_signals": {"nodality": [], "authority": [], "treasure": [], "organization": []},
            "confidence": 0.0,
            "reasoning": f"Document low-relevance per scanner ({scan.get('relevance_score', 0)})",
        }
    time.sleep(0.3)

    # Role 3: Privacy Validator (local, validates primary)
    validation = None
    if primary:
        validation = role_privacy_validator(text, country, issue, primary)

    # Consensus computation
    scores = []
    if scan and "preliminary_stance" in scan:
        scores.append(("gemini_scanner", scan["preliminary_stance"]))
    if primary and "stance_score" in primary:
        scores.append(("groq_primary", primary["stance_score"]))
    if validation and "validation_stance_score" in validation:
        scores.append(("ollama_validator", validation["validation_stance_score"]))

    if scores:
        score_values = [s[1] for s in scores]
        consensus_score = statistics.mean(score_values)
        consensus_std = statistics.stdev(score_values) if len(score_values) > 1 else 0.0
    else:
        consensus_score = 0.0
        consensus_std = 1.0

    if consensus_std < 0.15:
        consensus_quality = "high_agreement"
    elif consensus_std < 0.35:
        consensus_quality = "partial_agreement"
    else:
        consensus_quality = "disagreement_flag"

    elapsed = time.time() - started

    return {
        "_meta": {
            "doc_id": doc_id,
            "country": country,
            "issue": issue,
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "elapsed_sec": round(elapsed, 2),
            "providers_used": [s[0] for s in scores],
            "consensus_quality": consensus_quality,
        },
        "ensemble": {
            "consensus_stance_score": round(consensus_score, 3),
            "consensus_std": round(consensus_std, 3),
            "individual_scores": dict(scores),
            "consensus_quality": consensus_quality,
        },
        "scanner": scan,
        "primary": primary,
        "validator": validation,
    }
