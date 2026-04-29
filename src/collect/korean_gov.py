"""Korean government documents collector — 외교부 + 환경부 + KEI/KIEP.

HEEDO-1 scope expansion: 한국 외교부·환경부 follow-up 문서 수집.
focal country는 브라질이지만, CINA 헌법 § "수업·논문 투트랙" 에서 한국 정책
실무 적용성을 검증하기 위해 한국 측 자료도 동등 수집한다.
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

# 알려진 핵심 페이지 (WebSearch + 도메인 지식 기반)
SEED_PAGES = [
    # 외교부 COP30 폐막 보도자료
    "https://www.mofa.go.kr/www/brd/m_4080/view.do?seq=376685",
    # 외교부 COP26 보도 (역사 비교용)
    "https://www.mofa.go.kr/www/brd/m_4080/view.do?seq=371781",
    # 외교부 기후환경과학외교국 안내
    "https://www.mofa.go.kr/www/wpge/m_3990/contents.do",
    # 환경부 기후 정책 일반
    "https://www.me.go.kr/home/web/policy_data/policySub.do?menuId=10262",
]


class KoreanGovCollector(CollectorBase):
    source_system = "korean_gov"
    source_type = "korean_gov"
    license_str = "Korean Government Open Data / 공공누리 1유형 추정"
    license_attribution = "© Republic of Korea Government (MOFA / Ministry of Environment)"

    def collect(
        self,
        seed_pages: list[str] | None = None,
        max_pdf_per_page: int = 5,
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

            # 1. HTML 자체 저장 (보도자료 본문)
            html_rec = self._save_html(seed, html)
            if html_rec:
                records.append(html_rec)

            # 2. 페이지에서 PDF 링크 발견
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
        return records

    # ------------------------------------------------------------------
    def _discover_pdfs(self, html: str, base_url: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        out = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.lower().endswith(".pdf") or "filedown" in href.lower() or "fileDownload" in href:
                full = urljoin(base_url, href)
                out.append(full)
        # dedupe preserving order
        seen = set()
        unique = []
        for u in out:
            if u not in seen:
                seen.add(u)
                unique.append(u)
        return unique

    def _save_html(self, url: str, html: str) -> dict | None:
        domain = urlparse(url).netloc.replace(".", "_")
        slug_raw = re.sub(r"[^A-Za-z0-9]+", "_", url.split("?")[-1] or domain).strip("_")[:80]
        slug = f"{domain}_{slug_raw}"
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
                "country_authors_initial": ["KOR"],
                "language": "ko",
                "topic_tags_initial": ["climate_diplomacy", "korea_policy"],
            },
        )

    def _download_pdf(self, url: str, source_seed: str) -> dict | None:
        slug = re.sub(r"[^A-Za-z0-9]+", "_", Path(urlparse(url).path).stem).strip("_")[:80]
        local = self.out_dir / f"{slug}.pdf"
        try:
            dl = self.http.download(url, local)
        except Exception as exc:
            logger.warning("Korean gov PDF download failed: %s — %s", url, exc)
            return None
        return self.write_meta(
            local_path=local,
            url=url,
            sha256=dl["sha256"],
            size_bytes=dl["size_bytes"],
            extra={
                "file_format": "pdf",
                "country_authors_initial": ["KOR"],
                "topic_tags_initial": ["climate_diplomacy", "korea_policy"],
                "source_page": source_seed,
            },
        )
