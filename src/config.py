"""CINA 전역 설정."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DELIVERABLES_DIR = ROOT / "deliverables"
DOCS_DIR = ROOT / "docs"

ISSUE_CODES = ["GGA-IND", "ADAPT-FIN", "L&D-OP", "NAPs", "MIT-ADAPT", "JT-ADAPT"]

ISSUE_DESCRIPTIONS = {
    "GGA-IND": "Global Goal on Adaptation indicators — quantitative vs qualitative, mandatory vs voluntary",
    "ADAPT-FIN": "Adaptation finance — 2x/3x multiplier, contributor base, delivery channels",
    "L&D-OP": "Loss and Damage Fund operations — direct access, eligibility, contribution base",
    "NAPs": "National Adaptation Plans — reporting cycles, technical support, iterative submission",
    "MIT-ADAPT": "Mitigation-Adaptation nexus — co-benefits, trade-offs, integrated treatment",
    "JT-ADAPT": "Just Transition with adaptation — vulnerable groups, indigenous rights, gender-responsive",
}

DEFAULT_COUNTRIES = [
    "Brazil", "EU", "United States", "China", "India",
    "AOSIS", "LDCs", "African Group", "AILAC", "Arab Group",
    "LMDC", "Japan", "South Korea", "Australia", "Saudi Arabia",
    "South Africa", "Norway", "Switzerland", "Mexico", "Colombia",
]


@dataclass
class Stage1Config:
    model: str = "claude-opus-4-7"
    temperature: float = 0.3
    k_samples: int = 5
    prompt_version: str = "v1.2"
    calibration_path: Path = DATA_DIR / "calibration" / "platt.pkl"
    max_tokens: int = 1500


@dataclass
class Stage2Config:
    hidden_dim: int = 64
    num_layers: int = 3
    heads: int = 4
    learning_rate: float = 1e-3
    weight_decay: float = 1e-5
    epochs: int = 200
    patience: int = 30
    leiden_gamma: float = 1.0
    knn_k: int = 5
    hypergraph_min_support: float = 0.2
    hypergraph_min_issues: int = 2
    hypergraph_max_issues: int = 4
    seed: int = 42


@dataclass
class Stage3Config:
    focal_country: str = "Brazil"
    cop: int = 30
    sector: str = "adaptation"
    language: Literal["ko", "en"] = "ko"
    max_words_per_section: int = 600
    temperature: float = 0.2
    max_regeneration_attempts: int = 3
    model: str = "claude-opus-4-7"


@dataclass
class CinaConfig:
    stage1: Stage1Config = field(default_factory=Stage1Config)
    stage2: Stage2Config = field(default_factory=Stage2Config)
    stage3: Stage3Config = field(default_factory=Stage3Config)
    countries: list[str] = field(default_factory=lambda: DEFAULT_COUNTRIES)
    issues: list[str] = field(default_factory=lambda: ISSUE_CODES)
    rate_limit_per_sec: float = 1.0


def default_config() -> CinaConfig:
    return CinaConfig()
