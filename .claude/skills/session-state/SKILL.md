---
name: session-state
description: CINA 협의체의 세션 간 지속성 관리. council_sessions/state.json 읽기·쓰기·요약, 라운드 초기화, 장기 컨텍스트 압축. 세션이 재시작되어도 협의체가 이어지도록 하는 인프라 skill.
---

# Session State Management Skill

## 목적

Claude Code 세션은 재시작되거나 컨텍스트가 truncate될 수 있다. CINA 협의체는 여러 라운드에 걸쳐 누적 작업하므로, **파일 기반 지속성**이 필수다. 이 skill은 그 인프라를 담당한다.

## 주요 작업

### 1. 초기 상태 생성 (`init`)
`council_sessions/` 디렉토리 전체 초기화:
```
council_sessions/
├── state.json              # 현재 라운드, gate 상태
├── LEDGER.md               # append-only 라운드 기록
├── README.md               # 사용법
└── round_1/                # 첫 라운드 디렉토리 (빈)
    └── tasks/
```

초기 `state.json`:
```json
{
  "project": "CINA",
  "framework_version": "2.0",
  "current_round": 0,
  "rounds_completed": [],
  "active_tasks": {},
  "quality_gates": {
    "G1_data_coverage": {"status": "not_started", "value": null},
    "G2_evidence_grounding": {"status": "not_started", "value": null},
    "G3_theory_grounding": {"status": "not_started", "value": null},
    "G4_dual_review": {"status": "not_started", "value": null},
    "G5_heedo_alignment": {"status": "not_started", "value": null}
  },
  "blocked_on": null,
  "next_action": "Team-lead to assign round 1 tasks",
  "created_at": "ISO-now",
  "updated_at": "ISO-now",
  "convergence_signal": {"consecutive_no_new_gap": 0, "max_reached": 1}
}
```

### 2. 상태 읽기 (`read`)
```python
state = json.loads(Path("council_sessions/state.json").read_text())
```
반환 시 편의 method:
- `state.current_round`
- `state.gate_summary()` → `"G1:pass, G2:pending, ..."`
- `state.is_blocked()` → bool

### 3. 원자적 갱신 (`update`)
```python
def atomic_update(patch: dict):
    path = Path("council_sessions/state.json")
    state = json.loads(path.read_text())
    deep_merge(state, patch)
    state["updated_at"] = now_iso()
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    tmp.replace(path)  # atomic rename
```

권한: 이 skill만 state.json을 직접 수정. 다른 skill/agent는 이 skill 경유.

### 4. 라운드 종료 (`finalize_round`)
입력: round_N 완료 결과
동작:
1. `state.current_round = N`
2. `state.rounds_completed.append({round: N, date, outcome, ...})`
3. `LEDGER.md`에 새 블록 append
4. Convergence signal 업데이트

### 5. 컨텍스트 압축 (`compress`)
에이전트 context가 초과 위험 시:
- 지난 3라운드 LEAD_REPORT만 유지
- 그 이전은 `LEDGER.md` 요약으로 대체
- 장기 결정 사항만 `council_sessions/long_term_decisions.md`로 이관

### 6. 수렴 판정 (`check_convergence`)
```python
def check_convergence(state):
    gates = state["quality_gates"]
    all_pass = all(g["status"] == "pass" for g in gates.values())
    no_new_gap = state["convergence_signal"]["consecutive_no_new_gap"] >= 2
    within_budget = state["current_round"] <= 10
    
    if all_pass and no_new_gap:
        return "converged"
    if not within_budget:
        return "max_rounds"
    if state.get("blocked_on"):
        return f"blocked:{state['blocked_on']}"
    return "in_progress"
```

## 파일 잠금 (Lock)

동시 접근 방지:
```python
from filelock import FileLock
with FileLock("council_sessions/.state.lock", timeout=10):
    # read → modify → write
```

## Schema 검증

매 쓰기 전에 Pydantic 모델로 검증 (`src/council/state_schema.py`):
```python
class QualityGate(BaseModel):
    status: Literal["pass", "fail", "pending", "partial", "not_started"]
    value: float | None = None
    last_evaluated: datetime | None = None

class CouncilState(BaseModel):
    project: str
    framework_version: str
    current_round: int
    rounds_completed: list[dict]
    quality_gates: dict[str, QualityGate]
    blocked_on: str | None
    next_action: str
    created_at: datetime
    updated_at: datetime
    convergence_signal: dict
```

## 공개 API

이 skill이 다른 skill·에이전트에 제공하는 operations:
- `session_state.init()` — 디렉토리 초기화
- `session_state.read()` → CouncilState
- `session_state.update(patch)` — atomic
- `session_state.finalize_round(round_n, outcome)`
- `session_state.compress()` — context 절약
- `session_state.check_convergence()` → str
- `session_state.create_round_dir(n)` — `round_N/` 하위 생성

## 호출 예시

council-orchestrator가 Phase E에서:
```python
session_state.update({
  "current_round": N,
  "quality_gates": gates_result,
  "next_action": "Team-lead to plan round N+1 or declare convergence",
})

status = session_state.check_convergence()
if status == "converged":
    create_final_synthesis()
```

## 실패 모드

- Lock timeout (동시 접근) → 10초 재시도
- Schema 검증 실패 → rollback, 오류 로그
- 파일 손상 → `.backup` 자동 저장 정책 (매 쓰기 전 copy)

## 의존성

Python:
- `filelock`, `pydantic`, `pathlib`

내부:
- 모든 council 관련 skill·에이전트가 이 skill에 의존
- 직접 state.json 조작 금지
