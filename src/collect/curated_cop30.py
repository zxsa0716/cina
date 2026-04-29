"""Curated COP30 official documents collector.

이 collector는 WebSearch로 발견한 정확한 UNFCCC URL들을 직접 fetch한다.
동적 portal scraping보다 안정적이고, 결정적 협상문(Belém Package, GGA decisions,
UAE-Belém Indicators thematic targets)을 보장한다.
"""
from __future__ import annotations

import logging
from pathlib import Path
from urllib.parse import urlparse

from .base import CollectorBase

logger = logging.getLogger(__name__)


# COP30 Belém Package 핵심 결정문
COP30_BELEM_PACKAGE = [
    # Cover-style decisions and Mutirão
    ("https://unfccc.int/sites/default/files/resource/DT_-cop30-01.pdf",
     "Mutirao_Decision_DT_cop30_01"),

    # CMA.7 Paris Agreement decisions
    ("https://unfccc.int/sites/default/files/resource/cma2025_L24_adv.pdf",
     "FCCC_PA_CMA_2025_L24_advance"),
    ("https://unfccc.int/sites/default/files/resource/cma2025_L25_adv.pdf",
     "FCCC_PA_CMA_2025_L25_advance"),
    ("https://unfccc.int/sites/default/files/resource/cma2025_L25E.pdf",
     "FCCC_PA_CMA_2025_L25E_final"),
    ("https://unfccc.int/sites/default/files/resource/cma2025_07.pdf",
     "FCCC_PA_CMA_2025_07"),
    ("https://unfccc.int/sites/default/files/resource/cma2025_08.pdf",
     "FCCC_PA_CMA_2025_08"),

    # Global Goal on Adaptation core decisions
    ("https://unfccc.int/sites/default/files/resource/gga_cop30_5.pdf",
     "GGA_COP30_decision_5"),
    ("https://unfccc.int/sites/default/files/resource/cma7_8a_gga_auv.pdf",
     "CMA7_8a_GGA_advance_unedited"),

    # COP30 INF document
    ("https://unfccc.int/sites/default/files/resource/cp2025_inf02_adv.pdf",
     "FCCC_CP_2025_INF02_advance"),

    # SBSTA follow-up
    ("https://unfccc.int/sites/default/files/resource/sbsta2026_04_adv.pdf",
     "FCCC_SBSTA_2026_04_advance"),
]

# UAE-Belém Adaptation Indicators thematic targets (target 9 hierarchy)
# 9(a)-(i): water, food, health, ecosystems, infrastructure, livelihoods,
#           cultural heritage, natural ecosystems, freshwater
UAE_BELEM_INDICATORS = [
    ("https://unfccc.int/sites/default/files/resource/9a_Water_supply_and_sanitation.pdf",
     "UAE_Belem_9a_Water"),
    ("https://unfccc.int/sites/default/files/resource/9(b)_Food_and_agricultural_production.pdf",
     "UAE_Belem_9b_Food"),
    ("https://unfccc.int/sites/default/files/resource/9(c)_Health_impacts_and_health_services.pdf",
     "UAE_Belem_9c_Health"),
    ("https://unfccc.int/sites/default/files/resource/9(e)_Infrastructure_and_human_settlements.pdf",
     "UAE_Belem_9e_Infrastructure"),
]
# 9(d), 9(f), 9(g), 9(h), 9(i) — try brute force patterns
UAE_BELEM_BRUTE_PATTERNS = [
    "https://unfccc.int/sites/default/files/resource/9(d)_Ecosystems_and_biodiversity.pdf",
    "https://unfccc.int/sites/default/files/resource/9d_Ecosystems_and_biodiversity.pdf",
    "https://unfccc.int/sites/default/files/resource/9(f)_Poverty_and_livelihoods.pdf",
    "https://unfccc.int/sites/default/files/resource/9f_Livelihoods.pdf",
    "https://unfccc.int/sites/default/files/resource/9(g)_Cultural_heritage.pdf",
    "https://unfccc.int/sites/default/files/resource/9(h)_Disaster_risk_reduction.pdf",
    "https://unfccc.int/sites/default/files/resource/9(i)_Climate_information.pdf",
]

# Synthesis & Submission documents
SYNTHESIS_DOCS = [
    ("https://unfccc.int/sites/default/files/resource/Synthesis%20of%20Submissions%20UAE-Belem%20Work%20programme%20Final.pdf",
     "Synthesis_UAE_Belem_WP_Final"),
    ("https://unfccc.int/sites/default/files/resource/Synthesis%20of%20Submissions%20edited%20PDF.pdf",
     "Synthesis_Submissions_edited"),
    ("https://unfccc.int/sites/default/files/resource/COP-29-Outcomes-on-GGA-Presentation.pdf",
     "COP29_GGA_Outcomes_Presentation"),
]

# OECD / C2ES analysis (Tier-3 context)
EXPERT_ANALYSIS = [
    ("https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/06/considerations-for-taking-forward-the-uae-belem-work-programme-on-adaptation-indicators_710823ca/e60310fc-en.pdf",
     "OECD_2025_UAE_Belem_considerations"),
    ("https://www.c2es.org/wp-content/uploads/2025/05/20250502-C2ES-GGA-indicators-principles-v5.2.pdf",
     "C2ES_2025_GGA_indicators_principles"),
]


class CuratedCop30Collector(CollectorBase):
    """Direct-URL collector for the Belém Package, GGA decisions, and indicators."""

    source_system = "unfccc.int"
    source_type = "cop30_curated"
    license_str = "UN Open License / Mixed (OECD: see docs)"
    license_attribution = "© UNFCCC / © OECD / © C2ES"

    def collect(
        self,
        include_indicators: bool = True,
        include_brute_force: bool = True,
        include_synthesis: bool = True,
        include_expert_analysis: bool = True,
    ) -> list[dict]:
        records: list[dict] = []

        targets = list(COP30_BELEM_PACKAGE)
        if include_indicators:
            targets += UAE_BELEM_INDICATORS
            if include_brute_force:
                # Brute force: try, allow failure silently
                for url in UAE_BELEM_BRUTE_PATTERNS:
                    targets.append((url, Path(urlparse(url).path).stem))
        if include_synthesis:
            targets += SYNTHESIS_DOCS
        if include_expert_analysis:
            targets += EXPERT_ANALYSIS

        for url, slug in targets:
            local = self.out_dir / f"{slug}.pdf"
            try:
                dl = self.http.download(url, local)
            except Exception as exc:
                logger.warning("Curated download failed for %s: %s", url, exc)
                continue
            extras = {
                "session": "COP30",
                "topic_tags_initial": ["adaptation", "GGA"],
                "doc_kind": "decision_or_indicator",
            }
            if "OECD" in slug or "C2ES" in slug:
                extras["doc_kind"] = "expert_analysis"
                extras["topic_tags_initial"].append("expert_advice")
            if "Synthesis" in slug:
                extras["doc_kind"] = "synthesis"
            if slug.startswith("UAE_Belem_9"):
                extras["doc_kind"] = "indicator_target"
                extras["uae_belem_target"] = slug.split("_")[2]  # e.g., '9a'
            rec = self.write_meta(
                local_path=local,
                url=url,
                sha256=dl["sha256"],
                size_bytes=dl["size_bytes"],
                extra=extras,
            )
            records.append(rec)
        return records
