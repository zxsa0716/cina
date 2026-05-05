# Security Policy

## Supported versions

CINA is a graduate research project; only the latest tagged release on `main`
receives security attention.

| Version | Supported          |
|---------|--------------------|
| v3.0.x  | ✅                |
| v2.0.x  | ⚠️ best-effort   |
| < v2.0  | ❌                |

## Reporting a vulnerability

If you discover a security or privacy vulnerability — for example:

- A leaked API key or credential in commit history
- An LLM provider configuration that exposes user data
- A vulnerability in our dependency tree (PyTorch, NetworkX, matplotlib, etc.)
- Any way the pipeline could exfiltrate sensitive document content

**Please do NOT open a public GitHub issue.**

Instead, email the maintainer privately at:
**zxsa0716@kookmin.ac.kr**

with the subject line `[SECURITY] CINA <short description>`.

## What we promise

- We will acknowledge receipt within **5 business days**.
- We will publish a fix or written response within **30 days** when the issue
  is reproducible and within the project's scope.
- We will credit you in `CHANGELOG.md` (if you wish) once the issue is resolved.

## Sensitive data handling

CINA processes only **publicly available** UNFCCC documents, NDCs, ENB
summaries, and IPCC reports. The data manifest at
`data/manifest/manifest.jsonl` tracks license + sha256 + retrieval timestamp
for every input. We do **not** ingest:

- Confidential negotiation documents
- Personally identifiable information
- Industry confidential data

If you find any such material has been accidentally committed, please report
via the email above so we can purge it from history (using `git filter-repo` or
similar) and force-push.

## LLM provider keys

API keys for Gemini, Groq, Anthropic, OpenRouter, etc. **must never** be
committed. The `.gitignore` excludes `.env*`, `*.token`, `secrets/`, etc. If
you accidentally commit one, treat it as compromised: rotate the key
immediately and contact the maintainer.

---

**Maintainer**: Heedo Choi (zxsa0716@kookmin.ac.kr)
**Last updated**: 2026-05-05
