from __future__ import annotations
import json
from datetime import UTC, datetime
from pathlib import Path


def heartbeat(path: Path, experiment_id: str, status: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"experiment_id": experiment_id, "status": status, "timestamp": datetime.now(UTC).isoformat()}, indent=2) + "\n", encoding="utf-8")
