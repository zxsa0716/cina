"""Round 6 / Round 5 remediation collector.

Task T01 Round 5 직접 대응:
  P0-2 UNFCCC SBI/SBSTA contact group informal notes (GGA, co-facilitator, SB62/SB63)
  P0-4 COP28-30 Troika joint letters (보강)
  KEI KACCC 적응 매거진 (대리 KEI WP — KEI WP 시리즈 직접 PDF 미공개 확인 후 공개 가능 대안)

Castro 2025 (P0-1) 는 SWISSUbase restricted-access 확인 — access_request placeholder 처리.
"""
from __future__ import annotations

import logging
from pathlib import Path

from .base import CollectorBase

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# P0-2: UNFCCC SBI/SBSTA informal notes — co-facilitator / contact group
# ---------------------------------------------------------------------------

UNFCCC_INFORMAL_NOTES = [
    # 1. INFORMAL NOTE BY THE CO-FACILITATORS on SBSTA 63 agenda item 5(a)
    #    GGA — COP30 Nov 2025 (primary GGA informal note)
    (
        "https://unfccc.int/sites/default/files/resource/gga_cop30.pdf",
        "UNFCCC_SBSTA63_SBI63_GGA_informal_note_cop30",
        "Multiple",
        "SBSTA63/SBI63",
        "co_facilitator_informal_note",
    ),
    # 2. DRAFT TEXT on SBSTA 62 agenda item 5(a) SBI 62 agenda item 11(a)
    #    GGA — SB62 Bonn June 2025 (pre-COP30 draft text)
    (
        "https://unfccc.int/sites/default/files/resource/GGA_dt_sb62.pdf",
        "UNFCCC_SBSTA62_SBI62_GGA_draft_text_sb62",
        "Multiple",
        "SBSTA62/SBI62",
        "co_facilitator_draft_text",
    ),
    # 3. DRAFT TEXT on SBSTA 63 agenda item 5(a) SBI 63 agenda item 12(a)
    #    GGA — SB63 / COP30 (versioned draft text 0)
    (
        "https://unfccc.int/sites/default/files/resource/gga_cop30_0.pdf",
        "UNFCCC_SBSTA63_GGA_draft_text_cop30_v0",
        "Multiple",
        "SBSTA63",
        "co_facilitator_draft_text",
    ),
    # 4. Co-facilitators' informal note on SBI 63 agenda item 8 / SBSTA 63 agenda item 7
    #    Mitigation Work Programme — COP30 (MWP co-facilitator note)
    (
        "https://unfccc.int/sites/default/files/resource/MWP_cop30_2.pdf",
        "UNFCCC_SBI63_SBSTA63_MWP_cofac_note_cop30",
        "Multiple",
        "SBI63/SBSTA63",
        "co_facilitator_informal_note",
    ),
    # 5. Proposal by the Presidency on CMA 7 agenda item 8(a) — GGA (Brazilian presidency draft)
    (
        "https://unfccc.int/sites/default/files/resource/gga_cop30_5.pdf",
        "UNFCCC_CMA7_GGA_presidency_proposal_cop30_v5",
        "BRA",
        "CMA7/COP30",
        "presidency_proposal",
    ),
    # 6. SB Chairs joint note ahead of SB 62 (pre-Bonn chairs' scenario note)
    (
        "https://unfccc.int/sites/default/files/resource/SB62_JointNote.pdf",
        "UNFCCC_SB62_chairs_joint_note",
        "Multiple",
        "SBI62/SBSTA62",
        "chairs_joint_note",
    ),
    # 7. SB Chairs joint note ahead of SB 63 (pre-COP30 chairs' scenario note)
    (
        "https://unfccc.int/sites/default/files/resource/SB63_JointNote.pdf",
        "UNFCCC_SB63_chairs_joint_note",
        "Multiple",
        "SBI63/SBSTA63",
        "chairs_joint_note",
    ),
    # 8. Technical Report by the Expert Group on Indicators for the GGA targets 2025
    (
        "https://unfccc.int/sites/default/files/resource/Technical%20Report%20by%20the%20Expert%20Group%20on%20Indicators%20for%20the%20GGA%20targets%202025.pdf",
        "UNFCCC_GGA_expert_group_technical_report_indicators_2025",
        "Multiple",
        "SB62/SB63",
        "expert_group_technical_report",
    ),
    # 9. Synthesis of submissions on the UAE-Belém work programme
    (
        "https://unfccc.int/sites/default/files/resource/Synthesis%20of%20Submissions%20UAE-Belem%20Work%20programme%20Final.pdf",
        "UNFCCC_UAE_Belem_WP_synthesis_submissions",
        "Multiple",
        "SB62",
        "synthesis_document",
    ),
    # 10. Note by COP Presidency Consultations 11 Sep 2025 (Troika + pre-COP30 process)
    (
        "https://unfccc.int/sites/default/files/resource/Note_Presidency_Consultations_11Sep25.pdf",
        "UNFCCC_presidency_consultations_11sep2025",
        "Multiple",
        "COP30_prepcom",
        "presidency_consultation_note",
    ),
]

