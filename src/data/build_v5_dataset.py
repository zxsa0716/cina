"""Build CINA v5 expanded dataset (50 countries x 8 issues x 6 COPs = 2,400 records).

v4 -> v5 upgrades (academic rigor):
  - Coverage: 30 -> 50 countries, 6 -> 8 issues, 5 -> 6 COPs (COP25-COP30)
  - Schema: per-record NATO 4-axis individual sub-scores
  - Schema: frame distribution (5-class probability vector, not single label)
  - Schema: coalition_membership_score (computed per-COP)
  - Schema: procedural_authority_composite (single 0-1 score)
  - Schema: translation_gap_delta (domestic vs international stance distance)
  - Schema: evidence_quote with location_field (paragraph / line / submission_id)
  - Schema: prompt_version + extraction_timestamp + reproducibility_hash

NOT a substitute for real LLM extraction on actual UNFCCC documents -- this is
the CANONICAL EXTENDED CORPUS for the v5 program/visualization layer. v3
canonical 13-country verified patterns are preserved as anchors; v4 17 new
countries are kept; v5 adds 20 new countries via documented stance heuristics.

Reproducibility:
  - seed=42 (fixed)
  - all randomness goes through random.Random(seed) instance
  - output schema hash recorded in metadata header

Author: Heedo Choi (Kookmin University, Department of Climate Technology Convergence)
License: MIT
"""

from __future__ import annotations

import hashlib
import json
import random
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "data" / "processed" / "stances_v5.jsonl"
META_OUT = ROOT / "data" / "processed" / "stances_v5_meta.json"

DATASET_VERSION = "5.1.0"   # 5.1: expanded verified evidence quotes (10 -> 125)
PROMPT_VERSION = "stance_extract_v1.3"

# ---------------------------------------------------------------------------
# 50 countries with regional + economic + block grouping
# ---------------------------------------------------------------------------

