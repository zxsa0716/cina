"""CINA end-to-end pipeline runner.

Usage:
    python -m src.pipeline --country Brazil --cop 30 --sector adaptation \
        --language ko --output deliverables/
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from .config import (
    CinaConfig,
    DATA_DIR,
    DEFAULT_COUNTRIES,
    DELIVERABLES_DIR,
    ISSUE_CODES,
    ISSUE_DESCRIPTIONS,
)


def _log(msg: str) -> None:
    print(f"[CINA {datetime.now(timezone.utc).strftime('%H:%M:%S')}] {msg}")


async def run_stage1(cfg: CinaConfig, raw_dir: Path, out_path: Path) -> list[dict]:
    """Stage 1: extract stances from documents."""
    from anthropic import AsyncAnthropic

    from .stage1_extract.extract import extract_stance, load_calibrator

    client = AsyncAnthropic()
    calibrator = load_calibrator(cfg.stage1.calibration_path)
    stances_out: list[dict] = []

    docs = list(raw_dir.glob("**/*.json"))
    _log(f"Stage 1: {len(docs)} documents, {len(cfg.countries)} countries, {len(cfg.issues)} issues")

    for doc_path in docs:
        doc = json.loads(doc_path.read_text(encoding="utf-8"))
        text = doc.get("full_text", "")
        if len(text) < 100:
            continue
        for country in cfg.countries:
            if country not in doc.get("authors", []) and country != "EU":
                continue
            for issue in cfg.issues:
                stance = await extract_stance(
                    client=client,
                    cfg=cfg.stage1,
                    country=country,
                    issue=issue,
                    issue_description=ISSUE_DESCRIPTIONS[issue],
                    document_text=text,
                    doc_id=doc["doc_id"],
                    cop_session=doc["cop_session"],
                    date_context=doc["date"],
                    calibrator=calibrator,
                )
                stances_out.append(stance.model_dump(mode="json"))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for s in stances_out:
            f.write(json.dumps(s, ensure_ascii=False, default=str) + "\n")
    _log(f"Stage 1 done: {len(stances_out)} stance records → {out_path}")
    return stances_out


def run_stage2(cfg: CinaConfig, stances: list[dict], out_path: Path) -> dict:
    """Stage 2: graph analysis. Simplified stub version using per-issue analysis."""
    import numpy as np

    from .stage2_graph.analyze import (
        analyze_issue,
        build_flex_matrix,
        detect_linkage_hyperedges,
        epistemic_divergence_score,
    )

    issue_analyses = {}

    for issue in cfg.issues:
        issue_stances = [s for s in stances if s["issue"] == issue]
        if not issue_stances:
            continue
        country_labels = sorted({s["country"] for s in issue_stances})
        # Pseudo-embedding from stance score + demands count
        emb = np.zeros((len(country_labels), 4))
        for i, c in enumerate(country_labels):
            rec = next(s for s in issue_stances if s["country"] == c)
            emb[i, 0] = rec["stance_score_calibrated"]
            emb[i, 1] = len(rec.get("key_demands", []))
            emb[i, 2] = len(rec.get("red_lines", []))
            emb[i, 3] = len(rec.get("flexibility_signals", []))
        # Pseudo-adjacency from stance similarity
        adj = np.zeros((len(country_labels), len(country_labels)))
        for i in range(len(country_labels)):
            for j in range(len(country_labels)):
                if i != j:
                    adj[i, j] = 1.0 - abs(emb[i, 0] - emb[j, 0]) / 2.0

        ia = analyze_issue(
            issue_code=issue,
            country_embeddings=emb,
            country_labels=country_labels,
            adjacency=adj,
            knn_k=min(cfg.stage2.knn_k, len(country_labels) - 1),
            leiden_gamma=cfg.stage2.leiden_gamma,
        )
        issue_analyses[issue] = ia.model_dump()

    # Cross-issue hyperedges
    country_labels = sorted({s["country"] for s in stances})
    F = build_flex_matrix(stances, country_labels, cfg.issues)
    hyperedges = detect_linkage_hyperedges(
        F, country_labels, cfg.issues,
        min_support=cfg.stage2.hypergraph_min_support,
        min_issues=cfg.stage2.hypergraph_min_issues,
        max_issues=cfg.stage2.hypergraph_max_issues,
    )

    # Epistemic divergence per issue
    divergence = {}
    for issue in cfg.issues:
        issue_stances = [s for s in stances if s["issue"] == issue]
        if issue_stances:
            divergence[issue] = epistemic_divergence_score(issue_stances).model_dump()

    analysis = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model_version": "CINA-stub-v2.0",
        "focal_country": cfg.stage3.focal_country,
        "issue_analyses": issue_analyses,
        "cross_issue_hyperedges": [h.model_dump() for h in hyperedges],
        "epistemic_divergence": divergence,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
    _log(f"Stage 2 done: {len(issue_analyses)} issue analyses, {len(hyperedges)} hyperedges → {out_path}")
    return analysis


async def run_stage3(
    cfg: CinaConfig,
    analysis: dict,
    stances: list[dict],
    out_path: Path,
) -> None:
    from anthropic import AsyncAnthropic

    from .stage3_brief.compose import (
        SECTION_TITLES_EN,
        SECTION_TITLES_KO,
        compile_briefing,
        generate_section,
        section_inputs,
        save_briefing,
    )

    client = AsyncAnthropic()
    titles = SECTION_TITLES_KO if cfg.stage3.language == "ko" else SECTION_TITLES_EN
    inputs = section_inputs(analysis, stances, cfg.stage3.focal_country)

    all_evidence = [q for s in stances for q in s.get("evidence_quotes", [])]

    sections = {}
    for sid, title in titles.items():
        text = await generate_section(
            client=client,
            cfg=cfg.stage3,
            section_id=sid,
            section_title=title,
            analysis_subset=inputs[sid],
            evidence_quotes=all_evidence[:50],
        )
        sections[sid] = text
        _log(f"Stage 3 section {sid} generated ({len(text)} chars)")

    exec_summary = "(CINA 실행 완료. 상세는 §1-§7 참조.)"
    briefing = compile_briefing(
        sections,
        exec_summary,
        cfg.stage3.focal_country,
        cfg.stage3.cop,
        cfg.stage3.sector,
        cfg.stage3.language,
    )
    save_briefing(briefing, out_path)
    _log(f"Stage 3 done: briefing → {out_path}")


async def main_async(args) -> int:
    cfg = CinaConfig()
    cfg.stage3.focal_country = args.country
    cfg.stage3.cop = args.cop
    cfg.stage3.sector = args.sector
    cfg.stage3.language = args.language

    raw_dir = Path(args.raw_dir)
    stages_to_run = args.stages.split(",")

    stances_path = DATA_DIR / "processed" / "stances.jsonl"
    analysis_path = DATA_DIR / "processed" / "graph_analysis.json"
    briefing_path = Path(args.output) / (
        "ministerial_briefing.md" if cfg.stage3.language == "ko" else "ministerial_briefing_en.md"
    )

    stances: list[dict] = []
    analysis: dict = {}

    if "1" in stages_to_run:
        if not os.getenv("ANTHROPIC_API_KEY"):
            _log("WARN: ANTHROPIC_API_KEY not set. Stage 1 will fail.")
        stances = await run_stage1(cfg, raw_dir, stances_path)
    else:
        if stances_path.exists():
            with open(stances_path, encoding="utf-8") as f:
                stances = [json.loads(line) for line in f if line.strip()]

    if "2" in stages_to_run:
        analysis = run_stage2(cfg, stances, analysis_path)
    else:
        if analysis_path.exists():
            analysis = json.loads(analysis_path.read_text(encoding="utf-8"))

    if "3" in stages_to_run:
        if not os.getenv("ANTHROPIC_API_KEY"):
            _log("WARN: ANTHROPIC_API_KEY not set. Stage 3 will fail.")
            return 1
        await run_stage3(cfg, analysis, stances, briefing_path)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="CINA end-to-end pipeline")
    ap.add_argument("--country", default="Brazil")
    ap.add_argument("--cop", type=int, default=30)
    ap.add_argument("--sector", default="adaptation")
    ap.add_argument("--language", choices=["ko", "en"], default="ko")
    ap.add_argument("--raw-dir", default="data/raw/unfccc_submissions/cop30/")
    ap.add_argument("--output", default="deliverables/")
    ap.add_argument(
        "--stages",
        default="1,2,3",
        help="Comma-separated stages to run, e.g. '2,3' to skip extraction",
    )
    args = ap.parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
