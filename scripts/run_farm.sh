#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m runner.run_farm "$@"