COUNTRIES_V5 = {
    # --- v3 canonical 13 ------------------------------------------------------
    "Brazil":       {"region": "LatAm",  "income": "upper-mid", "ndgain": 65, "co2_pc":  2.3, "block": ["G77", "BASIC"]},
    "EU":           {"region": "Europe", "income": "high",      "ndgain": 80, "co2_pc":  6.5, "block": ["HAC"]},
    "USA":          {"region": "NorAm",  "income": "high",      "ndgain": 78, "co2_pc": 14.0, "block": ["Umbrella"]},
    "China":        {"region": "Asia",   "income": "upper-mid", "ndgain": 70, "co2_pc":  7.4, "block": ["G77", "BASIC", "LMDC"]},
    "India":        {"region": "Asia",   "income": "lower-mid", "ndgain": 50, "co2_pc":  1.9, "block": ["G77", "BASIC", "LMDC"]},
    "AOSIS":        {"region": "SIDS",   "income": "mixed",     "ndgain": 45, "co2_pc":  1.5, "block": ["G77", "AOSIS"]},
    "Korea":        {"region": "Asia",   "income": "high",      "ndgain": 78, "co2_pc": 11.5, "block": ["EIG"]},
    "Saudi":        {"region": "MENA",   "income": "high",      "ndgain": 60, "co2_pc": 18.0, "block": ["G77", "Arab"]},
    "Japan":        {"region": "Asia",   "income": "high",      "ndgain": 80, "co2_pc":  8.4, "block": ["Umbrella"]},
    "AILAC":        {"region": "LatAm",  "income": "mid",       "ndgain": 65, "co2_pc":  2.5, "block": ["G77", "AILAC"]},
    "AGN":          {"region": "Africa", "income": "low-mid",   "ndgain": 35, "co2_pc":  1.0, "block": ["G77", "AGN"]},
    "LMDC":         {"region": "mixed",  "income": "mid",       "ndgain": 55, "co2_pc":  5.5, "block": ["G77", "LMDC"]},
    "Multi":        {"region": "global", "income": "mixed",     "ndgain": 70, "co2_pc":  4.0, "block": []},

    # --- v4 new 17 -------------------------------------------------------------
    "Canada":       {"region": "NorAm",  "income": "high",      "ndgain": 82, "co2_pc": 14.2, "block": ["Umbrella"]},
    "Australia":    {"region": "Oceania","income": "high",      "ndgain": 80, "co2_pc": 15.5, "block": ["Umbrella"]},
    "Norway":       {"region": "Europe", "income": "high",      "ndgain": 84, "co2_pc":  6.7, "block": ["EIG"]},
    "UK":           {"region": "Europe", "income": "high",      "ndgain": 81, "co2_pc":  5.5, "block": ["Umbrella"]},
    "Germany":      {"region": "Europe", "income": "high",      "ndgain": 83, "co2_pc":  8.0, "block": ["EU"]},
    "France":       {"region": "Europe", "income": "high",      "ndgain": 81, "co2_pc":  5.0, "block": ["EU"]},
    "Mexico":       {"region": "LatAm",  "income": "upper-mid", "ndgain": 60, "co2_pc":  3.5, "block": ["EIG", "AILAC"]},
    "Indonesia":    {"region": "Asia",   "income": "lower-mid", "ndgain": 50, "co2_pc":  2.3, "block": ["G77", "ASEAN"]},
    "South Africa": {"region": "Africa", "income": "upper-mid", "ndgain": 55, "co2_pc":  7.0, "block": ["G77", "BASIC", "AGN"]},
    "Egypt":        {"region": "MENA",   "income": "lower-mid", "ndgain": 45, "co2_pc":  2.4, "block": ["G77", "Arab", "AGN"]},
    "Türkiye":      {"region": "MENA",   "income": "upper-mid", "ndgain": 65, "co2_pc":  5.4, "block": []},
    "Maldives":     {"region": "SIDS",   "income": "upper-mid", "ndgain": 35, "co2_pc":  3.0, "block": ["G77", "AOSIS"]},
    "Marshall Is":  {"region": "SIDS",   "income": "upper-mid", "ndgain": 35, "co2_pc":  3.5, "block": ["G77", "AOSIS"]},
    "Tuvalu":       {"region": "SIDS",   "income": "upper-mid", "ndgain": 30, "co2_pc":  0.8, "block": ["G77", "AOSIS"]},
    "Bangladesh":   {"region": "Asia",   "income": "lower-mid", "ndgain": 40, "co2_pc":  0.5, "block": ["G77", "LDC"]},
    "Ethiopia":     {"region": "Africa", "income": "low",       "ndgain": 30, "co2_pc":  0.2, "block": ["G77", "LDC", "AGN"]},
    "Nepal":        {"region": "Asia",   "income": "low",       "ndgain": 35, "co2_pc":  0.5, "block": ["G77", "LDC"]},

    # --- v5 new 20 -------------------------------------------------------------
    "Switzerland":  {"region": "Europe", "income": "high",      "ndgain": 86, "co2_pc":  4.3, "block": ["EIG"]},
    "Spain":        {"region": "Europe", "income": "high",      "ndgain": 78, "co2_pc":  5.4, "block": ["EU"]},
    "Italy":        {"region": "Europe", "income": "high",      "ndgain": 77, "co2_pc":  5.6, "block": ["EU"]},
    "New Zealand":  {"region": "Oceania","income": "high",      "ndgain": 82, "co2_pc":  7.5, "block": ["Umbrella"]},
    "Argentina":    {"region": "LatAm",  "income": "upper-mid", "ndgain": 60, "co2_pc":  4.0, "block": ["G77"]},
    "Colombia":     {"region": "LatAm",  "income": "upper-mid", "ndgain": 60, "co2_pc":  1.7, "block": ["G77", "AILAC"]},
    "Chile":        {"region": "LatAm",  "income": "high",      "ndgain": 70, "co2_pc":  4.6, "block": ["G77", "AILAC"]},
    "Peru":         {"region": "LatAm",  "income": "upper-mid", "ndgain": 55, "co2_pc":  1.8, "block": ["G77", "AILAC"]},
    "Costa Rica":   {"region": "LatAm",  "income": "upper-mid", "ndgain": 70, "co2_pc":  1.5, "block": ["G77", "AILAC"]},
    "Vietnam":      {"region": "Asia",   "income": "lower-mid", "ndgain": 45, "co2_pc":  3.5, "block": ["G77", "ASEAN"]},
    "Thailand":     {"region": "Asia",   "income": "upper-mid", "ndgain": 55, "co2_pc":  4.2, "block": ["G77", "ASEAN"]},
    "Philippines":  {"region": "Asia",   "income": "lower-mid", "ndgain": 40, "co2_pc":  1.3, "block": ["G77", "ASEAN", "CVF"]},
    "Pakistan":     {"region": "Asia",   "income": "lower-mid", "ndgain": 40, "co2_pc":  0.9, "block": ["G77", "LMDC"]},
    "Iran":         {"region": "MENA",   "income": "lower-mid", "ndgain": 55, "co2_pc":  7.5, "block": ["G77", "LMDC"]},
    "UAE":          {"region": "MENA",   "income": "high",      "ndgain": 65, "co2_pc": 22.0, "block": ["G77", "Arab"]},
    "Qatar":        {"region": "MENA",   "income": "high",      "ndgain": 60, "co2_pc": 38.0, "block": ["G77", "Arab"]},
    "Kenya":        {"region": "Africa", "income": "lower-mid", "ndgain": 35, "co2_pc":  0.4, "block": ["G77", "AGN"]},
    "Ghana":        {"region": "Africa", "income": "lower-mid", "ndgain": 40, "co2_pc":  0.6, "block": ["G77", "AGN"]},
    "Senegal":      {"region": "Africa", "income": "lower-mid", "ndgain": 35, "co2_pc":  0.7, "block": ["G77", "AGN", "LDC"]},
    "Morocco":      {"region": "MENA",   "income": "lower-mid", "ndgain": 50, "co2_pc":  1.9, "block": ["G77", "Arab", "AGN"]},
}

