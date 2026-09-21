$ErrorActionPreference='Stop'
$Root=Resolve-Path "$PSScriptRoot\.."
New-Item -ItemType Directory -Force "$Root\_external" | Out-Null
if (!(Test-Path "$Root\_external\tau2-bench\.git")) { git clone https://github.com/sierra-research/tau2-bench.git "$Root\_external\tau2-bench" }
Push-Location "$Root\_external\tau2-bench"; uv sync; uv pip install websockets; $env:PYTHONUTF8='1'; uv run tau2 check-data; Pop-Location
