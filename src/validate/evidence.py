"""Evidence validator: verify every claim against stance database and analysis JSON.

docs/06_stage3_briefing_generation.md §4 및 .claude/skills/evidence-validator/SKILL.md 참조.
"""
from __future__ import annotations

import re
from typing import Iterable

from rapidfuzz import fuzz

from ..schemas import VerifiedClaim, VerificationReport

NUMERIC_RE = re.compile(r"(?<![\w.])-?\d+(?:[,.]\d+)?(?!\w)")


def split_sentences(text: str) -> list[str]:
    """Naive sentence split. 한국어·영어 모두 커버하는 간단한 휴리스틱."""
    out = []
    buf = []
    for ch in text:
        buf.append(ch)
        if ch in ".!?。！？":
            out.append("".join(buf).strip())
            buf = []
    if buf:
        out.append("".join(buf).strip())
    return [s for s in out if s]


def contains_numeric_claim(sent: str) -> bool:
    return bool(NUMERIC_RE.search(sent))


def extract_numbers(sent: str) -> list[str]:
    return NUMERIC_RE.findall(sent)


def verify_number(n: str, evidence_base: Iterable[str], analysis_json_blob: str) -> bool:
    target = n.replace(",", "")
    for e in evidence_base:
        if target in e.replace(",", ""):
            return True
    return target in analysis_json_blob.replace(",", "")


def verify_quote(quote: str, source_texts: list[str], threshold: float = 85.0) -> bool:
    for t in source_texts:
        if fuzz.partial_ratio(quote, t) >= threshold:
            return True
    return False


def validate_section(
    section_text: str,
    stances: list[dict],
    analysis: dict,
    source_texts: list[str],
) -> VerificationReport:
    sentences = split_sentences(section_text)
    verified: list[VerifiedClaim] = []
    unverified: list[dict] = []
    warnings: list[dict] = []

    evidence_texts = [
        q["quote"] for s in stances for q in s.get("evidence_quotes", [])
    ]
    import json as _json

    analysis_blob = _json.dumps(analysis, ensure_ascii=False)

    for idx, sent in enumerate(sentences):
        if not sent or len(sent) < 20:
            continue
        claim_id = f"C{idx:03d}"
        is_numeric = contains_numeric_claim(sent)
        if is_numeric:
            numbers = extract_numbers(sent)
            if not all(verify_number(n, evidence_texts, analysis_blob) for n in numbers):
                unverified.append(
                    {
                        "claim_id": claim_id,
                        "sentence": sent,
                        "reason": f"Unverifiable numbers: {numbers}",
                    }
                )
                continue
        # structural terms
        structural_terms = [
            "bridge", "centrality", "cluster", "coalition", "divergence",
            "브릿지", "중심성", "클러스터", "연합", "분열",
        ]
        has_structural = any(term in sent.lower() for term in structural_terms)
        if has_structural and not any(term in analysis_blob.lower() for term in structural_terms):
            warnings.append(
                {
                    "claim_id": claim_id,
                    "sentence": sent,
                    "reason": "Uses structural language but weak match to analysis JSON.",
                }
            )
            continue

        verified.append(
            VerifiedClaim(
                claim_id=claim_id,
                sentence=sent,
                confidence=0.85 if is_numeric else 0.75,
            )
        )

    return VerificationReport(
        draft_section=section_text[:100],
        verified_claims=verified,
        unverified_claims=unverified,
        warnings=warnings,
        total_sentences=len(sentences),
        verified_count=len(verified),
        unverified_count=len(unverified),
    )
