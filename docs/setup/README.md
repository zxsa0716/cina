# 🔧 Setup & deployment guides

GitHub repository configuration, deployment, and CI guides.

| File | Description |
|------|-------------|
| [`GITHUB_FINAL_SETUP.md`](GITHUB_FINAL_SETUP.md) | The 4 GitHub-UI clicks that cannot be automated (About section / Pages / Social preview / Release publication). All optional but recommended for a complete public presentation. |
| [`GITHUB_REPO_GUIDE.md`](GITHUB_REPO_GUIDE.md) | Detailed GitHub repo configuration reference: badges, social preview, releases, pinned issues, GitHub Pages, CodeQL/Dependabot, arXiv preprint upload checklist, Zenodo/ORCID registration. |
| [`WORKFLOW_INSTALL.md`](WORKFLOW_INSTALL.md) | How to install the GitHub Actions CI workflows (which need a PAT with `workflow` scope to push). Two options: re-create PAT, or paste workflows via Web UI. |

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
