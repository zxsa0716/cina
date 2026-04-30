"""Stage 1 Ollama qwen2.5:3b 확장 — Local LLM, zero cost, 무제한.

Heedo가 Ollama Gemma 4 (9.9GB)로 시도했으나 RAM 부족.
대신 qwen2.5:3b (1.8GB)로 실행 — 6GB RAM에서 안정 작동.

Multi-LLM ensemble 정상화:
- Gemini scanner (cloud, 1000 RPD)
- Groq primary (cloud, 30 RPM, $0)
- Ollama qwen2.5:3b validator (local, unlimited, $0)
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
logger = logging.getLogger("cina.stage1.ollama")

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))


# Stage 1 빈 cells 채우기 — Gemini quota 한도 미적용 추출
NEW_TARGETS = [
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoSetorial_Cidades.pdf",
     "country": "Brazil", "issue": "NAPs", "doc_id": "Plano_Cidades"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoSetorial_Energia.pdf",
     "country": "Brazil", "issue": "MIT-ADAPT", "doc_id": "Plano_Energia"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoSetorial_Transportes.pdf",
     "country": "Brazil", "issue": "MIT-ADAPT", "doc_id": "Plano_Transportes"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoTematico_Biodiversidade.pdf",
     "country": "Brazil", "issue": "GGA-IND", "doc_id": "Plano_Biodiversidade"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoTematico_Povos_Indigenas.pdf",
     "country": "Brazil", "issue": "JT-ADAPT", "doc_id": "Plano_Povos_Indigenas"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoTematico_Igualdade_Racial.pdf",
     "country": "Brazil", "issue": "JT-ADAPT", "doc_id": "Plano_Igualdade"},
    {"path": "data/raw/round8/plano_clima_17/Brazil_PlanoTematico_Oceano_Costeira.pdf",
     "country": "Brazil", "issue": "GGA-IND", "doc_id": "Plano_Oceano"},
    {"path": "data/raw/round3/AOSIS_GGA_submission/AOSIS_SCF_needs_survey.pdf",
     "country": "AOSIS", "issue": "ADAPT-FIN", "doc_id": "AOSIS_SCF"},
    {"path": "data/raw/round3/AOSIS_GGA_submission/AOSIS_MAHWP3_written_inputs.pdf",
     "country": "AOSIS", "issue": "L&D-OP", "doc_id": "AOSIS_MAHWP3"},
    {"path": "data/raw/round3/AOSIS_GGA_submission/AOSIS_SB60_joint_opening_2024.pdf",
     "country": "AOSIS", "issue": "NAPs", "doc_id": "AOSIS_SB60"},
    {"path": "data/raw/tier4/AGN_GGA_submission/AGN_intervention_on_GGA.pdf",
     "country": "African Group", "issue": "GGA-IND", "doc_id": "AGN_GGA"},
    {"path": "data/raw/round3/LMDC_AILAC_submission/LMDC_supplementary_note_9_1_DEA.pdf",
     "country": "LMDC", "issue": "ADAPT-FIN", "doc_id": "LMDC_DEA"},
    {"path": "data/raw/round8/adaptation_communication/Korea_Republic_Adaptation_Communication_2023.pdf",
     "country": "South Korea", "issue": "ADAPT-FIN", "doc_id": "KOR_AdComm_FIN"},
    {"path": "data/raw/ndcs/EU/EU_2025-11_DK_2025_11_05_20EU_20NDC.pdf",
     "country": "EU", "issue": "GGA-IND", "doc_id": "EU_NDC_GGA"},
    {"path": "data/raw/ndcs/EU/EU_2025-11_DK_2025_11_05_20EU_20NDC.pdf",
     "country": "EU", "issue": "MIT-ADAPT", "doc_id": "EU_NDC_MIT"},
    {"path": "data/raw/round5/group_submission/Arab_Group_NCQG_Workplan_2024.pdf",
     "country": "Saudi Arabia", "issue": "ADAPT-FIN", "doc_id": "ArabGroup_FIN"},
    {"path": "data/raw/round5/group_submission/Arab_Group_NCQG_Workplan_2024.pdf",
     "country": "Saudi Arabia", "issue": "GGA-IND", "doc_id": "ArabGroup_GGA"},
    {"path": "data/raw/unfccc_submissions/cop30_curated/UAE_Belem_9e_Infrastructure.pdf",
     "country": "Multi", "issue": "GGA-IND", "doc_id": "UAE_9e_Infra"},
    {"path": "data/raw/round5/historical_GGA/CMA6_GGA_AUV_COP29.pdf",
     "country": "Multi", "issue": "GGA-IND", "doc_id": "CMA6_GGA_COP29"},
    {"path": "data/raw/round5/historical_GGA/CMA5_GGA_AUV_GlasgowSharm.pdf",
     "country": "Multi", "issue": "GGA-IND", "doc_id": "CMA5_GGA_Glasgow"},
]

SYSTEM_PROMPT = """You are a climate diplomacy analyst. Extract structured stance from UNFCCC documents in JSON.

