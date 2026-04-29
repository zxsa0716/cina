"""NDC Registry collector.

Source: https://unfccc.int/NDCREG
PDF pattern: https://unfccc.int/sites/default/files/{YYYY-MM}/{filename}.pdf
"""
from __future__ import annotations

import logging
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from .base import CollectorBase
from ..data.identifiers import CINA_COUNTRIES, country_iso3

logger = logging.getLogger(__name__)

BASE = "https://unfccc.int"
REGISTRY = f"{BASE}/NDCREG"


class NdcRegistryCollector(CollectorBase):
    source_system = "unfccc.int"
    source_type = "ndc"
    license_str = "Sovereign / UN Open"
    license_attribution = "© Submitting Party / UNFCCC"

    def collect(
        self,
        countries: list[str] | None = None,
        max_per_country: int = 2,
        use_dynamic_fallback: bool = True,
    ) -> list[dict]:
        try:
            resp = self.http.fetch(REGISTRY)
        except Exception as exc:
            logger.error("NDC registry fetch failed: %s", exc)
            return []

        all_links = self._parse_registry(resp.text)
        logger.info("Discovered %d NDC entries (static)", len(all_links))

        if not all_links and use_dynamic_fallback:
            logger.info("NDC registry static yield 0; falling back to Playwright")
            try:
                from .dynamic_browser import DynamicBrowserClient
                browser = DynamicBrowserClient(headless=True)
                anchors = browser.extract_pdf_links(
                    REGISTRY,
                    wait_for_selector="a[href*='/sites/default/files/']",
                    wait_ms_after_load=5000,
                    max_paginate_clicks=20,
                    next_button_selector="a[rel='next'], a.pager__item--next",
                )
                for a in anchors:
                    iso = self._guess_iso3(a.get("text", "")) or self._guess_iso3(a["url"])
                    all_links.append({"url": a["url"], "title": a.get("text"), "iso3": iso})
                logger.info("Dynamic fallback discovered %d NDC PDFs", len(all_links))
            except Exception as exc:
                logger.error("Dynamic fallback failed: %s", exc)

        target_iso3s = None
        if countries:
            target_iso3s = set()
            for c in countries:
                iso = country_iso3(c)
                if iso:
                    target_iso3s.add(iso)
                else:
                    logger.warning("Unknown country: %s", c)

        records = []
        per_country: dict[str, int] = {}
        for entry in all_links:
            iso = entry.get("iso3")
            if target_iso3s and iso and iso not in target_iso3s and iso != "EU":
                continue
            if iso and per_country.get(iso, 0) >= max_per_country:
                continue
            rec = self._download_ndc(entry)
            if rec:
                records.append(rec)
                if iso:
                    per_country[iso] = per_country.get(iso, 0) + 1
        return records

    # ------------------------------------------------------------------
    def _parse_registry(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        entries = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if not href.lower().endswith(".pdf"):
                continue
            if "/sites/default/files/" not in href:
                continue
            full = urljoin(BASE, href)
            title = a.get_text(strip=True)
            iso3 = self._guess_iso3(title) or self._guess_iso3(href)
            entries.append({"url": full, "title": title, "iso3": iso3})
        return entries

    @staticmethod
    def _guess_iso3(text: str) -> str | None:
        if not text:
            return None
        # quick heuristics: look for country name match in NDC title
        for iso3, meta in CINA_COUNTRIES.items():
            n = meta["name"].lower()
            if n in text.lower() or iso3.lower() in text.lower():
                return iso3
        return None

    def _download_ndc(self, entry: dict) -> dict | None:
        url = entry["url"]
        iso = entry.get("iso3") or "UNK"
        # extract YYYY-MM from URL
        m = re.search(r"/(\d{4}-\d{2})/", url)
        ym = m.group(1) if m else "unknown"
        slug = re.sub(r"[^A-Za-z0-9]+", "_", Path(urlparse(url).path).stem).strip("_")
        local = self.out_dir / iso / f"{iso}_{ym}_{slug}.pdf"
        try:
            dl = self.http.download(url, local)
        except Exception as exc:
            logger.warning("NDC download failed for %s: %s", url, exc)
            return None
        return self.write_meta(
            local_path=local,
            url=url,
            sha256=dl["sha256"],
            size_bytes=dl["size_bytes"],
            extra={
                "iso3": iso,
                "submission_year_month": ym,
                "title": entry.get("title"),
                "topic_tags_initial": ["NDC"],
                "country_authors_initial": [iso],
            },
        )
