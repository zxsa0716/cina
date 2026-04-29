"""Base collector class shared by all source-specific collectors."""
from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .http_client import CinaHttpClient
from .manifest import append_record, doc_id_from_url, now_iso

logger = logging.getLogger(__name__)


class CollectorBase(ABC):
    """Base class for all CINA data collectors."""

    source_system: str = ""        # e.g., "unfccc.int"
    source_type: str = ""           # e.g., "unfccc_submission"
    license_str: str = ""           # license name
    license_attribution: str = ""

    def __init__(
        self,
        out_dir: Path,
        http: CinaHttpClient | None = None,
    ) -> None:
        self.out_dir = Path(out_dir)
        self.http = http or CinaHttpClient()
        self.out_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    @abstractmethod
    def collect(self, **kwargs) -> list[dict]:
        """Collect documents per the source's pattern. Returns manifest entries."""
        ...

    # ------------------------------------------------------------------
    def write_meta(
        self,
        local_path: Path,
        url: str,
        sha256: str,
        size_bytes: int,
        extra: dict | None = None,
    ) -> dict:
        """Write `<file>.meta.json` and return the manifest record."""
        record = {
            "doc_id": doc_id_from_url(self.source_type, url),
            "source_system": self.source_system,
            "source_type": self.source_type,
            "source_url": url,
            "retrieved_at": now_iso(),
            "license": self.license_str,
            "license_attribution": self.license_attribution,
            "sha256": sha256,
            "filesize_bytes": size_bytes,
            "raw_file_path": str(local_path),
            "extraction_status": "pending",
            "verification_status": "pending",
        }
        if extra:
            record.update(extra)

        meta_path = local_path.with_suffix(local_path.suffix + ".meta.json")
        meta_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        append_record(record)
        return record
