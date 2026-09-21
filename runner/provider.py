from __future__ import annotations

import json
import os

from .config import load_dotenv


def provider_settings() -> tuple[str, str, str, dict]:
    """Return agent model, user model, reviewer model and safe LiteLLM args."""
    load_dotenv()
    default = os.getenv("MODEL_NAME", "")
    agent = os.getenv("AGENT_MODEL", default)
    user = os.getenv("USER_MODEL", default)
    reviewer = os.getenv("REVIEW_MODEL", default)
    if not agent or not user:
        raise RuntimeError("Set AGENT_MODEL and USER_MODEL (or MODEL_NAME) in the environment/.env")
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required")
    args: dict[str, str] = {}
    if base := os.getenv("OPENAI_BASE_URL"):
        args["api_base"] = base.rstrip("/")
    return agent, user, reviewer, args


def llm_args_json(args: dict) -> str:
    return json.dumps(args, separators=(",", ":"))