ISSUES = ["GGA-IND", "GGA-MOI", "NAPs", "JT-ADAPT", "L&D-OP", "FINANCE-ADAPT", "TRANS-FIN", "TECH-TRANS"]

COPS = ["COP25", "COP26", "COP27", "COP28", "COP29", "COP30"]

CHAIRS = {
    "COP25": "Spain",   # held in Madrid; Chile presidency in absentia
    "COP26": "UK",
    "COP27": "Egypt",
    "COP28": "UAE",
    "COP29": "Azerbaijan",
    "COP30": "Brazil",
}

# ---------------------------------------------------------------------------
# v3 canonical stance matrix (13 countries x 6 v3-issues) - PRESERVED
# 6-vec corresponds to: [GGA-IND, GGA-MOI, NAPs, JT-ADAPT, L&D-OP, FINANCE-ADAPT]
# ---------------------------------------------------------------------------

V3_CANONICAL = {
    "Brazil":       [0.95, 0.78, 0.88, 0.92, 0.55, 0.70],
    "EU":           [0.55, 0.65, 0.72, 0.60, 0.45, 0.58],
    "USA":          [0.30, 0.20, 0.50, 0.40,-0.20, 0.25],
    "China":        [-0.30,0.40, 0.55, 0.50, 0.65, 0.70],
    "India":        [-0.15,0.55, 0.60, 0.45, 0.85, 0.90],
    "AOSIS":        [0.85, 0.90, 0.78, 0.65, 0.95, 0.92],
    "Korea":        [0.65, 0.62, 0.75, 0.78, 0.39, 0.55],
    "Saudi":        [-0.55,-0.65,0.20,-0.30, 0.10, 0.40],
    "Japan":        [0.45, 0.50, 0.62, 0.55, 0.30, 0.48],
    "AILAC":        [0.85, 0.85, 0.80, 0.70, 0.85, 0.85],
    "AGN":          [0.65, 0.70, 0.72, 0.62, 0.75, 0.70],
    "LMDC":         [-0.20,0.50, 0.55, 0.40, 0.55, 0.60],
    "Multi":        [0.75, 0.65, 0.70, 0.60, 0.55, 0.65],
}

# v4 new 17 countries (preserved)
V4_NEW = {
    "Canada":       [0.45, 0.50, 0.65, 0.55, 0.20, 0.35],
    "Australia":    [0.40, 0.35, 0.55, 0.45, 0.10, 0.30],
    "Norway":       [0.70, 0.78, 0.78, 0.72, 0.65, 0.82],
    "UK":           [0.65, 0.70, 0.72, 0.65, 0.55, 0.62],
    "Germany":      [0.65, 0.72, 0.75, 0.68, 0.50, 0.65],
    "France":       [0.60, 0.68, 0.72, 0.65, 0.48, 0.60],
    "Mexico":       [0.60, 0.65, 0.72, 0.70, 0.50, 0.55],
    "Indonesia":    [-0.10,0.55, 0.60, 0.45, 0.75, 0.80],
    "South Africa": [0.05, 0.65, 0.65, 0.55, 0.75, 0.75],
    "Egypt":        [-0.10,0.60, 0.62, 0.50, 0.70, 0.72],
    "Türkiye":      [0.20, 0.35, 0.45, 0.30, 0.15, 0.30],
    "Maldives":     [0.85, 0.92, 0.78, 0.65, 0.95, 0.92],
    "Marshall Is":  [0.88, 0.94, 0.80, 0.68, 0.97, 0.94],
    "Tuvalu":       [0.90, 0.95, 0.82, 0.70, 0.98, 0.95],
    "Bangladesh":   [0.55, 0.78, 0.65, 0.55, 0.92, 0.92],
    "Ethiopia":     [0.45, 0.75, 0.62, 0.50, 0.85, 0.88],
    "Nepal":        [0.50, 0.78, 0.65, 0.55, 0.90, 0.90],
}

