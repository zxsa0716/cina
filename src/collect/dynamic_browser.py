"""Playwright-based dynamic page collector for sites with JS-rendered listings.

UNFCCC documents portal, NDC Registry, and ENB event pages all render document
links client-side. BeautifulSoup-only collectors return zero hits.

Usage: instantiate `DynamicBrowserClient` and call `extract_links(url, selectors)`.

Install:
    pip install playwright
    playwright install chromium

Note: Chromium binary ~200 MB. Use headless mode by default.
"""
from __future__ import annotations

import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

logger = logging.getLogger(__name__)


class DynamicBrowserClient:
    """Thin wrapper over Playwright sync API.

    Designed to drop into existing collectors when their static fetch yields
    no anchors. Lazy-imports playwright so the static stack still works without
    the dependency installed.
    """

    def __init__(
        self,
        headless: bool = True,
        timeout_ms: int = 30000,
        user_agent: str | None = None,
    ) -> None:
        try:
            from playwright.sync_api import sync_playwright  # noqa: F401
        except ImportError as exc:
            raise RuntimeError(
                "playwright not installed. Run: pip install playwright && "
                "playwright install chromium"
            ) from exc
        self.headless = headless
        self.timeout_ms = timeout_ms
        self.user_agent = user_agent or (
            "CINA-Research/2.0 (academic; "
            "Climate Issue-Network Analysis; "
            "contact: zxsa0716@kookmin.ac.kr)"
        )

    @contextmanager
    def _page(self) -> Iterator:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(user_agent=self.user_agent)
            page = context.new_page()
            page.set_default_timeout(self.timeout_ms)
            try:
                yield page
            finally:
                context.close()
                browser.close()

    def render_html(
        self,
        url: str,
        wait_for_selector: Optional[str] = None,
        wait_ms_after_load: int = 1500,
    ) -> str:
        """Return fully-rendered HTML."""
        with self._page() as page:
            page.goto(url, wait_until="domcontentloaded")
            if wait_for_selector:
                try:
                    page.wait_for_selector(wait_for_selector, timeout=self.timeout_ms)
                except Exception as exc:
                    logger.warning("Selector wait failed: %s — %s", wait_for_selector, exc)
            page.wait_for_timeout(wait_ms_after_load)
            return page.content()

    def extract_pdf_links(
        self,
        url: str,
        wait_for_selector: Optional[str] = None,
        wait_ms_after_load: int = 1500,
        max_paginate_clicks: int = 0,
        next_button_selector: Optional[str] = None,
    ) -> list[dict]:
        """Render page, extract PDF anchor metadata. Optionally click pagination."""
        from bs4 import BeautifulSoup

        anchors: list[dict] = []
        with self._page() as page:
            page.goto(url, wait_until="domcontentloaded")
            if wait_for_selector:
                try:
                    page.wait_for_selector(wait_for_selector, timeout=self.timeout_ms)
                except Exception:
                    pass
            page.wait_for_timeout(wait_ms_after_load)

            for click_idx in range(max_paginate_clicks + 1):
                html = page.content()
                soup = BeautifulSoup(html, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if href.lower().endswith(".pdf"):
                        anchors.append(
                            {
                                "url": href if href.startswith("http")
                                else f"https:{href}" if href.startswith("//")
                                else href,
                                "text": a.get_text(strip=True),
                            }
                        )
                if click_idx == max_paginate_clicks or not next_button_selector:
                    break
                try:
                    page.click(next_button_selector, timeout=5000)
                    page.wait_for_timeout(wait_ms_after_load)
                except Exception:
                    break

        # dedupe preserving order
        seen = set()
        unique = []
        for a in anchors:
            key = a["url"]
            if key not in seen:
                seen.add(key)
                unique.append(a)
        return unique