# ---------------------------------------------------------------------------
# P0-4: COP28-30 Troika joint letters (보강 — historical + 2024/2025 additions)
# ---------------------------------------------------------------------------

TROIKA_LETTERS = [
    # 1st Troika letter — March 2024 (COP29 incoming + COP28 + COP30)
    (
        "https://unfccc.int/sites/default/files/resource/presidencies_troika_letter_to_parties.pdf",
        "Troika_first_letter_to_parties_mar2024",
        "ARE_AZE_BRA",
        "COP28-30_Troika",
        "troika_joint_letter",
    ),
    # 2nd Troika letter — July 2024
    (
        "https://unfccc.int/sites/default/files/resource/troika_second_letter_to_parties_and_observers__july_2024.pdf",
        "Troika_second_letter_to_parties_jul2024",
        "ARE_AZE_BRA",
        "COP28-30_Troika",
        "troika_joint_letter",
    ),
    # Joint Statement — Feb 2025 (post-Baku, pre-Belém)
    (
        "https://unfccc.int/sites/default/files/resource/Joint_Statement_of_the_COP28_COP29_and_COP30_Presidencies_Troika.pdf",
        "Troika_joint_statement_feb2025",
        "ARE_AZE_BRA",
        "COP28-30_Troika",
        "troika_joint_statement",
    ),
    # Troika Statement 2025 — July 2025
    (
        "https://unfccc.int/sites/default/files/resource/2025_Joint_Statement_COP_Presidencies_Troika.pdf",
        "Troika_joint_statement_jul2025",
        "ARE_AZE_BRA",
        "COP28-30_Troika",
        "troika_joint_statement",
    ),
    # Troika Concept Note SB62 (procedural coordination)
    (
        "https://unfccc.int/sites/default/files/resource/Troika_Concept_Note_SB%2062.pdf",
        "Troika_concept_note_sb62",
        "ARE_AZE_BRA",
        "SB62",
        "troika_concept_note",
    ),
]

# ---------------------------------------------------------------------------
# KEI / KACCC publications — public open PDFs (P0-3 대안)
# Note: KEI WP 시리즈는 repository.kei.re.kr 에서 접근 불가 (open-access 미제공).
# 공개 대안: KACCC ADAPTATION 매거진 + KACCC 국제동향 뉴스레터 (기후변화 적응 정책)
# ---------------------------------------------------------------------------

KEI_KACCC_PUBLICATIONS = [
    # ADAPTATION Magazine 2024 Vol.1 (June 2024)
    (
        "https://kaccc.kei.re.kr/home/boardDownload.es?mid=a10502010000&bid=0006&list_no=3443&seq=1&bef_yn=",
        "KEI_KACCC_ADAPTATION_2024_vol1",
        "KEI/KACCC",
        "KOR_NAP",
        "kei_kaccc_adaptation_magazine",
    ),
    # ADAPTATION Magazine 2024 Vol.2 (Dec 2024)
    (
        "https://kaccc.kei.re.kr/home/boardDownload.es?mid=a10502010000&bid=0006&list_no=3993&seq=1&bef_yn=",
        "KEI_KACCC_ADAPTATION_2024_vol2",
        "KEI/KACCC",
        "KOR_NAP",
        "kei_kaccc_adaptation_magazine",
    ),
    # ADAPTATION Magazine 2023 Vol.2 (Dec 2023)
    (
        "https://kaccc.kei.re.kr/home/boardDownload.es?mid=a10502010000&bid=0006&list_no=3345&seq=1&bef_yn=Y",
        "KEI_KACCC_ADAPTATION_2023_vol2",
        "KEI/KACCC",
        "KOR_NAP",
        "kei_kaccc_adaptation_magazine",
    ),
    # ADAPTATION Magazine 2023 Vol.1 (June 2023)
    (
        "https://kaccc.kei.re.kr/home/boardDownload.es?mid=a10502010000&bid=0006&list_no=3223&seq=1&bef_yn=Y",
        "KEI_KACCC_ADAPTATION_2023_vol1",
        "KEI/KACCC",
        "KOR_NAP",
        "kei_kaccc_adaptation_magazine",
    ),
    # ADAPTATION Magazine 2025 Vol.1 (June 2025)
    (
        "https://kaccc.kei.re.kr/home/boardDownload.es?mid=a10502010000&bid=0006&list_no=4120&seq=1&bef_yn=",
        "KEI_KACCC_ADAPTATION_2025_vol1",
        "KEI/KACCC",
        "KOR_NAP",
        "kei_kaccc_adaptation_magazine",
    ),
    # Korea Adaptation Communication to UNFCCC (2023, official PDF)
    (
        "https://unfccc.int/sites/default/files/ACR/2023-03/The%20Republic%20of%20Koreas%20Adaptation%20Communication.pdf",
        "KOR_Adaptation_Communication_UNFCCC_2023",
        "KOR",
        "KOR_NAP",
        "national_adaptation_communication",
    ),
    # Korea 3rd National Climate Change Adaptation Plan 2021-2025 (summary PDF)
    (
        "http://www.climate.go.kr/home/cc_data/policy/3_nation_climate_change_adaptation_step_summary.pdf",
        "KOR_3rd_NCCAP_2021_2025_summary",
        "KOR",
        "KOR_NAP",
        "national_adaptation_plan",
    ),
]


