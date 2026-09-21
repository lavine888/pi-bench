# PI-Bench

**Autonomous Agent Evaluation Farm powered by τ³-bench.**

Run, stress-test and analyze thousands of real-world Agent ↔ User ↔ Tool interactions.

## What It Does

PI-Bench is a thin, resilient orchestration and evidence layer over the official `tau2` CLI. It schedules real simulations, preserves upstream trajectories locally, aggregates provider-reported token usage, retries failed batches, and publishes compact benchmark summaries.

## Architecture

`PI-Bench runner → official tau2 CLI → Agent ↔ User Simulator ↔ Domain Tools → reward/review → summaries`

It does not reimplement the benchmark engine.

## Quick Start

Requirements: Git, [uv](https://docs.astral.sh/uv/), and Python 3.12–3.13 (uv installs an isolated compatible Python).

```bash
git clone https://github.com/lavine888/pi-bench.git
cd pi-bench
./scripts/bootstrap.sh                 # Windows: .\scripts\bootstrap.ps1
cp .env.example .env
```

## Configure Model API

Credentials are environment-only. For an OpenAI-compatible API:

```dotenv
OPENAI_API_KEY=...
OPENAI_BASE_URL=https://provider.example/v1
AGENT_MODEL=openai/provider-model-name
USER_MODEL=openai/provider-model-name
REVIEW_MODEL=openai/provider-model-name
```

The `openai/` prefix tells LiteLLM to use its OpenAI-compatible adapter. Never commit `.env`.

## Run One Experiment

```bash
python -m runner.run_experiment --config configs/smoke.yaml
```

The smoke config runs five retail tasks, one trial, concurrency one, max 100 steps, verbose logs, and auto-resume. Raw results remain under `_external/tau2-bench/data/simulations/`.

## Run Agent Farm

```bash
python -m runner.run_farm --domains retail airline telecom --trials 3 --tasks 20 --concurrency 4 --auto-review
python -m runner.run_farm --duration 24h --continuous --domains retail airline telecom --trials 3 --tasks 50 --concurrency 8 --auto-review
```

The farm gives every batch a unique ID and retries failed subprocesses with exponential backoff. Start at concurrency 1 and ramp conservatively within provider RPM/TPM limits.

## View Dashboard / Status

```bash
python -m runner.status
cd _external/tau2-bench && uv run tau2 view
```

A web dashboard is intentionally deferred until real runs exist; native `tau2 view` is the fastest trajectory UI.

## Results

- `results/latest.json`: latest aggregate metrics
- `results/leaderboard.csv`: append-only experiment summary
- `results/token-usage.jsonl`: provider-reported per-call usage (local by default)
- `docs/RESULTS.md`: publishable narrative

## Token Usage

PI-Bench reads actual `usage` attached by τ³/LiteLLM to trajectory messages. Missing usage remains missing; it is never represented as an estimate. Input, output, cached, reasoning, latency, role, task, and trial fields are normalized where the provider supplies them.

## Reliability Experiments

The subprocess boundary provides crash isolation, timeout enforcement through τ³, retries, backoff, and resume. Planned fault injection covers process kills, API timeouts, tool failures, interruptions, worker restarts, and interrupted writes.

## Upstream

PI-Bench builds on [sierra-research/tau2-bench](https://github.com/sierra-research/tau2-bench), currently τ³-bench. It is cloned at bootstrap rather than vendored. See `results/upstream-version.json` for the exact tested revision and `upstream/README.md` for attribution. Upstream licensing applies to upstream code and data.
