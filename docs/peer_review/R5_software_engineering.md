# R5 — 소프트웨어 공학 / DevOps 교수 — Review (COMPLETE)

> **Persona**: Google ML Engineer / KAIST 전산학부 / Apache 프로젝트 maintainer
> **Mode**: simulated peer review · adversarial weighting 30%
> **Status**: ✅ Complete · 2026-05-05

---

## 1. Summary judgement

학술 repository 표준에서는 **상위 25%** 수준의 reproducibility (manifest sha256, sample data, MIT, Makefile, Dockerfile, 5-LLM provider abstraction). 그러나 production-grade SE 표준에서는 **(i) pytest 0% coverage**, **(ii) requirements 비-pinned**, **(iii) type hint 일관성 부재**, **(iv) master orchestrator subprocess hang 관찰**, **(v) GitHub Actions 미설치 (workflow scope 부재)** 등 5가지 구조적 문제가 있다. JOSS (Journal of Open Source Software) 또는 Software Impacts 투고를 위해서는 이 5가지 P0 수정이 필수.

## 2. Rubric scores

| Dimension | Score | One-line justification |
|-----------|-------|------------------------|
| D1 Theoretical contribution | 1.5/5 | SE 분과 기여 거의 없음 (학술 도구 wrapper). |
| D2 Methodological rigor (engineering) ⭐ | 2.0/5 | pytest 0%, type hint 부분적, retry/backoff 부재. |
| D3 Empirical robustness | 2.0/5 | Subprocess orchestrator hang 관찰 + Docker build pass 미확인. |
| D4 Honesty / framing | 3.5/5 | WORKFLOW_INSTALL.md에서 PAT scope 한계 정직 인정. |
| D5 Reproducibility ⭐ | 4.0/5 | Manifest sha256, Makefile, Dockerfile, sample data 우수. requirements pin 약점만 빼면 5점. |
| D6 Practical / policy | 4.0/5 | LLM smoke test offline mode는 production CI 통합에 매우 실용적. |
| D7 Literature integration | 3.0/5 | NATO/IR 이론 외 SE/MLOps literature 인용 거의 없음. |
| D8 Writing quality (code documentation) | 3.5/5 | docstring 양호하나 type hint 일관성 부족. |
| D9 Novelty argument | 3.0/5 | 5-LLM provider 추상화는 production 스택으로 가치 있음. |
| D10 Submission readiness | 2.5/5 | JOSS / Software Impacts 투고 위해 위 5가지 P0 필수. |

**Total: 29.0/50** · **Average: 2.90/5**

## 3. Top 3 strengths

1. **5-LLM provider 추상화 + offline smoke test mode (`src/stage1_extract/llm_smoke_test.py`)는 production-grade design**. CI 통합 가능 (exit code 0/1), provider tier 자동 판정 (1 OK invokable, 2 OK ensemble, 3+ robust α). 이런 production readiness check는 학술 repository에서 보기 드문 수준.

2. **Master orchestrator (`src/run_all.py`)의 8-step + auto-generated RUN_REPORT.md 구조는 modular orchestration의 모범**. 단계별 status / duration / artifacts / metrics 자동 기록은 ML pipeline 표준 (MLflow, Kedro)과 정렬.

3. **`docs/social_preview.png`의 매트플롯립 기반 자동 생성 + Korean font auto-detection은 Windows/macOS/Linux 호환 우수**. Cross-platform reproducibility.

## 4. Top 3 weaknesses (specific, actionable)

1. **`tests/` 폴더 자체가 없음 (pytest coverage 0%)**. 191개 tracked file 중 단일 unit test 파일도 없음. `requirements.txt`에 pytest는 listed되어 있으나 사용 흔적이 없다. 최소한 (a) `cross_llm_consistency` Krippendorff α 계산의 unit test, (b) `bayesian_hierarchical` variance decomposition의 numerical regression test, (c) `rgat` model forward pass smoke test는 필수. JOSS 투고는 test coverage ≥ 80% 권장하므로 desk reject 위험.

2. **`requirements.txt`가 `>=X.Y.Z` 표기 + `pyproject.toml` 없음 + lockfile 부재**. PyTorch가 다음 minor version에서 R-GAT API breaking change 시 빌드 실패. 권장: `poetry init` + `poetry.lock` 또는 `pip-tools`로 `requirements-lock.txt` 생성. 현재 `Dockerfile`도 unpinned dep로 빌드되므로 시간 지나면 같은 Dockerfile에서 다른 결과 발생 가능.