# v5 new 20 countries (heuristic from documented stance literature)
V5_NEW = {
    "Switzerland":  [0.72, 0.75, 0.78, 0.74, 0.62, 0.78],   # EIG progressive, near-Norway profile
    "Spain":        [0.62, 0.68, 0.72, 0.66, 0.55, 0.62],   # EU mainstream + COP25 host
    "Italy":        [0.55, 0.62, 0.68, 0.60, 0.42, 0.55],
    "New Zealand":  [0.58, 0.65, 0.70, 0.62, 0.45, 0.58],   # Umbrella but progressive
    "Argentina":    [0.42, 0.55, 0.62, 0.50, 0.55, 0.60],   # G77 moderate
    "Colombia":     [0.75, 0.78, 0.75, 0.68, 0.80, 0.78],   # AILAC progressive
    "Chile":        [0.80, 0.82, 0.78, 0.70, 0.82, 0.82],   # AILAC chair-emeritus (COP25)
    "Peru":         [0.72, 0.75, 0.72, 0.65, 0.78, 0.75],   # AILAC
    "Costa Rica":   [0.85, 0.85, 0.78, 0.70, 0.88, 0.85],   # AILAC norm-entrepreneur
    "Vietnam":      [0.35, 0.62, 0.65, 0.55, 0.78, 0.78],   # ASEAN G77
    "Thailand":     [0.30, 0.55, 0.62, 0.50, 0.65, 0.70],
    "Philippines":  [0.55, 0.78, 0.68, 0.58, 0.92, 0.88],   # CVF chair history
    "Pakistan":     [0.45, 0.75, 0.65, 0.55, 0.92, 0.92],   # LMDC + flood crisis
    "Iran":         [-0.25,0.50, 0.45, 0.35, 0.60, 0.65],   # LMDC defensive
    "UAE":          [0.55, 0.50, 0.60, 0.55, 0.35, 0.55],   # Petro-state + COP28 host
    "Qatar":        [-0.40,-0.50,0.30,-0.20, 0.20, 0.35],   # Petro-defensive
    "Kenya":        [0.55, 0.72, 0.70, 0.60, 0.78, 0.75],   # AGN active
    "Ghana":        [0.50, 0.70, 0.68, 0.58, 0.75, 0.72],
    "Senegal":      [0.55, 0.75, 0.68, 0.58, 0.85, 0.82],   # AGN + LDC
    "Morocco":      [0.45, 0.62, 0.65, 0.55, 0.65, 0.62],
}

CANONICAL_ALL = {**V3_CANONICAL, **V4_NEW, **V5_NEW}

# ---------------------------------------------------------------------------
# v5 new 2 issues: TRANS-FIN, TECH-TRANS (per-country mean stance, heuristic)
# These extend the original 6-vec to an 8-vec
# ---------------------------------------------------------------------------

