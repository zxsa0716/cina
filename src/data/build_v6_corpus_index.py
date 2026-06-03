"""Build v6 corpus manifest + search index.

Walks data/corpus/, extracts metadata from YAML front-matter, computes
sha256, and produces:
  - data/corpus/manifest.jsonl   (one record per document)
  - data/corpus/search_index.json (TF-IDF style inverted index for retrieval)

Author: Heedo Choi (Kookmin University)
License: MIT
"""

from __future__ import annotations
import hashlib, json, re, math
from collections import defaultdict, Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CORPUS = ROOT / "data" / "corpus"
MANIFEST = CORPUS / "manifest.jsonl"
INDEX = CORPUS / "search_index.json"

# ---- helpers -------------------------------------------------------------

def parse_yaml_frontmatter(text: str) -> tuple[dict, str]:
    """Tiny YAML frontmatter parser (only top-level scalars and 1-deep lists)."""
    if not text.startswith("---"): return {}, text
    end = text.find("\n---", 4)
    if end == -1: return {}, text
    meta = {}
    block = text[4:end]
    cur_key = None
    for line in block.splitlines():
        if not line.strip() or line.startswith("#"): continue
        if line.startswith("  ") and cur_key:
            # 1-deep list or dict (loose handling)
            stripped = line.strip()
            if stripped.startswith("- "):
                if not isinstance(meta.get(cur_key), list): meta[cur_key] = []
                meta[cur_key].append(stripped[2:].strip())
            elif ":" in stripped:
                k, v = stripped.split(":", 1)
                if not isinstance(meta.get(cur_key), dict): meta[cur_key] = {}
                meta[cur_key][k.strip()] = v.strip()
            continue
        m = re.match(r"^([^:]+):\s*(.*)$", line)
        if m:
            k = m.group(1).strip(); v = m.group(2).strip()
            cur_key = k
            if v == "":
                meta[k] = None
            elif v.startswith("[") and v.endswith("]"):
                meta[k] = [x.strip().strip('"') for x in v[1:-1].split(",") if x.strip()]
            elif v.lower() in ("true", "false"):
                meta[k] = v.lower() == "true"
            else:
                meta[k] = v.strip('"')
    body = text[end+4:].strip()
    return meta, body


# ---- main ----------------------------------------------------------------

STOP = {
    "the","a","an","and","or","but","is","are","was","were","be","been","of","in","on",
    "at","to","for","with","by","as","that","this","it","its","not","no","yes","from","into",
    "본","해","이","그","저","것","및","또","수","의","에","에서","으로","로","를","을","는","가","이",
    "있다","없다","한다","된다","것이다","위해","대한","이는","으로써","해서","하는","된","된다고",
    "있는","해서","아닌","따라","대해","대해서","through","over","under","above","below",
    "this","that","these","those","such","than","then","there","where","when","what","which",
}

def tokenize(text: str) -> list[str]:
    """Mixed Korean / English tokenizer."""
    if not text: return []
    # Korean: split by spaces, keep multi-char hangul tokens
    # English: lowercase + alpha-num
    raw = re.findall(r"[가-힣]+|[A-Za-z0-9_\-\.&]+", text.lower())
    return [t for t in raw if len(t) > 1 and t not in STOP]


