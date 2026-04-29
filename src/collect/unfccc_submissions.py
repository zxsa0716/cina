"""UNFCCC Documents Portal collector.

Source: https://unfccc.int/documents
Filter pattern: ?f[0]=topic:{ID}&f[1]=conference:{ID}&f[2]=country:{ISO3}

Strategy:
1. Fetch listing page with topic/conference/country filters.
2. Parse HTML for document links (PDF + symbol metadata).
3. Download each PDF, write .meta.json, record in manifest.
"""
from __future__ import annotations

import logging
import re
from pathlib import Path
from urllib.parse import quote, urljoin

from bs4 import BeautifulSoup

from .base import CollectorBase

logger = logging.getLogger(__name__)

BASE = "https://unfccc.int"
DOCS_URL = f"{BASE}/documents"

# Topic IDs from docs/11_source_catalog.md §1.3
TOPIC_IDS = {
    "adaptation": 1136,
    "naps": 3812,
    "loss_damage": 3558,
    "ac": 3484,
}


def build_listing_url(
    topic_id: int | None = None,
    conference_id: int | None = None,
    country_id: int | None = None,
    page: int = 0,
) -> str:
    parts = []
    idx = 0
    if topic_id is not None:
        parts.append(f"f%5B{idx}%5D=topic%3A{topic_id}")
        idx += 1
    if conference_id is not None:
        parts.append(f"f%5B{idx}%5D=conference%3A{conference_id}")
        idx += 1
    if country_id is not None:
        parts.append(f"f%5B{idx}%5D=country%3A{country_id}")
        idx += 1
    if page > 0:
        parts.append(f"page={page}")
    qs = "&".join(parts)
    return f"{DOCS_URL}?{qs}" if qs else DOCS_URL


class UnfcccSubmissionsCollector(CollectorBase):
    source_system = "unfccc.int"
    source_type = "unfccc_submission"
    license_str = "UN Open License"
    license_attribution = "© UNFCCC"

    def collect(
        self,
        topic: str = "adaptation",
        conference_id: int | None = None,
        country_id: int | None = None,
        max_pages: int = 5,
        max_documents: int | None = None,
        use_dynamic_fallback: bool = True,
    ) -> list[dict]:
        topic_id = TOPIC_IDS.get(topic.lower())
        if topic_id is None:
            raise ValueError(f"Unknown topic '{topic}'. Choose from {list(TOPIC_IDS)}")

        records = []
        static_zero = True
        for page in range(max_pages):
            url = build_listing_url(topic_id, conference_id, country_id, page)
            try:
                resp = self.http.fetch(url)
            except Exception as exc:
                logger.warning("Listing page %s failed: %s", url, exc)
                break

            doc_links = self._parse_listing(resp.text)
            if not doc_links:
                break
            static_zero = False

            for link in doc_links:
                if max_documents is not None and len(records) >= max_documents:
                    return records
                rec = self._download_document(link)
                if rec:
                    records.append(rec)

        # Dynamic fallback when static parser yields nothing (UNFCCC SPA)
        if static_zero and use_dynamic_fallback:
            logger.info("Static collector yielded 0; falling back to Playwright")
            try:
                from .dynamic_browser import DynamicBrowserClient
                browser = DynamicBrowserClient(headless=True)
                first_url = build_listing_url(topic_id, conference_id, country_id, 0)
                anchors = browser.extract_pdf_links(
                    first_url,
                    wait_for_selector="a[href$='.pdf']",
                    wait_ms_after_load=4000,
                    max_paginate_clicks=max_pages - 1,
                    next_button_selector="a[rel='next'], a.pager__item--next",
                )
                logger.info("Dynamic fallback found %d PDF anchors", len(anchors))
                for link in anchors:
                    if max_documents is not None and len(records) >= max_documents:
                        break
                    link.setdefault("title", link.get("text"))
                    link["symbol"] = self._extract_symbol(link.get("text") or link["url"])
                    rec = self._download_document(link)
                    if rec:
                        records.append(rec)
            except Exception as exc:
                logger.error("Dynamic fallback failed: %s", exc)

        return records

    # ------------------------------------------------------------------
    def _parse_listing(self, html: str) -> list[dict]:
        """Extract document metadata from listing HTML."""
        soup = BeautifulSoup(html, "html.parser")
        out = []

        # UNFCCC's document list uses cards/rows with specific classes (subject to change).
        # Defensive: gather every PDF anchor + nearby symbol/title text.
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if not href.lower().endswith(".pdf"):
                continue
            full_url = urljoin(BASE, href)
            title = a.get_text(strip=True) or Path(href).stem
            symbol = self._extract_symbol(title) or self._extract_symbol(href)
            out.append({"url": full_url, "title": title, "symbol": symbol})
        return out

    @staticmethod
    def _extract_symbol(text: str) -> str | None:
        m = re.search(r"FCCC[/_][A-Z]+[/_]\d{4}[/_][\w.]+", text)
        return m.group(0).replace("_", "/") if m else None

    # ------------------------------------------------------------------
    def _download_document(self, link: dict) -> dict | None:
        url = link["url"]
        symbol = link.get("symbol") or "unknown"
        slug = re.sub(r"[^A-Za-z0-9]+", "_", symbol or Path(url).stem).strip("_")
        local = self.out_dir / f"{slug}.pdf"
        try:
            dl = self.http.download(url, local)
        except Exception as exc:
            logger.warning("Download failed for %s: %s", url, exc)
            return None
        return self.write_meta(
            local_path=local,
            url=url,
            sha256=dl["sha256"],
            size_bytes=dl["size_bytes"],
            extra={
                "symbol": symbol,
                "title": link.get("title"),
            },
        )
