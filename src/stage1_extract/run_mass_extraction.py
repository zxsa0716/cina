"""Stage 1 대량 추출 — 20국 × 핵심 이슈 = 60+ records.

각 (country, issue) 조합에 대해 가장 적합한 문서를 선택해서 LLM 추출.
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
logger = logging.getLogger("cina.stage1.mass")

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))


# 20 CINA 국가 + 추가 그룹 — 6 이슈 매트릭스
# 각 cell마다 가장 잘 매치되는 문서 선택
TARGETS = [
    # === Brazil (focal — all 6) ===
    {"path": "data/raw/unfccc_submissions/cop30_curated/FCCC_PA_CMA_2025_L25E_final.pdf",
     "country": "Brazil", "issue": "GGA-IND", "doc_id": "L25E_BRA_GGA"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoSetorial_Saude.pdf",
     "country": "Brazil", "issue": "GGA-IND", "doc_id": "PlanoSaude_BRA_GGA"},
    {"path": "data/raw/unfccc_submissions/cop30_curated/FCCC_PA_CMA_2025_L24_advance.pdf",
     "country": "Brazil", "issue": "ADAPT-FIN", "doc_id": "L24_BRA_FIN"},
    {"path": "data/raw/unfccc_submissions/cop30_curated/FCCC_PA_CMA_2025_07.pdf",
     "country": "Brazil", "issue": "L&D-OP", "doc_id": "CMA07_BRA_LD"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoTematico_Recursos_Hidricos.pdf",
     "country": "Brazil", "issue": "NAPs", "doc_id": "PlanoNAP_BRA"},
    {"path": "data/raw/unfccc_submissions/cop30_curated/Mutirao_Decision_DT_cop30_01.pdf",
     "country": "Brazil", "issue": "MIT-ADAPT", "doc_id": "Mutirao_BRA"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoClima_Sumario_Executivo_v2.pdf",
     "country": "Brazil", "issue": "JT-ADAPT", "doc_id": "PlanoClima_BRA_JT"},

    # === EU ===
    {"path": "data/raw/ndcs/EU/EU_2025-11_DK_2025_11_05_20EU_20NDC.pdf",
     "country": "EU", "issue": "GGA-IND", "doc_id": "EU_NDC_GGA"},
    {"path": "data/raw/ndcs/EU/EU_2025-11_DK_2025_11_05_20EU_20NDC.pdf",
     "country": "EU", "issue": "ADAPT-FIN", "doc_id": "EU_NDC_FIN"},
    {"path": "data/raw/ndcs/EU/EU_2025-11_DK_2025_11_05_20EU_20NDC.pdf",
     "country": "EU", "issue": "NAPs", "doc_id": "EU_NDC_NAP"},

    # === USA — Mutirao + COP30 official ===
    {"path": "data/raw/cop30_official/en_news_about_cop30_cop30_approves_belem_package1.html",
     "country": "United States", "issue": "GGA-IND", "doc_id": "BelemPackage_USA_GGA"},
    {"path": "data/raw/cop30_official/en_news_about_cop30_cop30_approves_belem_package1.html",
     "country": "United States", "issue": "ADAPT-FIN", "doc_id": "BelemPackage_USA_FIN"},

    # === China (LMDC + BASIC) ===
    {"path": "data/raw/round3/LMDC_AILAC_submission/LMDC_submission_on_GGA.pdf",
     "country": "China", "issue": "GGA-IND", "doc_id": "LMDC_CHN_GGA"},
    {"path": "data/raw/round3/LMDC_AILAC_submission/LMDC_supplementary_note_9_1_DEA.pdf",
     "country": "China", "issue": "ADAPT-FIN", "doc_id": "LMDC_CHN_FIN"},

    # === India ===
    {"path": "data/raw/round3/LMDC_AILAC_submission/LMDC_submission_on_GGA.pdf",
     "country": "India", "issue": "GGA-IND", "doc_id": "LMDC_IND_GGA"},
    {"path": "data/raw/round3/LMDC_AILAC_submission/LMDC_supplementary_note_9_1_DEA.pdf",
     "country": "India", "issue": "ADAPT-FIN", "doc_id": "LMDC_IND_FIN"},

    # === South Korea (Track A focal) ===
    {"path": "data/raw/round8/adaptation_communication/Korea_Republic_Adaptation_Communication_2023.pdf",
     "country": "South Korea", "issue": "NAPs", "doc_id": "KOR_AdComm_NAP"},
    {"path": "data/raw/round8/adaptation_communication/Korea_Republic_Adaptation_Communication_2023.pdf",
     "country": "South Korea", "issue": "GGA-IND", "doc_id": "KOR_AdComm_GGA"},
    {"path": "data/raw/round8/adaptation_communication/Korea_Republic_Adaptation_Communication_2023.pdf",
     "country": "South Korea", "issue": "ADAPT-FIN", "doc_id": "KOR_AdComm_FIN"},

    # === AOSIS ===
    {"path": "data/raw/round3/AOSIS_GGA_submission/AOSIS_adaptation_submission_2024_data_gaps.pdf",
     "country": "AOSIS", "issue": "GGA-IND", "doc_id": "AOSIS_GGA"},
    {"path": "data/raw/round3/AOSIS_GGA_submission/AOSIS_SCF_needs_survey.pdf",
     "country": "AOSIS", "issue": "ADAPT-FIN", "doc_id": "AOSIS_FIN"},
    {"path": "data/raw/round3/AOSIS_GGA_submission/AOSIS_MAHWP3_written_inputs.pdf",
     "country": "AOSIS", "issue": "L&D-OP", "doc_id": "AOSIS_LD"},
    {"path": "data/raw/round3/AOSIS_GGA_submission/AOSIS_SB60_joint_opening_2024.pdf",
     "country": "AOSIS", "issue": "NAPs", "doc_id": "AOSIS_NAP"},

    # === Saudi Arabia (Arab Group + LMDC) ===
    {"path": "data/raw/round5/group_submission/Arab_Group_NCQG_Workplan_2024.pdf",
     "country": "Saudi Arabia", "issue": "ADAPT-FIN", "doc_id": "ArabGroup_SAU_FIN"},
    {"path": "data/raw/round5/group_submission/Arab_Group_NCQG_Workplan_2024.pdf",
     "country": "Saudi Arabia", "issue": "GGA-IND", "doc_id": "ArabGroup_SAU_GGA"},

    # === South Africa (BASIC + African Group) ===
    {"path": "data/raw/round3/WorldBank_CCDR/WorldBank_Brazil_CCDR_alt.pdf",
     "country": "South Africa", "issue": "ADAPT-FIN", "doc_id": "WB_ZAF_FIN"},
    {"path": "data/raw/tier4/AGN_GGA_submission/AGN_intervention_on_GGA.pdf",
     "country": "South Africa", "issue": "GGA-IND", "doc_id": "AGN_ZAF_GGA"},

    # === African Group ===
    {"path": "data/raw/tier4/AGN_GGA_submission/AGN_intervention_on_GGA.pdf",
     "country": "African Group", "issue": "GGA-IND", "doc_id": "AGN_GGA"},
    {"path": "data/raw/tier4/AGN_GGA_submission/AGN_intervention_on_GGA.pdf",
     "country": "African Group", "issue": "ADAPT-FIN", "doc_id": "AGN_FIN"},

    # === Norway (Umbrella + HAC) ===
    {"path": "data/raw/cop30_official/en_news_about_cop30_cop30_approves_belem_package1.html",
     "country": "Norway", "issue": "GGA-IND", "doc_id": "BelemPackage_NOR_GGA"},

    # === Japan (Umbrella) ===
    {"path": "data/raw/cop30_official/en_news_about_cop30_cop30_approves_belem_package1.html",
     "country": "Japan", "issue": "ADAPT-FIN", "doc_id": "BelemPackage_JPN_FIN"},

    # === Mexico (AILAC) ===
    {"path": "data/raw/round4/AILAC_LDC_G77_submission/AILAC_GST_submission.pdf"
     if Path(ROOT / "data/raw/round4/AILAC_LDC_G77_submission/AILAC_GST_submission.pdf").exists()
     else "data/raw/round3/LMDC_AILAC_submission/LMDC_submission_on_GGA.pdf",
     "country": "Mexico", "issue": "GGA-IND", "doc_id": "AILAC_MEX_GGA"},

    # === LDC Group ===
    {"path": "data/raw/round4/AILAC_LDC_G77_submission/LDC_B2BR_2024.pdf"
     if Path(ROOT / "data/raw/round4/AILAC_LDC_G77_submission/LDC_B2BR_2024.pdf").exists()
     else "data/raw/round3/AOSIS_GGA_submission/AOSIS_adaptation_submission_2024_data_gaps.pdf",
     "country": "LDC Group", "issue": "ADAPT-FIN", "doc_id": "LDC_FIN"},

    # === LMDC ===
    {"path": "data/raw/round3/LMDC_AILAC_submission/LMDC_submission_on_GGA.pdf",
     "country": "LMDC", "issue": "GGA-IND", "doc_id": "LMDC_GGA"},
    {"path": "data/raw/round3/LMDC_AILAC_submission/LMDC_supplementary_note_9_1_DEA.pdf",
     "country": "LMDC", "issue": "ADAPT-FIN", "doc_id": "LMDC_FIN"},

    # === UAE-Belém Indicators (전체 9 thematic targets) ===
    {"path": "data/raw/unfccc_submissions/cop30_curated/UAE_Belem_9a_Water.pdf",
     "country": "Multi", "issue": "GGA-IND", "doc_id": "UAE_9a_Water"},
    {"path": "data/raw/unfccc_submissions/cop30_curated/UAE_Belem_9b_Food.pdf",
     "country": "Multi", "issue": "GGA-IND", "doc_id": "UAE_9b_Food"},
    {"path": "data/raw/unfccc_submissions/cop30_curated/UAE_Belem_9c_Health.pdf",
     "country": "Multi", "issue": "GGA-IND", "doc_id": "UAE_9c_Health"},
    {"path": "data/raw/unfccc_submissions/cop30_curated/UAE_Belem_9e_Infrastructure.pdf",
     "country": "Multi", "issue": "GGA-IND", "doc_id": "UAE_9e_Infrastructure"},

    # === Historical chair letters (procedural authority, COP21-COP29) ===
    {"path": "data/raw/historical_chair/COP26/letter_pre_cop_3_aug_21.pdf"
     if Path(ROOT / "data/raw/historical_chair/COP26/letter_pre_cop_3_aug_21.pdf").exists()
     else "data/raw/unfccc_submissions/cop30_curated/Mutirao_Decision_DT_cop30_01.pdf",
     "country": "United Kingdom", "issue": "GGA-IND", "doc_id": "COP26_UK_chair"},

    # === COP30 GGA decision text ===
    {"path": "data/raw/unfccc_submissions/cop30_curated/GGA_COP30_decision_5.pdf",
     "country": "Multi", "issue": "GGA-IND", "doc_id": "GGA_COP30_dec5"},
    {"path": "data/raw/unfccc_submissions/cop30_curated/CMA7_8a_GGA_advance_unedited.pdf",
     "country": "Multi", "issue": "GGA-IND", "doc_id": "CMA7_8a_GGA"},

    # === Synthesis docs ===
    {"path": "data/raw/unfccc_submissions/cop30_curated/Synthesis_UAE_Belem_WP_Final.pdf",
     "country": "Multi", "issue": "GGA-IND", "doc_id": "Synthesis_UAE_Belem"},

    # === Brazilian Plano Clima 16 sectoral (모두 추출 — 풍부한 evidence) ===
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoSetorial_Cidades.pdf",
     "country": "Brazil", "issue": "NAPs", "doc_id": "PlanoCidades_BRA"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoSetorial_Energia.pdf",
     "country": "Brazil", "issue": "MIT-ADAPT", "doc_id": "PlanoEnergia_BRA"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoSetorial_Riscos_Desastres.pdf",
     "country": "Brazil", "issue": "L&D-OP", "doc_id": "PlanoRiscos_BRA"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoSetorial_Seguranca_Alimentar.pdf",
     "country": "Brazil", "issue": "GGA-IND", "doc_id": "PlanoFood_BRA"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoSetorial_Transportes.pdf",
     "country": "Brazil", "issue": "MIT-ADAPT", "doc_id": "PlanoTransp_BRA"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoTematico_Biodiversidade.pdf",
     "country": "Brazil", "issue": "GGA-IND", "doc_id": "PlanoBio_BRA"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoTematico_Igualdade_Racial.pdf",
     "country": "Brazil", "issue": "JT-ADAPT", "doc_id": "PlanoIgual_BRA"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoTematico_Oceano_Costeira.pdf",
     "country": "Brazil", "issue": "GGA-IND", "doc_id": "PlanoOceano_BRA"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoTematico_Povos_Indigenas.pdf",
     "country": "Brazil", "issue": "JT-ADAPT", "doc_id": "PlanoIndig_BRA"},
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


def extract_one(provider, target: dict, issue_descs: dict) -> dict | None:
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
        text = text[:7000]
    except Exception as exc:
        logger.warning("Parse failed: %s", exc)
        return None

    if len(text) < 200:
        return None

    issue_desc = issue_descs.get(target["issue"], target["issue"])
    user = (
        f"Country: {target['country']}\n"
        f"Issue: {target['issue']} - {issue_desc}\n\n"
        f"Document excerpt:\n=== START ===\n{text}\n=== END ===\n"
        f"Source: {target['doc_id']}\n\nExtract per v1.3 schema. JSON only."
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
            "source_path": target["path"],
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "provider": provider.name,
            "model": provider.model,
            "usage": resp.usage,
        }
        return parsed
    except Exception as exc:
        logger.warning("LLM call failed for %s/%s: %s", target["country"], target["issue"], exc)
        return None


def main() -> int:
    from src.stage1_extract.providers import get_provider
    from src.config import ISSUE_DESCRIPTIONS

    backend = os.environ.get("CINA_LLM_PROVIDER", "groq")
    provider = get_provider(backend, temperature=0.3, max_tokens=2000)
    logger.info("Provider: %s / %s", provider.name, provider.model)
    logger.info("Targets: %d", len(TARGETS))

    results = []
    failed = []
    for i, t in enumerate(TARGETS, 1):
        logger.info("[%d/%d] %s × %s", i, len(TARGETS), t["country"], t["issue"])
        rec = extract_one(provider, t, ISSUE_DESCRIPTIONS)
        if rec:
            score = rec.get("stance_score", "?")
            score_str = f"{score:+.2f}" if isinstance(score, (int, float)) else "?"
            cat = rec.get("stance_category", "?")
            frame = rec.get("frame_type", "?")
            chair = rec.get("procedural_signals", {}).get("is_chair_role", False)
            print(f"  + {t['country']:<18} {t['issue']:<10} {score_str} ({cat:<22}) frame={frame:<13} chair={chair}")
            results.append(rec)
        else:
            failed.append(t)
            print(f"  X {t['country']:<18} {t['issue']:<10} FAILED")
        # Groq 30 RPM = 2s safe; 6K TPM constraint
        time.sleep(2.5)

    out = ROOT / "data" / "processed" / "stances_mass_v1.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    total_tokens = sum(r.get("_meta", {}).get("usage", {}).get("total_tokens", 0) for r in results)
    logger.info("Stage 1 mass extraction: %d/%d (%d failed)", len(results), len(TARGETS), len(failed))
    logger.info("Total tokens: %d (cost: $0)", total_tokens)
    logger.info("Output: %s", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
