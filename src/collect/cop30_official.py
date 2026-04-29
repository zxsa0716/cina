"""COP30 Brazilian Presidency Official Site collector.

Source: https://cop30.br/en
Targets: Belém Package press release, GGA decisions, presidency letters.
"""
from __future__ import annotations

import logging
import re
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base import CollectorBase

logger = logging.getLogger(__name__)

BASE = "https://cop30.br"
SEED_URLS = [
    f"{BASE}/en/news-about-cop30",
    f"{BASE}/en/news-about-cop30/cop30-approves-belem-package1",
    f"{BASE}/en/cop30-presidency",
]


class Cop30OfficialCollector(CollectorBase):
    source_system = "cop30.br"
    source_type = "cop30_official"
    license_str = "Public statement (Brazilian Presidency)"
    license_attribution = "© COP30 / Brazilian Government"

    def collect(self, max_documents: int = 50) -> list[dict]:
        records = []
        seen = set()
        for seed in SEED_URLS:
            try:
                resp = self.http.fetch(seed)
            except Exception as exc:
                logger.warning("Seed fetch failed: %s — %s", seed, exc)
                continue
            # Save the HTML page itself
            rec_html = self._save_html(seed, resp.text)
            if rec_html:
                records.append(rec_html)

            # Discover linked PDFs (e.g., decisions, position letters)
            for url in self._discover_pdfs(resp.text):
                if url in seen:
                    continue
                seen.add(url)
                if len(records) >= max_documents:
                    break
                rec = self._download_pdf(url)
                if rec:
                    records.append(rec)
        return records

    # ------------------------------------------------------------------
    def _discover_pdfs(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        return sorted(
            urljoin(BASE, a["href"])
            for a in soup.find_all("a", href=True)
            if a["href"].lower().endswith(".pdf")
        )

    def _save_html(self, url: str, html: str) -> dict | None:
        slug = re.sub(r"[^A-Za-z0-9]+", "_", url.replace(BASE, "")).strip("_")[:80] or "index"
        local = self.out_dir / f"{slug}.html"
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_text(html, encoding="utf-8")
        import hashlib
        sha = hashlib.sha256(html.encode()).hexdigest()
        return self.write_meta(
            local_path=local,
            url=url,
            sha256=sha,
            size_bytes=len(html),
            extra={"file_format": "html", "session": "COP30"},
        )

    def _download_pdf(self, url: str) -> dict | None:
        slug = re.sub(r"[^A-Za-z0-9]+", "_", Path(url).stem).strip("_")[:80]
        local = self.out_dir / f"{slug}.pdf"
        try:
            dl = self.http.download(url, local)
        except Exception as exc:
            logger.warning("PDF download failed: %s — %s", url, exc)
            return None
        return self.write_meta(
            local_path=local,
            url=url,
            sha256=dl["sha256"],
            size_bytes=dl["size_bytes"],
            extra={"file_format": "pdf", "session": "COP30"},
        )
