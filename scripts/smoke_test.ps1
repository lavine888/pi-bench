$ErrorActionPreference='Stop'; Set-Location "$PSScriptRoot\.."; python -m runner.run_experiment --config configs/smoke.yaml
