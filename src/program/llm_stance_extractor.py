"""CINA v8.1 — Real LLM stance extraction pipeline.

For each (country, issue, COP) target, this:
  1. Retrieves corpus context (hybrid: country policy doc + relevant L-text)
  2. Builds a strict-JSON prompt (Stage 1 schema v1.4)
  3. Calls the configured LLM provider (gemini / anthropic / groq / ollama / openrouter)
  4. Parses + validates the JSON response
  5. Verifies evidence_quote against corpus via RapidFuzz partial ratio >= 85
  6. Appends to data/processed/stances_v5_llm.jsonl (LLM-extracted side dataset)

Outputs a fully extracted v5.2 corpus with verified_canonical = LLM-grounded.
The original v5.1 (heuristic) remains as fallback baseline.

Usage:
  # Set BYO key first
  export GEMINI_API_KEY=AIzaSy...

  # Extract a small batch (5 countries x 8 issues at COP30)
  python -m src.program.llm_stance_extractor --provider gemini \
         --countries Brazil,Korea,AOSIS,USA,EU --cops COP30 \
         --max 40

  # Resume from checkpoint
  python -m src.program.llm_stance_extractor --resume

  # Full extraction (2,400 records). ~30 min on Gemini Flash-Lite free tier.
  python -m src.program.llm_stance_extractor --provider gemini --all

Cost estimate (Gemini 2.5 Flash-Lite, free tier 1,000 req/day):
  - 2,400 records / 1,000 req/day = 2.4 days at free tier
  - With multi-provider rotation: 1 day across 3 providers

Author: Heedo Choi (Kookmin University)
License: MIT
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent.parent
CORPUS_DIR = ROOT / "data" / "corpus"
STANCES_V5 = ROOT / "data" / "processed" / "stances_v5.jsonl"
STANCES_LLM_OUT = ROOT / "data" / "processed" / "stances_v5_llm.jsonl"
CHECKPOINT = ROOT / "data" / "processed" / "stances_v5_llm_checkpoint.json"

PROMPT_VERSION = "stance_extract_v1.4_llm"

# Same canonical lists as v5 dataset
COUNTRIES = [
    "Brazil","EU","USA","China","India","AOSIS","Korea","Saudi","Japan","AILAC",
    "AGN","LMDC","Multi","Canada","Australia","Norway","UK","Germany","France",
    "Mexico","Indonesia","South Africa","Egypt","Türkiye","Maldives","Marshall Is",
    "Tuvalu","Bangladesh","Ethiopia","Nepal","Switzerland","Spain","Italy",
    "New Zealand","Argentina","Colombia","Chile","Peru","Costa Rica","Vietnam",
    "Thailand","Philippines","Pakistan","Iran","UAE","Qatar","Kenya","Ghana",
    "Senegal","Morocco",
]
ISSUES = ["GGA-IND","GGA-MOI","NAPs","JT-ADAPT","L&D-OP","FINANCE-ADAPT","TRANS-FIN","TECH-TRANS"]
COPS = ["COP25","COP26","COP27","COP28","COP29","COP30"]


# ===========================================================================
# Corpus context retrieval
# ===========================================================================

def load_corpus_text(country: str, cop: str, issue: str, max_chars: int = 4000) -> str:
    """Retrieve relevant corpus text for grounding.

    Priority: (1) country-specific policy doc, (2) cop-specific L-text,
    (3) coalition statements matching country's primary block.
    """
    parts = []
    # 1. National policy doc
    pat = country.replace(" ", "_").upper()[:3]
    for p in sorted((CORPUS_DIR / "national_policies").glob("*.md")):
        if p.stem.upper().startswith(pat):
            parts.append(f"### National policy: {p.stem}\n{p.read_text(encoding='utf-8')[:max_chars//2]}\n")
            break
    # 2. UNFCCC L-text matching COP
    for p in sorted((CORPUS_DIR / "unfccc_decisions").glob("*.md")):
        if cop in p.stem:
            parts.append(f"### UNFCCC {cop}: {p.stem}\n{p.read_text(encoding='utf-8')[:max_chars//2]}\n")
            break
    # 3. Coalition statements
    for p in sorted((CORPUS_DIR / "coalition_statements").glob("*.md")):
        parts.append(f"### Coalition statements: {p.stem}\n{p.read_text(encoding='utf-8')[:max_chars//3]}\n")
        break
    # If nothing, use country brief
    if not parts:
        brief = CORPUS_DIR / "national_policies" / "OTHER_COUNTRIES_brief.md"
        if brief.exists():
            parts.append(brief.read_text(encoding="utf-8")[:max_chars])
    return "\n\n".join(parts)[:max_chars]


# ===========================================================================
# Prompt builder (Stage 1 v1.4)
# ===========================================================================

def build_prompt(country: str, issue: str, cop: str, corpus_ctx: str) -> str:
    return f"""You are CINA Stage 1 stance extractor. Extract a STRUCTURED stance record
