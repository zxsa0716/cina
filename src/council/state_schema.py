"""Council state schema. See .claude/skills/session-state/SKILL.md."""
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


GateStatus = Literal["pass", "fail", "pending", "partial", "not_started"]


class QualityGate(BaseModel):
    status: GateStatus
    value: float | None = None
    last_evaluated: datetime | None = None


class RoundRecord(BaseModel):
    round: int
    date: str
    outcome: str
    llm_calls: dict[str, int] = Field(default_factory=dict)
    cost_usd: float = 0.0
    duration_min: float = 0.0
    notes: str | None = None


class ConvergenceSignal(BaseModel):
    consecutive_no_new_gap: int = 0
    max_rounds_budget: int = 10


class CouncilState(BaseModel):
    project: str = "CINA"
    framework_version: str = "2.0"
    current_round: int = 0
    rounds_completed: list[RoundRecord] = Field(default_factory=list)
    active_tasks: dict[str, str] = Field(default_factory=dict)
    quality_gates: dict[str, QualityGate]
    blocked_on: str | None = None
    next_action: str = ""
    convergence_signal: ConvergenceSignal = Field(default_factory=ConvergenceSignal)
    heedo_directives: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
