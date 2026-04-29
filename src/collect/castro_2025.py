"""Castro et al. 2025 ENB dataset collector.

Source: https://www.nature.com/articles/s41597-025-06262-4
Castro, P., Kristof, V., Kammerer, M., & Cogne, T. (2025).
Participation, Cooperation and Conflict in UN Climate Negotiations.
Nature Scientific Data.

Strategy:
1. Fetch article HTML.
2. Discover supplementary data link (Figshare/Zenodo).
3. Download CSV/JSON files.

Note: Nature articles often link supplementary data via static-content.springer.com.
We respect ScienceDirect/Springer terms — fetch only declared supplements.
"""
from __future__ import annotations

import logging
import re
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base import CollectorBase

logger = logging.getLogger(__name__)

ARTICLE_URL = "https://www.nature.com/articles/s41597-025-06262-4"


class Castro2025Collector(CollectorBase):
    source_system = "nature.com"
    source_type = "castro_2025"
    license_str = "CC BY 4.0 (Nature Scientific Data, verify on landing)"
    license_attribution = "Castro et al. 2025, Nature Sci Data, DOI:10.1038/s41597-025-06262-4"

    def collect(self) -> list[dict]:
        records = []
        # 1. Save the article HTML for citation reproducibility
        try:
            resp = self.http.fetch(ARTICLE_URL)
        except Exception as exc:
            logger.error("Article fetch failed: %s", exc)
            return records

        html_local = self.out_dir / "castro_2025_article.html"
        html_local.write_text(resp.text, encoding="utf-8")
        import hashlib
        sha = hashlib.sha256(resp.text.encode()).hexdigest()
        records.append(self.write_meta(
            local_path=html_local,
            url=ARTICLE_URL,
            sha256=sha,
            size_bytes=len(resp.text),
            extra={"format": "html", "role": "article_landing"},
        ))

        # 2. Discover supplementary data URLs
        soup = BeautifulSoup(resp.text, "html.parser")
        data_urls = self._discover_data_urls(soup)
        logger.info("Discovered %d candidate data URLs", len(data_urls))

        for url in data_urls:
            rec = self._download_supplement(url)
            if rec:
                records.append(rec)

        return records

    def _discover_data_urls(self, soup: BeautifulSoup) -> list[str]:
        candidates = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            href_low = href.lower()
            if any(host in href_low for host in [
                "figshare.com", "zenodo.org",
                "static-content.springer.com",
                "/MediaObjects/",
            ]):
                full = href if href.startswith("http") else urljoin("https://www.nature.com", href)
                candidates.append(full)
        # dedupe preserving order
        seen = set()
        out = []
        for u in candidates:
            if u not in seen:
                seen.add(u)
                out.append(u)
        return out

    def _download_supplement(self, url: str) -> dict | None:
        slug = re.sub(r"[^A-Za-z0-9]+", "_", Path(url).stem).strip("_")[:80] or "supplement"
        ext_match = re.search(r"\.(csv|json|xlsx|zip|pdf|tar\.gz)(?:\?|$)", url.lower())
        ext = ext_match.group(0).split("?")[0] if ext_match else ""
        local = self.out_dir / f"{slug}{ext}"
        try:
            dl = self.http.download(url, local)
        except Exception as exc:
            logger.warning("Supplement download failed: %s — %s", url, exc)
            return None
        return self.write_meta(
            local_path=local,
            url=url,
            sha256=dl["sha256"],
            size_bytes=dl["size_bytes"],
            extra={"role": "supplementary_data", "format": ext.lstrip(".")},
        )
