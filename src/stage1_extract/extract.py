"""Stage 1: LLM stance extraction with multi-sampling and calibration.

docs/04_stage1_stance_extraction.md 참조.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import pickle
from datetime import datetime
from pathlib import Path

import numpy as np
from anthropic import AsyncAnthropic
from rapidfuzz import fuzz
from scipy.stats import beta

from ..config import Stage1Config
from ..schemas import (
    EpistemicAlignment,
    EvidenceQuote,
    ExtractionMetadata,
    Stance,
)


# ---------------------------------------------------------------------------
# Prompt loading
# ---------------------------------------------------------------------------
def load_prompt_v1_2() -> tuple[str, str]:
    """System and user prompt templates for extraction v1.2.

    Returns:
        (system_prompt, user_template)
    """
    system = """You are a specialized climate diplomacy analyst. Your task is to extract
a country's stance on a specific climate negotiation issue from official UNFCCC documents.

Theoretical framework:
- A country's stance reflects its "win-set" — the intersection of international and
  domestic political feasibility (Putnam 1988, Two-Level Games).
- Within a stance, distinguish:
  * key_demands: what the country actively seeks
  * red_lines: hard constraints imposed by domestic politics
  * flexibility_signals: language suggesting the country could move

Analyst discipline:
1. Cite only direct quotes from the provided document. No paraphrasing in evidence.
2. If the document does not address the issue, return stance_score=0, confidence=0, empty arrays.
3. Use the full [-1, +1] range. Do NOT default to ±0.5.
4. If a country's statement is ambiguous, lower confidence and widen your mental uncertainty.

Output: strict JSON matching the required schema. No markdown, no commentary."""

    user_template = """Country: {country}
Issue: {issue_label} — {issue_description}

Document excerpt:
=== DOC START ===
{paragraphs_joined}
=== DOC END ===
Source document ID: {doc_id}

Extract the country's stance on this specific issue. If the document speaks about other
issues, do NOT invent a stance — return stance_score=0, confidence=0, and empty arrays.

