"""Stage 1 시드 추출 — Groq/Gemini/Ollama provider 사용.

Heedo가 환경변수 설정 후 실행:
    set GROQ_API_KEY=...
    set CINA_LLM_PROVIDER=groq
    python -m src.stage1_extract.run_seed_extraction
"""
from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import fitz  # pymupdf

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger("cina.stage1.seed")

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))


SEED_DOCS = [
    {
        "path": "data/raw/unfccc_submissions/cop30_curated/FCCC_PA_CMA_2025_L25E_final.pdf",
        "doc_id": "FCCC_PA_CMA_2025_L25E_final",
        "country": "Brazil",
        "issue": "GGA-IND",
        "issue_desc": "Global Goal on Adaptation Indicators",
        "cop": "COP30",
        "date": "2025-11-22",
    },
    {
        "path": "data/raw/round3/AOSIS_GGA_submission/AOSIS_adaptation_submission_2024_data_gaps.pdf",
        "doc_id": "AOSIS_adaptation_submission_2024",
        "country": "AOSIS",
        "issue": "GGA-IND",
        "issue_desc": "GGA indicators - SIDS perspective",
        "cop": "COP30",
        "date": "2024-04-03",
    },
    {
        "path": "data/raw/round3/LMDC_AILAC_submission/LMDC_submission_on_GGA.pdf",
        "doc_id": "LMDC_submission_on_GGA",
        "country": "India",
        "issue": "GGA-IND",
        "issue_desc": "GGA indicators - LMDC sovereignty stance",
        "cop": "COP30",
        "date": "2024-08-15",
    },
    {
        "path": "data/raw/round8/plano_clima_17/Brazil_PlanoClima_Sumario_Executivo_v2.pdf",
        "doc_id": "Brazil_PlanoClima_Sumario_Executivo",
        "country": "Brazil",
        "issue": "JT-ADAPT",
        "issue_desc": "Just Transition with Adaptation - Brazil domestic policy",
        "cop": "COP30",
        "date": "2024-05-15",
    },
    {
        "path": "data/raw/round8/adaptation_communication/Korea_Republic_Adaptation_Communication_2023.pdf",
        "doc_id": "Korea_Republic_AdComm_2023",
        "country": "South Korea",
        "issue": "NAPs",
        "issue_desc": "National Adaptation Plans - Korean policy framework",
        "cop": "COP28",
        "date": "2023-03-01",
    },
]

SYSTEM_PROMPT = """You are a climate diplomacy analyst extracting a country's stance from official UNFCCC documents.

Output strictly valid JSON with these fields:
- stance_score: float in [-1, 1] (-1=strong oppose, 0=neutral, +1=strong support)
- stance_category: one of [strong_support, support, conditional_support, neutral_or_silent, oppose, strong_oppose]
- key_demands: list of strings (what country seeks)
- red_lines: list of strings (hard constraints)
- flexibility_signals: list of strings (language suggesting movement)
- evidence_quotes: list of objects with {quote: string, location: string}
- frame_type: one of [scientific, justice, sovereignty, security, development, mixed]
- instrument_signals: object with keys nodality, authority, treasure, organization (each a list of direct quotes)
- confidence: float in [0,1]
- reasoning: short explanation

Cite ONLY direct quotes from the document. No paraphrasing in evidence_quotes."""


def extract_one(provider, seed: dict) -> dict | None:
    if not Path(seed["path"]).exists():
        logger.warning("File not found: %s", seed["path"])
        return None

    try:
        doc = fitz.open(seed["path"])
        text = ""
        for page in doc[:10]:
            text += page.get_text() + "\n\n"
        doc.close()
        text = text[:8000]
    except Exception as exc:
        logger.error("PDF parse failed for %s: %s", seed["path"], exc)
        return None

    country = seed["country"]
    issue = seed["issue"]
    desc = seed["issue_desc"]
    doc_id = seed["doc_id"]

    user = (
        f"Country: {country}\n"
        f"Issue: {issue} - {desc}\n\n"
        f"Document excerpt:\n=== DOC START ===\n{text}\n=== DOC END ===\n"
        f"Source: {doc_id}\n\n"
        f"Extract the stance. JSON only."
    )

    try:
        resp = provider.complete(
            system=SYSTEM_PROMPT,
            user=user,
            json_schema={"type": "object"},
        )
        parsed = resp.parse_json(strict=False)
        if not parsed:
            return None
        parsed["_meta"] = {
            "doc_id": doc_id,
            "country": country,
            "issue": issue,
            "cop": seed["cop"],
            "date_context": seed["date"],
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "provider": provider.name,
            "model": provider.model,
            "usage": resp.usage,
        }
        return parsed
    except Exception as exc:
        logger.error("LLM call failed for %s/%s: %s", country, issue, exc)
        return None


def main() -> int:
    from src.stage1_extract.providers import get_provider

    backend = os.environ.get("CINA_LLM_PROVIDER", "groq").lower()
    provider = get_provider(backend, temperature=0.3, max_tokens=2000)
    logger.info("Provider: %s / %s", provider.name, provider.model)

    results = []
    for seed in SEED_DOCS:
        logger.info("Extract: %s / %s", seed["country"], seed["issue"])
        rec = extract_one(provider, seed)
        if rec:
            score = rec.get("stance_score", "?")
            score_str = f"{score:.2f}" if isinstance(score, (int, float)) else "?"
            cat = rec.get("stance_category", "?")
            conf = rec.get("confidence", "?")
            frame = rec.get("frame_type", "?")
            print(f"  + {seed['country']:<14} {seed['issue']:<10} stance={score_str} ({cat}), conf={conf}, frame={frame}")
            ks = rec.get("key_demands", [])
            if ks:
                print(f"      key_demands: {ks[:2]}")
            results.append(rec)
        else:
            print(f"  X {seed['country']} / {seed['issue']} FAILED")

    out = ROOT / "data" / "processed" / "stances_seed_v1.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    total_tokens = sum(r.get("_meta", {}).get("usage", {}).get("total_tokens", 0) for r in results)
    logger.info("Stage 1 seed extraction complete: %d/%d", len(results), len(SEED_DOCS))
    logger.info("Output: %s", out)
    logger.info("Total tokens: %d (cost: $0 free tier)", total_tokens)
    return 0


if __name__ == "__main__":
    sys.exit(main())
