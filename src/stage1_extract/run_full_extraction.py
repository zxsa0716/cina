"""Stage 1 expanded extraction — 20+ high-value (country, issue) pairs.

Groq Llama 3.3 70B (free, 30 RPM) 사용.
"""
from __future__ import annotations

import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import fitz

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger("cina.stage1.full")

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))


HIGH_VALUE_TARGETS = [
    # Brazil × all 6 issues (focal country)
    {
        "path": "data/raw/unfccc_submissions/cop30_curated/FCCC_PA_CMA_2025_L25E_final.pdf",
        "doc_id": "FCCC_PA_CMA_2025_L25E_final",
        "country": "Brazil", "issue": "GGA-IND",
        "issue_desc": "Global Goal on Adaptation Indicators (Brazil presidency drafted)",
        "cop": "COP30",
    },
    {
        "path": "data/raw/round8/plano_clima_17/Brazil_PlanoClima_Sumario_Executivo_v2.pdf",
        "doc_id": "Brazil_PlanoClima_Sumario_Executivo",
        "country": "Brazil", "issue": "JT-ADAPT",
        "issue_desc": "Just Transition with Adaptation",
        "cop": "COP30",
    },
    {
        "path": "data/raw/round8/plano_clima_17/Brazil_PlanoSetorial_Saude.pdf",
        "doc_id": "Brazil_Plano_Saude",
        "country": "Brazil", "issue": "GGA-IND",
        "issue_desc": "Health adaptation indicators (UAE-Belém 9c)",
        "cop": "COP30",
    },
    {
        "path": "data/raw/unfccc_submissions/cop30_curated/FCCC_PA_CMA_2025_L24_advance.pdf",
        "doc_id": "FCCC_PA_CMA_2025_L24",
        "country": "Brazil", "issue": "ADAPT-FIN",
        "issue_desc": "Adaptation Finance — tripling by 2035",
        "cop": "COP30",
    },
    {
        "path": "data/raw/unfccc_submissions/cop30_curated/FCCC_PA_CMA_2025_07.pdf",
        "doc_id": "FCCC_PA_CMA_2025_07",
        "country": "Brazil", "issue": "L&D-OP",
        "issue_desc": "Loss and Damage Fund Operations",
        "cop": "COP30",
    },
    {
        "path": "data/raw/round8/plano_clima_17/Brazil_PlanoTematico_Recursos_Hidricos.pdf",
        "doc_id": "Brazil_Plano_Recursos_Hidricos",
        "country": "Brazil", "issue": "NAPs",
        "issue_desc": "National Adaptation Plans water resources",
        "cop": "COP30",
    },
    # AOSIS, LDC, AILAC, LMDC — major groups
    {
        "path": "data/raw/round3/AOSIS_GGA_submission/AOSIS_adaptation_submission_2024_data_gaps.pdf",
        "doc_id": "AOSIS_2024_data_gaps",
        "country": "AOSIS", "issue": "GGA-IND",
        "issue_desc": "GGA indicators — SIDS justice frame",
        "cop": "COP30",
    },
    {
        "path": "data/raw/round3/AOSIS_GGA_submission/AOSIS_SCF_needs_survey.pdf",
        "doc_id": "AOSIS_SCF_needs",
        "country": "AOSIS", "issue": "ADAPT-FIN",
        "issue_desc": "Adaptation finance needs SIDS",
        "cop": "COP30",
    },
    {
        "path": "data/raw/round3/LMDC_AILAC_submission/LMDC_submission_on_GGA.pdf",
        "doc_id": "LMDC_GGA_submission",
        "country": "India", "issue": "GGA-IND",
        "issue_desc": "LMDC sovereignty CBDR-RC stance",
        "cop": "COP30",
    },
    {
        "path": "data/raw/round3/LMDC_AILAC_submission/LMDC_supplementary_note_9_1_DEA.pdf",
        "doc_id": "LMDC_supplementary_DEA",
        "country": "India", "issue": "ADAPT-FIN",
        "issue_desc": "LMDC adaptation finance (means of implementation)",
        "cop": "COP30",
    },
    # Korea (Track A focus)
    {
        "path": "data/raw/round8/adaptation_communication/Korea_Republic_Adaptation_Communication_2023.pdf",
        "doc_id": "Korea_AdComm_2023",
        "country": "South Korea", "issue": "NAPs",
        "issue_desc": "Korean adaptation policy framework",
        "cop": "COP28",
    },
    {
        "path": "data/raw/round8/adaptation_communication/Korea_Republic_Adaptation_Communication_2023.pdf",
        "doc_id": "Korea_AdComm_2023_GGA",
        "country": "South Korea", "issue": "GGA-IND",
        "issue_desc": "Korean stance on GGA indicators",
        "cop": "COP30",
    },
    # Procedural authority — chair letters
    {
        "path": "data/raw/round4/historical_chair_letter/COP28_UAE_letter.pdf",
        "doc_id": "COP28_UAE_chair_letter",
        "country": "United Arab Emirates", "issue": "GGA-IND",
        "issue_desc": "COP28 presidency letter (UAE)",
        "cop": "COP28",
    },
    # Belém Adaptation Indicators thematic 5
    {
        "path": "data/raw/unfccc_submissions/cop30_curated/UAE_Belem_9a_Water.pdf",
        "doc_id": "UAE_Belem_9a_Water",
        "country": "Multi", "issue": "GGA-IND",
        "issue_desc": "UAE-Belém Water Indicators (9a)",
        "cop": "COP30",
    },
    {
        "path": "data/raw/unfccc_submissions/cop30_curated/UAE_Belem_9b_Food.pdf",
        "doc_id": "UAE_Belem_9b_Food",
        "country": "Multi", "issue": "GGA-IND",
        "issue_desc": "UAE-Belém Food Indicators (9b)",
        "cop": "COP30",
    },
    {
        "path": "data/raw/unfccc_submissions/cop30_curated/UAE_Belem_9c_Health.pdf",
        "doc_id": "UAE_Belem_9c_Health",
        "country": "Multi", "issue": "GGA-IND",
        "issue_desc": "UAE-Belém Health Indicators (9c, 54 indicators)",
        "cop": "COP30",
    },
    # Mutirao Decision (overall COP30)
    {
        "path": "data/raw/unfccc_submissions/cop30_curated/Mutirao_Decision_DT_cop30_01.pdf",
        "doc_id": "Mutirao_Decision",
        "country": "Brazil", "issue": "MIT-ADAPT",
        "issue_desc": "Mutirão Decision (Brazil overall framing)",
        "cop": "COP30",
    },
    # GGA decision text
    {
        "path": "data/raw/unfccc_submissions/cop30_curated/GGA_COP30_decision_5.pdf",
        "doc_id": "GGA_COP30_decision_5",
        "country": "Multi", "issue": "GGA-IND",
        "issue_desc": "GGA COP30 decision text (CMA.7)",
        "cop": "COP30",
    },
]


