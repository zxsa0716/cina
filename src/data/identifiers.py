"""CINA single source of truth for all identifiers.

docs/13_reference_tables.md 의 Python 표현. 모든 collector·refinement·analysis
는 이 모듈만 import 한다.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# 1. Countries (CINA core 20)
# ---------------------------------------------------------------------------
CINA_COUNTRIES: dict[str, dict] = {
    "BRA": {"slug": "brazil", "name": "Brazil", "region": "LAC"},
    "EU":  {"slug": "eu", "name": "European Union", "region": "Europe"},
    "USA": {"slug": "usa", "name": "United States of America", "region": "NA"},
    "CHN": {"slug": "china", "name": "China", "region": "Asia"},
    "IND": {"slug": "india", "name": "India", "region": "Asia"},
    "JPN": {"slug": "japan", "name": "Japan", "region": "Asia"},
    "KOR": {"slug": "south_korea", "name": "Korea, Republic of", "region": "Asia"},
    "AUS": {"slug": "australia", "name": "Australia", "region": "Oceania"},
    "CAN": {"slug": "canada", "name": "Canada", "region": "NA"},
    "NOR": {"slug": "norway", "name": "Norway", "region": "Europe"},
    "CHE": {"slug": "switzerland", "name": "Switzerland", "region": "Europe"},
    "MEX": {"slug": "mexico", "name": "Mexico", "region": "LAC"},
    "ZAF": {"slug": "south_africa", "name": "South Africa", "region": "Africa"},
    "SAU": {"slug": "saudi_arabia", "name": "Saudi Arabia", "region": "MENA"},
    "ARE": {"slug": "uae", "name": "United Arab Emirates", "region": "MENA"},
    "EGY": {"slug": "egypt", "name": "Egypt", "region": "MENA"},
    "COL": {"slug": "colombia", "name": "Colombia", "region": "LAC"},
    "CHL": {"slug": "chile", "name": "Chile", "region": "LAC"},
    "CRI": {"slug": "costa_rica", "name": "Costa Rica", "region": "LAC"},
    "KEN": {"slug": "kenya", "name": "Kenya", "region": "Africa"},
}

# ---------------------------------------------------------------------------
# 2. Negotiating groups
# ---------------------------------------------------------------------------
CINA_GROUPS: dict[str, dict] = {
    "g77":      {"name": "G77+China", "size": 134},
    "eu_g":     {"name": "European Union", "size": 27},
    "umbrella": {"name": "Umbrella Group", "size": 10},
    "eig":      {"name": "Environmental Integrity Group", "size": 5},
    "aosis":    {"name": "Alliance of Small Island States", "size": 39},
    "ldc":      {"name": "Least Developed Countries", "size": 45},
    "african":  {"name": "African Group", "size": 54},
    "arab":     {"name": "Arab Group", "size": 22},
    "ailac":    {"name": "AILAC", "size": 8},
    "basic":    {"name": "BASIC", "size": 4},
    "lmdc":     {"name": "Like-Minded Developing Countries", "size": 25},
    "hac":      {"name": "High Ambition Coalition", "size": 70},
    "amazon":   {"name": "Amazon Cooperation Treaty", "size": 8},
}

# Country → groups (ISO3 → list of group slugs)
GROUP_MEMBERSHIP: dict[str, list[str]] = {
    "BRA": ["g77", "basic", "amazon"],
    "EU":  ["eu_g", "hac"],
    "USA": ["umbrella"],
    "CHN": ["g77", "basic", "lmdc"],
    "IND": ["g77", "basic", "lmdc"],
    "JPN": ["umbrella"],
    "KOR": ["eig"],
    "AUS": ["umbrella"],
    "CAN": ["umbrella"],
    "NOR": ["umbrella", "hac"],
    "CHE": ["eig", "hac"],
    "MEX": ["eig", "ailac", "hac"],
    "ZAF": ["g77", "basic", "african"],
    "SAU": ["g77", "arab", "lmdc"],
    "ARE": ["g77", "arab"],
    "EGY": ["g77", "arab", "african"],
    "COL": ["g77", "ailac", "hac"],
    "CHL": ["g77", "ailac", "hac"],
    "CRI": ["g77", "ailac", "hac"],
    "KEN": ["g77", "african"],
}

# ---------------------------------------------------------------------------
# 3. Issues (Adaptation sector — CINA v2.0 fixed set)
# ---------------------------------------------------------------------------
CINA_ISSUES: dict[str, dict] = {
    "GGA-IND": {
        "label": "Global Goal on Adaptation Indicators",
        "paris_article": "Art. 7.1",
        "unfccc_topic_id": 1136,
        "priority": "P0",
    },
    "ADAPT-FIN": {
        "label": "Adaptation Finance",
        "paris_article": "Art. 9",
        "priority": "P0",
    },
    "L&D-OP": {
        "label": "Loss and Damage Fund Operations",
        "paris_article": "Art. 8",
        "unfccc_topic_id": 3558,
        "priority": "P0",
    },
    "NAPs": {
        "label": "National Adaptation Plans",
        "paris_article": "Art. 7.9",
        "unfccc_topic_id": 3812,
        "priority": "P1",
    },
    "MIT-ADAPT": {
        "label": "Mitigation-Adaptation Nexus",
        "paris_article": "Art. 7.7",
        "priority": "P2",
    },
    "JT-ADAPT": {
        "label": "Just Transition with Adaptation",
        "paris_article": "UAE JTWP",
        "priority": "P2",
    },
}

ISSUE_KEYWORDS: dict[str, list[str]] = {
    "GGA-IND": [
        "Global Goal on Adaptation", "GGA", "UAE Framework",
        "adaptation indicator", "Belém Adaptation Indicators",
        "indicator framework", "global resilience",
    ],
    "ADAPT-FIN": [
        "adaptation finance", "adaptation funding", "NCQG",
        "doubling adaptation finance", "tripling adaptation finance",
        "adaptation gap", "GCF adaptation",
    ],
    "L&D-OP": [
        "Loss and Damage", "L&D Fund", "FRLD",
        "non-economic loss", "Santiago Network",
        "direct access", "Sharm el-Sheikh dialogue",
    ],
    "NAPs": [
        "National Adaptation Plan", "NAPs", "LEG",
        "iterative submission", "NAP central",
    ],
    "MIT-ADAPT": [
        "mitigation-adaptation", "co-benefits", "synergies",
        "trade-offs", "integrated approach",
    ],
    "JT-ADAPT": [
        "Just Transition", "JTWP", "vulnerable populations",
        "indigenous", "gender-responsive adaptation",
        "labour rights",
    ],
}

# ---------------------------------------------------------------------------
# 4. COP sessions
# ---------------------------------------------------------------------------
CINA_SESSIONS: dict[str, dict] = {
    "COP21": {"year": 2015, "place": "Paris", "slug": "cop21"},
    "COP22": {"year": 2016, "place": "Marrakech", "slug": "cop22"},
    "COP23": {"year": 2017, "place": "Bonn", "slug": "cop23"},
    "COP24": {"year": 2018, "place": "Katowice", "slug": "cop24"},
    "COP25": {"year": 2019, "place": "Madrid", "slug": "cop25"},
    "COP26": {"year": 2021, "place": "Glasgow", "slug": "cop26"},
    "COP27": {"year": 2022, "place": "Sharm el-Sheikh", "slug": "cop27"},
    "COP28": {"year": 2023, "place": "Dubai", "slug": "cop28"},
    "COP29": {"year": 2024, "place": "Baku", "slug": "cop29"},
    "COP30": {"year": 2025, "place": "Belém", "slug": "cop30"},
    "SBI60": {"year": 2024, "place": "Bonn", "slug": "sbi60"},
    "SBI61": {"year": 2024, "place": "Baku", "slug": "sbi61"},
    "SBI62": {"year": 2025, "place": "Bonn", "slug": "sbi62"},
    "SBSTA60": {"year": 2024, "place": "Bonn", "slug": "sbsta60"},
    "SBSTA61": {"year": 2024, "place": "Baku", "slug": "sbsta61"},
    "SBSTA62": {"year": 2025, "place": "Bonn", "slug": "sbsta62"},
}

# ---------------------------------------------------------------------------
# 5. Country Power Index (Stage 2 epistemic divergence)
# ---------------------------------------------------------------------------
# 산출: 0.4*GDP_log + 0.3*CO2_log + 0.2*historical_agenda_setting + 0.1*group_leadership
# 단, COP30에 한해 의장국 보너스 +0.05 (BRA만)
COUNTRY_POWER_INDEX: dict[str, float] = {
    "BRA": 0.85,  # 의장국 + BASIC
    "EU":  0.95,
    "USA": 0.90,
    "CHN": 0.92,
    "IND": 0.78,
    "JPN": 0.74,
    "KOR": 0.60,
    "AUS": 0.62,
    "CAN": 0.62,
    "NOR": 0.58,
    "CHE": 0.55,
    "MEX": 0.50,
    "ZAF": 0.65,
    "SAU": 0.70,
    "ARE": 0.55,
    "EGY": 0.45,
    "COL": 0.40,
    "CHL": 0.42,
    "CRI": 0.38,
    "KEN": 0.40,
    # 그룹 노드 (협상 그룹 자체)
    "AOSIS-group": 0.62,
    "LDC-group": 0.55,
}

# ---------------------------------------------------------------------------
# 6. Validation helpers
# ---------------------------------------------------------------------------
def validate_country(code: str) -> bool:
    return code in CINA_COUNTRIES

def validate_issue(code: str) -> bool:
    return code in CINA_ISSUES

def validate_session(code: str) -> bool:
    return code in CINA_SESSIONS

def country_iso3(name_or_slug: str) -> str | None:
    """Resolve country name or slug to ISO3 code."""
    n = name_or_slug.strip().lower()
    for iso3, meta in CINA_COUNTRIES.items():
        if meta["slug"] == n or meta["name"].lower() == n or iso3.lower() == n:
            return iso3
    return None

def session_slug(code: str) -> str | None:
    s = CINA_SESSIONS.get(code.upper())
    return s["slug"] if s else None

__all__ = [
    "CINA_COUNTRIES",
    "CINA_GROUPS",
    "CINA_ISSUES",
    "CINA_SESSIONS",
    "ISSUE_KEYWORDS",
    "GROUP_MEMBERSHIP",
    "COUNTRY_POWER_INDEX",
    "validate_country",
    "validate_issue",
    "validate_session",
    "country_iso3",
    "session_slug",
]
