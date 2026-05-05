# CINA — convenience targets
# Usage: make <target>

PYTHON ?= python
PIP    ?= $(PYTHON) -m pip

.DEFAULT_GOAL := help

.PHONY: help install run smoke smoke-offline rgat figs cross-llm bayes paper clean lint format ci test

help:                    ## Show this help
	@echo "CINA — convenience targets"
	@echo ""
	@echo "Setup:"
	@echo "  install       Install all dependencies (requirements.txt)"
	@echo ""
	@echo "Pipeline:"
	@echo "  run           Run the full master pipeline (cached LLM)"
	@echo "  run-live      Run with --live-llm (requires API keys)"
	@echo "  smoke         Test all configured LLM providers"
	@echo "  smoke-offline Offline mock LLM smoke test (no network)"
	@echo "  rgat          Train R-GAT (200 epochs)"
	@echo "  cross-llm     Run cross-LLM Krippendorff alpha analysis"
	@echo "  bayes         Run Bayesian variance decomposition"
	@echo "  figs          Regenerate all 10 publication figures"
	@echo "  social        Regenerate the social preview image"
	@echo ""
	@echo "Quality:"
	@echo "  lint          Run ruff lint"
	@echo "  format        Run black"
	@echo "  test          Run pytest"
	@echo "  ci            lint + test + smoke-offline (matches GitHub Actions)"
	@echo ""
	@echo "Utility:"
	@echo "  clean         Remove __pycache__ and .pytest_cache"
	@echo ""

install:                 ## Install all dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:                     ## Master pipeline (cached LLM)
	$(PYTHON) -m src.run_all

run-live:                ## Master pipeline with real LLM calls
	$(PYTHON) -m src.run_all --live-llm

smoke:                   ## All LLM providers
	$(PYTHON) -m src.stage1_extract.llm_smoke_test

smoke-offline:           ## Offline mock LLM smoke test
	$(PYTHON) -m src.stage1_extract.llm_smoke_test --offline

rgat:                    ## Train R-GAT
	$(PYTHON) -m src.stage2_graph.rgat --epochs 200

cross-llm:               ## Cross-LLM Krippendorff alpha
	$(PYTHON) -m src.stage1_extract.cross_llm_consistency \
		--output data/processed/cross_llm_agreement.json

bayes:                   ## Bayesian variance decomposition
	$(PYTHON) -m src.analysis.bayesian_hierarchical \
		--output data/processed/bayesian_decomposition.json

figs:                    ## Regenerate publication figures
	$(PYTHON) -m src.viz.publication_figures
	$(PYTHON) -m src.stage2_graph.generate_rgat_attention_figure

social:                  ## Regenerate social preview image
	$(PYTHON) -m src.viz.social_preview

paper:                   ## Quick word count of paper.md
	@wc -w deliverables/paper.md

lint:                    ## Run ruff
	ruff check src/

format:                  ## Run black
	black --line-length 100 src/

test:                    ## Run pytest
	pytest -v

ci:                      ## Mirror GitHub Actions CI locally
	$(MAKE) lint || true
	$(MAKE) smoke-offline
	$(MAKE) cross-llm
	$(MAKE) bayes

clean:                   ## Remove cache directories
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".ruff_cache" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned"
