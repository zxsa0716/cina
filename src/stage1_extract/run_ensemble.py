"""Run multi-LLM ensemble extraction on seed documents.

Usage:
    set GEMINI_API_KEY=...
    set GROQ_API_KEY=...
    # Ollama assumed running on localhost:11434
    python -m src.stage1_extract.run_ensemble
"""
from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

import fitz

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger("cina.stage1.ensemble")

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from src.stage1_extract.ensemble import ensemble_extract


SEED_DOCS = [
    {
        "path": "data/raw/unfccc_submissions/cop30_curated/FCCC_PA_CMA_2025_L25E_final.pdf",
        "doc_id": "FCCC_PA_CMA_2025_L25E_final",
        "country": "Brazil",
        "issue": "GGA-IND",
        "issue_desc": "Global Goal on Adaptation Indicators - Brazil presidency drafting",
    },
    {
        "path": "data/raw/round3/AOSIS_GGA_submission/AOSIS_adaptation_submission_2024_data_gaps.pdf",
        "doc_id": "AOSIS_adaptation_submission_2024",
        "country": "AOSIS",
        "issue": "GGA-IND",
        "issue_desc": "Global Goal on Adaptation Indicators - SIDS justice frame",
    },
    {
        "path": "data/raw/round3/LMDC_AILAC_submission/LMDC_submission_on_GGA.pdf",
        "doc_id": "LMDC_submission_on_GGA",
        "country": "India",
        "issue": "GGA-IND",
        "issue_desc": "Global Goal on Adaptation - LMDC sovereignty CBDR-RC",
    },
    {
        "path": "data/raw/round8/plano_clima_17/Brazil_PlanoClima_Sumario_Executivo_v2.pdf",
        "doc_id": "Brazil_PlanoClima_Sumario_Executivo",
        "country": "Brazil",
        "issue": "JT-ADAPT",
        "issue_desc": "Just Transition with adaptation - Brazil domestic Plano Clima",
    },
]


def main() -> int:
    # Verify all 3 LLM env vars are present
    needs = []
    if not os.environ.get("GEMINI_API_KEY"):
        needs.append("GEMINI_API_KEY")
    if not os.environ.get("GROQ_API_KEY"):
        needs.append("GROQ_API_KEY")
    if needs:
        logger.warning("Missing env vars: %s — some roles will skip", needs)

    out = ROOT / "data" / "processed" / "stances_ensemble_v1.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    results = []

    for seed in SEED_DOCS:
        path = ROOT / seed["path"]
        if not path.exists():
            logger.warning("Skip (not found): %s", path)
            continue

        try:
            doc = fitz.open(str(path))
            text = ""
            for page in doc[:10]:
                text += page.get_text() + "\n\n"
            doc.close()
        except Exception as exc:
            logger.error("PDF parse failed: %s", exc)
            continue

        logger.info(
            "Ensemble: %s / %s (doc_chars=%d)",
            seed["country"], seed["issue"], len(text),
        )
        rec = ensemble_extract(
            text=text,
            country=seed["country"],
            issue=seed["issue"],
            issue_desc=seed["issue_desc"],
            doc_id=seed["doc_id"],
        )
        results.append(rec)

        ens = rec["ensemble"]
        meta = rec["_meta"]
        print(f"  + {seed['country']:<14} {seed['issue']:<10} "
              f"consensus={ens['consensus_stance_score']:.2f} "
              f"std={ens['consensus_std']:.2f} "
              f"({ens['consensus_quality']}) "
              f"providers={meta['providers_used']} "
              f"time={meta['elapsed_sec']}s")
        for prov, score in ens["individual_scores"].items():
            print(f"      {prov}: {score:.2f}")

    with open(out, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    logger.info("Ensemble extractions saved: %d → %s", len(results), out)

    # Summary stats
    if results:
        std_values = [r["ensemble"]["consensus_std"] for r in results]
        agreements = [r["ensemble"]["consensus_quality"] for r in results]
        high = sum(1 for a in agreements if a == "high_agreement")
        partial = sum(1 for a in agreements if a == "partial_agreement")
        disagree = sum(1 for a in agreements if a == "disagreement_flag")
        print()
        print(f"=== Ensemble summary ===")
        print(f"  Mean consensus std: {sum(std_values)/len(std_values):.3f}")
        print(f"  High agreement: {high}/{len(results)}")
        print(f"  Partial:        {partial}/{len(results)}")
        print(f"  Disagreement:   {disagree}/{len(results)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
