"""Round 7 broad data collection — autonomous fallback paths.

Castro 차단 + ND-GAIN ZIP 차단 후 자율 우회 경로:
1. IMF Climate Data Explorer (ArcGIS Hub) — ND-GAIN 직접 CSV/JSON
2. WRI Climate Watch NDC data — open download
3. OECD Measuring Progress 2024 — direct PDF
4. World Bank CCKP — open data on AWS
5. GitHub openclimatedata/ndc-assessments — open repo
6. Carbon Brief 추가 + Reuters/AP COP30 분석
7. Brazilian/Korean 정부 추가 (KMA, 환경부 자료실 deep)
8. ENB historical bulletins archive.org 우회 (Castro 재현 토대)
"""
from __future__ import annotations

import logging
from pathlib import Path

from .base import CollectorBase

logger = logging.getLogger(__name__)


# IMF Climate Data Explorer — ND-GAIN dataset (ArcGIS Hub feature service)
# UID: e6604c14a46f44cbbb4ee1a5e9996c49 (NDGAIN), 다른 dataset도 동일 패턴
IMF_CLIMATE_DATA = [
    # IMF-Adapted ND-GAIN (CSV via ArcGIS Hub query)
    ("https://climatedata.imf.org/api/download/v1/items/e6604c14a46f44cbbb4ee1a5e9996c49/csv?layers=0",
     "IMF_ND_GAIN_country_index_csv", "Global", "BASELINE"),
    # IMF Climate Change Indicators 메인 페이지
    ("https://climatedata.imf.org/datasets",
     "IMF_climate_data_index_html", "Global", "BASELINE"),
]

# OECD Measuring Progress in Adapting (Tier-3 expert analysis)
OECD_ADAPTATION = [
    ("https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/06/measuring-progress-in-adapting-to-a-changing-climate_71e9c519/8cfe45af-en.pdf",
     "OECD_Measuring_Progress_Adapting_2024", "Multiple", "BASELINE"),
]

# World Bank CCKP — Brazil/India/China specific
WB_CCKP_COUNTRY = [
    ("https://climateknowledgeportal.worldbank.org/sites/default/files/2021-09/15494-WB_Brazil%20Country%20Profile-WEB%20%282%29.pdf",
     "WB_CCKP_Brazil_climate_profile", "BRA", "BASELINE"),
    ("https://climateknowledgeportal.worldbank.org/sites/default/files/2021-04/15462-WB_India%20Country%20Profile-WEB.pdf",
     "WB_CCKP_India_climate_profile", "IND", "BASELINE"),
    ("https://climateknowledgeportal.worldbank.org/sites/default/files/2021-04/15463-WB_Indonesia%20Country%20Profile-WEB.pdf",
     "WB_CCKP_Indonesia_climate_profile", "IDN", "BASELINE"),
]

# WRI Climate Watch — NDC explorer + tracking
WRI_CLIMATE_WATCH = [
    ("https://www.climatewatchdata.org/api/v1/data/historical_emissions?regions=BRA,IND,CHN,USA,EUU,KOR&source_ids=2",
     "WRI_climate_watch_historical_emissions_API", "Multiple", "BASELINE"),
    ("https://github.com/WRI-ClimateWatch/ndc/archive/refs/heads/master.zip",
     "WRI_ClimateWatch_NDC_repo_master", "Multiple", "MULTI"),
]

# GitHub openclimatedata — NDC assessments (raw data)
OPENCLIMATEDATA = [
    ("https://github.com/openclimatedata/ndc-assessments/archive/refs/heads/main.zip",
     "openclimatedata_ndc_assessments_main", "Multiple", "MULTI"),
]

# Castro 재현 — github.com/victorkristof/phd-thesis (PhD repo with ENB code)
CASTRO_REPRODUCTION = [
    ("https://github.com/victorkristof/phd-thesis/archive/refs/heads/main.zip",
     "victorkristof_phd_thesis_main", "Global", "BASELINE"),
]

# ENB historical (COP21-COP30 final summaries — Castro 재현용 input)
ENB_HISTORICAL = [
    # ENB Vol 12 — known final summary patterns. Source: enb.iisd.org/sites/default/files/{YYYY-MM}/enb12{NNN}e.pdf
    # COP21 final ~ enb12663e
    ("https://enb.iisd.org/sites/default/files/2015-12/enb12663e.pdf", "enb12663e_COP21_Paris_final", "Multiple", "COP21"),
    # COP22 final ~ enb12702e
    ("https://enb.iisd.org/sites/default/files/2016-11/enb12702e.pdf", "enb12702e_COP22_Marrakech_final", "Multiple", "COP22"),
    # COP23 final ~ enb12714e
    ("https://enb.iisd.org/sites/default/files/2017-11/enb12714e.pdf", "enb12714e_COP23_Bonn_final", "Multiple", "COP23"),
    # COP24 final ~ enb12747e
    ("https://enb.iisd.org/sites/default/files/2018-12/enb12747e.pdf", "enb12747e_COP24_Katowice_final", "Multiple", "COP24"),
    # COP25 final ~ enb12775e
    ("https://enb.iisd.org/sites/default/files/2019-12/enb12775e.pdf", "enb12775e_COP25_Madrid_final", "Multiple", "COP25"),
    # COP26 final ~ enb12793e
    ("https://enb.iisd.org/sites/default/files/2021-11/enb12793e.pdf", "enb12793e_COP26_Glasgow_final", "Multiple", "COP26"),
    # COP27 final ~ enb12823e
    ("https://enb.iisd.org/sites/default/files/2022-11/enb12823e.pdf", "enb12823e_COP27_Sharm_final", "Multiple", "COP27"),
    # COP28 final ~ enb12846e
    ("https://enb.iisd.org/sites/default/files/2023-12/enb12846e.pdf", "enb12846e_COP28_Dubai_final", "Multiple", "COP28"),
    # COP29 final ~ enb12871e
    ("https://enb.iisd.org/sites/default/files/2024-11/enb12871e.pdf", "enb12871e_COP29_Baku_final", "Multiple", "COP29"),
    # COP30 final = enb12888e (이미 수집)
]