# Map: country -> [TRANS-FIN (transparency on finance), TECH-TRANS (technology transfer)]
V5_NEW_ISSUES = {
    "Brazil":       [0.65, 0.72], "EU":           [0.78, 0.60], "USA":          [0.55, 0.45],
    "China":        [0.45, 0.85], "India":        [0.55, 0.92], "AOSIS":        [0.82, 0.80],
    "Korea":        [0.62, 0.70], "Saudi":        [-0.20, 0.40], "Japan":        [0.65, 0.62],
    "AILAC":        [0.75, 0.78], "AGN":          [0.70, 0.85], "LMDC":         [0.50, 0.82],
    "Multi":        [0.65, 0.65],
    "Canada":       [0.55, 0.50], "Australia":    [0.50, 0.45], "Norway":       [0.78, 0.65],
    "UK":           [0.70, 0.55], "Germany":      [0.72, 0.62], "France":       [0.70, 0.60],
    "Mexico":       [0.65, 0.70], "Indonesia":    [0.55, 0.78], "South Africa": [0.60, 0.78],
    "Egypt":        [0.55, 0.75], "Türkiye":      [0.30, 0.55], "Maldives":     [0.80, 0.82],
    "Marshall Is":  [0.82, 0.84], "Tuvalu":       [0.85, 0.85],
    "Bangladesh":   [0.70, 0.88], "Ethiopia":     [0.65, 0.82], "Nepal":        [0.68, 0.85],
    "Switzerland":  [0.80, 0.65], "Spain":        [0.65, 0.58], "Italy":        [0.60, 0.55],
    "New Zealand":  [0.62, 0.55], "Argentina":    [0.50, 0.65], "Colombia":     [0.72, 0.78],
    "Chile":        [0.78, 0.80], "Peru":         [0.70, 0.72], "Costa Rica":   [0.82, 0.80],
    "Vietnam":      [0.55, 0.78], "Thailand":     [0.50, 0.65], "Philippines":  [0.72, 0.85],
    "Pakistan":     [0.62, 0.85], "Iran":         [0.20, 0.55], "UAE":          [0.55, 0.62],
    "Qatar":        [-0.10, 0.45], "Kenya":        [0.65, 0.78], "Ghana":        [0.62, 0.72],
    "Senegal":      [0.65, 0.78], "Morocco":      [0.50, 0.65],
}

# Now build full 8-vec per country
def _full_stance_vec(country: str) -> list[float]:
    """6-vec + 2-vec = 8-vec across all v5 issues."""
    six = CANONICAL_ALL[country]
    two = V5_NEW_ISSUES[country]
    return list(six) + list(two)

# Per-COP shift: extends v4 to include COP25 baseline
COP_SHIFTS = {
    "COP25": {  # Madrid Dec 2019, Chile presidency, pre-pandemic baseline
        "scale": 0.92,  # slightly less mature negotiations on adaptation indicators
        "country_offsets": {"USA": -0.05, "Spain": +0.05}  # USA Trump-era 1st term
    },
    "COP26": {  # baseline reference
        "scale": 1.0,
        "country_offsets": {"UK": +0.04}  # host effect
    },
    "COP27": {
        "scale": 1.0,
        "country_offsets": {"USA": -0.05, "AOSIS": +0.03, "Bangladesh": +0.05, "Egypt": +0.04}
    },
    "COP28": {  # UAE chair, justice frame surge
        "scale": 1.0,
        "country_offsets": {"AOSIS": +0.05, "AILAC": +0.03, "USA": +0.05, "UAE": +0.06}
    },
    "COP29": {  # Azerbaijan chair, Trump return
        "scale": 1.0,
        "country_offsets": {"USA": -0.10, "Maldives": +0.04, "Tuvalu": +0.04, "Argentina": -0.05}
    },
    "COP30": {  # Brazil chair (current focal)
        "scale": 1.0,
        "country_offsets": {"Brazil": +0.05, "AOSIS": +0.03, "Türkiye": +0.02}
    },
}


# ---------------------------------------------------------------------------
# NATO 4-axis instrument profiles (per-issue baseline + per-country adjust)
# ---------------------------------------------------------------------------

NATO_ISSUE_BASELINE = {
    # nodality, authority, treasure, organization (each 0-1)
    "GGA-IND":       (0.55, 0.20, 0.15, 0.30),   # information-heavy, soft law
    "GGA-MOI":       (0.35, 0.30, 0.55, 0.45),   # means of implementation = treasure+org
    "NAPs":          (0.40, 0.55, 0.40, 0.65),   # national plans = strong organisation
    "JT-ADAPT":      (0.35, 0.40, 0.55, 0.55),   # just transition = treasure-heavy
    "L&D-OP":        (0.20, 0.30, 0.85, 0.70),   # loss & damage operationalisation = treasure-heavy
    "FINANCE-ADAPT": (0.25, 0.35, 0.90, 0.55),
    "TRANS-FIN":     (0.75, 0.55, 0.30, 0.50),   # transparency on finance = nodality-heavy
    "TECH-TRANS":    (0.50, 0.45, 0.50, 0.70),   # tech transfer = org-heavy
}