Output JSON ONLY:
{
  "stance_score": float in [-1, 1],
  "stance_category": "strong_support|support|conditional_support|neutral_or_silent|oppose|strong_oppose",
  "key_demands": [string],
  "red_lines": [string],
  "frame_type": "scientific|justice|sovereignty|security|development|mixed",
  "is_chair_role": bool,
  "is_pen_holder": bool,
  "confidence": float in [0,1]
}

Cite ONLY direct quotes. JSON only."""


def extract_via_ollama(text: str, country: str, issue: str, doc_id: str) -> dict | None:
    import ollama
    client = ollama.Client(host="http://localhost:11434")

    user = f"Country: {country}\nIssue: {issue}\nDocument:\n{text[:4000]}\nSource: {doc_id}\n\nExtract per JSON schema."

    try:
        resp = client.chat(
            model="qwen2.5:3b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user},
            ],
            format="json",
            options={"temperature": 0.3, "num_predict": 800},
        )
        content = resp.get("message", {}).get("content", "")
        if not content:
            return None
        parsed = json.loads(content)
        parsed["_meta"] = {
            "doc_id": doc_id,
            "country": country,
            "issue": issue,
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "provider": "ollama",
            "model": "qwen2.5:3b",
            "usage": {
                "prompt_tokens": resp.get("prompt_eval_count", 0),
                "eval_tokens": resp.get("eval_count", 0),
            },
        }
        return parsed
    except Exception as exc:
        logger.warning("Ollama extract failed: %s", exc)
        return None


def main() -> int:
    results = []
    for i, target in enumerate(NEW_TARGETS, 1):
        path = ROOT / target["path"]
        if not path.exists():
            logger.warning("Skip (not found): %s", path)
            continue

        try:
            doc = fitz.open(str(path))
            text = ""
            for page in doc[:5]:
                text += page.get_text() + "\n"
            doc.close()
        except Exception as exc:
            logger.warning("PDF parse failed: %s", exc)
            continue

        if len(text) < 200:
            continue

        logger.info("[%d/%d] %s × %s", i, len(NEW_TARGETS), target["country"], target["issue"])
        rec = extract_via_ollama(text, target["country"], target["issue"], target["doc_id"])
        if rec:
            score = rec.get("stance_score", "?")
            score_str = f"{score:+.2f}" if isinstance(score, (int, float)) else "?"
            cat = rec.get("stance_category", "?")
            frame = rec.get("frame_type", "?")
            chair = rec.get("is_chair_role", False)
            pen = rec.get("is_pen_holder", False)
            print(f"  + {target['country']:<14} {target['issue']:<10} {score_str} ({cat:<22}) frame={frame:<13} chair={chair} pen={pen}")
            results.append(rec)
        else:
            print(f"  X {target['country']:<14} {target['issue']:<10} FAILED")

    out = ROOT / "data" / "processed" / "stances_ollama_v1.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    total_eval = sum(r.get("_meta", {}).get("usage", {}).get("eval_tokens", 0) for r in results)
    logger.info("Ollama Stage 1 expansion: %d/%d", len(results), len(NEW_TARGETS))
    logger.info("Output: %s | Total eval tokens: %d ($0)", out, total_eval)
    return 0


if __name__ == "__main__":
    sys.exit(main())