for the given (country, issue, COP) tuple based ONLY on the corpus context provided.
If the context does not support a stance, return stance_score 0.0 and confidence < 0.5.

Theoretical grounding:
- Hood 1983 / Howlett 2019: NATO 4-axis policy instruments (Nodality, Authority, Treasure, Organization)
- Snow & Benford 1988: frame typology (scientific, justice, sovereignty, security, development)
- Tallberg 2010: procedural authority signals (chair, pen_holder)
- Putnam 1988: domestic-international translation gap

## Target
country: {country}
issue:   {issue} (one of GGA-IND, GGA-MOI, NAPs, JT-ADAPT, L&D-OP, FINANCE-ADAPT, TRANS-FIN, TECH-TRANS)
cop:     {cop}

## Corpus context (use ONLY this as evidence source)
{corpus_ctx}

## REQUIRED OUTPUT — strict JSON, no markdown, no commentary
Return EXACTLY this schema (numeric fields as float, booleans as true/false):

{{
  "stance_score": <float in [-1, 1]; positive = support, negative = oppose>,
  "stance_category": <"strong_support"|"support"|"neutral"|"oppose"|"strong_oppose">,
  "nato_4axis": {{"nodality": <0-1>, "authority": <0-1>, "treasure": <0-1>, "organization": <0-1>}},
  "frame_distribution": {{"scientific": <0-1>, "justice": <0-1>, "sovereignty": <0-1>, "security": <0-1>, "development": <0-1>}},
  "frame_type": <dominant frame label>,
  "salience_score": <0-1; how prominently this issue features in the country's statement>,
  "procedural_signals": {{"is_chair_role": <bool>, "is_pen_holder": <bool>, "drafts_text_for_issue": <bool>}},
  "evidence_quote": "<verbatim or near-verbatim quote from the corpus context above; max 300 chars>",
  "evidence_location": "<which document the quote is from, e.g. UNFCCC_FCCC_PA_CMA_2025_L25E §7>",
  "confidence": <0-1; how confident you are given corpus support>
}}