# Country-level NATO multipliers (more-developed countries tend to use authority more)
def _nato_multiplier(country: str) -> tuple[float, float, float, float]:
    info = COUNTRIES_V5[country]
    income = info["income"]
    if income == "high":
        return (1.0, 1.2, 1.1, 1.0)
    if income == "upper-mid":
        return (1.0, 1.0, 1.0, 1.0)
    if income in ("lower-mid", "mid", "low-mid"):
        return (1.1, 0.85, 0.9, 1.1)   # more nodality, less authority
    if income == "low":
        return (1.15, 0.75, 0.8, 1.15)
    return (1.0, 1.0, 1.0, 1.0)


# ---------------------------------------------------------------------------
# Frame distribution (5-class probability per record)
# ---------------------------------------------------------------------------

FRAME_LABELS = ["scientific", "justice", "sovereignty", "security", "development"]

def _frame_distribution(country: str, issue: str, rng: random.Random) -> dict:
    info = COUNTRIES_V5[country]
    blocks = set(info["block"])
    base = {"scientific": 0.10, "justice": 0.10, "sovereignty": 0.10, "security": 0.10, "development": 0.10}
    if "AOSIS" in blocks or "LDC" in blocks or "CVF" in blocks:
        base["justice"] += 0.45
        base["security"] += 0.15
    elif "BASIC" in blocks or "LMDC" in blocks:
        base["sovereignty"] += 0.35
        base["justice"] += 0.15 if issue in ("L&D-OP", "FINANCE-ADAPT", "TECH-TRANS") else 0.05
    elif "Arab" in blocks and country in ("Saudi", "Qatar", "UAE"):
        base["sovereignty"] += 0.40
    elif "AILAC" in blocks:
        base["development"] += 0.25
        base["justice"] += 0.20
    elif "EIG" in blocks or "HAC" in blocks:
        base["development"] += 0.30
        base["scientific"] += 0.20
    elif "EU" in blocks or "Umbrella" in blocks:
        base["development"] += 0.30
        base["scientific"] += 0.15
    elif "AGN" in blocks:
        base["justice"] += 0.30
        base["development"] += 0.15
    # add jitter and renormalise
    jittered = {k: max(0.01, v + rng.gauss(0, 0.04)) for k, v in base.items()}
    total = sum(jittered.values())
    return {k: round(v / total, 3) for k, v in jittered.items()}


def _dominant_frame(dist: dict) -> str:
    return max(dist.items(), key=lambda x: x[1])[0]


# ---------------------------------------------------------------------------
# Procedural authority composite (single 0-1 score)
# ---------------------------------------------------------------------------

def _procedural_composite(is_chair: bool, is_pen: bool, drafts: bool) -> float:
    score = 0.0
    if is_chair:  score += 0.55
    if is_pen:    score += 0.30
    if drafts:    score += 0.15
    return round(min(1.0, score), 3)


# ---------------------------------------------------------------------------
# Coalition membership score (per country, per COP -- closeness to dominant
# coalition partition)
# ---------------------------------------------------------------------------

COALITION_LABELS = {
    "G77+China": ["G77"],
    "Umbrella":  ["Umbrella"],
    "EU+HAC":    ["EU", "HAC"],
    "EIG":       ["EIG"],
    "AOSIS":     ["AOSIS"],
    "AGN":       ["AGN"],
    "AILAC":     ["AILAC"],
    "LMDC":      ["LMDC"],
    "Arab":      ["Arab"],
    "ASEAN":     ["ASEAN"],
    "LDC":       ["LDC"],
}

def _coalition_membership(country: str) -> dict:
    info = COUNTRIES_V5[country]
    blocks = set(info["block"])
    members = []
    for coal, mark in COALITION_LABELS.items():
        if any(m in blocks for m in mark):
            members.append(coal)
    primary = members[0] if members else "Independent"
    return {"primary": primary, "all": members or ["Independent"]}


# ---------------------------------------------------------------------------
# Translation gap delta (computed at country level, attached to each record)
# ---------------------------------------------------------------------------

# Domestic policy stance proxies (national NAP / domestic policy doc stance)
# Heuristic: derived from full 8-vec mean + nationalist bias
def _domestic_stance(country: str) -> float:
    vec = _full_stance_vec(country)
    info = COUNTRIES_V5[country]
    bias = 0.0
    if info["income"] in ("high", "upper-mid"):
        bias += 0.10   # domestic policies tend to be stronger than international flexibility
    if "BASIC" in info["block"] or "LMDC" in info["block"]:
        bias += 0.15   # strong domestic, weak international (Brazil paradox pattern)
    return max(-1.0, min(1.0, sum(vec) / len(vec) + bias))


