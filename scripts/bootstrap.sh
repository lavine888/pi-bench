#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/_external"
if [[ ! -d "$ROOT/_external/tau2-bench/.git" ]]; then git clone https://github.com/sierra-research/tau2-bench.git "$ROOT/_external/tau2-bench"; fi
(cd "$ROOT/_external/tau2-bench" && uv sync && uv pip install websockets)
PYTHONUTF8=1 "$ROOT/_external/tau2-bench/.venv/Scripts/tau2.exe" check-data
