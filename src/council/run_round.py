"""Run one CINA council round via Anthropic API.

This is the CLI-driven alternative to Claude Code's interactive /cina-council-round.
Uses the Anthropic API directly to invoke each agent role in sequence (Phases A–E).

Usage:
    python -m src.council.run_round --round next
    python -m src.council.run_round --round 3 --phases A,B,C,D,E
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from anthropic import AsyncAnthropic

from . import state_manager as sm

ROOT = Path(__file__).resolve().parent.parent.parent
AGENTS_DIR = ROOT / ".claude" / "agents"


def load_agent_prompt(name: str) -> str:
    path = AGENTS_DIR / f"{name}.md"
    text = path.read_text(encoding="utf-8")
    # Strip frontmatter
    if text.startswith("---"):
        parts = text.split("---", 2)
        return parts[2].strip() if len(parts) >= 3 else text
    return text


AGENT_MODELS = {
    "team-lead": "claude-opus-4-7",
    "policy-data-collector": "claude-sonnet-4-6",
    "data-refinement-analyst": "claude-sonnet-4-6",
    "policy-science-professor": "claude-opus-4-7",
    "ir-political-professor": "claude-opus-4-7",
}


async def invoke_agent(
    client: AsyncAnthropic, name: str, user_prompt: str, max_tokens: int = 4000
) -> dict:
    system = load_agent_prompt(name)
    model = AGENT_MODELS[name]
    t0 = time.time()
    msg = await client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user_prompt}],
    )
    dt = time.time() - t0
    return {
        "agent": name,
        "model": model,
        "text": msg.content[0].text,
        "input_tokens": msg.usage.input_tokens,
        "output_tokens": msg.usage.output_tokens,
        "latency_sec": dt,
    }


def build_kickoff_prompt(round_n: int) -> str:
    state = sm.read()
    return f"""You are starting Round {round_n} of the CINA council.

STATE:
{state.model_dump_json(indent=2)}

HEEDO DIRECTIVES (permanent constitution):
{json.dumps(state.heedo_directives, ensure_ascii=False, indent=2)}

Your job for Phase A:
1. Identify the 5 gaps (data/theory/method/eval/narrative).
2. Write 4 task files under council_sessions/round_{round_n}/tasks/
   - collector_task.md
   - refinement_task.md
   - policy_prof_task.md
   - ir_prof_task.md
3. Return a kickoff summary (≤200 words) listing each gap and assigned agent.

The task files must follow this template:
---
assigned_to: <agent>
round: {round_n}
priority: high|medium|low
depends_on: [...]
---

## 목적
## 구체 산출물 (checklist)
## 품질 기준
## 제공된 컨텍스트

---

Write the actual task files to disk now and return the kickoff summary.
"""


async def phase_a(client: AsyncAnthropic, round_n: int) -> dict:
    sm.create_round_dir(round_n)
    prompt = build_kickoff_prompt(round_n)
    result = await invoke_agent(client, "team-lead", prompt, max_tokens=3500)
    # In practice the team-lead should write files itself; here we log its output
    (sm.COUNCIL_DIR / f"round_{round_n}" / "tasks" / "_kickoff_output.md").write_text(
        result["text"], encoding="utf-8"
    )
    return result


async def phase_b(client: AsyncAnthropic, round_n: int) -> list[dict]:
    task_dir = sm.COUNCIL_DIR / f"round_{round_n}" / "tasks"
    collector_task = (task_dir / "collector_task.md").read_text(encoding="utf-8") if (task_dir / "collector_task.md").exists() else "(no task file; proceed with defaults)"
    refine_task = (task_dir / "refinement_task.md").read_text(encoding="utf-8") if (task_dir / "refinement_task.md").exists() else "(no task file; proceed with defaults)"

    collector_prompt = f"Round {round_n} task:\n\n{collector_task}\n\nExecute and write outputs to council_sessions/round_{round_n}/data_collection/."
    refine_prompt = f"Round {round_n} task:\n\n{refine_task}\n\nExecute and write outputs to council_sessions/round_{round_n}/refinement/."

    results = await asyncio.gather(
        invoke_agent(client, "policy-data-collector", collector_prompt, max_tokens=3500),
        invoke_agent(client, "data-refinement-analyst", refine_prompt, max_tokens=3500),
    )
    out_dir = sm.COUNCIL_DIR / f"round_{round_n}"
    (out_dir / "data_collection" / "_agent_output.md").write_text(results[0]["text"], encoding="utf-8")
    (out_dir / "refinement" / "_agent_output.md").write_text(results[1]["text"], encoding="utf-8")
    return results


async def phase_c(client: AsyncAnthropic, round_n: int) -> list[dict]:
    task_dir = sm.COUNCIL_DIR / f"round_{round_n}" / "tasks"
    pol_task = (task_dir / "policy_prof_task.md").read_text(encoding="utf-8") if (task_dir / "policy_prof_task.md").exists() else ""
    ir_task = (task_dir / "ir_prof_task.md").read_text(encoding="utf-8") if (task_dir / "ir_prof_task.md").exists() else ""

    data_col = (sm.COUNCIL_DIR / f"round_{round_n}" / "data_collection" / "_agent_output.md").read_text(encoding="utf-8")
    refine_col = (sm.COUNCIL_DIR / f"round_{round_n}" / "refinement" / "_agent_output.md").read_text(encoding="utf-8")

    ctx = f"\n\nCURRENT ROUND DATA COLLECTION OUTPUT:\n{data_col}\n\nCURRENT ROUND REFINEMENT OUTPUT:\n{refine_col}\n"

    pol_prompt = f"Round {round_n} task:\n\n{pol_task}{ctx}\n\nWrite critique to council_sessions/round_{round_n}/policy_science/critique.md."
    ir_prompt = f"Round {round_n} task:\n\n{ir_task}{ctx}\n\nWrite critique to council_sessions/round_{round_n}/ir_political/critique.md."

    results = await asyncio.gather(
        invoke_agent(client, "policy-science-professor", pol_prompt, max_tokens=4500),
        invoke_agent(client, "ir-political-professor", ir_prompt, max_tokens=4500),
    )
    out_dir = sm.COUNCIL_DIR / f"round_{round_n}"
    (out_dir / "policy_science" / "critique.md").write_text(results[0]["text"], encoding="utf-8")
    (out_dir / "ir_political" / "critique.md").write_text(results[1]["text"], encoding="utf-8")
    return results


async def phase_d_e(client: AsyncAnthropic, round_n: int, prior_results: list[dict]) -> dict:
    out_dir = sm.COUNCIL_DIR / f"round_{round_n}"
    pol_crit = (out_dir / "policy_science" / "critique.md").read_text(encoding="utf-8")
    ir_crit = (out_dir / "ir_political" / "critique.md").read_text(encoding="utf-8")

    prompt = f"""Phase D + E for Round {round_n}.

