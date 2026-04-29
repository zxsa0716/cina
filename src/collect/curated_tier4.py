"""Tier-4 보조 소스 collector.

docs/11_source_catalog.md §8 명시된 Tier-4 보조 소스 정식 통합:
- ND-GAIN Country Index 2024 Technical Report (Stage 2 country features 입력)
- Climate Action Tracker country pages (HTML)
- New Climate Institute / EU Parliament Brazil briefs
- AGN GGA intervention + UNFCCC Negotiating Group chairs document
- KIEP 보고서 (가능 시)
"""
from __future__ import annotations

import logging
from pathlib import Path

from .base import CollectorBase

logger = logging.getLogger(__name__)


# ND-GAIN — 적응 취약성·준비도 (Stage 2 country features)
NDGAIN_TARGETS = [
    ("https://gain.nd.edu/assets/581554/nd_gain_countryindex_technicalreport_2024.pdf",
     "ND_GAIN_Country_Index_Technical_2024", "Global", "BASELINE"),
]

# Climate Action Tracker country pages (HTML, country profile evidence)
CAT_TARGETS = [
    ("https://climateactiontracker.org/countries/brazil/", "CAT_Brazil_profile", "BRA", "policy"),
    ("https://climateactiontracker.org/countries/eu/", "CAT_EU_profile", "EU", "policy"),
    ("https://climateactiontracker.org/countries/india/", "CAT_India_profile", "IND", "policy"),
    ("https://climateactiontracker.org/countries/china/", "CAT_China_profile", "CHN", "policy"),
    ("https://climateactiontracker.org/countries/usa/", "CAT_USA_profile", "USA", "policy"),
    ("https://climateactiontracker.org/countries/south-korea/", "CAT_Korea_profile", "KOR", "policy"),
    ("https://climateactiontracker.org/countries/japan/", "CAT_Japan_profile", "JPN", "policy"),
    ("https://climateactiontracker.org/countries/saudi-arabia/", "CAT_Saudi_profile", "SAU", "policy"),
    ("https://climateactiontracker.org/countries/south-africa/", "CAT_SouthAfrica_profile", "ZAF", "policy"),
    ("https://climateactiontracker.org/countries/mexico/", "CAT_Mexico_profile", "MEX", "policy"),
]

# Carbon Brief / European Parliament / New Climate (Tier-4 analysis)
EXPERT_BRIEFS = [
    ("https://www.europarl.europa.eu/RegData/etudes/BRIE/2022/738185/EPRS_BRI(2022)738185_EN.pdf",
     "EU_Parliament_Brazil_climate_brief_2022", "BRA", "policy"),
    ("https://newclimate.org/sites/default/files/2021/11/NewClimate_TrackingCurrentPolicies_Nov21.pdf",
     "NewClimate_Tracking_30_emitters_2021", "Multiple", "policy"),
]

# AGN African Group submissions on GGA (Round 5 IR P0 backfill)
AGN_AFRICAN_GROUP = [
    ("https://unfccc.int/sites/default/files/resource/AGN_intervention_GGA1.pdf",
     "AGN_intervention_on_GGA", "African Group", "GGA-IND"),
]

# UNFCCC Negotiating Group chairs (chair_metadata 보강)
GROUP_CHAIRS_REFERENCE = [
    ("https://unfccc.int/sites/default/files/resource/UNFCCC_Negotiating_Group_Group_Chairs_and_Coordinators.pdf",
     "UNFCCC_Negotiating_Group_Chairs_Coordinators", "Multiple", "MULTI"),
]


class CuratedTier4Collector(CollectorBase):
    source_system = "tier4_curated"
    source_type = "tier4_curated"
    license_str = "Mixed (CC BY 4.0 / EU Open / UN Open / fair use academic)"
    license_attribution = "© Various (ND-GAIN / CAT / NewClimate / EU Parliament / UNFCCC AGN)"

    def collect(self) -> list[dict]:
        records = []
        all_targets = []
        all_targets += [(u, s, c, sess, "ndgain_baseline") for u, s, c, sess in NDGAIN_TARGETS]
        all_targets += [(u, s, c, sess, "cat_country_profile") for u, s, c, sess in CAT_TARGETS]
        all_targets += [(u, s, c, sess, "expert_brief") for u, s, c, sess in EXPERT_BRIEFS]
        all_targets += [(u, s, c, sess, "AGN_GGA_submission") for u, s, c, sess in AGN_AFRICAN_GROUP]
        all_targets += [(u, s, c, sess, "group_chairs_reference") for u, s, c, sess in GROUP_CHAIRS_REFERENCE]

        for url, slug, country, sess, kind in all_targets:
            ext = ".pdf" if url.lower().endswith(".pdf") else ".html"
            local = self.out_dir / kind / f"{slug}{ext}"
            try:
                dl = self.http.download(url, local)
            except Exception as exc:
                logger.warning("Tier4 download failed for %s: %s", url, exc)
                continue
            extras = {
                "session": sess,
                "doc_kind": kind,
                "country_authors_initial": [country] if country and country != "Multiple" else [],
            }
            if kind == "ndgain_baseline":
                extras["topic_tags_initial"] = ["adaptation", "vulnerability", "ND-GAIN", "baseline"]
            elif kind == "cat_country_profile":
                extras["topic_tags_initial"] = ["climate_action_tracker", "country_policy"]
            elif kind == "expert_brief":
                extras["topic_tags_initial"] = ["expert_advice", "country_brief"]
            elif kind == "AGN_GGA_submission":
                extras["topic_tags_initial"] = ["adaptation", "GGA", "AGN", "African Group"]
            elif kind == "group_chairs_reference":
                extras["topic_tags_initial"] = ["procedural", "chair_metadata", "reference"]

            rec = self.write_meta(
                local_path=local,
                url=url,
                sha256=dl["sha256"],
                size_bytes=dl["size_bytes"],
                extra=extras,
            )
            records.append(rec)
        return records