def build_index():
    records = []
    docs_text = {}
    for p in sorted(CORPUS.rglob("*.md")):
        if p.name.lower() == "readme.md": continue
        raw = p.read_text(encoding="utf-8")
        meta, body = parse_yaml_frontmatter(raw)
        sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        doc = {
            "path":        rel,
            "doc_id":      meta.get("doc_id") or p.stem,
            "title":       meta.get("title") or p.stem,
            "short_title": meta.get("short_title", meta.get("title", p.stem)),
            "type":        meta.get("type", "uncategorised"),
            "cop":         meta.get("cop"),
            "country":     meta.get("country"),
            "iso3":        meta.get("iso3"),
            "issues_addressed": meta.get("issues_addressed", []),
            "language":    meta.get("language", "en"),
            "license":     meta.get("license"),
            "official_url": meta.get("official_url"),
            "adoption_date": meta.get("adoption_date"),
            "sha256":      sha,
            "size_bytes":  len(raw.encode("utf-8")),
            "n_tokens":    len(body.split()),
            "category_dir": rel.split("/")[2] if rel.startswith("data/corpus/") else "unknown",
        }
        records.append(doc)
        docs_text[doc["doc_id"]] = (doc["title"] or "") + "\n\n" + body

    # also CSVs in quantitative/
    for p in sorted((CORPUS / "quantitative").glob("*.csv")):
        raw = p.read_text(encoding="utf-8")
        sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        records.append({
            "path": rel, "doc_id": p.stem, "title": p.stem.replace("_", " "),
            "short_title": p.stem, "type": "quantitative_csv",
            "cop": None, "country": None, "iso3": None,
            "issues_addressed": [], "language": "en",
            "license": "CC BY 4.0 / OECD CRS license / source-specific",
            "official_url": None, "adoption_date": None,
            "sha256": sha, "size_bytes": len(raw.encode("utf-8")),
            "n_tokens": len(raw.split()),
            "category_dir": "quantitative",
        })
        docs_text[p.stem] = raw[:5000]  # first 5kB for keyword index

    # also BibTeX
    bib = CORPUS / "academic_references" / "bibliography.bib"
    if bib.exists():
        raw = bib.read_text(encoding="utf-8")
        sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        rel = str(bib.relative_to(ROOT)).replace("\\", "/")
        records.append({
            "path": rel, "doc_id": "bibliography",
            "title": "CINA Academic Bibliography (25+ entries)",
            "short_title": "bibliography.bib", "type": "bibtex",
            "cop": None, "country": None, "iso3": None,
            "issues_addressed": [], "language": "en",
            "license": "CC BY 4.0 (compilation)",
            "official_url": None, "adoption_date": None,
            "sha256": sha, "size_bytes": len(raw.encode("utf-8")),
            "n_tokens": len(raw.split()),
            "category_dir": "academic_references",
        })
        docs_text["bibliography"] = raw

    # ----- write manifest -----
    MANIFEST.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n",
        encoding="utf-8"
    )
    print(f"[manifest] {len(records)} docs -> {MANIFEST}")

    # ----- build TF-IDF style inverted index -----
    N = len(docs_text)
    df = Counter()                              # term -> doc count
    tf_per_doc = {}                              # doc_id -> {term: freq}
    for doc_id, text in docs_text.items():
        toks = tokenize(text)
        c = Counter(toks)
        tf_per_doc[doc_id] = c
        for t in c.keys():
            df[t] += 1

    # IDF (smooth)
    idf = {t: math.log((1 + N) / (1 + d)) + 1.0 for t, d in df.items()}

    # Per-doc length normalisation
    inverted = defaultdict(list)                # term -> [(doc_id, tfidf_weight), ...]
    for doc_id, c in tf_per_doc.items():
        if not c: continue
        norm = math.sqrt(sum((f * idf.get(t, 1.0)) ** 2 for t, f in c.items())) or 1.0
        for t, f in c.items():
            w = (f * idf.get(t, 1.0)) / norm
            inverted[t].append([doc_id, round(w, 4)])
    # keep top-30 docs per term to limit index size
    for t in list(inverted.keys()):
        lst = sorted(inverted[t], key=lambda x: -x[1])[:30]
        inverted[t] = lst

    index_obj = {
        "version":    "v6.0.0",
        "n_docs":     N,
        "n_terms":    len(inverted),
        "generated":  datetime.now(timezone.utc).isoformat(),
        "idf":        {t: round(v, 4) for t, v in idf.items()},
        "inverted":   dict(inverted),
    }
    INDEX.write_text(json.dumps(index_obj, ensure_ascii=False), encoding="utf-8")
    print(f"[index] {N} docs, {len(inverted)} unique terms -> {INDEX} ({INDEX.stat().st_size//1024} KB)")


if __name__ == "__main__":
    build_index()
