"""Round 5 supplementary curated collector.

Round 3 refinement 후속 + 두 교수 추가 권고 + Round 4 collector_feedback 직접 대응.

대상:
- FCCC/SBI/2025 + FCCC/SBSTA/2025 추가 conclusions / INF / L-document
- Arab Group NCQG submission
- Cultural Heritage GGA submission (ICOMOS)
- CMA.6 GGA AUV (COP29 outcome)
- CMA.5 Glasgow-Sharm el-Sheikh GGA work programme (역사 추적)
- LSE consultation, CGIAR GGA negotiation updates (expert analysis)
- Mo Ibrahim Foundation Africa COP outcomes
- ARG 1.5 Technical paper UAE Framework
- OWID CO2 emissions CSV (realist baseline)
"""
from __future__ import annotations

import logging
from pathlib import Path

from .base import CollectorBase

logger = logging.getLogger(__name__)


# SBI/SBSTA 2025 documents (procedural authority, draft conclusions)
SBI_SBSTA_2025 = [
    ("https://unfccc.int/sites/default/files/resource/sbi2025_06E.pdf",
     "FCCC_SBI_2025_06E", "Multiple", "SBI62"),
    ("https://unfccc.int/sites/default/files/resource/sbi2025_inf02.pdf",
     "FCCC_SBI_2025_INF02", "Multiple", "SBI62"),
    ("https://unfccc.int/sites/default/files/resource/sbi2025_inf06.pdf",
     "FCCC_SBI_2025_INF06", "Multiple", "SBI62"),
    ("https://unfccc.int/sites/default/files/resource/sbi2025_08a01.pdf",
     "FCCC_SBI_2025_08_Add1", "Multiple", "SBI62"),
    ("https://unfccc.int/sites/default/files/resource/sbsta2025_04_adv.pdf",
     "FCCC_SBSTA_2025_04_advance", "Multiple", "SBSTA62"),
    ("https://unfccc.int/sites/default/files/resource/sbsta2025_04E.pdf",
     "FCCC_SBSTA_2025_04E", "Multiple", "SBSTA62"),
    ("https://unfccc.int/sites/default/files/resource/sbsta2025_inf01.pdf",
     "FCCC_SBSTA_2025_INF01", "Multiple", "SBSTA62"),
    ("https://unfccc.int/sites/default/files/resource/sbsta2025_L05_adv_3.pdf",
     "FCCC_SBSTA_2025_L05_advance", "Multiple", "SBSTA62"),
    ("https://unfccc.int/sites/default/files/resource/sbsta2025_L08_adv_.pdf",
     "FCCC_SBSTA_2025_L08_advance", "Multiple", "SBSTA62"),
]

# Group submissions previously missing
GROUP_SUBMISSIONS = [
    # Arab Group NCQG Workplan 2024
    ("https://www4.unfccc.int/sites/SubmissionsStaging/Documents/202402150845---20240702_Arab_Group_NCQG_Workplan_2024_Final.pdf",
     "Arab_Group_NCQG_Workplan_2024", "Arab Group", "NCQG"),
    # ICOMOS Cultural Heritage GGA submission
    ("https://www4.unfccc.int/sites/SubmissionsStaging/Documents/202407301054---Culture%20Heritage%20Submission%20GGA%2030%20July%202024.pdf",
     "ICOMOS_Cultural_Heritage_GGA_2024", "ICOMOS", "GGA-WP"),
]

# Historical GGA decisions (전임 의장국 비교)
HISTORICAL_GGA = [
    # CMA.6 GGA (COP29 Baku outcome)
    ("https://unfccc.int/sites/default/files/resource/CMA6_agenda_item_9a_GGA_AUV.pdf",
     "CMA6_GGA_AUV_COP29", "Multiple", "COP29"),
    # CMA.5 Glasgow-Sharm el-Sheikh GGA work programme
    ("https://unfccc.int/sites/default/files/resource/cma5_auv_8a_gga.pdf",
     "CMA5_GGA_AUV_GlasgowSharm", "Multiple", "COP28"),
]

