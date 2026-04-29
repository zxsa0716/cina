"""Historical presidency letters collector — Round 4 T01.

Target: COP21–COP27 presidency letters/notifications to expand
chair_metadata N from 32 to 80+.

IR 교수 비판 직접 대응:
  - chair_metadata N=32 중 75% COP30 단일 → 시계열 확장
  - Bayer-Urpelainen panel N>100 미달 → 역사적 의장단 문서 추가

소스 전략:
  COP26-27: UNFCCC /sites/default/files — 직접 PDF URL 확인됨
  COP24-25: UNFCCC notification PDFs + COP25 GCF report
  COP22-23: UNFCCC session documents (non-paper / notification)
  COP30:    CPD letters (2nd–12th) — 추가 의장단 시계열 확보
  COP21:    UNFCCC /sites/default/files — information note (incoming president)
"""
from __future__ import annotations

import logging
from pathlib import Path

from .base import CollectorBase

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# COP26 (UK, Alok Sharma) — confirmed PDF URLs
# ---------------------------------------------------------------------------
COP26_LETTERS = [
    # First letter to parties — July 2021 pre-ministerial
    (
        "https://unfccc.int/sites/default/files/resource/COP26%20%20President%20Designate%20Open%20letter.pdf",
        "COP26_GBR_Sharma_president_designate_open_letter_jul2021",
        "GBR",
        "COP26",
    ),
    # Pre-COP letter to all parties — September 2021
    (
        "https://unfccc.int/sites/default/files/resource/210921_Pre-COP_letter_CPD_final.pdf",
        "COP26_GBR_Sharma_pre_cop_letter_sep2021",
        "GBR",
        "COP26",
    ),
    # Ministerial letter on Climate/Technology Finance
    (
        "https://unfccc.int/sites/default/files/resource/Ministerial%20Letter%20to%20All%20Parties%20CTF%20final.pdf",
        "COP26_GBR_Sharma_ministerial_letter_CTF",
        "GBR",
        "COP26",
    ),
    # President Designate Reflections Note — October 2021
    (
        "https://unfccc.int/sites/default/files/resource/COP26%20President%20Designate%20Reflections%20Note.pdf",
        "COP26_GBR_Sharma_reflections_note_oct2021",
        "GBR",
        "COP26",
    ),
    # Pre-COP26 Chairs' Summary (joint COP25+COP26)
    (
        "https://unfccc.int/sites/default/files/resource/Pre-COP26%20chairs%20summary%20Final.pdf",
        "COP26_joint_pre_cop26_chairs_summary",
        "GBR",
        "COP26",
    ),
]

# ---------------------------------------------------------------------------
# COP27 (Egypt, Sameh Shoukry) — confirmed PDF URLs
# ---------------------------------------------------------------------------
COP27_LETTERS = [
    # Incoming COP27 President letter — 1 November 2022
    (
        "https://unfccc.int/sites/default/files/resource/1_November_incoming_COP27_President_%20letter.pdf",
        "COP27_EGY_Shoukry_incoming_president_letter_01nov2022",
        "EGY",
        "COP27",
    ),
    # During-COP President update — 16 November 2022
    (
        "https://unfccc.int/sites/default/files/resource/16%20November%20COP27%20President%20update.pdf",
        "COP27_EGY_Shoukry_president_update_16nov2022",
        "EGY",
        "COP27",
    ),
]

# ---------------------------------------------------------------------------
# COP25 (Chile, Carolina Schmidt) — confirmed PDF URL
# ---------------------------------------------------------------------------
COP25_LETTERS = [
    # COP25 Presidency GCF report to COP26 (inter-COP handover document)
    (
        "https://unfccc.int/sites/default/files/resource/Memo%20GCF%20COP25%20Presidency%20report%20to%20COP26.pdf",
        "COP25_CHL_Schmidt_GCF_presidency_report_to_COP26",
        "CHL",
        "COP25",
    ),
    # COP25 notification to parties (venue/dates confirmation)
    (
        "https://unfccc.int/sites/default/files/resource/notification_to_parties_cop25_cmp15_cma2.pdf",
        "COP25_notification_to_parties_cop25_cmp15_cma2",
        "CHL",
        "COP25",
    ),
]