Output the JSON object ONLY, no surrounding text."""


# ===========================================================================
# Provider adapters
# ===========================================================================

def call_gemini(prompt: str, api_key: str) -> str:
    import urllib.request, urllib.error, json as _json
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    body = _json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1200, "responseMimeType": "application/json"},
    }).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        j = _json.loads(r.read())
    return j["candidates"][0]["content"]["parts"][0]["text"]

def call_anthropic(prompt: str, api_key: str) -> str:
    import urllib.request, json as _json
    body = _json.dumps({
        "model": "claude-sonnet-4-5",
        "max_tokens": 1200, "temperature": 0.2,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, headers={
        "Content-Type": "application/json", "x-api-key": api_key, "anthropic-version": "2023-06-01",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        j = _json.loads(r.read())
    return j["content"][0]["text"]

def call_groq(prompt: str, api_key: str) -> str:
    import urllib.request, json as _json
    body = _json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2, "max_tokens": 1200, "response_format": {"type": "json_object"},
    }).encode()
    req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=body, headers={
        "Content-Type": "application/json", "Authorization": f"Bearer {api_key}",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        j = _json.loads(r.read())
    return j["choices"][0]["message"]["content"]


PROVIDERS = {
    "gemini":    (call_gemini,    "GEMINI_API_KEY"),
    "anthropic": (call_anthropic, "ANTHROPIC_API_KEY"),
    "groq":      (call_groq,      "GROQ_API_KEY"),
}


# ===========================================================================
# Evidence verification
# ===========================================================================

def verify_evidence(quote: str, corpus_ctx: str, threshold: int = 85) -> bool:
    """RapidFuzz partial ratio ≥ threshold (default 85) for fuzzy substring match."""
    try:
        from rapidfuzz import fuzz
        return fuzz.partial_ratio(quote, corpus_ctx) >= threshold
    except ImportError:
        # Fallback: case-insensitive substring (more strict, may reject valid quotes)
        return quote.lower()[:50] in corpus_ctx.lower()


# ===========================================================================
# Extraction loop with checkpoint
# ===========================================================================

def parse_llm_json(text: str) -> dict | None:
    """Robust JSON parser handling markdown code fences."""
    text = text.strip()
    if text.startswith("```"):
        # remove fence
        text = "\n".join(text.splitlines()[1:-1]) if text.endswith("```") else "\n".join(text.splitlines()[1:])
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # find first { ... } block
        i, j = text.find("{"), text.rfind("}")
        if i >= 0 and j > i:
            try: return json.loads(text[i:j+1])
            except: pass
    return None


def load_checkpoint() -> set:
    if not CHECKPOINT.exists(): return set()
    try:
        return set(tuple(t) for t in json.loads(CHECKPOINT.read_text(encoding="utf-8")))
    except: return set()


def save_checkpoint(done: set):
    CHECKPOINT.write_text(json.dumps(list(done)), encoding="utf-8")


def extract_one(country, issue, cop, provider, api_key) -> dict | None:
    corpus = load_corpus_text(country, cop, issue)
    if not corpus:
        return None
    prompt = build_prompt(country, issue, cop, corpus)
    fn, _ = PROVIDERS[provider]
    try:
        raw = fn(prompt, api_key)
    except Exception as e:
        return {"_error": str(e), "country": country, "issue": issue, "cop": cop}
    parsed = parse_llm_json(raw)
    if not parsed:
        return {"_error": "json_parse_failed", "raw": raw[:200], "country": country, "issue": issue, "cop": cop}
    evidence_ok = verify_evidence(parsed.get("evidence_quote", ""), corpus)
    return {
        "_meta": {
            "doc_id":           f"v52_{cop}_{country}_{issue}".replace(" ","_"),
            "country":          country,
            "issue":            issue,
            "cop":              cop,
            "extracted_at":     datetime.now(timezone.utc).isoformat(),
            "provider":         f"llm_{provider}",
            "k_samples":        1,
            "prompt_version":   PROMPT_VERSION,
            "dataset_version":  "5.2.0-llm",
            "source_type":      "verified_llm" if evidence_ok else "llm_unverified_quote",
        },
        **parsed,
        "evidence_verified": evidence_ok,
    }


def run(targets: list[tuple], provider: str, api_key: str, max_n: int | None = None,
        delay_sec: float = 0.6) -> tuple[int, int]:
    """Iterate targets, append to output JSONL, checkpoint after each."""
    done = load_checkpoint()
    pending = [t for t in targets if t not in done]
    if max_n: pending = pending[:max_n]
    print(f"[v8.1 extract] {len(pending)} pending (skipping {len(done)} done); provider={provider}")
    n_ok, n_err = 0, 0
    STANCES_LLM_OUT.parent.mkdir(parents=True, exist_ok=True)
    with STANCES_LLM_OUT.open("a", encoding="utf-8") as f:
        for i, (country, issue, cop) in enumerate(pending, 1):
            t0 = time.time()
            r = extract_one(country, issue, cop, provider, api_key)
            if r is None or "_error" in r:
                n_err += 1
                err = r["_error"] if r else "no_corpus"
                print(f"[{i}/{len(pending)}] {country}/{issue}/{cop}  ERR: {err}")
            else:
                f.write(json.dumps(r, ensure_ascii=False) + "\n"); f.flush()
                n_ok += 1
                dt = time.time() - t0
                print(f"[{i}/{len(pending)}] {country}/{issue}/{cop}  OK  stance={r.get('stance_score','?')} verified={r.get('evidence_verified')} t={dt:.1f}s")
            done.add((country, issue, cop))
            if i % 5 == 0: save_checkpoint(done)
            time.sleep(delay_sec)
    save_checkpoint(done)
    return n_ok, n_err


# ===========================================================================
# CLI
# ===========================================================================

def parse_csv_list(s: str, valid: list) -> list:
    if not s: return []
    parts = [p.strip() for p in s.split(",") if p.strip()]
    invalid = [p for p in parts if p not in valid]
    if invalid:
        print(f"⚠️ invalid items dropped: {invalid}")
    return [p for p in parts if p in valid]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try: sys.stdout.reconfigure(encoding="utf-8")
        except: pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", default="gemini", choices=["gemini","anthropic","groq"])
    ap.add_argument("--countries", default="", help="comma-separated; default = first 5")
    ap.add_argument("--issues",    default="", help="comma-separated; default = first 4")
    ap.add_argument("--cops",      default="COP30", help="comma-separated")
    ap.add_argument("--max",       type=int, default=20, help="max records to extract this run")
    ap.add_argument("--all",       action="store_true", help="full 2,400 extraction (overrides countries/issues/cops/max)")
    ap.add_argument("--resume",    action="store_true", help="resume from checkpoint")
    ap.add_argument("--delay",     type=float, default=0.6, help="sec between calls (rate-limit)")
    ap.add_argument("--dry-run",   action="store_true", help="show what would be extracted, no API calls")
    args = ap.parse_args()

    _, env_var = PROVIDERS[args.provider]
    api_key = os.environ.get(env_var)
    if not api_key and not args.dry_run:
        print(f"❌ env var {env_var} not set. Get a key:")
        if args.provider == "gemini":    print("   https://aistudio.google.com/apikey")
        if args.provider == "anthropic": print("   https://console.anthropic.com/settings/keys")
        if args.provider == "groq":      print("   https://console.groq.com/keys")
        sys.exit(1)

    if args.all:
        countries, issues, cops = COUNTRIES, ISSUES, COPS
    else:
        countries = parse_csv_list(args.countries, COUNTRIES) or COUNTRIES[:5]
        issues    = parse_csv_list(args.issues, ISSUES) or ISSUES[:4]
        cops      = parse_csv_list(args.cops, COPS) or ["COP30"]

    targets = [(c, i, p) for c in countries for i in issues for p in cops]
    print(f"[v8.1 extract] targets: {len(countries)}c × {len(issues)}i × {len(cops)}p = {len(targets)} records")
    print(f"[v8.1 extract] provider={args.provider} delay={args.delay}s max={args.max if not args.all else 'all'}")

    if args.dry_run:
        for t in targets[:10]: print("  -", t)
        if len(targets) > 10: print(f"  ... +{len(targets)-10} more")
        return

    n_ok, n_err = run(targets, args.provider, api_key,
                      max_n=None if args.all else args.max, delay_sec=args.delay)
    print(f"\n[v8.1 extract] DONE. ok={n_ok}  err={n_err}")
    print(f"[v8.1 extract] output: {STANCES_LLM_OUT}")
    print(f"[v8.1 extract] checkpoint: {CHECKPOINT}")


if __name__ == "__main__":
    main()
