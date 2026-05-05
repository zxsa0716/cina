"""CINA — LLM Provider Smoke Test (production readiness check).

Validates that every configured LLM provider in the multi-provider stack
can be invoked end-to-end on a tiny canonical CINA prompt, returning a
parseable structured response.

Usage:
    python -m src.stage1_extract.llm_smoke_test
    python -m src.stage1_extract.llm_smoke_test --providers gemini,groq
    python -m src.stage1_extract.llm_smoke_test --offline   # mock only

The smoke test does NOT do the full Stage 1 extraction — it only verifies
provider connectivity and response parsing on a 1-pair example. Use this
before running `python -m src.pipeline` or `--live-llm` modes.

Author: Heedo Choi (Kookmin University, Department of Climate Technology Convergence)
License: MIT
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent.parent

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Smoke test prompt (CINA-shaped)
# ---------------------------------------------------------------------------

SMOKE_TEST_PROMPT = """You are CINA Stage 1, an expert climate negotiation analyst.

Extract the stance of the country named below on the given issue from this snippet.
Return STRICT JSON in this exact schema (no markdown fence, no prose):

{
  "stance_score": <float in [-1.0, 1.0]; +1 strong support, -1 strong oppose>,
  "stance_category": <"strong_support"|"support"|"neutral"|"oppose"|"strong_oppose">,
  "frame_type": <"scientific"|"justice"|"sovereignty"|"security"|"development"|"mixed">,
  "evidence_quote": <verbatim string from the snippet, ≤ 30 words>,
  "confidence": <float in [0.0, 1.0]>
}

