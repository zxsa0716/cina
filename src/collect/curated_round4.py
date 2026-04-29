"""Round 4 supplementary curated collector.

Round 2 cross_review CR3.1 (historical chair_metadata) + CR3.4 (frame_type
justice/development) + CR3.7 (non-state actors) 직접 대응.

소스 카탈로그:
- COP26-COP30 historical presidency letters (chair_metadata 시계열)
- IIPFCC, indigenous peoples submissions (non-state actor)
- AILAC GST submission (frame_type=justice/development)
- LDC Baku-Belém Roadmap submission
- G77+China submission
- Global Solidarity Taskforce submission
- COP30 cover decision drafts
"""
from __future__ import annotations

import logging
from pathlib import Path

from .base import CollectorBase

logger = logging.getLogger(__name__)


# Historical presidency letters — chair_metadata N=17 → 30+ 확장 (CR3.1 직접 대응)
HISTORICAL_PRESIDENCY = [
    # COP28 UAE Sultan Al Jaber
    ("https://unfccc.int/sites/default/files/resource/cop28_publish_letter_october_2023_enfinal.pdf",
     "COP28_UAE_presidency_letter_oct2023", "ARE", "COP28"),
    # COP29 Azerbaijan Mukhtar Babayev
    ("https://unfccc.int/sites/default/files/resource/COP29_President%20Designate_First%20Letter%20to%20Parties%20and%20observer%20States.pdf",
     "COP29_AZE_president_designate_first_letter", "AZE", "COP29"),
]

# COP30 presidency letters (Brazilian)
COP30_PRESIDENCY = [
    ("https://cop30.br/en/brazilian-presidency/letters-from-the-president/letter-from-the-brazilian-presidency",
     "COP30_BRA_first_letter_from_president_html", "BRA", "COP30"),
]

# Non-state actor / Indigenous submissions (CR3.7 직접 대응)
NON_STATE_INDIGENOUS = [
    # IIPFCC Article 6 input
    ("https://unfccc.int/sites/default/files/resource/SBM014_Call_for_input_annotations_SD_Tool_IIPFCC.pdf",
     "IIPFCC_SBM014_call_input_annotations", "IIPFCC", "MULTI"),
    # IIPFCC submission on traditional knowledge (older but foundational)
    ("https://unfccc.int/files/parties_observers/submissions_from_observers/application/pdf/865.pdf",
     "IIPFCC_submission_traditional_knowledge", "IIPFCC", "MULTI"),
    # AIPP + IWGIA joint submission (Indigenous Peoples)
    ("https://www4.unfccc.int/sites/SubmissionsStaging/Documents/202009012224---Final_AIPP_IWGIA_Submission_1_September_2020.pdf",
     "AIPP_IWGIA_joint_submission_2020", "AIPP_IWGIA", "MULTI"),
    # COP30 LCIPP notification (procedural meta)
    ("https://unfccc.int/sites/default/files/resource/notification_to_parties_and_observer_states_cop30.pdf",
     "COP30_notification_to_parties_observers_LCIPP", "Multiple", "COP30"),
]

# AILAC formal submission (frame_type=justice + development direct evidence — CR3.4)
AILAC_LDC_G77 = [
    ("https://unfccc.int/sites/default/files/resource/202210211110---AILAC%20Submsion%20on%20GST_TD1.2.pdf",
     "AILAC_GST_TD1_2_submission_2022", "AILAC", "GST1"),
    # LDC Group Baku to Belém Roadmap to 1.3T preliminary views
    ("https://unfccc.int/sites/default/files/resource/LDCs_B2BR.docx.pdf",
     "LDC_Baku_Belem_1_3T_roadmap_views", "LDC", "COP30"),
    # G77 and China Baku-Belém submission
    ("https://unfccc.int/sites/default/files/resource/G77_and_China.pdf",
     "G77_China_Baku_Belem_1_3T_submission", "G77", "COP30"),
    # Global Solidarity Taskforce (Solidarity Levies in B2BR)
    ("https://unfccc.int/sites/default/files/resource/Global_Solidarity_Taskforce_Baku_Belem_Roadmap_submission.pdf",
     "Global_Solidarity_Taskforce_B2BR_2025", "Global_Solidarity_Taskforce", "COP30"),
]

