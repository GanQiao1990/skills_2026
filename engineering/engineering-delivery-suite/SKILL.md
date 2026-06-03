---
name: engineering-delivery-suite
description: "Umbrella skill for software and systems engineering delivery across backend, frontend, DevOps, SRE, security, data, AI, mobile, embedded, database, architecture, code review, technical writing, and integration specialties. Use for engineering plans, architecture, implementation guidance, debugging, reviews, reliability, security, performance, or technical documentation."
---

# Engineering Delivery Suite

Use this class-level entry for engineering work that does not require a more specialized non-agent skill.

## Core workflow
1. Identify system boundary, users, failure modes, constraints, stack, and deployment context.
2. Choose the smallest safe approach consistent with scalability, security, maintainability, and delivery time.
3. Specify interfaces, data model, tests, observability, rollback, and ownership.
4. Implement/review with evidence: commands run, diffs, test output, risk notes.
5. Document operational behavior and next maintenance hooks.

## Interpreting multi-part user requests
When the user provides a numbered list of requested actions and then says a command like "执行" / "do it" / "proceed", treat the list as cumulative unless they explicitly ask you to choose one option. Do not collapse the list into a single choice request when the natural reading is "perform all of these steps in order".

## Startup topology discovery
Before treating a repository as a conventional frontend/backend app, inspect the actual entrypoints and docs first.

- Check manifests and docs first: `pyproject.toml`, `package.json`, `README*`, Dockerfiles, compose files, and obvious server entrypoints.
- If there is no JS frontend manifest and the docs/Dockerfile point to Jupyter/Notebook/Lab, classify the repo as a notebook/web-app service rather than inventing a separate frontend.
- When a user says “run frontend and backend” but the repo is notebook-centric, explain that the documented runtime is Jupyter Lab/Notebook and launch that service instead of guessing a React/FastAPI split.
- Verify the service with both a listening-port check and an HTTP probe, then report the concrete URL/token or other access handle.
- Jupyter-specific verification pitfall: `/lab` may return `405 Method Not Allowed` to `HEAD` requests even when the service is healthy. Do not treat a failed `curl -I` as a startup failure by itself; prefer a port-listener check plus a normal `GET` probe and accept `302` redirects as healthy.
- Restart workflow pitfall: before trying to kill an old notebook service, poll the tracked background process and separately check whether the port is still bound. If the old process already exited and the port is free, skip straight to launching the replacement instance.

## Subdomains
- **Architecture/backend/frontend/mobile**: APIs, UI implementation, data flow, integration.
- **DevOps/SRE/database/security**: infra, CI/CD, reliability, indexes, threat modeling.
- **AI/data/voice/email/integration**: ML/data pipelines, ASR, email intelligence, Feishu/DingTalk/WeChat.
- **Embedded/FPGA/IoT/driver**: firmware, hardware interfaces, validation.
- **Review/minimal-change/technical writing**: code quality, scoped fixes, docs.

## Python package index mirrors (uv / pip)
When a Python project fails because the default PyPI endpoint is slow or unreachable, prefer a scoped mirror fix before inventing alternative install workflows.

- First prefer project-local `uv.toml` for `uv`-managed repos.
- At the top level of `uv.toml`, use `index-url` and `extra-index-url` for package mirrors.
- Do not use `default-index` as a top-level key in `uv.toml`; that shape is rejected by uv's config parser.
- A practical China-friendly project config is:

```toml
index-url = "https://pypi.tuna.tsinghua.edu.cn/simple"
extra-index-url = ["https://mirrors.aliyun.com/pypi/simple"]
index-strategy = "unsafe-best-match"
```

- After writing the config, verify with a small `uv pip install --dry-run <package> -v` against a package that is not already present in the target environment.
- If the user wants the behavior beyond one repo, also offer a user-level pip config in `~/.config/pip/pip.conf` and a user-level uv config in `~/.config/uv/uv.toml` with the same mirror settings.
- When verifying installs, do not assume the distribution name equals the Python import name. If imports still fail after a successful install, inspect package metadata (for example `importlib.metadata.distribution(...).read_text('top_level.txt')`) before declaring the package missing. Example mappings seen in practice: `fhaviary` installs the `aviary` module, and `fhlmi` installs the `lmi` module.

## Commercializing lightweight research web apps
When a research/prototype app needs to become commercially distributable while preserving its basic architecture, add product-grade seams rather than rewriting the stack: config, auth, database, user-scoped storage, prompt-profile customization, stability limits, docs, and a smoke test. See `references/commercializing-lightweight-research-apps.md` for a compact FastAPI/static-frontend/CLI pattern.

