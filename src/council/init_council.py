"""Initialize CINA council: create state.json and round_0 scaffold.

Usage:
    python -m src.council.init_council
"""
from __future__ import annotations

import argparse

from . import state_manager as sm

DEFAULT_HEEDO_DIRECTIVES = [
    "CINA must be publishable-grade (target: Global Environmental Change or NeurIPS Climate Change AI Workshop 2026).",
    "Retrospective validation on COP30 Belém Adaptation Indicators is the primary empirical test.",
    "Maintain both course-submission track (Korean ministerial briefing) and paper-draft track (English methodology).",
    "LLM-GNN-LLM pipeline novelty must stay intact across all rounds.",
    "All claims must be evidence-traceable (text quote + structural fact) — no hallucination tolerated.",
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Overwrite existing state.json")
    args = ap.parse_args()

    if sm.STATE_PATH.exists() and not args.force:
        print(f"state.json already exists at {sm.STATE_PATH}. Use --force to reinit.")
        return 1

    state = sm.init(heedo_directives=DEFAULT_HEEDO_DIRECTIVES)
    print(f"Initialized council state at {sm.STATE_PATH}")
    print(f"Round 0 baseline set. Run `python -m src.council.run_round --round next` to start Round 1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
