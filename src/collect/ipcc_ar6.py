"""IPCC AR6 WG2 (Adaptation) chapter collector.

Source: https://www.ipcc.ch/report/ar6/wg2/
Pattern: https://www.ipcc.ch/report/ar6/wg2/downloads/report/IPCC_AR6_WGII_Chapter{NN}.pdf

CINA needs Ch.16 (Key Risks), Ch.17 (Decision-Making), Ch.18 (Climate Resilient Development).
"""
from __future__ import annotations

import logging
from pathlib import Path

from .base import CollectorBase

logger = logging.getLogger(__name__)

DOWNLOAD_BASE = "https://www.ipcc.ch/report/ar6/wg2/downloads/report"

CINA_CHAPTERS = {
    "01": "Point of Departure and Key Concepts",
    "16": "Key Risks across Sectors and Regions",
    "17": "Decision-Making Options for Managing Risk",
    "18": "Climate Resilient Development Pathways",
}


class IpccAr6Collector(CollectorBase):
    source_system = "ipcc.ch"
    source_type = "ipcc_ar6_wg2"
    license_str = "IPCC Open Use"
    license_attribution = "© IPCC AR6 WGII"

    def collect(self, chapters: list[str] | None = None) -> list[dict]:
        chapters = chapters or list(CINA_CHAPTERS.keys())
        records = []
        for ch in chapters:
            url = f"{DOWNLOAD_BASE}/IPCC_AR6_WGII_Chapter{ch}.pdf"
            local = self.out_dir / f"AR6_WG2_Chapter{ch}.pdf"
            try:
                dl = self.http.download(url, local)
            except Exception as exc:
                logger.warning("Chapter %s download failed: %s", ch, exc)
                continue
            rec = self.write_meta(
                local_path=local,
                url=url,
                sha256=dl["sha256"],
                size_bytes=dl["size_bytes"],
                extra={
                    "chapter_number": ch,
                    "chapter_title": CINA_CHAPTERS.get(ch, ""),
                    "wg": "WGII",
                },
            )
            records.append(rec)
        return records