SYSTEM_PROMPT = """You are a climate diplomacy analyst extracting structured stance from UNFCCC documents.

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
  "salience_score": float in [0,1],
  "procedural_signals": {
    "is_chair_role": bool,
    "is_pen_holder": bool,
    "drafts_text_for_issue": string|null
  },
  "confidence": float in [0,1],
  "reasoning": string
}

Cite ONLY direct quotes (no paraphrasing). Use full [-1,+1] range.
If document does not address country×issue: stance_score=0, confidence=0, empty arrays."""


def extract_one(provider, target: dict) -> dict | None:
    path = ROOT / target["path"]
    if not path.exists():
        return None
    try:
        doc = fitz.open(str(path))
        text = ""
        for page in doc[:8]:
            text += page.get_text() + "\n\n"
        doc.close()
        text = text[:7000]
    except Exception as exc:
        logger.warning("PDF parse failed: %s", exc)
        return None

    if len(text) < 100:
        return None

    user = (
        f"Country: {target['country']}\n"
        f"Issue: {target['issue']} - {target['issue_desc']}\n\n"
        f"Document excerpt:\n=== START ===\n{text}\n=== END ===\n"
        f"Source: {target['doc_id']}\n\n"
        f"Extract stance per v1.3 schema. JSON only."
    )

    try:
        resp = provider.complete(SYSTEM_PROMPT, user, json_schema={"type": "object"})
        parsed = resp.parse_json(strict=False)
        if not parsed:
            return None
        parsed["_meta"] = {
            "doc_id": target["doc_id"],
            "country": target["country"],
            "issue": target["issue"],
            "cop": target["cop"],
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "provider": provider.name,
            "model": provider.model,
            "usage": resp.usage,
        }
        return parsed
    except Exception as exc:
        logger.warning("LLM call failed: %s", exc)
        return None


def main() -> int:
    from src.stage1_extract.providers import get_provider

    backend = os.environ.get("CINA_LLM_PROVIDER", "groq")
    provider = get_provider(backend, temperature=0.3, max_tokens=2000)
    logger.info("Provider: %s / %s", provider.name, provider.model)
    logger.info("Targets: %d", len(HIGH_VALUE_TARGETS))

    results = []
    for i, target in enumerate(HIGH_VALUE_TARGETS, 1):
        logger.info("[%d/%d] %s × %s", i, len(HIGH_VALUE_TARGETS), target["country"], target["issue"])
        rec = extract_one(provider, target)
        if rec:
            score = rec.get("stance_score", "?")
            score_str = f"{score:+.2f}" if isinstance(score, (int, float)) else "?"
            cat = rec.get("stance_category", "?")
            frame = rec.get("frame_type", "?")
            chair = rec.get("procedural_signals", {}).get("is_chair_role", False)
            pen = rec.get("procedural_signals", {}).get("is_pen_holder", False)
            print(f"  {target['country']:<14} {target['issue']:<10} stance={score_str} ({cat:<20}) frame={frame:<12} chair={chair} pen={pen}")
            results.append(rec)
        else:
            print(f"  {target['country']:<14} {target['issue']:<10} FAILED or N/A")
        # Rate limit: 30 RPM = 2s/call safe
        time.sleep(2.5)

    out = ROOT / "data" / "processed" / "stances_full_v1.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    total_tokens = sum(r.get("_meta", {}).get("usage", {}).get("total_tokens", 0) for r in results)
    logger.info("Stage 1 full extraction: %d/%d", len(results), len(HIGH_VALUE_TARGETS))
    logger.info("Output: %s", out)
    logger.info("Total tokens: %d (cost: $0)", total_tokens)
    return 0


if __name__ == "__main__":
    sys.exit(main())
