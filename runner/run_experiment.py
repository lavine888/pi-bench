from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

from .config import ExperimentConfig, ROOT
from .provider import llm_args_json, provider_settings
from .summarize import summarize_result

UPSTREAM = ROOT / "_external" / "tau2-bench"


def run(config: ExperimentConfig, experiment_id: str | None = None) -> Path:
    if not (UPSTREAM / "pyproject.toml").exists():
        raise RuntimeError("Upstream missing; run scripts/bootstrap first")
    agent, user, reviewer, llm_args = provider_settings()
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    experiment_id = experiment_id or f"{config.domain}_t{config.tasks}_r{config.trials}_c{config.concurrency}_{stamp}"
    cmd = ["uv", "run", "tau2", "run", "--domain", config.domain,
           "--agent-llm", agent, "--user-llm", user,
           "--num-tasks", str(config.tasks), "--num-trials", str(config.trials),
           "--max-concurrency", str(config.concurrency), "--max-steps", str(config.max_steps),
           "--timeout", str(config.timeout), "--seed", str(config.seed), "--save-to", experiment_id]
    if llm_args:
        encoded = llm_args_json(llm_args)
        cmd += ["--agent-llm-args", encoded, "--user-llm-args", encoded]
    if config.verbose_logs: cmd.append("--verbose-logs")
    if config.auto_resume: cmd.append("--auto-resume")
    if config.auto_review:
        cmd += ["--auto-review", "--review-model", reviewer or agent]
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    log_path = ROOT / "logs" / f"{experiment_id}.log"
    log_path.parent.mkdir(exist_ok=True)
    started = time.monotonic()
    with log_path.open("a", encoding="utf-8") as log:
        # Never log the environment or credentials.
        result = subprocess.run(cmd, cwd=UPSTREAM, env=env, stdout=log, stderr=subprocess.STDOUT)
    result_path = UPSTREAM / "data" / "simulations" / experiment_id / "results.json"
    if result.returncode:
        raise RuntimeError(f"tau2 exited {result.returncode}; inspect {log_path}")
    summarize_result(result_path, experiment_id, config.domain, agent, user, time.monotonic() - started, config.concurrency)
    return result_path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/smoke.yaml")
    p.add_argument("--experiment-id")
    args = p.parse_args()
    print(run(ExperimentConfig.from_yaml(args.config), args.experiment_id))

if __name__ == "__main__": main()
