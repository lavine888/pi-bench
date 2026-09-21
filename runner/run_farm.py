from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict
from datetime import UTC, datetime, timedelta
from pathlib import Path

from .config import ExperimentConfig, ROOT
from .run_experiment import run


def failure(event: dict) -> None:
    event["timestamp"] = datetime.now(UTC).isoformat()
    path = ROOT / "logs" / "failures.jsonl"; path.parent.mkdir(exist_ok=True)
    with path.open("a", encoding="utf-8") as f: f.write(json.dumps(event) + "\n")


def main() -> None:
    p = argparse.ArgumentParser(description="PI-Bench resilient tau2 farm")
    p.add_argument("--domains", nargs="+", default=["retail"])
    p.add_argument("--trials", type=int, default=3); p.add_argument("--tasks", type=int, default=20)
    p.add_argument("--concurrency", type=int, default=4); p.add_argument("--max-steps", type=int, default=100)
    p.add_argument("--retries", type=int, default=2); p.add_argument("--auto-review", action="store_true")
    p.add_argument("--continuous", action="store_true"); p.add_argument("--duration", help="e.g. 24h")
    args = p.parse_args()
    deadline = None
    if args.duration:
        hours = float(args.duration.removesuffix("h")); deadline = datetime.now(UTC) + timedelta(hours=hours)
    cycle = 0
    while True:
        for domain in args.domains:
            if deadline and datetime.now(UTC) >= deadline: return
            cfg = ExperimentConfig(domain, args.tasks, args.trials, args.concurrency, args.max_steps, auto_review=args.auto_review)
            experiment_id = f"{domain}_t{args.tasks}_r{args.trials}_c{args.concurrency}_cycle{cycle}_{datetime.now(UTC):%Y%m%dT%H%M%SZ}"
            for attempt in range(args.retries + 1):
                try:
                    run(cfg, experiment_id); break
                except Exception as exc:
                    failure({"experiment_id": experiment_id, "domain": domain, "attempt": attempt, "status": "RETRYING" if attempt < args.retries else "FAILED", "error": str(exc)})
                    if attempt == args.retries: break
                    time.sleep(min(60, 2 ** attempt * 5))
        cycle += 1
        if not args.continuous: return

if __name__ == "__main__": main()