Country: Brazil
Issue: GGA-IND (Global Goal on Adaptation — Indicators)
Document snippet:
"The Conference of the Parties serving as the meeting of the Parties to the Paris Agreement
adopts the 59 voluntary, non-prescriptive, non-punitive, facilitative indicators across
seven thematic targets of the Global Goal on Adaptation, recognising that these shall not
create new financial obligations or commitments for Parties."
"""


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class ProviderResult:
    provider: str
    status: str          # "ok" | "missing_key" | "error" | "skipped"
    latency_ms: float = 0.0
    parsed: Optional[dict] = None
    raw_response: str = ""
    error: str = ""

    def emoji(self) -> str:
        return {"ok": "✅", "missing_key": "🔑", "error": "❌", "skipped": "⏭️"}[self.status]

    def to_summary_dict(self) -> dict:
        d = asdict(self)
        if d["raw_response"] and len(d["raw_response"]) > 200:
            d["raw_response"] = d["raw_response"][:200] + "... (truncated)"
        return d


# ---------------------------------------------------------------------------
# Per-provider test functions
# ---------------------------------------------------------------------------

def _try_parse_json(text: str) -> Optional[dict]:
    """Attempt to parse a JSON object from LLM output (handles fences)."""
    text = text.strip()
    # Strip markdown fence if present
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1] if lines[-1].startswith("```") else lines[1:])
    # Try to find first { ... } block
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass
    return None


def test_gemini() -> ProviderResult:
    if not os.environ.get("GEMINI_API_KEY"):
        return ProviderResult("gemini", "missing_key",
                              error="GEMINI_API_KEY not set")
    try:
        import google.generativeai as genai
    except ImportError:
        return ProviderResult("gemini", "error",
                              error="google-generativeai not installed; pip install google-generativeai")

    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        t0 = time.time()
        resp = model.generate_content(SMOKE_TEST_PROMPT,
                                       generation_config={"temperature": 0.3})
        latency = (time.time() - t0) * 1000
        text = resp.text if hasattr(resp, "text") else str(resp)
        parsed = _try_parse_json(text)
        if parsed and "stance_score" in parsed:
            return ProviderResult("gemini", "ok", latency, parsed, text)
        return ProviderResult("gemini", "error", latency, raw_response=text,
                              error="JSON parse failed or missing stance_score")
    except Exception as e:
        return ProviderResult("gemini", "error", error=f"{type(e).__name__}: {e}")


def test_groq() -> ProviderResult:
    if not os.environ.get("GROQ_API_KEY"):
        return ProviderResult("groq", "missing_key",
                              error="GROQ_API_KEY not set")
    try:
        from groq import Groq
    except ImportError:
        return ProviderResult("groq", "error",
                              error="groq package not installed; pip install groq")

    try:
        client = Groq()
        t0 = time.time()
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": SMOKE_TEST_PROMPT}],
            temperature=0.3,
            max_tokens=512
        )
        latency = (time.time() - t0) * 1000
        text = resp.choices[0].message.content
        parsed = _try_parse_json(text)
        if parsed and "stance_score" in parsed:
            return ProviderResult("groq", "ok", latency, parsed, text)
        return ProviderResult("groq", "error", latency, raw_response=text,
                              error="JSON parse failed or missing stance_score")
    except Exception as e:
        return ProviderResult("groq", "error", error=f"{type(e).__name__}: {e}")


def test_anthropic() -> ProviderResult:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return ProviderResult("anthropic", "missing_key",
                              error="ANTHROPIC_API_KEY not set")
    try:
        from anthropic import Anthropic
    except ImportError:
        return ProviderResult("anthropic", "error",
                              error="anthropic package not installed; pip install anthropic")

    try:
        client = Anthropic()
        t0 = time.time()
        resp = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=512,
            temperature=0.3,
            messages=[{"role": "user", "content": SMOKE_TEST_PROMPT}]
        )
        latency = (time.time() - t0) * 1000
        text = resp.content[0].text
        parsed = _try_parse_json(text)
        if parsed and "stance_score" in parsed:
            return ProviderResult("anthropic", "ok", latency, parsed, text)
        return ProviderResult("anthropic", "error", latency, raw_response=text,
                              error="JSON parse failed or missing stance_score")
    except Exception as e:
        return ProviderResult("anthropic", "error", error=f"{type(e).__name__}: {e}")


def test_ollama() -> ProviderResult:
    try:
        import ollama
    except ImportError:
        return ProviderResult("ollama", "error",
                              error="ollama package not installed; pip install ollama")

    try:
        # Check daemon connectivity
        models = ollama.list()
        model_names = [m.get("name", m.get("model", "")) for m in models.get("models", [])]
        target_model = next((m for m in model_names if "qwen" in m.lower()), None)
        if not target_model:
            target_model = next((m for m in model_names if m), None)
        if not target_model:
            return ProviderResult("ollama", "error",
                                  error="no models pulled; run `ollama pull qwen2.5:3b`")

        t0 = time.time()
        resp = ollama.generate(model=target_model, prompt=SMOKE_TEST_PROMPT,
                                options={"temperature": 0.3, "num_predict": 400})
        latency = (time.time() - t0) * 1000
        text = resp.get("response", "")
        parsed = _try_parse_json(text)
        if parsed and "stance_score" in parsed:
            return ProviderResult(f"ollama_{target_model}", "ok", latency, parsed, text)
        return ProviderResult(f"ollama_{target_model}", "error", latency,
                              raw_response=text,
                              error="JSON parse failed or missing stance_score")
    except Exception as e:
        return ProviderResult("ollama", "error", error=f"{type(e).__name__}: {e}")


def test_openrouter() -> ProviderResult:
    if not os.environ.get("OPENROUTER_API_KEY"):
        return ProviderResult("openrouter", "missing_key",
                              error="OPENROUTER_API_KEY not set")
    try:
        import requests
    except ImportError:
        return ProviderResult("openrouter", "error",
                              error="requests not installed")

    try:
        t0 = time.time()
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": [{"role": "user", "content": SMOKE_TEST_PROMPT}],
                "temperature": 0.3,
                "max_tokens": 512
            },
            timeout=60
        )
        latency = (time.time() - t0) * 1000
        if r.status_code != 200:
            return ProviderResult("openrouter", "error", latency,
                                  error=f"HTTP {r.status_code}: {r.text[:200]}")
        data = r.json()
        text = data["choices"][0]["message"]["content"]
        parsed = _try_parse_json(text)
        if parsed and "stance_score" in parsed:
            return ProviderResult("openrouter", "ok", latency, parsed, text)
        return ProviderResult("openrouter", "error", latency, raw_response=text,
                              error="JSON parse failed or missing stance_score")
    except Exception as e:
        return ProviderResult("openrouter", "error", error=f"{type(e).__name__}: {e}")


def test_offline_mock() -> ProviderResult:
    """Offline mock: always succeeds, useful for CI / testing the orchestration."""
    t0 = time.time()
    mock_response = json.dumps({
        "stance_score": 0.95,
        "stance_category": "strong_support",
        "frame_type": "development",
        "evidence_quote": "59 voluntary, non-prescriptive, non-punitive, facilitative indicators",
        "confidence": 0.92
    })
    parsed = json.loads(mock_response)
    return ProviderResult("offline_mock", "ok",
                          (time.time() - t0) * 1000,
                          parsed, mock_response)


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

ALL_PROVIDERS = {
    "gemini":     test_gemini,
    "groq":       test_groq,
    "anthropic":  test_anthropic,
    "ollama":     test_ollama,
    "openrouter": test_openrouter,
    "offline":    test_offline_mock
}


def main():
    parser = argparse.ArgumentParser(description="CINA LLM provider smoke test")
    parser.add_argument("--providers", default="all",
                        help="Comma-separated provider list, or 'all'")
    parser.add_argument("--output",
                        default="data/processed/llm_smoke_test_report.json",
                        help="Output JSON report path")
    parser.add_argument("--offline", action="store_true",
                        help="Only run the offline mock (no network calls)")
    args = parser.parse_args()

    if args.offline:
        providers = ["offline"]
    elif args.providers == "all":
        providers = list(ALL_PROVIDERS.keys())
    else:
        providers = [p.strip() for p in args.providers.split(",")]

    print("=" * 70)
    print(" CINA — LLM provider smoke test")
    print("=" * 70)
    print(f" Testing {len(providers)} provider(s): {', '.join(providers)}")
    print()

    results: list[ProviderResult] = []
    for p in providers:
        if p not in ALL_PROVIDERS:
            print(f" {p:<20s} — UNKNOWN provider; skipping")
            continue
        print(f" {p:<20s} — testing... ", end="", flush=True)
        try:
            r = ALL_PROVIDERS[p]()
        except Exception as e:
            r = ProviderResult(p, "error", error=str(e))
        results.append(r)

        if r.status == "ok":
            score = r.parsed.get("stance_score", "?") if r.parsed else "?"
            cat = r.parsed.get("stance_category", "?") if r.parsed else "?"
            print(f"{r.emoji()} {r.latency_ms:>7.0f}ms  stance={score} ({cat})")
        else:
            err = r.error[:60] if r.error else ""
            print(f"{r.emoji()} {r.status:<14s} {err}")

    # Summary
    print()
    print("=" * 70)
    n_ok = sum(1 for r in results if r.status == "ok")
    n_total = len(results)
    print(f" Production readiness: {n_ok}/{n_total} providers operational")
    if n_ok >= 1:
        print(f" ✅ At least one provider works — CINA Stage 1 is invokable")
    if n_ok >= 2:
        print(f" ✅ Multiple providers — Cross-LLM ensemble (E2) feasible")
    if n_ok >= 3:
        print(f" ⭐ ≥3 providers — robust cross-LLM Krippendorff α measurable")
    print("=" * 70)

    # Save report
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "providers_tested": providers,
            "n_ok": n_ok,
            "n_total": n_total,
            "results": [r.to_summary_dict() for r in results]
        }, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n Report: {out.relative_to(ROOT)}")

    # Exit code: 0 if at least one OK, else 1
    sys.exit(0 if n_ok >= 1 else 1)


if __name__ == "__main__":
    main()
