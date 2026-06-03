---
name: ai-scientist-v2
description: Operate and troubleshoot the local AI-Scientist-v2 / AI Scientist Cloud project at /home/qiao/dockerai/AI-Scientist-v2. Use when the user asks to run AI-Scientist-v2, generate or manage research ideas, launch BFTS paper-generation experiments, configure OpenAI/Semantic Scholar keys, use the Streamlit AI Scientist Cloud console, inspect experiment outputs/logs/PDFs/reviews, debug this project’s launcher/web app/configuration, or run paper queries/citation searches that should use the s2-api skill with S2_API_KEY from /home/qiao/dockerai/AI-Scientist-v2/.env.
---

# AI-Scientist-v2

## Project root

Default local project: `/home/qiao/dockerai/AI-Scientist-v2`.

Always run commands from that directory unless the user gives a different checkout. Treat this project as an autonomous code-execution system: prefer sandboxed/container execution, avoid exposing secrets, and do not run expensive experiments without confirming model, idea file, cost/timeout, and whether writeup/review should run.

For detailed command recipes and file map, read `references/project-guide.md`.

## Fast workflow

1. **Check readiness**
   - Verify `.env` or environment variables for `OPENAI_API_KEY`; use `S2_API_KEY` for higher-throughput Semantic Scholar literature search.
   - Use `AI_SCIENTIST_MODEL` as the default model for ideation when `--model` is omitted.
   - Inspect `bfts_config.yaml` before long runs; the effective BFTS knobs live under `agent`, `agent.stages`, `agent.multi_seed_eval`, and `agent.search`.

2. **Generate ideas**
   - Input is a topic/workshop Markdown file with title/keywords/TL;DR/abstract-style scope.
   - Run `ai_scientist/perform_ideation_temp_free.py`; it writes a same-stem `.json` idea file.
   - The ideation script performs Semantic Scholar searches through `ai_scientist/tools/semantic_scholar.py`; for paper/literature queries, use the `s2-api` skill and load `S2_API_KEY` from `/home/qiao/dockerai/AI-Scientist-v2/.env`. Report rate-limit/key problems clearly.

3. **Run a BFTS experiment**
   - Use `launch_scientist_bfts.py --load_ideas <ideas.json> --idea_idx <n> --model <model>`.
   - Add `--skip_writeup` for faster debugging; add/omit `--skip_review` based on whether the user wants auto-review.
   - Use `--load_code` only when a same-stem `.py` file should seed the experiment.

4. **Inspect results**
   - Runs create timestamped directories under `experiments/`.
   - Look for `logs/0-run/unified_tree_viz.html`, `experiment_results/`, PDFs, `review_text.txt`, `review_img_cap_ref.json`, and `token_tracker*.json`.
   - Report exact paths and last meaningful log lines when diagnosing failures.

5. **Use the web console**
   - Launch with `bash run_web.sh --port 8501 --host 127.0.0.1`.
   - The Streamlit console manages ideas, background jobs, BFTS config, papers/reviews, API registrations, verification keys, and API settings.
   - Bind to `0.0.0.0` only behind HTTPS/auth; set `AI_SCIENTIST_APP_PASSWORD` and/or access-key gating for public/internal testing.

## Safety and operations

- This project executes LLM-written Python. Confirm before running jobs that can spawn long GPU/LLM workloads.
- Never print full API keys, `API_ACCESS_KEY_FERNET`, encrypted tokens, or full verification-key pools. Distribute only plaintext `ASIC-TST-...` verification keys when explicitly requested.
- Do not kill unrelated host processes. The launcher only terminates child processes spawned by the current run; keep that behavior.
- If Semantic Scholar returns 401/429/TLS/network errors, explain the cause and suggest checking `S2_API_KEY`, rate limits, CA/proxy/VPN, or skipping citation-heavy stages.

## Common user intents

- “Generate ideas for X” → create/check a Markdown topic file, run ideation, inspect the generated JSON.
- “Run AI Scientist on this idea” → confirm cost/model/runtime, adjust `bfts_config.yaml` if needed, run launcher, stream logs.
- “Open the cloud UI” → run `run_web.sh`, then share localhost URL.
- “Why did my run fail?” → inspect `_web_jobs/*.log` or experiment `logs/`, dependencies, API auth, CUDA/GPU state, and writeup/review artifacts.
- “Paper query / citations” → invoke the `s2-api` skill and query Semantic Scholar with `S2_API_KEY` loaded from `/home/qiao/dockerai/AI-Scientist-v2/.env`; fall back to other paper-search skills only if S2 is unavailable or insufficient.
