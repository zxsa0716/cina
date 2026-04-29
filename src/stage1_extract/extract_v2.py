"""Stage 1 v2 — provider-agnostic stance extraction.

기존 extract.py는 Anthropic SDK에 직접 결합되어 있었음.
v2는 provider abstraction을 사용하여 무료 LLM (Gemini/Groq/Ollama)로 작동.

Usage:
    from src.stage1_extract.extract_v2 import extract_stance_v2

    # Gemini default (free 1000 RPD)
    stance = extract_stance_v2(country='Brazil', issue='GGA-IND', ...)

    # 또는 환경변수로 backend 선택
    # export CINA_LLM_PROVIDER=ollama  # local zero-cost
"""
from __future__ import annotations

import hashlib
import logging
import time
from datetime import datetime
from pathlib import Path

from .extract import (
    aggregate_samples,
    calibrate_score,
    classify_category,
    load_calibrator,
    load_prompt_v1_2,
    prompt_hash,
    verify_evidence_quotes,
)
from .providers import get_provider, LLMProvider
from ..config import Stage1Config
from ..schemas import (
    EpistemicAlignment,
    EvidenceQuote,
    ExtractionMetadata,
    Stance,
)

logger = logging.getLogger(__name__)


def extract_samples_v2(
    provider: LLMProvider,
    country: str,
    issue: str,
    issue_description: str,
    paragraphs: str,
    doc_id: str,
    n_samples: int = 5,
) -> list[dict]:
    """Provider-agnostic multi-sample extraction."""
    system, user_template = load_prompt_v1_2()
    user = user_template.format(
        country=country,
        issue_label=issue,
        issue_description=issue_description,
        paragraphs_joined=paragraphs,
        doc_id=doc_id,
    )

    samples = []
    for i in range(n_samples):
        try:
            resp = provider.complete(system=system, user=user, json_schema={"type": "object"})
            sample = resp.parse_json(strict=False)
            if sample:
                samples.append(sample)
            else:
                logger.warning("Sample %d empty/parse fail for %s/%s", i, country, issue)
            # Rate-limit gentle (provider 자체에서 retry-aware하면 더 좋음)
            time.sleep(0.5)
        except Exception as exc:
            logger.warning("Sample %d failed for %s/%s: %s", i, country, issue, exc)
    return samples


def extract_stance_v2(
    country: str,
    issue: str,
    issue_description: str,
    document_text: str,
    doc_id: str,
    cop_session: str,
    date_context: str,
    cfg: Stage1Config | None = None,
    provider: LLMProvider | None = None,
    calibrator=None,
) -> Stance:
    """Free-LLM-friendly stance extraction.

    Args:
        provider: LLMProvider instance. If None, uses CINA_LLM_PROVIDER env (default 'gemini').
    """
    cfg = cfg or Stage1Config()
    provider = provider or get_provider(
        temperature=cfg.temperature,
        max_tokens=cfg.max_tokens,
    )

    samples = extract_samples_v2(
        provider=provider,
        country=country,
        issue=issue,
        issue_description=issue_description,
        paragraphs=document_text,
        doc_id=doc_id,
        n_samples=cfg.k_samples,
    )

    if not samples:
        logger.error("All %d samples failed for %s/%s", cfg.k_samples, country, issue)
        # Fallback: empty stance
        samples = [{
            "country": country, "issue": issue, "stance_score": 0.0,
            "stance_category": "neutral_or_silent", "key_demands": [],
            "red_lines": [], "flexibility_signals": [],
            "evidence_quotes": [], "confidence": 0.0,
            "reasoning": "All LLM samples failed.",
        }]

    agg = aggregate_samples(samples)

    verified_quotes = verify_evidence_quotes(agg["evidence_quotes"], document_text)
    if not verified_quotes:
        verified_quotes = [
            {"quote": "[NO VERIFIED QUOTE — stance set to neutral]",
             "source_doc_id": doc_id, "paragraph": 0}
        ]
        agg["stance_score_mean"] = 0.0
        agg["ci_lower_95"] = -0.3
        agg["ci_upper_95"] = 0.3

    calibrated = calibrate_score(agg["stance_score_mean"], calibrator)
    category = classify_category(calibrated, bool(agg["flexibility_signals"]))

    system, user_template = load_prompt_v1_2()
    stance = Stance(
        stance_id=f"{country.lower().replace(' ', '_')}-{issue.lower()}-"
                  f"{cop_session.lower()}-{datetime.utcnow().timestamp():.0f}",
        country=country,
        issue=issue,
        issue_description=issue_description,
        cop_session=cop_session,
        date_context=date_context,
        stance_score_raw_samples=agg["sample_stance_scores"],
        stance_score_mean=agg["stance_score_mean"],
        stance_score_std=agg["stance_score_std"],
        stance_score_calibrated=calibrated,
        ci_lower_95=agg["ci_lower_95"],
        ci_upper_95=agg["ci_upper_95"],
        stance_category=category,
        key_demands=agg["key_demands"],
        red_lines=agg["red_lines"],
        flexibility_signals=agg["flexibility_signals"],
        evidence_quotes=[EvidenceQuote(**q) for q in verified_quotes],
        epistemic_alignment=EpistemicAlignment(),
        extraction_metadata=ExtractionMetadata(
            model=provider.model,
            temperature=cfg.temperature,
            samples=cfg.k_samples,
            prompt_version=cfg.prompt_version,
            prompt_hash=prompt_hash(system, user_template),
            extracted_at=datetime.utcnow(),
        ),
    )
    return stance
