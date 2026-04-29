"""Tier-4b 보강 collector — Carbon Brief, ND-GAIN ZIP, KIEP, WRI/IISD blog.

CuratedTier4Collector 외 추가 Tier-4 소스로 BUILD_AUDIT v1의 75% → 95%+ 도달.
"""
from __future__ import annotations

import logging
from pathlib import Path

from .base import CollectorBase

logger = logging.getLogger(__name__)


# Carbon Brief COP30 분석 articles (HTML)
CARBON_BRIEF = [
    ("https://www.carbonbrief.org/cop30-key-outcomes-agreed-at-the-un-climate-talks-in-belem/",
     "CarbonBrief_COP30_key_outcomes", "Multiple", "COP30"),
    ("https://www.carbonbrief.org/cop30-key-outcomes-for-food-forests-land-and-nature-at-the-un-climate-talks-in-belem/",
     "CarbonBrief_COP30_food_forests", "Multiple", "COP30"),
    ("https://www.carbonbrief.org/qa-cop30-could-finally-agree-how-to-track-the-global-goal-on-adaptation/",
     "CarbonBrief_COP30_GGA_QA", "Multiple", "COP30"),
    ("https://www.carbonbrief.org/analysis-why-cop30s-tripling-adaptation-finance-target-is-less-ambitious-than-it-seems/",
     "CarbonBrief_COP30_tripling_finance_analysis", "Multiple", "COP30"),
    ("https://www.carbonbrief.org/debriefed-21-november-2025-cop30-debriefed-mutirao-text-latest-roadmaps-explained-cop-finish-times-plotted/",
     "CarbonBrief_COP30_DeBriefed_21Nov", "Multiple", "COP30"),
]

# ND-GAIN Country Index ZIP (Stage 2 country features 9-dim baseline)
NDGAIN_DATA = [
    ("https://nd-gain.org/assets/647440/ndgain_countryindex_2026.zip",
     "ND_GAIN_country_index_2026_full_dataset", "Global", "BASELINE"),
]

# WRI / IISD analysis (high-quality COP30 outcome briefs)
WRI_IISD_BLOGS = [
    ("https://blog.iese.edu/finance-and-nature/2025/cop30-in-belem-key-outcomes-and-what-they-enable-next/",
     "IESE_finance_nature_COP30", "Multiple", "COP30"),
    ("https://www.globalccsinstitute.com/wp-content/uploads/2025/12/COP30-Outcomes-1225.pdf",
     "Global_CCS_Institute_COP30_Dec2025", "Multiple", "COP30"),
]

# Mo Ibrahim Foundation Africa COPs (이미 round5에 있으나 추가 분석 보고)
AFRICA_FOCUSED = [
    ("https://www.tandfonline.com/doi/pdf/10.1080/10220461.2024.2357327",
     "AGN_understanding_paper_2024", "African Group", "MULTI"),
]


class CuratedTier4bCollector(CollectorBase):
    source_system = "tier4b_curated"
    source_type = "tier4b_curated"
    license_str = "Mixed (Carbon Brief CC BY-NC-ND / ND-GAIN CC BY 4.0 / Springer fair use)"
    license_attribution = "© Various (Carbon Brief / ND-GAIN / IESE / Global CCS Institute / Taylor & Francis)"

    def collect(self) -> list[dict]:
        records = []
        all_targets = []
        all_targets += [(u, s, c, sess, "carbon_brief_analysis") for u, s, c, sess in CARBON_BRIEF]
        all_targets += [(u, s, c, sess, "ndgain_full_data") for u, s, c, sess in NDGAIN_DATA]
        all_targets += [(u, s, c, sess, "wri_iisd_brief") for u, s, c, sess in WRI_IISD_BLOGS]
        all_targets += [(u, s, c, sess, "africa_focused_analysis") for u, s, c, sess in AFRICA_FOCUSED]

        for url, slug, country, sess, kind in all_targets:
            if url.lower().endswith(".zip"):
                ext = ".zip"
            elif url.lower().endswith(".pdf"):
                ext = ".pdf"
            else:
                ext = ".html"
            local = self.out_dir / kind / f"{slug}{ext}"
            try:
                dl = self.http.download(url, local)
            except Exception as exc:
                logger.warning("Tier4b download failed for %s: %s", url, exc)
                continue
            extras = {
                "session": sess,
                "doc_kind": kind,
                "country_authors_initial": [country] if country and country != "Multiple" else [],
            }
            if kind == "carbon_brief_analysis":
                extras["topic_tags_initial"] = ["adaptation", "GGA", "carbon_brief", "expert_journalism"]
            elif kind == "ndgain_full_data":
                extras["topic_tags_initial"] = ["adaptation", "vulnerability", "ND-GAIN", "baseline_data"]
                extras["doc_kind"] = "data_zip"
            elif kind == "wri_iisd_brief":
                extras["topic_tags_initial"] = ["expert_advice", "COP30_outcome"]
            elif kind == "africa_focused_analysis":
                extras["topic_tags_initial"] = ["AGN", "African Group", "academic_analysis"]
            rec = self.write_meta(
                local_path=local,
                url=url,
                sha256=dl["sha256"],
                size_bytes=dl["size_bytes"],
                extra=extras,
            )
            records.append(rec)
        return records
