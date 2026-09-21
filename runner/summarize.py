from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .config import ROOT


def _walk_messages(sim: dict) -> list[dict]:
    if sim.get("messages") is not None:
        return sim["messages"]
    out = []
    for tick in sim.get("ticks") or []:
        for key in ("agent_chunk", "user_chunk"):
            if tick.get(key): out.append(tick[key])
        for key in ("agent_tool_results", "user_tool_results"):
            out.extend(tick.get(key) or [])
    return out


def _usage(message: dict) -> tuple[int, int, int | None, int | None]:
    u = message.get("usage") or {}
    inp = int(u.get("prompt_tokens", u.get("input_tokens", 0)) or 0)
    out = int(u.get("completion_tokens", u.get("output_tokens", 0)) or 0)
    details = u.get("prompt_tokens_details") or u.get("input_tokens_details") or {}
    output_details = u.get("completion_tokens_details") or u.get("output_tokens_details") or {}
    return inp, out, details.get("cached_tokens"), output_details.get("reasoning_tokens")


def summarize_result(path: Path, experiment_id: str, domain: str, model: str, runtime: float, concurrency: int) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    sims = data.get("simulations", [])
    inp = out = requests = tool_calls = 0
    usage_rows = []
    rewards, steps = [], []
    for sim in sims:
        messages = _walk_messages(sim)
        steps.append(len(messages))
        reward = ((sim.get("reward_info") or {}).get("reward"))
        if reward is not None: rewards.append(float(reward))
        for msg in messages:
            i, o, cached, reasoning = _usage(msg)
            if i or o:
                requests += 1; inp += i; out += o
                role = "agent" if msg.get("role") == "assistant" else "user"
                usage_rows.append({"timestamp": msg.get("timestamp") or datetime.now(UTC).isoformat(), "experiment_id": experiment_id, "domain": domain, "task_id": sim.get("task_id"), "trial": sim.get("trial"), "role": role, "model": model, "input_tokens": i, "output_tokens": o, "total_tokens": i + o, "cached_tokens": cached, "reasoning_tokens": reasoning, "latency_ms": round(float(msg.get("generation_time_seconds") or 0) * 1000), "status": "success"})
            tool_calls += len(msg.get("tool_calls") or [])
    completed = len(sims); successful = sum(r > 0 for r in rewards)
    summary = {"runtime_seconds": round(runtime, 2), "requests": requests, "total_tokens": inp + out, "input_tokens": inp, "output_tokens": out, "tokens_per_minute": round((inp + out) / runtime * 60, 2) if runtime else 0, "completed_simulations": completed, "successful_simulations": successful, "failed_simulations": completed - successful, "tool_calls": tool_calls}
    results = ROOT / "results"; results.mkdir(exist_ok=True)
    with (results / "token-usage.jsonl").open("a", encoding="utf-8") as f:
        for row in usage_rows: f.write(json.dumps(row) + "\n")
    (results / "latest.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    leaderboard = results / "leaderboard.csv"
    fields = ["experiment_id","domain","model","tasks","trials","seed","concurrency","completed","pass_rate","avg_reward","avg_steps","requests","input_tokens","output_tokens","total_tokens","runtime_seconds","tokens_per_minute","errors","timestamp"]
    row = {"experiment_id": experiment_id,"domain": domain,"model": model,"tasks": len(data.get("tasks", [])),"trials": max((s.get("trial") or 0 for s in sims), default=0) + 1,"seed": (sims[0].get("seed") if sims else ""),"concurrency": concurrency,"completed": completed,"pass_rate": successful/completed if completed else 0,"avg_reward": sum(rewards)/len(rewards) if rewards else 0,"avg_steps": sum(steps)/len(steps) if steps else 0,**{k: summary[k] for k in ("requests","input_tokens","output_tokens","total_tokens","runtime_seconds","tokens_per_minute")},"errors": completed-len(rewards),"timestamp": datetime.now(UTC).isoformat()}
    with leaderboard.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if f.tell() == 0: writer.writeheader()
        writer.writerow(row)
    return summary
