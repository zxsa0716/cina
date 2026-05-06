# 🔧 Setup & deployment guides

GitHub repository configuration, deployment, and CI guides.

| File | Description |
|------|-------------|
| ⚡ [`BYO_LLM_SETUP.md`](BYO_LLM_SETUP.md) | **NEW v4.1** — Ask CINA Program의 LLM 모드 활성화 가이드. Gemini · Anthropic · Groq 3종 provider 키 발급 → 브라우저에 입력 → 자연어 답변 활성화의 3-step 프로세스. |
| [`3_CLICKS_REMAINING.md`](3_CLICKS_REMAINING.md) | About + Social preview + Release 3가지 GitHub UI 클릭 가이드 (정확한 텍스트 + 단계). |
| [`GITHUB_FINAL_SETUP.md`](GITHUB_FINAL_SETUP.md) | The 4 GitHub-UI clicks that cannot be automated. All optional but recommended for a complete public presentation. |
| [`GITHUB_REPO_GUIDE.md`](GITHUB_REPO_GUIDE.md) | Detailed GitHub repo configuration reference: badges, social preview, releases, pinned issues, GitHub Pages, CodeQL/Dependabot, arXiv preprint upload checklist, Zenodo/ORCID registration. |
| [`WORKFLOW_INSTALL.md`](WORKFLOW_INSTALL.md) | How to install the GitHub Actions CI workflows (which need a PAT with `workflow` scope to push). |

## Related

- [`../../Makefile`](../../Makefile) — `make help`, `make run`, `make smoke`, `make figs`, etc.
- [`../../Dockerfile`](../../Dockerfile) — reproducible container
- [`../../.github_workflows_to_install_manually/`](../../.github_workflows_to_install_manually/) — staged CI workflows (CI + tag-triggered release)
- [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md) — contributor guide

## Reproducibility

```bash
# Quick start (cached, reproducible)
make install
make smoke-offline   # 0-network LLM mock test
make run             # full master pipeline
make figs            # regenerate publication figures
```
