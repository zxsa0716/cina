"""CLI: Collect UNFCCC submissions, NDCs, ENB summaries.

Usage:
    python -m src.collect.run --source unfccc --cop 30 --sector adaptation \
        --countries Brazil,EU,India --output data/raw/
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def collect_unfccc_stub(
    cop: int,
    sector: str,
    countries: list[str],
    output_dir: Path,
    rate_limit_sec: float = 1.0,
) -> list[dict]:
    """Stub: UNFCCC 공식 submission portal 수집.

    실제 구현 시: requests로 https://unfccc.int/documents 쿼리 + PDF 다운로드.
    현재는 스캐폴드용 placeholder.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for country in countries:
        slug = country.lower().replace(" ", "_")
        doc_id = f"UNFCCC-STUB-COP{cop}-{slug}-adaptation"
        doc = {
            "doc_id": doc_id,
            "source": "unfccc_submission",
            "cop_session": f"COP{cop}",
            "subsidiary_body": "SBI",
            "document_type": "submission",
            "date": f"2025-06-01",
            "authors": [country],
            "topics": [sector],
            "language": "en",
            "full_text": f"[STUB] {country}'s submission on {sector} for COP{cop}.",
            "paragraphs": [],
            "url": None,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "sha256": sha256(doc_id),
        }
        manifest.append(doc)
        (output_dir / f"{doc_id}.json").write_text(
            json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        time.sleep(rate_limit_sec)
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser(description="CINA data collection")
    ap.add_argument("--source", choices=["unfccc", "ndc", "enb", "all"], default="unfccc")
    ap.add_argument("--cop", type=int, default=30)
    ap.add_argument("--sector", default="adaptation")
    ap.add_argument(
        "--countries",
        default="Brazil,EU,United States,China,India",
        help="Comma-separated country names.",
    )
    ap.add_argument("--output", default="data/raw/unfccc_submissions/cop30/")
    ap.add_argument("--rate-limit", type=float, default=1.0)
    args = ap.parse_args()

    output_dir = Path(args.output)
    countries = [c.strip() for c in args.countries.split(",") if c.strip()]

    if args.source in ("unfccc", "all"):
        print(f"Collecting UNFCCC submissions for COP{args.cop}, {args.sector}...")
        manifest = collect_unfccc_stub(
            args.cop, args.sector, countries, output_dir, args.rate_limit
        )
        print(f"Collected {len(manifest)} documents.")

    # TODO: implement NDC, ENB collectors
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
