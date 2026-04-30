"""Castro 2025 cooperation matrix 자동 재현 — enb-mining 알고리즘 변형.

이미 수집한 ENB PDF에서 직접 추출:
- 각 ENB 문단 분석
- "Country/Group stated/supported/opposed/disagreed/agreed" 패턴 매칭
- pairwise cooperation/conflict frequency 산출
- 결과: data/processed/castro_reproduction_v1.json
"""
from __future__ import annotations

import json
import logging
import re
import sys
from collections import defaultdict
from pathlib import Path

import fitz

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger("cina.castro.repro")

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))


def load_parties_groupings() -> tuple[set[str], set[str]]:
    """Load enb-mining parties.txt + groupings.txt."""
    base = ROOT / "data" / "raw" / "round7" / "castro_reproduction_repo" / "enb-mining-main" / "data"
    parties_path = base / "parties.txt"
    groupings_path = base / "groupings.txt"

    parties = set()
    groupings = set()

    if parties_path.exists():
        for line in parties_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            # parties.txt format: "Brazil [G-77, BASIC, Mountain Landlocked]" or "Brazil"
            name = line.split("[")[0].split(":")[0].strip()
            if name:
                parties.add(name)

    if groupings_path.exists():
        for line in groupings_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            # groupings.txt format: "AOSIS: Alliance of Small Island States"
            name = line.split(":")[0].strip()
            if name:
                groupings.add(name)

    return parties, groupings


# Cooperation/conflict signal patterns
COOPERATION_VERBS = [
    r"supported", r"agreed with", r"endorsed", r"backed", r"echoed",
    r"aligned with", r"joined", r"concurred with", r"welcomed",
    r"co-sponsored", r"co-led",
]
CONFLICT_VERBS = [
    r"opposed", r"disagreed", r"rejected", r"objected", r"contested",
    r"countered", r"challenged", r"resisted", r"declined",
]


def extract_text_from_pdf(path: Path) -> str:
    try:
        doc = fitz.open(str(path))
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        return text
    except Exception as exc:
        logger.warning("PDF parse failed: %s — %s", path, exc)
        return ""


def find_actor_in_sentence(sentence: str, parties: set[str], groupings: set[str]) -> list[str]:
    """국가/그룹 식별."""
    found = []
    for entity in parties.union(groupings):
        if len(entity) < 3:
            continue
        # word boundary match
        pattern = r"\b" + re.escape(entity) + r"\b"
        if re.search(pattern, sentence, re.IGNORECASE):
            found.append(entity)
    return found


def extract_interactions(text: str, parties: set[str], groupings: set[str]) -> list[dict]:
    """Extract cooperation/conflict pairs from sentences."""
    interactions = []
    sentences = re.split(r"(?<=[.!?])\s+", text)

    for sent in sentences:
        if len(sent) < 20:
            continue

        # 1. Cooperation pattern
        for verb in COOPERATION_VERBS:
            matches = re.findall(rf"(\w+(?:\s+\w+)*)\s+{verb}\s+([\w\s,]+?)(?:\.|;|$)", sent, re.IGNORECASE)
            for actor_a, actor_b in matches:
                a_actors = find_actor_in_sentence(actor_a[-100:], parties, groupings)
                b_actors = find_actor_in_sentence(actor_b[:100], parties, groupings)
                for a in a_actors:
                    for b in b_actors:
                        if a != b:
                            interactions.append({
                                "actor_a": a, "actor_b": b,
                                "type": "cooperation",
                                "verb": verb,
                                "sentence_excerpt": sent[:200],
                            })

        # 2. Conflict pattern
        for verb in CONFLICT_VERBS:
            matches = re.findall(rf"(\w+(?:\s+\w+)*)\s+{verb}\s+([\w\s,]+?)(?:\.|;|$)", sent, re.IGNORECASE)
            for actor_a, actor_b in matches:
                a_actors = find_actor_in_sentence(actor_a[-100:], parties, groupings)
                b_actors = find_actor_in_sentence(actor_b[:100], parties, groupings)
                for a in a_actors:
                    for b in b_actors:
                        if a != b:
                            interactions.append({
                                "actor_a": a, "actor_b": b,
                                "type": "conflict",
                                "verb": verb,
                                "sentence_excerpt": sent[:200],
                            })

    return interactions


