# R5 — 소프트웨어 공학 / DevOps 교수 — Review Brief

> **Persona**: Google ML Engineer / KAIST 전산학부 / Apache 프로젝트 maintainer
> **분과 기여 영역**: 코드 품질, 재현성, CI/CD, 모듈성, 의존성 관리
> **Mode**: simulated peer review · adversarial weighting 30%
> **Status**: ☐ Pending · ☐ In progress · ☐ Complete

## 핵심 평가 관점
이 reviewer는 학술 주장은 부차적으로 보고, **재현성·코드 품질·CI/CD·테스트 커버리지**를 본다. "1-command 재현"이 가능한가, requirements pin 되어 있는가, type hint coverage, pytest coverage가 충족되는가가 핵심.

## Reading list
| 우선순위 | 파일 |
|---------|------|
| ⭐ P0 | `src/run_all.py`, `src/stage1_extract/llm_smoke_test.py` |
| ⭐ P0 | `src/stage2_graph/rgat.py`, `src/viz/publication_figures.py` |
| ⭐ P0 | `Makefile`, `Dockerfile`, `.github_workflows_to_install_manually/` |
| ⭐ P0 | `requirements.txt`, `pyproject.toml` (없으면 issue) |
| P1 | `tests/` (있으면) |
| P1 | `RUN_REPORT.md` |

## Adversarial 검토 8가지
1. **pytest 실제 테스트 부재** — `tests/` 폴더 자체가 없거나 비어있음. coverage 0%
2. **requirements.txt 비-pinned** — 모든 dependency가 `>=X.Y.Z` 표기, lockfile 없음
3. **Type hint coverage 미측정** — mypy / pyright 통과 여부 미입증
4. **Master orchestrator subprocess 구조의 fragility** — 이전 세션에서 `python -m src.run_all` hang 관찰. subprocess 호출 대신 직접 import 권장
5. **GitHub Actions 미설치** — workflow 파일이 `.github_workflows_to_install_manually/`에 staged. 실제 CI 작동 미확인
6. **LLM provider 호출의 retry/backoff 부재** — rate limit 시 graceful degradation 미구현
7. **Bayesian PyMC 의존성 optional** — fallback NumPy ML이 PyMC와 정확히 동등하지 않음에도 같은 출력 형식
8. **Docker image build 미테스트** — Dockerfile은 있으나 actual build pass 여부 미확인

## Rubric (D2 + D5가 핵심)

| Dim | Score | Justification |
|-----|-------|---------------|
| D1 Theoretical contribution | __/5 | |
| D2 Methodological rigor (engineering) ⭐ | __/5 | |
| D3 Empirical robustness | __/5 | |
| D4 Honesty / framing | __/5 | |
| D5 Reproducibility ⭐ | __/5 | |
| D6 Practical / policy | __/5 | |
| D7 Literature integration | __/5 | |
| D8 Writing quality (code documentation) | __/5 | |
| D9 Novelty argument | __/5 | |
| D10 Submission readiness | __/5 | |
| **Total** | **__/50** | |

## 작성 시
### Top 3 strengths / weaknesses
### Most likely reject reason at JOSS / Software Impacts
### Worst code smell
### Required revisions (P0/P1/P2)
### Venue recommendation
☐ Top SE (ICSE / FSE) ☐ JOSS (Journal of Open Source Software) ☐ Software Impacts ☐ GitHub release only ☐ Reject
**Reasoning**:
### Open questions

---
*Reviewer signature*: R5 SE Persona · Simulated peer review.