# Korean 추가 — KMA 기상청 + KEEI + 환경부 자료실
KOREAN_EXTENDED = [
    ("https://www.kma.go.kr/file/2024_climate_white_paper.pdf",
     "KMA_2024_climate_white_paper", "KOR", "MULTI"),
    ("https://www.me.go.kr/synap/synapView.do?atchFileId=FILE_000000000040527&fileSeq=1",
     "KOR_MOE_adaptation_PDF_attempt1", "KOR", "KOR_NAP"),
]

# Brazilian 추가 — Plano Nacional 1차 (2008) historical
BRAZILIAN_EXTENDED = [
    ("https://antigo.mma.gov.br/estruturas/smcq_climaticas/_arquivos/plano_nacional_mudanca_clima.pdf",
     "BRA_Plano_Nacional_Mudanca_Clima_2008_v1", "BRA", "HISTORICAL"),
]


class CuratedRound7Collector(CollectorBase):
    source_system = "round7_curated"
    source_type = "round7_curated"
    license_str = "Mixed (CC BY 4.0 / IMF / WRI / OECD / WB Open / fair use)"
    license_attribution = "© Various (IMF / WRI / OECD / World Bank / GitHub repos / IISD ENB)"

    def collect(self) -> list[dict]:
        records = []
        all_targets = []
        all_targets += [(u, s, c, sess, "imf_climate_data") for u, s, c, sess in IMF_CLIMATE_DATA]
        all_targets += [(u, s, c, sess, "oecd_adaptation_pub") for u, s, c, sess in OECD_ADAPTATION]
        all_targets += [(u, s, c, sess, "wb_cckp_country") for u, s, c, sess in WB_CCKP_COUNTRY]
        all_targets += [(u, s, c, sess, "wri_climate_watch") for u, s, c, sess in WRI_CLIMATE_WATCH]
        all_targets += [(u, s, c, sess, "openclimatedata_ndc") for u, s, c, sess in OPENCLIMATEDATA]
        all_targets += [(u, s, c, sess, "castro_reproduction_repo") for u, s, c, sess in CASTRO_REPRODUCTION]
        all_targets += [(u, s, c, sess, "enb_historical_summary") for u, s, c, sess in ENB_HISTORICAL]
        all_targets += [(u, s, c, sess, "korean_extended") for u, s, c, sess in KOREAN_EXTENDED]
        all_targets += [(u, s, c, sess, "brazilian_historical") for u, s, c, sess in BRAZILIAN_EXTENDED]

        for url, slug, country, sess, kind in all_targets:
            if url.lower().endswith(".csv"):
                ext = ".csv"
            elif url.lower().endswith(".zip"):
                ext = ".zip"
            elif url.lower().endswith(".pdf"):
                ext = ".pdf"
            elif "api" in url.lower() and "data.imf" in url.lower():
                ext = ".csv"
            elif "?" in url and not url.lower().endswith(".pdf"):
                ext = ".json"
            else:
                ext = ".html"
            local = self.out_dir / kind / f"{slug}{ext}"
            try:
                dl = self.http.download(url, local)
            except Exception as exc:
                logger.warning("Round7 download failed for %s: %s", url, exc)
                continue
            extras = {
                "session": sess,
                "doc_kind": kind,
                "country_authors_initial": [country] if country and country != "Multiple" else [],
                "round_target": "round7_autonomous_fallback",
            }
            tag_map = {
                "imf_climate_data": ["adaptation", "vulnerability", "ND-GAIN", "IMF", "baseline"],
                "oecd_adaptation_pub": ["expert_advice", "OECD", "adaptation_measurement"],
                "wb_cckp_country": ["world_bank", "country_profile", "baseline"],
                "wri_climate_watch": ["wri", "climate_watch", "ndc_data"],
                "openclimatedata_ndc": ["openclimatedata", "ndc_assessments"],
                "castro_reproduction_repo": ["castro_2025", "reproduction", "github"],
                "enb_historical_summary": ["enb_summary", "historical", "castro_input"],
                "korean_extended": ["korea_policy", "domestic_extended"],
                "brazilian_historical": ["brazil_historical", "PNAC"],
            }
            extras["topic_tags_initial"] = tag_map.get(kind, [])
            rec = self.write_meta(
                local_path=local,
                url=url,
                sha256=dl["sha256"],
                size_bytes=dl["size_bytes"],
                extra=extras,
            )
            records.append(rec)
        return records
