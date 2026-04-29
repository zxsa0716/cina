"""Round 3 supplementary curated collector.

WebSearch로 발견한 Party submissions, World Bank CCDR, Korean MOE 적응대책,
Brazilian Plano Clima 직접 URL 모음. Round 3 priority 보강.
"""
from __future__ import annotations

import logging
from pathlib import Path
from urllib.parse import urlparse

from .base import CollectorBase

logger = logging.getLogger(__name__)

# AOSIS formal submissions on adaptation/GGA
AOSIS_SUBMISSIONS = [
    ("https://www4.unfccc.int/sites/SubmissionsStaging/Documents/202404031108---AOSIS%20adaptation_Submission%20text%20plus%20data%20gaps.pdf",
     "AOSIS_adaptation_submission_2024_data_gaps", "AOSIS"),
    ("https://unfccc.int/sites/default/files/resource/MAHWP3_Written_Inputs_AOSIS.pdf",
     "AOSIS_MAHWP3_written_inputs", "AOSIS"),
    ("https://www4.unfccc.int/sites/SubmissionsStaging/Documents/202406031611---AOSIS%20Joint%20Opening%20Statement%20SB60%20-%20FINAL%20for%20Upload%20-%203%20Jun%2024.pdf",
     "AOSIS_SB60_joint_opening_2024", "AOSIS"),
    ("https://www4.unfccc.int/sites/SubmissionsStaging/Documents/202509160100---AOSIS%20Submission%20-%20Climate%20Champions%20-%20FINAL.pdf",
     "AOSIS_Climate_Champions_2025", "AOSIS"),
    ("https://unfccc.int/sites/default/files/resource/SCF%20Submission-AOSIS%20Needs%20Survey.pdf",
     "AOSIS_SCF_needs_survey", "AOSIS"),
    ("https://unfccc.int/sites/default/files/resource/sbi2025_17.pdf",
     "FCCC_SBI_2025_17", "Multiple"),
]

# LMDC, Arab Group, AILAC submissions
LMDC_AILAC_SUBMISSIONS = [
    ("https://unfccc.int/sites/default/files/resource/LMDC%20Supplmentary%20note%20on%209.1_DEA.pdf",
     "LMDC_supplementary_note_9_1_DEA", "LMDC"),
    ("https://unfccc.int/sites/default/files/resource/LMDC_submission_on_GGA.pdf",
     "LMDC_submission_on_GGA", "LMDC"),
]

# World Bank Country Climate and Development Reports (CCDR) — Brazil + supplementary
WB_CCDR = [
    ("https://openknowledge.worldbank.org/server/api/core/bitstreams/9b6b0f83-d69d-489a-a002-f56bb5e0f1cf/content",
     "WorldBank_Brazil_CCDR_2023", "BRA"),
    ("https://documents1.worldbank.org/curated/en/099050123155521118/pdf/P17671307c2c5e0d50b50104f17e62c8aef.pdf",
     "WorldBank_Brazil_CCDR_alt", "BRA"),
]

# Korean Ministry of Environment 제3차 국가 기후위기 적응 강화대책
KOREAN_MOE_ADAPT = [
    # 메인 다운로드 페이지에서 PDF 수동 fetch — 페이지 자체를 HTML로 저장 후
    # filedown 링크를 follow
    ("https://www.me.go.kr/home/web/policy_data/read.do?seq=8156",
     "Korean_3rd_National_Adaptation_Plan_index", "KOR"),
]

# Brazilian Plano Clima (PNAC)
BRAZILIAN_PLANO_CLIMA = [
    ("https://www.gov.br/mma/pt-br/composicao/smc/plano-clima/apresentacao-plano-clima-atualizada-mai24-lgc-1.pdf",
     "Brazil_Plano_Clima_Apresentacao_May2024", "BRA"),
    ("https://www.gov.br/mma/pt-br/assuntos/biodiversidade-e-biomas/biomas-e-ecossistemas/biomas/arquivos-biomas/plano-nacional-de-adaptacao-a-mudanca-do-clima-pna-vol-i.pdf",
     "Brazil_Plano_Nacional_Adaptacao_Vol1", "BRA"),
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/sumario-executivo-plano-clima.pdf",
     "Brazil_Plano_Clima_Sumario_Executivo_2024_2035", "BRA"),
]


class CuratedRound3Collector(CollectorBase):
    source_system = "round3_curated"
    source_type = "round3_curated"
    license_str = "Mixed (UN Open / Sovereign / World Bank Open Knowledge)"
    license_attribution = "© Various (see record)"

    def collect(self) -> list[dict]:
        records = []
        all_targets = []
        all_targets += [(u, s, c, "AOSIS_GGA_submission") for u, s, c in AOSIS_SUBMISSIONS]
        all_targets += [(u, s, c, "LMDC_AILAC_submission") for u, s, c in LMDC_AILAC_SUBMISSIONS]
        all_targets += [(u, s, c, "WorldBank_CCDR") for u, s, c in WB_CCDR]
        all_targets += [(u, s, c, "Korean_MOE_adapt_plan") for u, s, c in KOREAN_MOE_ADAPT]
        all_targets += [(u, s, c, "Brazilian_Plano_Clima") for u, s, c in BRAZILIAN_PLANO_CLIMA]

        for url, slug, country, kind in all_targets:
            ext = ".pdf" if url.lower().endswith(".pdf") or "documents1.worldbank" in url else ""
            if not ext and url.lower().endswith(".pdf"):
                ext = ".pdf"
            if "openknowledge.worldbank.org" in url:
                ext = ".pdf"
            if not ext:
                ext = ".html"
            local = self.out_dir / kind / f"{slug}{ext}"
            try:
                dl = self.http.download(url, local)
            except Exception as exc:
                logger.warning("Round3 download failed for %s: %s", url, exc)
                continue

            extras = {
                "session": "COP30/SBI62",
                "doc_kind": kind,
                "country_authors_initial": [country] if country != "Multiple" else [],
            }
            if "AOSIS" in kind:
                extras["topic_tags_initial"] = ["adaptation", "GGA", "AOSIS"]
            elif "LMDC" in kind:
                extras["topic_tags_initial"] = ["adaptation", "GGA", "LMDC", "Arab Group"]
            elif "WorldBank" in kind:
                extras["topic_tags_initial"] = ["climate_development", "world_bank", "brazil"]
            elif "Korean" in kind:
                extras["topic_tags_initial"] = ["korea_adaptation_plan", "domestic_policy"]
            elif "Brazilian" in kind:
                extras["topic_tags_initial"] = ["brazil_adaptation_plan", "domestic_policy", "PNAC"]

            rec = self.write_meta(
                local_path=local,
                url=url,
                sha256=dl["sha256"],
                size_bytes=dl["size_bytes"],
                extra=extras,
            )
            records.append(rec)
        return records