# ---------------------------------------------------------------------------
# Stance category classifier
# ---------------------------------------------------------------------------

def _classify_stance(score: float) -> str:
    if score >= 0.7: return "strong_support"
    if score >= 0.3: return "support"
    if score >= -0.3: return "neutral"
    if score >= -0.7: return "oppose"
    return "strong_oppose"


# ---------------------------------------------------------------------------
# Chair-role detection per (country, cop, issue)
# ---------------------------------------------------------------------------

def _infer_chair_role(country: str, cop: str, issue: str) -> dict:
    chair = CHAIRS.get(cop)
    is_chair = (country == chair)
    is_pen   = is_chair or (country == "Korea" and issue == "NAPs")
    drafts   = bool(is_chair) or (country == "Korea" and issue == "NAPs")
    return {
        "is_chair_role":         is_chair,
        "is_pen_holder":         is_pen,
        "drafts_text_for_issue": drafts,
    }


# ---------------------------------------------------------------------------
# Evidence quote bank (real-ish quotes for verified records; placeholder for rest)
# ---------------------------------------------------------------------------

# v5.1: import expanded verified evidence quotes (125 entries from corpus extraction)
try:
    from src.data.v5_evidence_quotes_expanded import get_verified_quote, n_verified
    _EVIDENCE_EXPANDED_AVAILABLE = True
except ImportError:
    _EVIDENCE_EXPANDED_AVAILABLE = False


def _evidence_quote(country: str, issue: str, cop: str) -> dict:
    """Returns {quote, location_field, source_type}.

    v5.1: First tries the expanded EVIDENCE_VERIFIED dict (125 entries),
    falls back to heuristic placeholder."""
    if _EVIDENCE_EXPANDED_AVAILABLE:
        verified = get_verified_quote(country, issue, cop)
        if verified:
            return {
                "quote":            verified["quote"],
                "location_field":   verified.get("source_paragraph") or "verified_excerpt",
                "source_type":      "verified_canonical",
                "source_doc":       verified.get("source_doc"),
            }
    # Heuristic placeholder
    return {
        "quote":          f"[{cop} {country} submission - {issue}] (auto-generated placeholder; real extraction would be LLM Stage 1 output on actual UNFCCC document)",
        "location_field": "heuristic_placeholder",
        "source_type":    "heuristic_extension",
    }


# ---------------------------------------------------------------------------
# Build a single record
# ---------------------------------------------------------------------------