3. **`src/run_all.py` subprocess-based orchestration의 fragility**. 이전 세션에서 master pipeline이 hang한 사례가 두 차례 관찰됨 (b1z9ldp8p, by6dbm8ks 백그라운드 task). subprocess.run() + capture_output=True 구조는 stdout/stderr 버퍼 deadlock 가능성. 권장: subprocess 대신 직접 import + function call 구조로 재작성 (대부분의 step은 같은 Python process 내에서 실행 가능).

## 5. Adversarial finding

### Most likely reject reason at JOSS / Software Impacts

> "본 software paper 후보는 학술 reproducibility 표준 (manifest sha256, sample data, MIT) 면에서는 우수하나, production SE 표준에서 다음 5가지 결함이 있다: (1) pytest unit test가 단 하나도 없음 (coverage 0%); (2) requirements.txt 비-pinned + lockfile 부재로 시간 경과 시 빌드 결정성 보장 불가; (3) GitHub Actions workflow가 .github_workflows_to_install_manually/에 staged 상태이며 실제 CI 실행 결과 미확인; (4) master orchestrator subprocess hang이 두 차례 관찰되어 production 안정성 의문; (5) Docker image의 actual build pass 여부가 RUN_REPORT에 기록되지 않음. JOSS Editor는 'JOSS-checks' 자동 검증에서 (1)(2) 즉시 fail, 'major revision' 권고할 가능성이 높다."

### Worst code smell

`src/run_all.py:S2_stage2`의 subprocess 호출:
```python
result = subprocess.run(
    [sys.executable, "-m", "src.stage2_graph.rgat", ...],
    capture_output=True, text=True, timeout=600, ...
)
```
같은 Python interpreter + 같은 import path를 가진 자체 모듈을 subprocess로 호출하는 것은 (a) 메모리 사용 비효율 (Python interpreter 두 번 spawn), (b) stdout/stderr 버퍼 deadlock 위험 (실제 두 차례 관찰), (c) 에러 propagation 약화 (exception이 stderr 문자열로만 전달). 권장: `from src.stage2_graph.rgat import train_rgat, RGATConfig, build_cina_synthetic_graph` 직접 import.

## 6. Required revisions before submission (priority-ordered)

- **P0 (must fix)**:
  1. `tests/` 폴더 + 최소 5개 unit test (cross_llm α, bayesian decomp, rgat smoke, llm smoke offline, viz publication_figures)
  2. `pyproject.toml` 또는 `requirements-lock.txt` 추가 (pinned deps)
  3. GitHub Actions workflow 실제 설치 + 첫 CI run 통과 확인
  4. `run_all.py` subprocess 대신 직접 import 구조로 refactoring (orchestrator hang 해결)
  5. Docker image build pass + smoke run 결과를 RUN_REPORT에 자동 기록
- **P1 (should fix)**:
  1. mypy / pyright type check 통과 (현재 type hint 누락 다수)
  2. LLM provider call에 retry + exponential backoff (`tenacity` 라이브러리 활용)
  3. ruff + black 통과 (현재 미실행 추정)
  4. JOSS paper template 작성 (`paper.md`을 별도)
- **P2 (nice to have)**:
  1. Pre-commit hooks (`.pre-commit-config.yaml`)
  2. CodeQL security scan 통과
  3. Sphinx 또는 MkDocs 자동 문서화

## 7. Venue recommendation

- ☐ Top SE (ICSE / FSE / OOPSLA)
- ☐ JOSS (Journal of Open Source Software) — 위 P0 수정 후
- ☐ Software Impacts (Elsevier) — 동일
- ☑️ GitHub release + Zenodo DOI (가장 현실적 first step)
- ☐ Reject

**Reasoning**: SE 분과 venue 본 투고는 위 P0 5가지 수정 후. 가장 현실적 first step은 GitHub release v3.0.0 publish + Zenodo 연동으로 영구 DOI 발급.

## 8. Open questions for the author

1. `tests/` 폴더가 부재한 이유는? CI 시간 제약? pytest 학습 곡선?
2. `pyproject.toml`을 도입한다면 poetry vs pip-tools 중 어느 것을 선호하는가?
3. Master orchestrator subprocess hang은 재현 가능한가? Reproducer minimal example을 issue로 등록할 수 있는가?
4. Docker image의 first build 시간 측정 결과가 있는가? CI에서 캐시 전략은?

---

*Reviewer signature*: R5 SE Persona (Google ML Eng / KAIST SE)
*Honesty disclosure*: Simulated peer review.
