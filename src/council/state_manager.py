"""Atomic state.json read/write with file lock.

Implements .claude/skills/session-state/SKILL.md contract.
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from filelock import FileLock

from .state_schema import CouncilState, QualityGate, RoundRecord

COUNCIL_DIR = Path(__file__).resolve().parent.parent.parent / "council_sessions"
STATE_PATH = COUNCIL_DIR / "state.json"
LOCK_PATH = COUNCIL_DIR / ".state.lock"
BACKUP_PATH = COUNCIL_DIR / ".state.backup.json"
LEDGER_PATH = COUNCIL_DIR / "LEDGER.md"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read() -> CouncilState:
    with FileLock(str(LOCK_PATH), timeout=10):
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return CouncilState.model_validate(data)


def atomic_write(state: CouncilState) -> None:
    with FileLock(str(LOCK_PATH), timeout=10):
        if STATE_PATH.exists():
            shutil.copy2(STATE_PATH, BACKUP_PATH)
        tmp = STATE_PATH.with_suffix(".tmp")
        tmp.write_text(state.model_dump_json(indent=2), encoding="utf-8")
        tmp.replace(STATE_PATH)


def init(heedo_directives: list[str] | None = None) -> CouncilState:
    gates = {
        g: QualityGate(status="not_started")
        for g in [
            "G1_data_coverage",
            "G2_evidence_grounding",
            "G3_theory_grounding",
            "G4_dual_review",
            "G5_heedo_alignment",
        ]
    }
    state = CouncilState(
        quality_gates=gates,
        next_action="Run /cina-council-round 1",
        heedo_directives=heedo_directives or [],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    COUNCIL_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write(state)
    return state


def create_round_dir(round_n: int) -> Path:
    """Create council_sessions/round_{N}/ with standard subdirectories."""
    root = COUNCIL_DIR / f"round_{round_n}"
    for sub in ["tasks", "data_collection", "refinement", "policy_science", "ir_political", "synthesis"]:
        (root / sub).mkdir(parents=True, exist_ok=True)
    return root


def finalize_round(round_n: int, outcome: str, llm_calls: dict[str, int], cost_usd: float, duration_min: float, notes: str | None = None) -> CouncilState:
    state = read()
    record = RoundRecord(
        round=round_n,
        date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        outcome=outcome,
        llm_calls=llm_calls,
        cost_usd=cost_usd,
        duration_min=duration_min,
        notes=notes,
    )
    state.rounds_completed.append(record)
    state.current_round = round_n
    state.updated_at = datetime.now(timezone.utc)
    atomic_write(state)

    # Append to LEDGER.md
    block = (
        f"\n## Round {round_n} — {record.date}\n\n"
        f"- **Outcome**: {outcome}\n"
        f"- **LLM calls**: {llm_calls}\n"
        f"- **Cost**: ${cost_usd:.2f}\n"
        f"- **Duration**: {duration_min:.0f} min\n"
    )
    if notes:
        block += f"- **Notes**: {notes}\n"
    with FileLock(str(LOCK_PATH), timeout=10):
        LEDGER_PATH.open("a", encoding="utf-8").write(block)

    return state


def update_quality_gate(gate_name: str, status: str, value: float | None = None) -> CouncilState:
    state = read()
    state.quality_gates[gate_name] = QualityGate(
        status=status, value=value, last_evaluated=datetime.now(timezone.utc)
    )
    state.updated_at = datetime.now(timezone.utc)
    atomic_write(state)
    return state


def check_convergence() -> str:
    state = read()
    gates = state.quality_gates
    all_pass = all(g.status == "pass" for g in gates.values())
    no_new_gap = state.convergence_signal.consecutive_no_new_gap >= 2
    budget = state.convergence_signal.max_rounds_budget

    if all_pass and no_new_gap:
        return "converged"
    if state.current_round >= budget:
        return "max_rounds"
    if state.blocked_on:
        return f"blocked:{state.blocked_on}"
    return "in_progress"
