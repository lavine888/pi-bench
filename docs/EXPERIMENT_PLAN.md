# Experiment Plan

1. Credential-gated retail smoke: 1 task, then 5 tasks at concurrency 1.
2. Retail: `t10_r2_c2`, then `t25_r3_c4`.
3. Retail, airline, telecom: at least 20 tasks × 3 trials.
4. Run `tau2 review` after stable batches.
5. Ramp concurrency 1 → 2 → 4 → 8 only while provider error and 429 rates remain acceptable.
6. Enable banking only with knowledge extras and retain upstream version metadata.

Raw trajectories stay local under `_external/tau2-bench/data/simulations`; only aggregate evidence and selected redacted samples are committed.