## Environment-file validation (.env / python-dotenv)
When the user asks you to improve or repair a project's `.env`, inspect the code's actual `load_dotenv()` / `os.getenv()` usage before editing the file.

When improving a neighboring repo by borrowing configuration patterns from a better-structured local project, prefer introducing a repo-level YAML config plus early `python-dotenv` loading instead of scattering new environment-variable reads across the launcher. Keep runtime overrides explicit (`--config`, env var for config path), preserve env-over-YAML precedence for sensitive deployment values, and move launch-critical constants into config-backed helpers. See `references/centralized-launch-config-pattern.md`.

- Do not assume every value present in an existing `.env` is actually consumed by the application.
- Normalize malformed YAML-like fragments inside `.env` (for example `api_key: ...`, `base_url: ...`, `model: ...`) into real `KEY=VALUE` lines only if the code actually reads those keys.
- Preserve existing secrets when rewriting the file; improve shape and comments rather than replacing values.
- If the code only auto-reads a small set of variables, keep `.env` focused on those required keys and move optional gateway/model hints into comments unless you are also updating the code to read them.
- For notebook-driven apps, if the user wants a non-default model or OpenAI-compatible gateway, document that `llm_name` / `llm_config` (or the project's equivalent runtime config object) may need to be passed explicitly in notebook/code instead of assuming `.env` alone will change behavior.
- When wiring LiteLLM to an OpenAI-compatible gateway from notebooks/UI, a bare model name may be insufficient. Normalize to a provider-qualified model string when needed (for example `openai/<model>`) so LiteLLM can infer the provider instead of failing with `LLM Provider NOT provided`.
- If a real smoke test reaches the upstream gateway and fails with a server-side 5xx, record that as evidence about current gateway behavior, not as a permanent constraint on the integration pattern. The durable lesson is the configuration shape and verification sequence, not that the gateway is "broken".

## Submission-artifact finalization
When the user asks to improve, repair, finalize, or "完善" an existing output/job directory for a competition or benchmark submission, treat it as an engineering delivery task with a hard artifact contract.

- Inspect the existing final artifacts and validator before changing anything.
- Prefer rerunning the smallest downstream stages that rebuild the final deliverables from cache rather than rerunning the full pipeline.
- Validate both the content contract and the packaged archive contents before declaring success.
- Do not stop at "validator passes" when the artifact encodes domain content such as retrosynthesis routes, evidence tables, or benchmark explanations. Also inspect whether the selected content is semantically meaningful to the user and the task, not merely schema-valid.
- For route-like scientific submissions, watch for a common failure mode: the backend returns a formally valid but overly trivial one-step route (for example a direct coupling from advanced intermediates) because the pipeline prefers minimum step count. If the user flags the route as unhelpful and deeper raw routes already exist in cache/backend output, curate or prefer a more explanatory multi-step route that still passes the validator and preserves the final product exactly.
- When curating a route manually from backend raw output, preserve forward reaction order, keep intermediates explicit, and re-run the downstream scoring/emit/validation steps so the final archive reflects the curated route rather than an untracked ad hoc CSV edit.
- See `references/submission-artifact-contracts.md` for a compact workflow covering CSV/log/ZIP verification and minimal-stage regeneration.

## Multi-entrypoint default drift and single-GPU CLI wrappers
When a repo exposes several ways to run the same workflow (for example CLI pipeline, agent orchestrator, and web/API job submission), inspect and align the defaults across all entrypoints before concluding that a recent optimization is "in place".

## External ecGEM / tuning-asset validation before scientific pipeline runs
When a local optimisation or benchmark repo depends on an upstream model-assets checkout (for example a separate `EnzymeTuning` or GECKO-style data directory), verify the asset root and the model class before launching long phases.

- Do not assume a same-named organism/model `.mat` file is interchangeable with the repo's expected ecGEM assets. A plain GEM may load fine but still produce a degenerate tuning run with zero enzyme metabolites and zero tunable kcat parameters.
- Before calling a kcat-tuning or enzyme-capacity workflow, check for ecGEM structure signals such as protein pseudo-reactions (`prot_`, `draw_prot_`) or a non-zero discovered enzyme-metabolite set. If these are absent, report that the run is structurally not doing real kcat tuning.
- If both XML and MAT versions of an ecGEM are present, prefer the XML/SBML path when MATLAB import fails on whitespace-containing reaction names (for example `protein pseudoreaction`). A whitespace-safe SBML loader can succeed where direct MAT import fails.
- For long benchmark/validation phases that expose no explicit `cores`/`processes` argument, use thread-count environment variables (`OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_NUM_THREADS`) to honour the requested core budget, and run the phase as a tracked background job with completion notification.
- See `references/ecgem-asset-validation.md` for a compact checklist and an EnzymeTuning/iML1515 example.

Also treat API-payload field-name validation as a first-class review item when editing launcher/bootstrap code. A tiny typo in a POST body can break initialization while the surrounding logic looks correct. Check payload keys against the local API reference or live implementation rather than assuming semantically similar names are accepted.

- Do not assume improving `pipeline.py` or a config file automatically updates the API layer or orchestrator defaults.
- If observed runs still use older conservative values, inspect job metadata / launch arguments to confirm which entrypoint actually supplied the parameters.
- Treat default drift as a first-class root cause when results contradict the apparent code defaults.

For external GPU-backed CLI tools that are effectively single-device jobs (for example docking wrappers around Vina-GPU), prefer the wrapper script over the raw binary when the wrapper carries environment setup, argument translation, or CPU fallback logic.

- Put the wrapper ahead of the raw binary in auto-detection order when the wrapper is the safer execution path.
- Do not scale worker count from `cpu_count()` just because the parent process is Python-parallelisable; for single-GPU tools this often creates a storm of avoidable task failures.
- Default GPU worker caps should be explicit and conservative (often 1) unless the specific tool has been verified to support safe concurrent jobs on the available device.
- In scored scientific pipelines, if route / schema validity is already strong but molecule score is weak, prioritize increasing successful docking throughput and candidate survival before further tuning the route stage.

## Long-running optimization / benchmark phases with implicit CPU parallelism
When a scientific optimization or benchmark phase has no explicit `--cores` / `--processes` CLI flag but the user asks to "use N cores", treat thread-level environment variables as the safe default interpretation instead of inventing unsupported arguments.

- First inspect the code for an explicit parallelism parameter. If none exists, use environment variables such as `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, and `NUMEXPR_NUM_THREADS` to request the desired CPU parallelism.
- For runs expected to take many minutes, launch them as tracked background processes with completion notification rather than blocking in the foreground. Poll process state and artifact creation instead of repeatedly restarting a silent long run.
- If a phase writes early setup artifacts (for example model-info and cached search-space files) but not the final summary yet, interpret that as progress unless the process exits or logs a real error. Silence alone is not evidence of a hang.
- Prefer a two-stage delivery pattern for expensive pipelines: (1) run the heavy benchmark / search stage to completion, verify its summary and winner artifacts, then (2) launch the downstream validation stage separately. This isolates failures and avoids throwing away completed search work.
- GPU only helps when the active path actually uses GPU-capable frameworks. For COBRA / LP-solver dominated workloads, a faster solver (for example Gurobi or CPLEX) is usually more impactful than an idle CUDA device.

## References


- Do not assume a file named like `eciML1515` or a repo named around enzyme tuning is automatically enough. Verify the actual loaded model structure.
- Before running the expensive phases, check for the true prerequisite assets the code expects: external `repo_root` checkout, model files, prior tables such as `mapped_kcats.csv`, and any required sidecar metadata.
- For GECKO/ecGEM-style workflows, inspect the loaded reaction ids for enzyme-supply / protein-pool structure (for example `prot_*`, `draw_prot_*`, protein pool reactions, or enzyme pseudo-metabolites). If those are absent, the pipeline may technically run but produce a zero-length tunable kcat space and therefore no real tuning.
- Treat "Phase A succeeds but kcat space = 0" as a semantic failure, not a success. Report clearly that the framework executed against the wrong model class.
- If both SBML and MATLAB model files exist, test both paths. A common durable pattern is: SBML can load successfully when MAT import fails because of whitespace-bearing variable names or similar identifier issues. Prefer the path that yields a structurally valid ecGEM, not merely the first existing file.
- For long benchmark phases, start them in the background with completion notification, but do the structural verification above first so you do not burn time benchmarking an invalid setup.

## References
- See `references/notebook-openai-compatible-gateway-diagnostics.md` for a compact pattern covering `.env` shaping, LiteLLM provider qualification, notebook config cells, and simple interactive UI wiring for notebook-centric Python apps.
Former narrow engineering persona skills are preserved under `references/`.
- See `references/python-package-mirrors.md` for a compact note on project-local uv mirror configuration and when to prefer project vs user scope.
- See `references/python-env-files.md` for a compact note on improving `.env` files based on the code's actual `load_dotenv()` / `os.getenv()` usage, especially for notebook-driven projects.