Respond with JSON only, matching this schema:
{{
  "country": "...",
  "issue": "...",
  "stance_score": <number in [-1, 1]>,
  "stance_category": "<one of: strong_support, support, conditional_support, neutral_or_silent, oppose, strong_oppose>",
  "key_demands": ["..."],
  "red_lines": ["..."],
  "flexibility_signals": ["..."],
  "evidence_quotes": [
    {{"quote": "...", "source_doc_id": "...", "paragraph": <int>}}
  ],
  "confidence": <number in [0, 1]>,
  "reasoning": "..."
}}"""
    return system, user_template


def prompt_hash(system: str, user_template: str) -> str:
    h = hashlib.sha256()
    h.update(system.encode())
    h.update(user_template.encode())
    return h.hexdigest()[:16]


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------
async def _single_extract(
    client: AsyncAnthropic,
    cfg: Stage1Config,
    country: str,
    issue: str,
    issue_description: str,
    paragraphs: str,
    doc_id: str,
) -> dict:
    system, user_template = load_prompt_v1_2()
    user = user_template.format(
        country=country,
        issue_label=issue,
        issue_description=issue_description,
        paragraphs_joined=paragraphs,
        doc_id=doc_id,
    )
    msg = await client.messages.create(
        model=cfg.model,
        max_tokens=cfg.max_tokens,
        temperature=cfg.temperature,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = msg.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


async def extract_samples(
    client: AsyncAnthropic,
    cfg: Stage1Config,
    country: str,
    issue: str,
    issue_description: str,
    paragraphs: str,
    doc_id: str,
) -> list[dict]:
    tasks = [
        _single_extract(client, cfg, country, issue, issue_description, paragraphs, doc_id)
        for _ in range(cfg.k_samples)
    ]
    return await asyncio.gather(*tasks, return_exceptions=False)


# ---------------------------------------------------------------------------
# Aggregation and Bayesian CI
# ---------------------------------------------------------------------------
def aggregate_samples(samples: list[dict]) -> dict:
    scores = [s["stance_score"] for s in samples]
    confidences = [s.get("confidence", 0.5) for s in samples]

    total_w = sum(confidences) or 1.0
    weights = np.array(confidences) / total_w
    weighted_mean = float(np.sum(np.array(scores) * weights))

    rescaled = [(s + 1) / 2 for s in scores]
    k = len(samples)
    alpha_post = 1 + sum(rescaled) * k
    beta_post = 1 + (k - sum(rescaled)) * k
    ci_low_01, ci_up_01 = beta.ppf([0.025, 0.975], alpha_post, beta_post)
    ci_low = float(ci_low_01 * 2 - 1)
    ci_up = float(ci_up_01 * 2 - 1)

    merged_demands = list({d for s in samples for d in s.get("key_demands", [])})
    merged_red_lines = list({r for s in samples for r in s.get("red_lines", [])})
    merged_flex = list({f for s in samples for f in s.get("flexibility_signals", [])})

    all_quotes = [q for s in samples for q in s.get("evidence_quotes", [])]
    seen = set()
    unique_quotes = []
    for q in all_quotes:
        h = hashlib.md5(q["quote"].encode()).hexdigest()
        if h not in seen:
            seen.add(h)
            unique_quotes.append(q)

    return {
        "sample_stance_scores": scores,
        "stance_score_mean": weighted_mean,
        "stance_score_std": float(np.std(scores)),
        "ci_lower_95": ci_low,
        "ci_upper_95": ci_up,
        "key_demands": merged_demands,
        "red_lines": merged_red_lines,
        "flexibility_signals": merged_flex,
        "evidence_quotes": unique_quotes,
        "mean_confidence": float(np.mean(confidences)),
    }


# ---------------------------------------------------------------------------
# Calibration
# ---------------------------------------------------------------------------
def load_calibrator(path: Path):
    if not path.exists():
        return None
    with open(path, "rb") as f:
        return pickle.load(f)


def calibrate_score(raw_score: float, calibrator) -> float:
    if calibrator is None:
        return raw_score
    rescaled = (raw_score + 1) / 2
    prob = calibrator.predict_proba([[rescaled]])[0, 1]
    return float(prob * 2 - 1)


# ---------------------------------------------------------------------------
# Evidence verification
# ---------------------------------------------------------------------------
def verify_evidence_quotes(quotes: list[dict], source_text: str, threshold: float = 85) -> list[dict]:
    """fuzzy match 각 quote against source_text. 통과한 것만 리턴."""
    verified = []
    for q in quotes:
        score = fuzz.partial_ratio(q["quote"], source_text)
        if score >= threshold:
            verified.append(q)
    return verified


def classify_category(score: float, has_flexibility: bool = False) -> str:
    if score >= 0.7:
        return "strong_support"
    if 0.3 <= score < 0.7:
        return "support"
    if 0.1 <= score < 0.3 and has_flexibility:
        return "conditional_support"
    if -0.1 < score < 0.1:
        return "neutral_or_silent"
    if -0.7 < score <= -0.1:
        return "oppose"
    return "strong_oppose"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
async def extract_stance(
    client: AsyncAnthropic,
    cfg: Stage1Config,
    country: str,
    issue: str,
    issue_description: str,
    document_text: str,
    doc_id: str,
    cop_session: str,
    date_context: str,
    calibrator=None,
) -> Stance:
    samples = await extract_samples(
        client, cfg, country, issue, issue_description, document_text, doc_id
    )
    agg = aggregate_samples(samples)

    verified_quotes = verify_evidence_quotes(agg["evidence_quotes"], document_text)
    if not verified_quotes:
        # 실패 시 의미 있는 stance로 볼 수 없음
        verified_quotes = [
            {"quote": "[NO VERIFIED QUOTE — stance set to neutral]", "source_doc_id": doc_id, "paragraph": 0}
        ]
        agg["stance_score_mean"] = 0.0
        agg["ci_lower_95"] = -0.3
        agg["ci_upper_95"] = 0.3

    calibrated = calibrate_score(agg["stance_score_mean"], calibrator)
    category = classify_category(calibrated, bool(agg["flexibility_signals"]))

    system, user_template = load_prompt_v1_2()
    stance = Stance(
        stance_id=f"{country.lower().replace(' ', '_')}-{issue.lower()}-{cop_session.lower()}-{datetime.utcnow().timestamp():.0f}",
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
            model=cfg.model,
            temperature=cfg.temperature,
            samples=cfg.k_samples,
            prompt_version=cfg.prompt_version,
            prompt_hash=prompt_hash(system, user_template),
            extracted_at=datetime.utcnow(),
        ),
    )
    return stance
