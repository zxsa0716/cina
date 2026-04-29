"""Stage 3: Graph-Grounded Briefing Generation.

docs/06_stage3_briefing_generation.md 참조.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from anthropic import AsyncAnthropic

from ..config import Stage3Config


SECTION_TITLES_KO = {
    "1": "§1. 현황 평가",
    "2": "§2. 연합 지형 (Coalition Map)",
    "3": "§3. 레버리지 분석",
    "4": "§4. 패키지 딜 기회",
    "5": "§5. Red Lines 및 위험",
    "6": "§6. 권고 전략 자세",
    "7": "§7. 시나리오 분석",
}
SECTION_TITLES_EN = {
    "1": "§1. Situation Assessment",
    "2": "§2. Coalition Map",
    "3": "§3. Leverage Analysis",
    "4": "§4. Package Deal Opportunities",
    "5": "§5. Red Lines and Risks",
    "6": "§6. Recommended Strategic Posture",
    "7": "§7. Scenario Analysis",
}


def section_prompt(
    section_id: str,
    section_title: str,
    analysis_subset: dict,
    evidence_quotes: list[dict],
    focal_country: str,
    language: str,
    max_words: int,
) -> str:
    lang_label = "Korean" if language == "ko" else "English"
    return f"""You are drafting a ministerial briefing for {focal_country}'s climate envoy.
You are writing Section {section_id}: {section_title}.

STRUCTURED ANALYSIS for this section (JSON):
{json.dumps(analysis_subset, ensure_ascii=False, indent=2)}

AVAILABLE EVIDENCE QUOTES (cite only these, by source_doc_id):
{json.dumps(evidence_quotes, ensure_ascii=False, indent=2)}

CONSTRAINTS:
1. Every factual claim must cite at least one evidence_quote via its source_doc_id.
2. Every structural claim (coalition, centrality, linkage, divergence) must cite the analysis JSON field.
3. Output language: {lang_label}. Tone: concise, official diplomatic brief.
4. Maximum length: {max_words} words.
5. Do not invent numbers or countries. Copy from provided data.
6. Format: Markdown under heading `## {section_title}`.

OUTPUT the section in Markdown only.
"""


def section_inputs(analysis: dict, stances: list[dict], focal_country: str) -> dict[str, dict]:
    """섹션별로 필요한 analysis subset 추출."""
    focal_stances = [s for s in stances if s.get("country") == focal_country]
    return {
        "1": {
            "focal_stances": focal_stances,
            "issues_covered": list(analysis.get("issue_analyses", {}).keys()),
        },
        "2": {
            "issue_communities": {
                k: v.get("communities", [])
                for k, v in analysis.get("issue_analyses", {}).items()
            }
        },
        "3": {
            "bridge_countries": {
                k: v.get("bridge_countries", [])
                for k, v in analysis.get("issue_analyses", {}).items()
            },
            "top_attention_nodes": {
                k: v.get("top_attention_nodes", [])
                for k, v in analysis.get("issue_analyses", {}).items()
            },
        },
        "4": {
            "hyperedges": analysis.get("cross_issue_hyperedges", []),
        },
        "5": {
            "epistemic_divergence": analysis.get("epistemic_divergence", {}),
            "focal_red_lines": [
                rl for s in focal_stances for rl in s.get("red_lines", [])
            ],
        },
        "6": {
            "focal_stances": focal_stances,
            "bridge_countries": {
                k: v.get("bridge_countries", [])
                for k, v in analysis.get("issue_analyses", {}).items()
            },
            "hyperedges": analysis.get("cross_issue_hyperedges", []),
        },
        "7": {
            "epistemic_divergence": analysis.get("epistemic_divergence", {}),
            "hyperedges": analysis.get("cross_issue_hyperedges", []),
        },
    }


async def generate_section(
    client: AsyncAnthropic,
    cfg: Stage3Config,
    section_id: str,
    section_title: str,
    analysis_subset: dict,
    evidence_quotes: list[dict],
) -> str:
    prompt = section_prompt(
        section_id=section_id,
        section_title=section_title,
        analysis_subset=analysis_subset,
        evidence_quotes=evidence_quotes,
        focal_country=cfg.focal_country,
        language=cfg.language,
        max_words=cfg.max_words_per_section,
    )
    msg = await client.messages.create(
        model=cfg.model,
        max_tokens=2500,
        temperature=cfg.temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def compile_briefing(
    sections: dict[str, str],
    executive_summary: str,
    focal_country: str,
    cop: int,
    sector: str,
    language: str,
) -> str:
    titles = SECTION_TITLES_KO if language == "ko" else SECTION_TITLES_EN

    if language == "ko":
        header = f"""# 외교부 기후환경과학외교국 보고

**문서**: CINA 자동생성 (Framework v2.0)
**대상**: {focal_country} 기후대사 귀하
**주제**: COP{cop} {sector.capitalize()} 협상 전략

---

## 경영진 요약

{executive_summary}

---
"""
    else:
        header = f"""# Ministerial Briefing — {focal_country}, COP{cop} {sector.capitalize()}

Prepared by: CINA Framework v2.0

---

## Executive Summary

{executive_summary}

---
"""
    body = "\n\n---\n\n".join(
        sections[sid] for sid in ["1", "2", "3", "4", "5", "6", "7"] if sid in sections
    )
    return header + body


def save_briefing(text: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
