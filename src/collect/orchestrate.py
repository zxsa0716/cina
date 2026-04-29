"""Unified collection orchestrator.

Usage:
    python -m src.collect.orchestrate --sources unfccc,enb,ndc,cop30,castro,ipcc \
        --topic adaptation --event cop30 --countries Brazil,EU,India

Or run individual stages:
    python -m src.collect.orchestrate --sources castro
    python -m src.collect.orchestrate --sources unfccc --topic adaptation --max 20
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from .brazilian_gov import BrazilianGovCollector
from .castro_2025 import Castro2025Collector
from .cop30_official import Cop30OfficialCollector
from .curated_cop30 import CuratedCop30Collector
from .curated_historical_chair import HistoricalChairCollector
from .curated_round3 import CuratedRound3Collector
from .curated_round4 import CuratedRound4Collector
from .curated_round5 import CuratedRound5Collector
from .curated_round6 import CuratedRound6Collector
from .curated_tier4 import CuratedTier4Collector
from .curated_tier4b import CuratedTier4bCollector
from .curated_round7 import CuratedRound7Collector
from .curated_round8 import CuratedRound8Collector
from .enb_curated import EnbCuratedCollector
from .http_client import CinaHttpClient
from .iisd_enb import IisdEnbCollector
from .ipcc_ar6 import IpccAr6Collector
from .korean_gov import KoreanGovCollector
from .manifest import coverage_summary, write_summary
from .ndc_registry import NdcRegistryCollector
from .unfccc_submissions import UnfcccSubmissionsCollector

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("cina.collect")

ROOT = Path(__file__).resolve().parent.parent.parent
RAW_BASE = ROOT / "data" / "raw"
RUNS_DIR = ROOT / "data" / "runs"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="CINA data collection orchestrator")
    ap.add_argument(
        "--sources",
        default="cop30,castro,ipcc",
        help="comma-separated: unfccc,enb,ndc,cop30,castro,ipcc",
    )
    ap.add_argument("--topic", default="adaptation")
    ap.add_argument("--event", default="cop30")
    ap.add_argument(
        "--countries",
        default="Brazil,European Union,United States,China,India,South Africa,Saudi Arabia",
    )
    ap.add_argument("--max", type=int, default=20, help="max docs per source")
    ap.add_argument("--no-robots", action="store_true", help="skip robots.txt check")
    ap.add_argument("--dry-run", action="store_true")
    return ap.parse_args(argv)


def run(args: argparse.Namespace) -> dict:
    started = datetime.now(timezone.utc)
    run_id = started.strftime("%Y%m%dT%H%M%SZ")
    run_dir = RUNS_DIR / f"collect_{run_id}"
    run_dir.mkdir(parents=True, exist_ok=True)

    http = CinaHttpClient(respect_robots=not args.no_robots)
    sources = [s.strip().lower() for s in args.sources.split(",") if s.strip()]
    countries = [c.strip() for c in args.countries.split(",") if c.strip()]

    summary: dict[str, dict] = {}

    if args.dry_run:
        logger.info("[DRY RUN] sources=%s; topic=%s; event=%s; countries=%s; max=%s",
                    sources, args.topic, args.event, countries, args.max)
        return {"dry_run": True, "sources": sources}

    if "cop30" in sources:
        c = Cop30OfficialCollector(out_dir=RAW_BASE / "cop30_official", http=http)
        recs = c.collect(max_documents=args.max)
        summary["cop30"] = {"count": len(recs)}

    if "castro" in sources:
        c = Castro2025Collector(out_dir=RAW_BASE / "castro_2025", http=http)
        recs = c.collect()
        summary["castro"] = {"count": len(recs)}

    if "ipcc" in sources:
        c = IpccAr6Collector(out_dir=RAW_BASE / "ipcc_ar6" / "wg2", http=http)
        recs = c.collect()
        summary["ipcc"] = {"count": len(recs)}

    if "unfccc" in sources:
        c = UnfcccSubmissionsCollector(
            out_dir=RAW_BASE / "unfccc_submissions" / args.event,
            http=http,
        )
        recs = c.collect(topic=args.topic, max_documents=args.max)
        summary["unfccc"] = {"count": len(recs)}

    if "enb" in sources:
        c = IisdEnbCollector(
            out_dir=RAW_BASE / "enb_summaries" / args.event,
            http=http,
        )
        recs = c.collect(event=args.event, max_documents=args.max)
        summary["enb"] = {"count": len(recs)}

    if "ndc" in sources:
        c = NdcRegistryCollector(out_dir=RAW_BASE / "ndcs", http=http)
        recs = c.collect(countries=countries, max_per_country=2)
        summary["ndc"] = {"count": len(recs)}

    if "curated" in sources:
        c = CuratedCop30Collector(
            out_dir=RAW_BASE / "unfccc_submissions" / "cop30_curated", http=http
        )
        recs = c.collect()
        summary["curated"] = {"count": len(recs)}

    if "enb_curated" in sources:
        c = EnbCuratedCollector(
            out_dir=RAW_BASE / "enb_summaries" / "cop30", http=http
        )
        recs = c.collect(max_total=args.max if args.max else 50)
        summary["enb_curated"] = {"count": len(recs)}

    if "korean" in sources:
        c = KoreanGovCollector(out_dir=RAW_BASE / "korean_gov", http=http)
        recs = c.collect(max_total=args.max if args.max else 30)
        summary["korean"] = {"count": len(recs)}

    if "brazilian" in sources:
        c = BrazilianGovCollector(out_dir=RAW_BASE / "brazilian_gov", http=http)
        recs = c.collect(max_total=args.max if args.max else 30)
        summary["brazilian"] = {"count": len(recs)}

    if "round3" in sources:
        c = CuratedRound3Collector(out_dir=RAW_BASE / "round3", http=http)
        recs = c.collect()
        summary["round3"] = {"count": len(recs)}

    if "round4" in sources:
        c = CuratedRound4Collector(out_dir=RAW_BASE / "round4", http=http)
        recs = c.collect()
        summary["round4"] = {"count": len(recs)}

    if "round5" in sources:
        c = CuratedRound5Collector(out_dir=RAW_BASE / "round5", http=http)
        recs = c.collect()
        summary["round5"] = {"count": len(recs)}

    if "historical_chair" in sources:
        c = HistoricalChairCollector(
            out_dir=RAW_BASE / "historical_chair", http=http
        )
        recs = c.collect()
        summary["historical_chair"] = {"count": len(recs)}

    if "round6" in sources:
        c = CuratedRound6Collector(out_dir=RAW_BASE / "round5", http=http)
        recs = c.collect()
        summary["round6"] = {"count": len(recs)}

    if "tier4" in sources:
        c = CuratedTier4Collector(out_dir=RAW_BASE / "tier4", http=http)
        recs = c.collect()
        summary["tier4"] = {"count": len(recs)}

    if "tier4b" in sources:
        c = CuratedTier4bCollector(out_dir=RAW_BASE / "tier4b", http=http)
        recs = c.collect()
        summary["tier4b"] = {"count": len(recs)}

    if "round7" in sources:
        c = CuratedRound7Collector(out_dir=RAW_BASE / "round7", http=http)
        recs = c.collect()
        summary["round7"] = {"count": len(recs)}

    if "round8" in sources:
        c = CuratedRound8Collector(out_dir=RAW_BASE / "round8", http=http)
        recs = c.collect()
        summary["round8"] = {"count": len(recs)}

    write_summary()
    cov = coverage_summary()
    summary["_coverage"] = cov

    elapsed = (datetime.now(timezone.utc) - started).total_seconds()
    summary["_meta"] = {
        "run_id": run_id,
        "started_at": started.isoformat(),
        "elapsed_sec": round(elapsed, 2),
        "args": vars(args),
    }

    out = run_dir / "summary.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("Run summary written: %s (elapsed=%.1fs)", out, elapsed)
    return summary


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        summary = run(args)
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        return 130
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