class CuratedRound6Collector(CollectorBase):
    """Round 6 collector for T01 P0-2/P0-4 + KEI substitutes.

    P0-1 Castro 2025 matrix: SWISSUbase restricted — placeholder only.
    P0-3 KEI WP: directly-downloadable KEI WPs not found; KACCC open PDFs used as proxy.
    """

    source_system = "round6_curated"
    source_type = "round6_curated"
    license_str = "Mixed (UN Open / KEI CC-BY-NC / Korea MOE open)"
    license_attribution = (
        "UNFCCC © UN public document (free reuse with attribution); "
        "KEI/KACCC © 한국환경연구원 (비영리 학술 목적 활용); "
        "KOR MOE public policy document"
    )

    def collect(self) -> list[dict]:
        records: list[dict] = []
        all_targets = (
            [(u, s, c, sess, kind) for u, s, c, sess, kind in UNFCCC_INFORMAL_NOTES]
            + [(u, s, c, sess, kind) for u, s, c, sess, kind in TROIKA_LETTERS]
            + [(u, s, c, sess, kind) for u, s, c, sess, kind in KEI_KACCC_PUBLICATIONS]
        )

        for url, slug, country, sess, kind in all_targets:
            # Determine file extension
            if url.lower().endswith(".csv"):
                ext = ".csv"
            elif "boardDownload" in url or not url.lower().endswith(".pdf"):
                ext = ".pdf"
            else:
                ext = ".pdf"

            # Route to sub-directory based on kind
            if kind in (
                "co_facilitator_informal_note",
                "co_facilitator_draft_text",
                "chairs_joint_note",
                "expert_group_technical_report",
                "synthesis_document",
                "presidency_proposal",
                "presidency_consultation_note",
            ):
                sub = "sbi_sbsta_notes"
            elif kind in (
                "troika_joint_letter",
                "troika_joint_statement",
                "troika_concept_note",
            ):
                sub = "troika_letters"
            else:
                sub = "kei_wp_series"

            local = self.out_dir / sub / f"{slug}{ext}"
            try:
                dl = self.http.download(url, local)
            except Exception as exc:
                logger.warning("Round6 download failed for %s: %s", url, exc)
                continue

            extras = {
                "session": sess,
                "doc_kind": kind,
                "country_authors_initial": (
                    [country] if country and country not in ("Multiple", "") else []
                ),
                "round_target": "round5_T01_remediation",
            }

            if kind in (
                "co_facilitator_informal_note",
                "co_facilitator_draft_text",
                "presidency_proposal",
            ):
                extras["topic_tags_initial"] = ["GGA-IND", "informal_note", "contact_group"]
                extras["chair_role"] = "co-facilitator"
                extras["tallberg_signal"] = "pre-cooking evidence candidate"
            elif kind in ("chairs_joint_note", "synthesis_document"):
                extras["topic_tags_initial"] = ["GGA-IND", "chairs_note", "procedural"]
                extras["chair_role"] = "sb-chair"
            elif kind == "expert_group_technical_report":
                extras["topic_tags_initial"] = [
                    "GGA-IND",
                    "expert_group",
                    "UAE_Belem_WP",
                ]
            elif kind == "presidency_consultation_note":
                extras["topic_tags_initial"] = [
                    "GGA",
                    "presidency",
                    "pre_COP30",
                ]
                extras["chair_role"] = "presidency"
            elif kind.startswith("troika"):
                extras["topic_tags_initial"] = [
                    "Troika",
                    "presidency_communication",
                    "NDC",
                    "1.5C",
                ]
                extras["chair_role"] = "troika_presidency"
            elif kind in (
                "kei_kaccc_adaptation_magazine",
                "national_adaptation_plan",
                "national_adaptation_communication",
            ):
                extras["topic_tags_initial"] = [
                    "adaptation",
                    "KOR_NAP",
                    "KEI",
                    "IRR_Korea_reference",
                ]
                extras["irr_korea_reference"] = "proxy_for_WP_series"

            rec = self.write_meta(
                local_path=local,
                url=url,
                sha256=dl["sha256"],
                size_bytes=dl["size_bytes"],
                extra=extras,
            )
            records.append(rec)

        return records
