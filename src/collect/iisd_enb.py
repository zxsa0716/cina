"""IISD Earth Negotiations Bulletin collector.

Source: https://enb.iisd.org/
ENB Vol 12 = UNFCCC. Pattern: enb12{NNN}e.pdf (e=English).

Strategy:
1. Fetch event index page (e.g., COP30) to discover daily bulletin URLs.
2. Download each PDF.
3. Annotate with session metadata.

Note: ENB blocks plain WebFetch. We use proper User-Agent (CINA-Research) and rate-limit.
License: CC BY-NC-SA 4.0 — academic non-commercial OK.
"""
from __future__ import annotations

import logging
import re
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base import CollectorBase

logger = logging.getLogger(__name__)

BASE = "https://enb.iisd.org"
EVENTS = {
    "cop30": f"{BASE}/un-climate-change-conference-cop30",
    "cop29": f"{BASE}/un-climate-change-conference-cop29",
    "cop28": f"{BASE}/un-climate-change-conference-cop28",
    "sb62":  f"{BASE}/bonn-climate-change-conference-sb62-sbi62-sbsta62",
}


class IisdEnbCollector(CollectorBase):
    source_system = "enb.iisd.org"
    source_type = "iisd_enb"
    license_str = "CC BY-NC-SA 4.0"
    license_attribution = "© IISD Earth Negotiations Bulletin"

    def collect(
        self,
        event: str = "cop30",
        max_documents: int | None = None,
        use_dynamic_fallback: bool = True,
        enb_volume_brute_force_range: tuple[int, int] | None = None,
    ) -> list[dict]:
        event_url = EVENTS.get(event.lower())
        if event_url is None:
            raise ValueError(f"Unknown event '{event}'. Choose from {list(EVENTS)}")

        pdf_urls: list[str] = []
        try:
            resp = self.http.fetch(event_url)
            pdf_urls = self._discover_pdfs(resp.text)
            logger.info("Discovered %d ENB PDFs (static) at %s", len(pdf_urls), event_url)
        except Exception as exc:
            logger.warning("Static event index fetch failed: %s", exc)

        if not pdf_urls and use_dynamic_fallback:
            logger.info("ENB static yielded 0; falling back to Playwright")
            try:
                from .dynamic_browser import DynamicBrowserClient
                browser = DynamicBrowserClient(headless=True)
                anchors = browser.extract_pdf_links(
                    event_url,
                    wait_for_selector="a[href*='enb12']",
                    wait_ms_after_load=4000,
                )
                pdf_urls = [a["url"] for a in anchors if "enb12" in a["url"].lower()]
                logger.info("ENB dynamic fallback found %d PDFs", len(pdf_urls))
            except Exception as exc:
                logger.warning("ENB dynamic fallback failed: %s", exc)

        if not pdf_urls and enb_volume_brute_force_range:
            lo, hi = enb_volume_brute_force_range
            logger.info("ENB brute force fallback: enb12{%d..%d}e.pdf", lo, hi)
            for n in range(lo, hi + 1):
                # Try common path patterns
                for prefix in [
                    f"{BASE}/sites/default/files/2025-11/enb12{n}e.pdf",
                    f"{BASE}/sites/default/files/2025-12/enb12{n}e.pdf",
                ]:
                    pdf_urls.append(prefix)

        records = []
        for url in pdf_urls:
            if max_documents is not None and len(records) >= max_documents:
                break
            rec = self._download(url, event)
            if rec:
                records.append(rec)
        return records

    def _discover_pdfs(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        pdfs = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.lower().endswith(".pdf") and "enb12" in href.lower():
                pdfs.add(urljoin(BASE, href))
            elif "enb12" in href and "/sites/default/files/" in href:
                pdfs.add(urljoin(BASE, href))
        return sorted(pdfs)

    def _download(self, url: str, event: str) -> dict | None:
        m = re.search(r"enb12(\d+)e", url, re.IGNORECASE)
        bulletin_id = m.group(1) if m else "unknown"
        local = self.out_dir / f"enb12{bulletin_id}e.pdf"
        try:
            dl = self.http.download(url, local)
        except Exception as exc:
            logger.warning("ENB download failed for %s: %s", url, exc)
            return None
        return self.write_meta(
            local_path=local,
            url=url,
            sha256=dl["sha256"],
            size_bytes=dl["size_bytes"],
            extra={
                "bulletin_id": bulletin_id,
                "event": event,
                "session": event.upper(),
                "topic_tags_initial": ["adaptation"],
            },
        )