# Expert analysis (Tier-3)
EXPERT_GGA_ANALYSIS = [
    # LSE consultation submission on GGA modalities
    ("https://www.lse.ac.uk/granthaminstitute/wp-content/uploads/2024/04/Modalities-for-the-Indicator-Work-Programme-under-the-Global-Goal-on-Adaptation_LSE-consultation-submission.pdf",
     "LSE_GGA_Modalities_consultation_2024", "LSE", "MULTI"),
    # CGIAR COP30 GGA Track Negotiation Updates
    ("https://cgspace.cgiar.org/server/api/core/bitstreams/a1bb1738-9d6b-45b9-aefa-04a8e1909c82/content",
     "CGIAR_COP30_GGA_Track_Negotiation_Updates", "CGIAR", "COP30"),
    # ARG 1.5 Technical paper UAE Framework
    ("https://arg1punto5.com/wp-content/uploads/2024/04/Technical-paper-ARG-1.5-UAE-Framework-for-Global-Climate-Resilience.pdf",
     "ARG_1_5_Technical_UAE_Framework", "ARG_1.5", "MULTI"),
    # Mo Ibrahim Foundation latest COPs on Africa
    ("https://mo.ibrahim.foundation/sites/default/files/2025-03/latest-cops-on-climate-change.pdf",
     "Mo_Ibrahim_Latest_COPs_Africa", "Mo_Ibrahim", "COP28-30"),
]

# Realist baseline data (CR3.5 직접 대응) — Our World in Data CO2
REALIST_BASELINE = [
    ("https://github.com/owid/co2-data/raw/master/owid-co2-data.csv",
     "OWID_CO2_data_master", "Global", "BASELINE"),
    ("https://nyc3.digitaloceanspaces.com/owid-public/data/co2/owid-co2-data.csv",
     "OWID_CO2_data_mirror", "Global", "BASELINE"),
]


class CuratedRound5Collector(CollectorBase):
    source_system = "round5_curated"
    source_type = "round5_curated"
    license_str = "Mixed (UN Open / observer / OWID CC BY 4.0)"
    license_attribution = "© Various (UNFCCC / Arab Group / ICOMOS / LSE / CGIAR / OWID)"

    def collect(self) -> list[dict]:
        records: list[dict] = []
        all_targets = []
        all_targets += [(u, s, c, sess, "SBI_SBSTA_2025") for u, s, c, sess in SBI_SBSTA_2025]
        all_targets += [(u, s, c, sess, "group_submission") for u, s, c, sess in GROUP_SUBMISSIONS]
        all_targets += [(u, s, c, sess, "historical_GGA") for u, s, c, sess in HISTORICAL_GGA]
        all_targets += [(u, s, c, sess, "expert_GGA_analysis") for u, s, c, sess in EXPERT_GGA_ANALYSIS]
        all_targets += [(u, s, c, sess, "realist_baseline") for u, s, c, sess in REALIST_BASELINE]

        for url, slug, country, sess, kind in all_targets:
            if "csv" in url.lower():
                ext = ".csv"
            elif url.lower().endswith(".pdf"):
                ext = ".pdf"
            else:
                ext = ".pdf"
            local = self.out_dir / kind / f"{slug}{ext}"
            try:
                dl = self.http.download(url, local)
            except Exception as exc:
                logger.warning("Round5 download failed for %s: %s", url, exc)
                continue

            extras = {
                "session": sess,
                "doc_kind": kind,
                "country_authors_initial": [country] if country and country != "Multiple" else [],
                "round_target": "round5_remediation",
            }
            if kind == "SBI_SBSTA_2025":
                extras["topic_tags_initial"] = ["adaptation", "draft_conclusions", "procedural"]
                extras["procedural_hint"] = "is_pen_holder=likely (chair-drafted)"
            elif kind == "group_submission":
                extras["topic_tags_initial"] = ["GGA", "ADAPT-FIN", "group_position"]
            elif kind == "historical_GGA":
                extras["topic_tags_initial"] = ["GGA-IND", "historical_decision", "chair_drafting"]
                extras["procedural_hint"] = "drafts_text=True (prev presidency)"
            elif kind == "expert_GGA_analysis":
                extras["topic_tags_initial"] = ["expert_advice", "GGA"]
            elif kind == "realist_baseline":
                extras["topic_tags_initial"] = ["realist_baseline", "CO2", "OWID"]
                extras["doc_kind"] = "data_csv"

            rec = self.write_meta(
                local_path=local,
                url=url,
                sha256=dl["sha256"],
                size_bytes=dl["size_bytes"],
                extra=extras,
            )
            records.append(rec)
        return records