# ---------------------------------------------------------------------------
# COP24 (Poland, Michal Kurtyka) — confirmed PDF URLs
# ---------------------------------------------------------------------------
COP24_LETTERS = [
    # Official notification to parties/observer states — COP24
    (
        "https://unfccc.int/sites/default/files/resource/notification_to_parties_and_observer_states_cop_24_cmp14_cma1.3.pdf",
        "COP24_POL_Kurtyka_notification_to_parties_oct2018",
        "POL",
        "COP24",
    ),
    # Pre-COP24 Krakow Summary Note — October 2018
    (
        "https://unfccc.int/sites/default/files/resource/Summarypre-COP_Krakow_2018_final.pdf",
        "COP24_POL_Kurtyka_pre_cop_krakow_summary_oct2018",
        "POL",
        "COP24",
    ),
]

# ---------------------------------------------------------------------------
# COP23 (Fiji, Frank Bainimarama) — confirmed PDF URL
# ---------------------------------------------------------------------------
COP23_LETTERS = [
    # Non-paper by COP23 President: Possible elements of outcomes
    (
        "https://unfccc.int/files/bodies/cop/application/pdf/possible_elements_outcomes_cp.23_16nov2017_22.00.pdf",
        "COP23_FJI_Bainimarama_possible_elements_outcomes_16nov2017",
        "FJI",
        "COP23",
    ),
    # COP23 Fiji notification to parties
    (
        "https://cop23.unfccc.int/sites/default/files/notification_to_parties_cop__23.pdf",
        "COP23_FJI_notification_to_parties_cop23",
        "FJI",
        "COP23",
    ),
]

# ---------------------------------------------------------------------------
# COP22 (Morocco, Salaheddine Mezouar) — official session documents
# ---------------------------------------------------------------------------
COP22_LETTERS = [
    # COP22 main session report — FCCC/CP/2016/10
    (
        "https://unfccc.int/resource/docs/2016/cop22/eng/10.pdf",
        "COP22_MAR_Mezouar_COP22_session_report_FCCC_CP_2016_10",
        "MAR",
        "COP22",
    ),
    # COP22 official daily document 15 November 2016
    (
        "https://unfccc.int/resource/docs/2016/cop22/OD/Marrakech2016-OD-20161115-en.pdf",
        "COP22_MAR_Mezouar_official_daily_15nov2016",
        "MAR",
        "COP22",
    ),
]

# ---------------------------------------------------------------------------
# COP21 (France, Laurent Fabius) — confirmed PDF URL
# ---------------------------------------------------------------------------
COP21_LETTERS = [
    # Information note: New COP21/CMP11 President (Fabius election)
    (
        "https://unfccc.int/sites/default/files/information_note_-_new_cop_21-cmp_11_president.pdf",
        "COP21_FRA_Fabius_new_president_information_note",
        "FRA",
        "COP21",
    ),
    # COP21 President statement — 5 December 2015
    (
        "https://unfccc.int/files/meetings/paris_nov_2015/in-session/application/pdf/cop_president_statement_5-december-2015_english.pdf",
        "COP21_FRA_Fabius_president_statement_05dec2015",
        "FRA",
        "COP21",
    ),
]

