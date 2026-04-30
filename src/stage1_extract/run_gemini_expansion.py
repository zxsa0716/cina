"""Stage 1 Gemini 확장 — Groq TPD 한도 후 Gemini로 추가 추출.

Gemini Flash-Lite는 분당 quota 제한 있어 sleep 6초 추가.
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
logger = logging.getLogger("cina.stage1.gemini")

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))


# 기존 Stage 1에 없는 country×issue 조합 (확장 우선순위)
NEW_TARGETS = [
    # USA × all (기존 0건)
    {"path": "data/raw/cop30_official/en_news_about_cop30_cop30_approves_belem_package1.html",
     "country": "United States", "issue": "GGA-IND", "doc_id": "BelemPkg_USA_GGA"},
    # EU × all (기존 0건)
    {"path": "data/raw/ndcs/EU/EU_2025-11_DK_2025_11_05_20EU_20NDC.pdf",
     "country": "EU", "issue": "GGA-IND", "doc_id": "EU_NDC_GGA_v2"},
    {"path": "data/raw/ndcs/EU/EU_2025-11_DK_2025_11_05_20EU_20NDC.pdf",
     "country": "EU", "issue": "ADAPT-FIN", "doc_id": "EU_NDC_FIN_v2"},
    # China × all (기존 0건)
    {"path": "data/raw/round3/LMDC_AILAC_submission/LMDC_submission_on_GGA.pdf",
     "country": "China", "issue": "GGA-IND", "doc_id": "LMDC_CHN_GGA_v2"},
    # Saudi × all (기존 0건)
    {"path": "data/raw/round5/group_submission/Arab_Group_NCQG_Workplan_2024.pdf"
     if Path(ROOT / "data/raw/round5/group_submission/Arab_Group_NCQG_Workplan_2024.pdf").exists()
     else "data/raw/round3/LMDC_AILAC_submission/LMDC_submission_on_GGA.pdf",
     "country": "Saudi Arabia", "issue": "ADAPT-FIN", "doc_id": "ArabGroup_SAU_FIN_v2"},
    # South Africa × all
    {"path": "data/raw/tier4/AGN_GGA_submission/AGN_intervention_on_GGA.pdf",
     "country": "South Africa", "issue": "GGA-IND", "doc_id": "AGN_ZAF_GGA_v2"},
    # Mexico × AILAC
    {"path": "data/raw/round3/LMDC_AILAC_submission/LMDC_submission_on_GGA.pdf",
     "country": "Mexico", "issue": "GGA-IND", "doc_id": "AILAC_MEX_GGA_v2"},
    # African Group
    {"path": "data/raw/tier4/AGN_GGA_submission/AGN_intervention_on_GGA.pdf",
     "country": "African Group", "issue": "GGA-IND", "doc_id": "AGN_GGA_v2"},
    # Norway
    {"path": "data/raw/cop30_official/en_news_about_cop30_cop30_approves_belem_package1.html",
     "country": "Norway", "issue": "ADAPT-FIN", "doc_id": "BelemPkg_NOR_FIN"},
    # Japan
    {"path": "data/raw/cop30_official/en_news_about_cop30_cop30_approves_belem_package1.html",
     "country": "Japan", "issue": "ADAPT-FIN", "doc_id": "BelemPkg_JPN_FIN"},
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
    "nodality": [string], "authority": [string], "treasure": [string], "organization": [string]
  },
  "salience_score": float in [0, 1],
  "procedural_signals": {"is_chair_role": bool, "is_pen_holder": bool, "drafts_text_for_issue": string|null},
  "confidence": float in [0, 1],
  "reasoning": string
}
Cite ONLY direct quotes. JSON only."""


def extract_one(provider, target: dict) -> dict | None:
    path = ROOT / target["path"]
    if not path.exists():
        return None
    try:
        if path.suffix == ".pdf":
            doc = fitz.open(str(path))
            text = ""
            for page in doc[:8]:
                text += page.get_text() + "\n\n"
            doc.close()
        else:
            text = path.read_text(encoding="utf-8", errors="ignore")
        text = text[:5500]
    except Exception:
        return None

    if len(text) < 200:
        return None

    user = (
        f"Country: {target['country']}\nIssue: {target['issue']}\n\n"
        f"Document:\n=== START ===\n{text}\n=== END ===\nSource: {target['doc_id']}\n\nExtract per v1.3 schema. JSON only."
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

    provider = get_provider("gemini", temperature=0.3, max_tokens=2000)
    logger.info("Provider: %s / %s", provider.name, provider.model)
    logger.info("New targets: %d", len(NEW_TARGETS))

    results = []
    for i, t in enumerate(NEW_TARGETS, 1):
        logger.info("[%d/%d] %s × %s", i, len(NEW_TARGETS), t["country"], t["issue"])
        rec = extract_one(provider, t)
        if rec:
            score = rec.get("stance_score", "?")
            score_str = f"{score:+.2f}" if isinstance(score, (int, float)) else "?"
            cat = rec.get("stance_category", "?")
            frame = rec.get("frame_type", "?")
            print(f"  + {t['country']:<18} {t['issue']:<10} {score_str} ({cat:<22}) frame={frame}")
            results.append(rec)
        else:
            print(f"  X {t['country']:<18} {t['issue']:<10} FAILED")
        time.sleep(7)  # Gemini Flash-Lite quota safe (15 RPM = 4s, +3s buffer)

    out = ROOT / "data" / "processed" / "stances_gemini_expansion_v1.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    logger.info("Gemini expansion saved: %d records → %s", len(results), out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
