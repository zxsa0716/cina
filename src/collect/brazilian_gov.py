"""Brazilian government documents collector — gov.br/planalto + gov.br/mma + gov.br/mre.

Brazilian focal country data: official COP30 statements, Ministry of Environment
positions, Itamaraty (foreign ministry) climate diplomacy.
"""
from __future__ import annotations

import hashlib
import logging
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from .base import CollectorBase

logger = logging.getLogger(__name__)

SEED_PAGES = [
    "https://www.gov.br/planalto/en/international-agenda/cop30",
    "https://www.gov.br/planalto/en/latest-news/2025/01/ambassador-andre-correa-do-lago-chosen-as-president-of-cop30",
    "https://www.gov.br/secom/en/latest-news/2024/12/cop30-brazil-works-to-consolidate-diplomatic-leadership-in-climate-agenda",
    "https://www.gov.br/planalto/en/international-agenda/cop30/the-un-validates-brazilian-actions-and-plans-for-cop30",
]


class BrazilianGovCollector(CollectorBase):
    source_system = "gov.br"
    source_type = "brazilian_gov"
    license_str = "Brazilian Government Public Statement"
    license_attribution = "© Federative Republic of Brazil (Planalto / MMA / MRE)"

    def collect(
        self,
        seed_pages: list[str] | None = None,
        max_pdf_per_page: int = 4,
        max_total: int = 30,
        use_dynamic_fallback: bool = True,
    ) -> list[dict]:
        seeds = seed_pages or SEED_PAGES
        records: list[dict] = []

        for seed in seeds:
            if len(records) >= max_total:
                break
            try:
                resp = self.http.fetch(seed)
            except Exception as exc:
                logger.warning("Seed fetch failed: %s — %s", seed, exc)
                continue
            html = resp.text
            html_rec = self._save_html(seed, html)
            if html_rec:
                records.append(html_rec)

            pdfs = self._discover_pdfs(html, seed)
            if not pdfs and use_dynamic_fallback:
                logger.info("No PDFs in static HTML for %s; trying Playwright", seed)
                try:
                    from .dynamic_browser import DynamicBrowserClient
                    browser = DynamicBrowserClient(headless=True)
                    anchors = browser.extract_pdf_links(seed, wait_ms_after_load=3000)
                    pdfs = [a["url"] for a in anchors]
                except Exception as exc:
                    logger.warning("Dynamic fallback failed: %s", exc)

            for url in pdfs[:max_pdf_per_page]:
                if len(records) >= max_total:
                    break
                rec = self._download_pdf(url, seed)
                if rec:
                    records.append(rec)

            # Auto-discover linked Brazilian gov pages for further fetch
            internal = self._discover_internal_links(html, seed)
            for inner in internal[:3]:
                if len(records) >= max_total:
                    break
                try:
                    inner_resp = self.http.fetch(inner)
                except Exception:
                    continue
                inner_html = inner_resp.text
                inner_rec = self._save_html(inner, inner_html)
                if inner_rec:
                    records.append(inner_rec)
        return records

    # ------------------------------------------------------------------
    def _discover_pdfs(self, html: str, base_url: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        out = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.lower().endswith(".pdf"):
                out.append(urljoin(base_url, href))
        seen = set()
        unique = []
        for u in out:
            if u not in seen:
                seen.add(u)
                unique.append(u)
        return unique

    def _discover_internal_links(self, html: str, base_url: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        domain = urlparse(base_url).netloc
        out = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full = urljoin(base_url, href)
            if urlparse(full).netloc != domain:
                continue
            if any(kw in full.lower() for kw in ["cop30", "climate", "adaptation", "ambiental"]):
                out.append(full)
        seen = set()
        unique = []
        for u in out:
            if u not in seen and u != base_url:
                seen.add(u)
                unique.append(u)
        return unique[:5]

    def _save_html(self, url: str, html: str) -> dict | None:
        slug = re.sub(r"[^A-Za-z0-9]+", "_", url.replace("https://www.gov.br/", "")).strip("_")[:80]
        if not slug:
            slug = "gov_br_page"
        local = self.out_dir / f"{slug}.html"
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_text(html, encoding="utf-8")
        sha = hashlib.sha256(html.encode()).hexdigest()
        return self.write_meta(
            local_path=local,
            url=url,
            sha256=sha,
            size_bytes=len(html),
            extra={
                "file_format": "html",
                "country_authors_initial": ["BRA"],
                "language": "en" if "/en/" in url else "pt",
                "session": "COP30",
                "topic_tags_initial": ["adaptation", "brazilian_presidency"],
            },
        )

    def _download_pdf(self, url: str, source_seed: str) -> dict | None:
        slug = re.sub(r"[^A-Za-z0-9]+", "_", Path(urlparse(url).path).stem).strip("_")[:80]
        local = self.out_dir / f"{slug}.pdf"
        try:
            dl = self.http.download(url, local)
        except Exception as exc:
            logger.warning("Brazilian gov PDF download failed: %s — %s", url, exc)
            return None
        return self.write_meta(
            local_path=local,
            url=url,
            sha256=dl["sha256"],
            size_bytes=dl["size_bytes"],
            extra={
                "file_format": "pdf",
                "country_authors_initial": ["BRA"],
                "session": "COP30",
                "topic_tags_initial": ["adaptation", "brazilian_presidency"],
                "source_page": source_seed,
            },
        )