# ---------------------------------------------------------------------------
# COP30 CPD letters — President-Designate André Corrêa do Lago (BRA)
# Adds cross-temporal depth for chair_metadata time series
# ---------------------------------------------------------------------------
COP30_CPD_LETTERS = [
    # Vision letter (March 2025)
    (
        "https://unfccc.int/sites/default/files/resource/10.03.25_final_vision_cop_30.pdf",
        "COP30_BRA_CPD_vision_letter_mar2025",
        "BRA",
        "COP30",
    ),
    # 2nd CPD letter (May 2025)
    (
        "https://unfccc.int/sites/default/files/resource/cop_30_2nd_letter.pdf",
        "COP30_BRA_CPD_2nd_letter_may2025",
        "BRA",
        "COP30",
    ),
    # 4th CPD letter (June 2025)
    (
        "https://unfccc.int/sites/default/files/resource/Fourth_CPD_Letter.pdf",
        "COP30_BRA_CPD_4th_letter_jun2025",
        "BRA",
        "COP30",
    ),
    # 5th CPD letter (August 2025)
    (
        "https://unfccc.int/sites/default/files/resource/Fifth_CPD_Letter.pdf",
        "COP30_BRA_CPD_5th_letter_aug2025",
        "BRA",
        "COP30",
    ),
    # 7th CPD letter (August 2025)
    (
        "https://unfccc.int/sites/default/files/resource/Seventh_CPD_Letter.pdf",
        "COP30_BRA_CPD_7th_letter_aug2025",
        "BRA",
        "COP30",
    ),
    # 10th/final CPD letter (November 2025)
    (
        "https://unfccc.int/sites/default/files/resource/091125_cop_30_10th_letter_en.pdf",
        "COP30_BRA_CPD_10th_final_letter_nov2025",
        "BRA",
        "COP30",
    ),
    # During-COP30 president letter (17 November 2025)
    (
        "https://unfccc.int/sites/default/files/resource/20251117_Letter_COP30_President.pdf",
        "COP30_BRA_president_letter_17nov2025",
        "BRA",
        "COP30",
    ),
    # 12th letter post-COP (January 2026)
    (
        "https://unfccc.int/sites/default/files/resource/27012026_cop30_12_th_letter_en.pdf",
        "COP30_BRA_CPD_12th_letter_jan2026",
        "BRA",
        "COP30",
    ),
]

# Master catalogue
HISTORICAL_CHAIR_LETTERS: list[tuple[str, str, str, str]] = (
    COP21_LETTERS
    + COP22_LETTERS
    + COP23_LETTERS
    + COP24_LETTERS
    + COP25_LETTERS
    + COP26_LETTERS
    + COP27_LETTERS
    + COP30_CPD_LETTERS
)


class HistoricalChairCollector(CollectorBase):
    """Collects COP21–COP27 + COP30 presidency/chair letters.

    Purpose: expand chair_metadata N=32 → 80+ to satisfy Bayer-Urpelainen
    panel requirements and IR professor critique (Round 3).
    """

    source_system = "unfccc.int"
    source_type = "presidency_letter"
    license_str = "UN Open License"
    license_attribution = "© UNFCCC Presidency / United Nations"

    def collect(self) -> list[dict]:
        records: list[dict] = []
        success = 0
        failure = 0

        for url, slug, iso3, sess in HISTORICAL_CHAIR_LETTERS:
            ext = ".pdf" if url.lower().endswith(".pdf") else ".html"
            local = self.out_dir / sess / f"{slug}{ext}"

            try:
                dl = self.http.download(url, local)
            except Exception as exc:
                logger.warning(
                    "[HistoricalChair] FAILED %s — %s: %s", sess, slug, exc
                )
                failure += 1
                continue

            rec = self.write_meta(
                local_path=local,
                url=url,
                sha256=dl["sha256"],
                size_bytes=dl["size_bytes"],
                extra={
                    "session": sess,
                    "country_authors_initial": [iso3],
                    "topic_tags_initial": [
                        "presidency",
                        "chair_letter",
                        "chair_metadata",
                    ],
                    "doc_kind": "historical_chair_letter",
                    "procedural_hint": "is_chair_role=True; is_pen_holder=likely",
                    "round_target": "round4_T01_historical_chair",
                },
            )
            records.append(rec)
            success += 1
            logger.info(
                "[HistoricalChair] OK %s — %s (%.1f KB)",
                sess,
                slug,
                dl["size_bytes"] / 1024,
            )

        logger.info(
            "[HistoricalChair] DONE: %d success, %d failed / %d total targets",
            success,
            failure,
            len(HISTORICAL_CHAIR_LETTERS),
        )
        return records