# COP30 GGA draft texts (Round 2 stages of negotiation — chair drafting evidence)
GGA_DRAFT_PROGRESSION = [
    ("https://unfccc.int/sites/default/files/resource/gga_cop30_3.pdf",
     "GGA_COP30_draft_text_3", "Multiple", "COP30"),
    # cma2025/07 conference INF report
    ("https://unfccc.int/sites/default/files/resource/cp2025_07a01a_adv.pdf",
     "FCCC_CP_2025_07a01a_advance", "Multiple", "COP30"),
]

# C2ES analysis for COP29 Baku outcomes (cross-temporal)
EXPERT_ANALYSIS_COP29 = [
    ("https://www.c2es.org/wp-content/uploads/2025/01/Key-Negotiations-Related-Outcomes-of-the-UN-Climate-Change-Conference-in-Baku.pdf",
     "C2ES_COP29_Baku_outcomes", "Multiple", "COP29"),
]


class CuratedRound4Collector(CollectorBase):
    source_system = "round4_curated"
    source_type = "round4_curated"
    license_str = "Mixed (UN Open / observer org / C2ES)"
    license_attribution = "© Various (UN / IIPFCC / AILAC / LDC / G77 / C2ES — see record)"

    def collect(self) -> list[dict]:
        records: list[dict] = []
        all_targets = []
        all_targets += [(u, s, c, sess, "historical_chair_letter") for u, s, c, sess in HISTORICAL_PRESIDENCY]
        all_targets += [(u, s, c, sess, "cop30_presidency_letter") for u, s, c, sess in COP30_PRESIDENCY]
        all_targets += [(u, s, c, sess, "non_state_indigenous") for u, s, c, sess in NON_STATE_INDIGENOUS]
        all_targets += [(u, s, c, sess, "AILAC_LDC_G77_submission") for u, s, c, sess in AILAC_LDC_G77]
        all_targets += [(u, s, c, sess, "GGA_draft_progression") for u, s, c, sess in GGA_DRAFT_PROGRESSION]
        all_targets += [(u, s, c, sess, "expert_analysis_COP29") for u, s, c, sess in EXPERT_ANALYSIS_COP29]

        for url, slug, country, sess, kind in all_targets:
            ext = ".pdf" if url.lower().endswith(".pdf") else ".html"
            local = self.out_dir / kind / f"{slug}{ext}"
            try:
                dl = self.http.download(url, local)
            except Exception as exc:
                logger.warning("Round4 download failed for %s: %s", url, exc)
                continue

            extras = {
                "session": sess,
                "doc_kind": kind,
                "country_authors_initial": [country] if country and country != "Multiple" else [],
                "round_target": "round4_remediation",
            }

            # Map kind to topic_tags + procedural_signal hints
            if kind == "historical_chair_letter":
                extras["topic_tags_initial"] = ["chair_letter", "presidency_communication", "adaptation"]
                extras["procedural_hint"] = "is_chair_role=True"
            elif kind == "cop30_presidency_letter":
                extras["topic_tags_initial"] = ["chair_letter", "BRA_presidency", "COP30"]
                extras["procedural_hint"] = "is_chair_role=True, is_pen_holder=likely"
            elif kind == "non_state_indigenous":
                extras["topic_tags_initial"] = ["non_state_actor", "indigenous", "JT-ADAPT", "MIT-ADAPT"]
                extras["frame_hint"] = "justice (likely)"
            elif kind == "AILAC_LDC_G77_submission":
                extras["topic_tags_initial"] = ["GGA", "ADAPT-FIN", "L&D-OP", "developing_country_coalition"]
                extras["frame_hint"] = "justice + development (CBDR-RC)"
            elif kind == "GGA_draft_progression":
                extras["topic_tags_initial"] = ["GGA-IND", "draft_text_progression", "chair_drafting"]
                extras["procedural_hint"] = "drafts_text=True (Brazilian presidency)"
            elif kind == "expert_analysis_COP29":
                extras["topic_tags_initial"] = ["expert_analysis", "COP29", "C2ES"]

            rec = self.write_meta(
                local_path=local,
                url=url,
                sha256=dl["sha256"],
                size_bytes=dl["size_bytes"],
                extra=extras,
            )
            records.append(rec)
        return records