def build_record(country: str, issue: str, cop: str, rng: random.Random) -> dict:
    info = COUNTRIES_V5[country]
    issue_idx = ISSUES.index(issue)
    base_stance = _full_stance_vec(country)[issue_idx]

    # apply COP-specific shifts
    shift = COP_SHIFTS[cop]
    offset = shift["country_offsets"].get(country, 0.0)
    stance = base_stance * shift["scale"] + offset + rng.gauss(0, 0.025)
    stance = max(-1.0, min(1.0, stance))

    # Bayesian-like CI (synthetic; would be real beta-binomial posterior in prod)
    std = 0.04 + rng.uniform(0, 0.03)
    ci_lo = max(-1.0, stance - 1.96 * std)
    ci_hi = min( 1.0, stance + 1.96 * std)

    # NATO 4-axis with country multiplier + jitter
    base_n, base_a, base_t, base_o = NATO_ISSUE_BASELINE[issue]
    mn, ma, mt, mo = _nato_multiplier(country)
    nato = {
        "nodality":     round(max(0, min(1, base_n * mn + rng.gauss(0, 0.04))), 3),
        "authority":    round(max(0, min(1, base_a * ma + rng.gauss(0, 0.04))), 3),
        "treasure":     round(max(0, min(1, base_t * mt + rng.gauss(0, 0.04))), 3),
        "organization": round(max(0, min(1, base_o * mo + rng.gauss(0, 0.04))), 3),
    }
    nato_sum = nato["nodality"] + nato["authority"] + nato["treasure"] + nato["organization"]

    frame_dist = _frame_distribution(country, issue, rng)
    dominant_frame = _dominant_frame(frame_dist)

    proc = _infer_chair_role(country, cop, issue)
    proc_composite = _procedural_composite(
        proc["is_chair_role"], proc["is_pen_holder"], bool(proc["drafts_text_for_issue"])
    )

    coalition = _coalition_membership(country)
    domestic = _domestic_stance(country)
    delta = round(domestic - stance, 3)   # translation gap

    ev = _evidence_quote(country, issue, cop)

    salience_base = 0.85 if issue in ("GGA-IND", "L&D-OP", "FINANCE-ADAPT") else 0.65
    salience = round(min(1.0, max(0.2, salience_base + rng.gauss(0, 0.07))), 3)

    confidence = round(0.85 + rng.gauss(0, 0.04), 3)
    confidence = max(0.6, min(0.99, confidence))

    record = {
        "_meta": {
            "doc_id":              f"v5_{cop}_{country}_{issue}".replace(" ", "_"),
            "country":             country,
            "iso3":                None,   # to be populated by post-processing
            "issue":               issue,
            "cop":                 cop,
            "extracted_at":        datetime.now(timezone.utc).isoformat(),
            "provider":            "v5_canonical_extension",
            "k_samples":           5,
            "prompt_version":      PROMPT_VERSION,
            "dataset_version":     DATASET_VERSION,
            "source_type":         ev["source_type"],
            "country_metadata":    info,
        },
        "stance_score":            round(stance, 3),
        "stance_score_mean":       round(stance, 3),
        "stance_score_std":        round(std, 4),
        "ci_lower_95":             round(ci_lo, 3),
        "ci_upper_95":             round(ci_hi, 3),
        "stance_category":         _classify_stance(stance),
        "frame_type":              dominant_frame,
        "frame_distribution":      frame_dist,
        "salience_score":          salience,
        "nato_4axis":              nato,
        "nato_axis_sum":           round(nato_sum, 3),
        "procedural_signals":      proc,
        "procedural_composite":    proc_composite,
        "coalition_membership":    coalition,
        "translation_gap_delta":   delta,
        "domestic_stance_proxy":   round(domestic, 3),
        "evidence_quote":          ev["quote"],
        "evidence_location":       ev["location_field"],
        "evidence_source_doc":     ev.get("source_doc"),
        "confidence":              confidence,
    }
    return record


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------

def build_dataset(seed: int = 42, output_path: Path = OUT) -> tuple[int, str]:
    rng = random.Random(seed)
    records = []
    for country in COUNTRIES_V5.keys():
        for issue in ISSUES:
            for cop in COPS:
                records.append(build_record(country, issue, cop, rng))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # write metadata
    meta = {
        "dataset_version":  DATASET_VERSION,
        "prompt_version":   PROMPT_VERSION,
        "seed":             seed,
        "n_records":        len(records),
        "n_countries":      len(COUNTRIES_V5),
        "n_issues":         len(ISSUES),
        "n_cops":           len(COPS),
        "countries":        list(COUNTRIES_V5.keys()),
        "issues":           ISSUES,
        "cops":             COPS,
        "chairs":           CHAIRS,
        "frame_labels":     FRAME_LABELS,
        "nato_axes":        ["nodality", "authority", "treasure", "organization"],
        "coalition_labels": list(COALITION_LABELS.keys()),
        "generated_at":     datetime.now(timezone.utc).isoformat(),
    }

    # reproducibility hash
    schema_keys = sorted(records[0].keys()) + sorted(records[0]["_meta"].keys())
    h = hashlib.sha256(json.dumps(schema_keys, sort_keys=True).encode()).hexdigest()[:16]
    meta["schema_hash"] = h

    # v8.5: builder_hash for cache invalidation (matches rebuild_if_stale check)
    builder_h = hashlib.sha256()
    here = Path(__file__).resolve()
    expanded = here.parent / "v5_evidence_quotes_expanded.py"
    builder_h.update(here.read_bytes())
    if expanded.exists(): builder_h.update(expanded.read_bytes())
    meta["builder_hash"] = builder_h.hexdigest()

    META_OUT.parent.mkdir(parents=True, exist_ok=True)
    META_OUT.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    return len(records), h


if __name__ == "__main__":
    import sys
    n, schema_hash = build_dataset()
    print(f"[v5 dataset] {n} records written to {OUT}")
    print(f"[v5 dataset] {len(COUNTRIES_V5)} countries x {len(ISSUES)} issues x {len(COPS)} COPs")
    print(f"[v5 dataset] schema hash: {schema_hash}")
    print(f"[v5 dataset] metadata:    {META_OUT}")
