# Current State

## Working

- Isolated τ³ core installation with Python 3.12.13
- Native `intro`, `check-data`, and CLI help
- PI-Bench config, experiment runner, retrying farm, provider mapping, status, and result/token aggregation
- Credential-free mock trajectory through official orchestrator, tool environment, and grader

## Running

- Nothing; execution is credential-gated.

## Completed

- Environment inspection and report
- Target repository and upstream clone
- Exact upstream revision capture
- Core dependency installation and Windows compatibility fixes
- OpenAI-compatible LiteLLM argument wiring
- Mock `create_task_1`: reward 1.0, one real tool call, three trajectory messages
- 23 relevant upstream tests passed (18 + 5 selections)

## Failed

- Initial core CLI import lacked `websockets`; repaired in bootstrap.
- Initial Windows check-data output used GBK; repaired with `PYTHONUTF8=1`.

## Blockers

- Missing `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `AGENT_MODEL`, and `USER_MODEL`.
- A real simulation can incur provider charges and therefore was not started without authorization/credentials.

## Current Metrics

- simulations: 1 credential-free plumbing validation (0 model benchmark simulations)
- tokens: 0
- requests: 0
- pass rate: 100% plumbing smoke; n/a for LLM benchmark
- concurrency: 0
- runtime: 0

## Next 3 Actions

1. Add credentials to ignored `.env` and run one retail task.
2. Run the five-task smoke and verify tool calls/reward/trajectory/token usage/native view.
3. Commit smoke evidence, then ramp retail to 2 concurrency.
