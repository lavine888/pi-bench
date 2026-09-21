# Troubleshooting

- **Missing model/key:** copy `.env.example` to `.env`; never commit `.env`.
- **OpenAI-compatible endpoint:** use a LiteLLM OpenAI model identifier (often `openai/<model>`) and set `OPENAI_BASE_URL`.
- **UnicodeEncodeError on Windows:** set `PYTHONUTF8=1`.
- **Missing websockets after core sync:** run `uv pip install websockets` in upstream (bootstrap does this).
- **Resume:** rerun with the same experiment ID; `--auto-resume` is enabled.
- **Raw results:** `_external/tau2-bench/data/simulations/<experiment_id>/results.json`.
