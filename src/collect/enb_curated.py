"""IISD ENB COP30 curated collector.

이 collector는 WebSearch로 발견한 정확한 ENB 일일 보고 URL과
final summary URL을 직접 fetch한다. 또한 enb12{NNN}e.pdf range를
brute force한다.
"""
from __future__ import annotations

import logging
from pathlib import Path

from .base import CollectorBase

logger = logging.getLogger(__name__)

BASE = "https://enb.iisd.org"

# COP30 일일 보고 페이지 (HTML — 본문 + 임베디드 PDF 링크)
COP30_DAILY_PAGES = [
    f"{BASE}/belem-un-climate-change-conference-cop30-summary",
    f"{BASE}/belem-un-climate-change-conference-cop30-daily-report-10nov2025",
    f"{BASE}/belem-un-climate-change-conference-cop30-daily-report-11nov2025",
    f"{BASE}/belem-un-climate-change-conference-cop30-daily-report-12nov2025",
    f"{BASE}/belem-un-climate-change-conference-cop30-daily-report-13nov2025",
    f"{BASE}/belem-un-climate-change-conference-cop30-daily-report-14nov2025",
    f"{BASE}/belem-un-climate-change-conference-cop30-daily-report-15nov2025",
    f"{BASE}/belem-un-climate-change-conference-cop30-daily-report-17nov2025",
    f"{BASE}/belem-un-climate-change-conference-cop30-daily-report-18nov2025",
    f"{BASE}/belem-un-climate-change-conference-cop30-daily-report-19nov2025",
    f"{BASE}/belem-un-climate-change-conference-cop30-daily-report-20nov2025",
    f"{BASE}/belem-un-climate-change-conference-cop30-daily-report-21nov2025",
    f"{BASE}/belem-un-climate-change-conference-cop30",  # event index
]

# 알려진 PDF: enb12888e (COP30 final summary). brute force range 12880-12895
KNOWN_ENB_PDFS = [
    "https://enb.iisd.org/sites/default/files/2025-11/enb12888e.pdf",
]
ENB_BRUTE_RANGE = range(12879, 12896)
ENB_BRUTE_PATTERNS = [
    "https://enb.iisd.org/sites/default/files/2025-11/enb{N}e.pdf",
    "https://enb.iisd.org/sites/default/files/2025-12/enb{N}e.pdf",
]


class EnbCuratedCollector(CollectorBase):
    source_system = "enb.iisd.org"
    source_type = "iisd_enb"
    license_str = "CC BY-NC-SA 4.0"
    license_attribution = "© IISD Earth Negotiations Bulletin (academic use)"

    def collect(
        self,
        max_total: int = 50,
        include_brute: bool = True,
    ) -> list[dict]:
        records: list[dict] = []

        # 1. Daily report HTML pages
        for page_url in COP30_DAILY_PAGES:
            if len(records) >= max_total:
                break
            try:
                resp = self.http.fetch(page_url)
            except Exception as exc:
                logger.warning("ENB page fetch failed: %s — %s", page_url, exc)
                continue
            slug = page_url.replace(BASE, "").strip("/").replace("/", "_")[:80] or "index"
            local = self.out_dir / f"{slug}.html"
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_text(resp.text, encoding="utf-8")
            import hashlib
            sha = hashlib.sha256(resp.text.encode()).hexdigest()
            rec = self.write_meta(
                local_path=local,
                url=page_url,
                sha256=sha,
                size_bytes=len(resp.text),
                extra={
                    "file_format": "html",
                    "session": "COP30",
                    "topic_tags_initial": ["enb_daily_report", "negotiation_diary"],
                },
            )
            records.append(rec)

        # 2. Known ENB PDFs
        for url in KNOWN_ENB_PDFS:
            if len(records) >= max_total:
                break
            slug = Path(url).stem
            local = self.out_dir / f"{slug}.pdf"
            try:
                dl = self.http.download(url, local)
            except Exception as exc:
                logger.warning("ENB PDF fetch failed: %s — %s", url, exc)
                continue
            rec = self.write_meta(
                local_path=local,
                url=url,
                sha256=dl["sha256"],
                size_bytes=dl["size_bytes"],
                extra={
                    "file_format": "pdf",
                    "session": "COP30",
                    "topic_tags_initial": ["enb_summary"],
                    "bulletin_id": slug.replace("enb12", "").replace("e", ""),
                },
            )
            records.append(rec)

        # 3. Brute force enb12{NNN}e.pdf range
        if include_brute:
            for n in ENB_BRUTE_RANGE:
                if len(records) >= max_total:
                    break
                for pattern in ENB_BRUTE_PATTERNS:
                    url = pattern.format(N=n)
                    if any(r.get("source_url") == url for r in records):
                        continue
                    slug = f"enb{n}e"
                    local = self.out_dir / f"{slug}.pdf"
                    if local.exists():
                        continue
                    try:
                        dl = self.http.download(url, local)
                    except Exception:
                        continue
                    rec = self.write_meta(
                        local_path=local,
                        url=url,
                        sha256=dl["sha256"],
                        size_bytes=dl["size_bytes"],
                        extra={
                            "file_format": "pdf",
                            "session": "COP30",
                            "bulletin_id": str(n),
                            "topic_tags_initial": ["enb_daily_report"],
                            "discovery_method": "brute_force",
                        },
                    )
                    records.append(rec)
                    break  # found valid pattern, don't try the other path
        return records