POLICY SCIENCE CRITIQUE:
{pol_crit}

IR CRITIQUE:
{ir_crit}

Your tasks:
1. Write synthesis/cross_review.md — agreements, disagreements, decisions.
2. Evaluate 5 quality gates (G1-G5); output synthesis/quality_gates.json.
3. Write LEAD_REPORT.md for this round following docs/10 §2.5 template.
4. Recommend next round focus or signal convergence.

Return the LEAD_REPORT text directly as your final message.
"""
    result = await invoke_agent(client, "team-lead", prompt, max_tokens=3500)
    (out_dir / "LEAD_REPORT.md").write_text(result["text"], encoding="utf-8")
    return result


def estimate_cost(results: list[dict]) -> float:
    # Rough Anthropic pricing: opus $15/M in, $75/M out; sonnet $3/M in, $15/M out
    total = 0.0
    for r in results:
        if "opus" in r["model"]:
            total += r["input_tokens"] / 1e6 * 15 + r["output_tokens"] / 1e6 * 75
        else:
            total += r["input_tokens"] / 1e6 * 3 + r["output_tokens"] / 1e6 * 15
    return total


async def run_round_async(round_n: int, phases: list[str]) -> None:
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    client = AsyncAnthropic()
    all_results: list[dict] = []
    t0 = time.time()

    if "A" in phases:
        print(f"[Round {round_n}] Phase A: team-lead kickoff")
        a = await phase_a(client, round_n)
        all_results.append(a)
    if "B" in phases:
        print(f"[Round {round_n}] Phase B: data agents (parallel)")
        b = await phase_b(client, round_n)
        all_results.extend(b)
    if "C" in phases:
        print(f"[Round {round_n}] Phase C: professors (parallel)")
        c = await phase_c(client, round_n)
        all_results.extend(c)
    if "D" in phases or "E" in phases:
        print(f"[Round {round_n}] Phase D+E: team-lead synthesis + report")
        d = await phase_d_e(client, round_n, all_results)
        all_results.append(d)

    duration_min = (time.time() - t0) / 60
    cost = estimate_cost(all_results)
    llm_calls = {}
    for r in all_results:
        llm_calls[r["agent"]] = llm_calls.get(r["agent"], 0) + 1

    sm.finalize_round(
        round_n=round_n,
        outcome=f"phases={','.join(phases)}",
        llm_calls=llm_calls,
        cost_usd=cost,
        duration_min=duration_min,
    )
    print(f"[Round {round_n}] done. Cost ${cost:.2f}, duration {duration_min:.1f} min")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", default="next", help="round number or 'next'")
    ap.add_argument("--phases", default="A,B,C,D,E")
    args = ap.parse_args()

    if args.round == "next":
        state = sm.read()
        round_n = state.current_round + 1
    else:
        round_n = int(args.round)

    phases = [p.strip().upper() for p in args.phases.split(",")]
    asyncio.run(run_round_async(round_n, phases))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
