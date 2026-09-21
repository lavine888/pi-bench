"""Credential-free deterministic smoke of tau2 orchestration, tools and grading.

This is plumbing validation, not an LLM benchmark result.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from tau2.agent.llm_agent import LLMAgentState, LLMSoloAgent
from tau2.data_model.message import AssistantMessage, ToolCall
from tau2.evaluator.evaluator import EvaluationType
from tau2.orchestrator.orchestrator import Orchestrator
from tau2.registry import registry
from tau2.run import get_tasks, run_simulation
from tau2.user.user_simulator import DummyUser


class DeterministicMockAgent(LLMSoloAgent):
    """Script the expected mock-domain tool call without invoking an LLM."""

    def generate_next_message(self, message, state: LLMAgentState):
        if message is None:
            reply = AssistantMessage(
                role="assistant",
                tool_calls=[ToolCall(id="local-smoke-create", name="create_task", arguments={"user_id": "user_1", "title": "Important Meeting"})],
                cost=0.0,
                usage={"prompt_tokens": 0, "completion_tokens": 0},
            )
        else:
            state.messages.append(message)
            reply = AssistantMessage(role="assistant", content=self.STOP_TOKEN, cost=0.0, usage={"prompt_tokens": 0, "completion_tokens": 0})
        state.messages.append(reply)
        return reply, state


def main() -> None:
    task = get_tasks("mock", task_ids=["create_task_1"])[0]
    environment = registry.get_env_constructor("mock")(solo_mode=True)
    agent = DeterministicMockAgent(environment.get_tools(), environment.get_policy(), task, "local/deterministic", {})
    orchestrator = Orchestrator(domain="mock", agent=agent, user=DummyUser(), environment=environment, task=task, max_steps=10, seed=300, solo_mode=True)
    result = run_simulation(orchestrator, evaluation_type=EvaluationType.ENV)
    payload = {
        "kind": "credential-free-plumbing-smoke",
        "disclaimer": "Deterministic scripted agent; not an LLM benchmark score.",
        "timestamp": datetime.now(UTC).isoformat(),
        "domain": "mock",
        "task_id": result.task_id,
        "termination_reason": result.termination_reason.value,
        "reward": result.reward_info.reward,
        "steps": len(result.get_messages()),
        "tool_calls": sum(len(getattr(m, "tool_calls", None) or []) for m in result.get_messages()),
        "trajectory": [m.model_dump(mode="json", exclude={"raw_data"}) for m in result.get_messages()],
    }
    root = Path(__file__).resolve().parents[1]
    output = root / "experiments" / "smoke" / "local_mock_result.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in payload.items() if k != "trajectory"}, indent=2))
    assert payload["reward"] == 1.0
    assert payload["tool_calls"] >= 1


if __name__ == "__main__":
    main()