def aggregate_to_matrix(interactions: list[dict]) -> dict:
    """Pairwise cooperation/conflict frequency matrix."""
    coop = defaultdict(lambda: defaultdict(int))
    conflict = defaultdict(lambda: defaultdict(int))

    for inter in interactions:
        a, b = inter["actor_a"], inter["actor_b"]
        if inter["type"] == "cooperation":
            coop[a][b] += 1
            coop[b][a] += 1  # symmetric
        elif inter["type"] == "conflict":
            conflict[a][b] += 1
            conflict[b][a] += 1

    return {
        "cooperation": {k: dict(v) for k, v in coop.items()},
        "conflict": {k: dict(v) for k, v in conflict.items()},
    }


def main() -> int:
    parties, groupings = load_parties_groupings()
    logger.info("Loaded %d parties, %d groupings", len(parties), len(groupings))

    # Available ENB PDFs
    enb_pdfs = []
    for path in (ROOT / "data" / "raw").rglob("enb12*.pdf"):
        enb_pdfs.append(path)
    logger.info("Found %d ENB PDFs", len(enb_pdfs))

    all_interactions = []
    for pdf in enb_pdfs:
        text = extract_text_from_pdf(pdf)
        if not text:
            continue
        interactions = extract_interactions(text, parties, groupings)
        for inter in interactions:
            inter["source_pdf"] = pdf.name
        all_interactions.extend(interactions)
        logger.info("  %s: %d interactions extracted", pdf.name, len(interactions))

    matrix = aggregate_to_matrix(all_interactions)

    # CINA 20국 + 12 그룹 필터 (relevant subset)
    from src.data.identifiers import CINA_COUNTRIES, CINA_GROUPS
    cina_actors = set()
    for iso3, meta in CINA_COUNTRIES.items():
        cina_actors.add(meta["name"])
    for gslug, gmeta in CINA_GROUPS.items():
        cina_actors.add(gmeta["name"])

    # Filter to CINA-relevant
    cina_coop = {}
    cina_conflict = {}
    for actor_a, partners in matrix["cooperation"].items():
        cina_partners = {b: c for b, c in partners.items() if b in cina_actors or any(b.lower() in actor.lower() for actor in cina_actors)}
        if cina_partners:
            cina_coop[actor_a] = cina_partners
    for actor_a, partners in matrix["conflict"].items():
        cina_partners = {b: c for b, c in partners.items() if b in cina_actors or any(b.lower() in actor.lower() for actor in cina_actors)}
        if cina_partners:
            cina_conflict[actor_a] = cina_partners

    output = {
        "_meta": {
            "n_pdfs": len(enb_pdfs),
            "n_interactions_total": len(all_interactions),
            "n_actors_cooperation": len(matrix["cooperation"]),
            "n_actors_conflict": len(matrix["conflict"]),
            "method": "enb-mining-style regex (verbs: support/agree vs oppose/disagree)",
            "license": "CC BY-NC-SA 4.0 (IISD ENB derived)",
            "note": "Auto-reproduction of Castro 2025 cooperation matrix using enb-mining algorithm. Lower precision than original (which uses BERT) but provides traceable baseline.",
        },
        "full_matrix": matrix,
        "cina_filtered": {
            "cooperation": cina_coop,
            "conflict": cina_conflict,
        },
        "all_interactions": all_interactions[:200],  # sample
    }

    out = ROOT / "data" / "processed" / "castro_reproduction_v1.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("Castro reproduction saved: %s", out)

    print()
    print("=== Castro 2025 Cooperation Matrix Reproduction ===")
    print(f"Total interactions: {len(all_interactions)}")
    print(f"  Cooperation pairs: {sum(len(v) for v in matrix['cooperation'].values()) // 2}")
    print(f"  Conflict pairs: {sum(len(v) for v in matrix['conflict'].values()) // 2}")
    print()
    print("=== Top cooperation pairs (CINA-relevant) ===")
    coop_list = []
    for a, partners in cina_coop.items():
        for b, c in partners.items():
            coop_list.append((a, b, c))
    coop_list.sort(key=lambda x: -x[2])
    for a, b, c in coop_list[:15]:
        print(f"  {a:<20} <-> {b:<20} freq={c}")
    print()
    print("=== Top conflict pairs (CINA-relevant) ===")
    conflict_list = []
    for a, partners in cina_conflict.items():
        for b, c in partners.items():
            conflict_list.append((a, b, c))
    conflict_list.sort(key=lambda x: -x[2])
    for a, b, c in conflict_list[:10]:
        print(f"  {a:<20} <-> {b:<20} freq={c}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
