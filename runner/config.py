from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_dotenv(path: Path = ROOT / ".env") -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass
class ExperimentConfig:
    domain: str
    tasks: int = 5
    trials: int = 1
    concurrency: int = 1
    max_steps: int = 100
    timeout: int = 900
    seed: int = 300
    verbose_logs: bool = True
    auto_resume: bool = True
    auto_review: bool = False

    @classmethod
    def from_yaml(cls, path: str | Path) -> "ExperimentConfig":
        data: dict[str, Any] = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        return cls(**data)
