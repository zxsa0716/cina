"""Shared HTTP client with rate limiting, retries, robots.txt awareness."""
from __future__ import annotations

import hashlib
import logging
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)

USER_AGENT = (
    "CINA-Research/2.0 "
    "(academic; Climate Issue-Network Analysis; "
    "contact: zxsa0716@kookmin.ac.kr)"
)


class RateLimiter:
    """Per-domain min interval rate limiter."""

    def __init__(self, default_interval_sec: float = 1.0) -> None:
        self.default = default_interval_sec
        self.last_request: dict[str, float] = {}
        self.overrides: dict[str, float] = {
            "unfccc.int": 1.0,
            "enb.iisd.org": 1.5,
            "www.iisd.org": 1.5,
            "cop30.br": 1.0,
            "www.ipcc.ch": 1.0,
            "www.nature.com": 2.0,
            "static-content.springer.com": 1.0,
        }

    def wait(self, domain: str) -> None:
        interval = self.overrides.get(domain, self.default)
        last = self.last_request.get(domain, 0.0)
        elapsed = time.time() - last
        if elapsed < interval:
            time.sleep(interval - elapsed)
        self.last_request[domain] = time.time()


class CinaHttpClient:
    """HTTP client with politeness, caching, and integrity checks."""

    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        respect_robots: bool = True,
        rate_limiter: Optional[RateLimiter] = None,
    ) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.cache_dir = cache_dir
        self.respect_robots = respect_robots
        self.rate_limiter = rate_limiter or RateLimiter()
        self._robots_cache: dict[str, RobotFileParser] = {}

    def _get_robots(self, domain: str) -> RobotFileParser:
        if domain in self._robots_cache:
            return self._robots_cache[domain]
        rp = RobotFileParser()
        try:
            rp.set_url(f"https://{domain}/robots.txt")
            rp.read()
        except Exception as exc:
            logger.warning("Failed to read robots.txt for %s: %s", domain, exc)
        self._robots_cache[domain] = rp
        return rp

    def can_fetch(self, url: str) -> bool:
        if not self.respect_robots:
            return True
        domain = urlparse(url).netloc
        rp = self._get_robots(domain)
        try:
            return rp.can_fetch(USER_AGENT, url)
        except Exception:
            return True

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=2, max=30),
        retry=retry_if_exception_type((requests.RequestException, requests.HTTPError)),
        reraise=True,
    )
    def fetch(self, url: str, timeout: int = 30) -> requests.Response:
        if not self.can_fetch(url):
            raise PermissionError(f"robots.txt disallows {url}")
        domain = urlparse(url).netloc
        self.rate_limiter.wait(domain)
        logger.info("GET %s", url)
        resp = self.session.get(url, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        return resp

    def download(self, url: str, dest: Path, overwrite: bool = False) -> dict:
        """Download to disk, return manifest dict (sha256, size, etc.)."""
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and not overwrite:
            logger.info("Cached: %s", dest)
            with open(dest, "rb") as f:
                content = f.read()
        else:
            resp = self.fetch(url)
            content = resp.content
            dest.write_bytes(content)
        return {
            "path": str(dest),
            "sha256": hashlib.sha256(content).hexdigest(),
            "size_bytes": len(content),
            "url": url,
        }
