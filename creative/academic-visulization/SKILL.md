---
name: academic-visulization
description: Use when working with the local /home/qiao/qiao_design/academic_visulization workspace for academic graphical abstracts, scientific image generation, professional portrait generation, paper-to-PPT conversion, or APIMart/OpenRouter video apps. Routes requests to the correct subproject and provides the right path, port, startup command pattern, and API-key expectations.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [academic-graphics, graphical-abstract, portrait, pptx, video, apimart, openrouter]
    related_skills: [scientific-visualization, scientific-slides, powerpoint, generate-image]
---

# Academic Visulization Workspace Router

## Overview

This skill covers the local workspace at:

`/home/qiao/qiao_design/academic_visulization`

Use it to route work to the correct subproject inside this workspace instead of guessing which app to open. The folder name is intentionally kept with the original misspelling `visulization`; use that exact spelling in paths and commands.

## Choose the right subproject

- `academic_graphic_apimart` — academic/biomedical graphical abstracts via APIMart GPT-Image-2; port `8025`; uses aspect-ratio sizes, not raw pixel sizes.
- `aidraw_version4_graphic_abstract` — OpenAI-compatible graphic-abstract app with sketch/image-edit support and optional PNG→SVG; port `8020`.
- `aidraw_version_1` — older academic figure generator with broader model/size options and optional SVG export; port `8010`.
- `ppt_maker` — paste a paper, generate a slide plan, create images, and export a PPTX deck; port `8765`.
- `protrait_apimart` — APIMart portrait generator; port `8026`; portrait-oriented aspect ratios.
- `aidraw_version_2` — OpenAI-compatible portrait app; port `8000`.
- `aidraw_version3_portrait` — newer OpenAI-compatible portrait app; port `8001`.
- `seedance_2` — OpenRouter / ByteDance Seedance 2.0 video generation; port `8027`.
- `veo3_apimart` — APIMart VEO3 video generation; port `8031`.
- `ai_draw` and `image_improve` — prompt/script scratchpads rather than polished web apps; inspect scripts before use.

## Environment expectations

- APIMart image/video apps expect `APIMART_API_KEY` and usually `APIMART_BASE_URL` in `.env`.
- OpenAI-compatible image apps expect `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and optional proxy settings.
- Seedance video app expects `OPENROUTER_API_KEY` and `OPENROUTER_BASE_URL`.
- Most README files are Windows-oriented (`start.bat`, Anaconda paths). On Linux, prefer direct `uvicorn` startup from the project directory.

## Linux startup pattern

For most web apps in this workspace:

```bash
cd /home/qiao/qiao_design/academic_visulization/<subproject>
python -m uvicorn api.main:app --host 127.0.0.1 --port <documented-port> --reload
```

Useful defaults from the workspace docs:

- `aidraw_version_1` → `8010`
- `aidraw_version_2` → `8000`
- `aidraw_version3_portrait` → `8001`
- `aidraw_version4_graphic_abstract` → `8020`
- `academic_graphic_apimart` → `8025`
- `protrait_apimart` → `8026`
- `seedance_2` → `8027`
- `veo3_apimart` → `8031`
- `ppt_maker` → `8765`

After launch, verify with `/health` or `/docs` when available.

## Working rules

- If the task is academic figure generation, first decide whether the user wants APIMart (`academic_graphic_apimart`) or OpenAI-compatible GPT-Image (`aidraw_version4_graphic_abstract` / `aidraw_version_1`).
- If the task is portrait generation, prefer `protrait_apimart` for APIMart workflows and `aidraw_version3_portrait` or `aidraw_version_2` for OpenAI-compatible workflows.
- If the task is paper-to-deck conversion, go directly to `ppt_maker`.
- If the task is video generation, route to `seedance_2` for OpenRouter/Seedance or `veo3_apimart` for APIMart VEO3.
- If the folder only contains prompt notes or ad-hoc scripts (`ai_draw`, `image_improve`), inspect the files before running anything; do not assume a stable service exists.

## Common pitfalls

1. The path contains a misspelling: use `academic_visulization`, not `academic_visualization`.
2. APIMart apps in this workspace often require aspect ratios like `16:9` or `2:3`, not pixel strings like `3840x2160`.
3. `start.bat` and some README commands are Windows-specific; on Linux, use direct Python/uvicorn commands.
4. Different subprojects use different providers and keys; do not reuse `OPENAI_API_KEY` where `APIMART_API_KEY` or `OPENROUTER_API_KEY` is required.
5. Multiple services use nearby ports; verify the port before launch to avoid collisions.

## Verification checklist

- Confirm the chosen subproject matches the user’s goal.
- Confirm the required `.env` keys exist for that subproject.
- Launch with the documented port.
- Verify service readiness with `/health`, `/docs`, or a successful local HTTP response.
- For output tasks, confirm the generated file path under that subproject’s `outputs/` directory.
