# 🔧 GitHub Actions workflows — manual install (one-time)

> **Why this file exists**: Pushing GitHub Actions workflow files requires a Personal Access Token with the `workflow` scope. Your current PAT does not have it. Two options to install the workflows.

## Option A — Re-create the PAT with `workflow` scope (recommended, 2 min)

1. https://github.com/settings/tokens
2. Click "Generate new token (classic)" or revoke the existing one
3. Tick the **`workflow`** scope (in addition to `repo`)
4. Save and update the token in your git credential manager:
   ```bash
   git config --global credential.helper manager
   # On the next push, you'll be prompted to re-authenticate
   ```
5. Then:
   ```bash
   cp .github_workflows_to_install_manually/*.yml .github/workflows/
   git add .github/workflows/
   git commit -m "Add GitHub Actions CI + release workflows"
   git push origin main
   ```

## Option B — Add workflows via GitHub Web UI (no PAT change, 3 min)

1. https://github.com/zxsa0716/cina/actions/new
2. Click "set up a workflow yourself"
3. Copy contents from `.github_workflows_to_install_manually/ci.yml` → paste → commit directly to main with name `.github/workflows/ci.yml`
4. Repeat for `release.yml`

After workflows are installed, every push triggers:
- Job 1 — offline smoke test (LLM mock + cross-LLM + Bayesian + JSON validation)
- Job 2 — all 10 publication figures regenerated → uploaded as artifact
- Job 3 — R-GAT sanity check (50 epochs CPU)

And every `v*.*.*` tag push automatically creates a GitHub Release with all figures attached.

---

**Files prepared for installation**:
- `.github_workflows_to_install_manually/ci.yml`
- `.github_workflows_to_install_manually/release.yml`
