# PI-Bench Results

## Credential-free mock validation

A deterministic agent completed the official mock task `create_task_1` through the real τ³ half-duplex orchestrator, environment tool execution, and environment grader.

- Reward: **1.0**
- Tool calls: **1** (`create_task`)
- Trajectory messages: **3**
- Termination: `agent_stop`
- Automated upstream tests: **23 passed** across mock tools, environment/run loading, dummy user, and orchestrator initialization/solo paths

Artifact: `experiments/smoke/local_mock_result.json`.

This validates benchmark plumbing only and is deliberately excluded from model leaderboard/token metrics because the agent was scripted and used zero LLM tokens. No paid API run has been executed. See `results/latest.json` and `docs/ENVIRONMENT_REPORT.md` for the credential blocker.
