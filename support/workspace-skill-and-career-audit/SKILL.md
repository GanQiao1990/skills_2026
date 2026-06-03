---
name: workspace-skill-and-career-audit
description: Audit a user's home/project workspace to infer evidenced technical skills, research capabilities, and likely career direction from files, repos, scripts, manuscripts, and outputs.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [workspace-audit, skills-assessment, career-guidance, evidence-based]
---

# Workspace Skill and Career Audit

Use this skill when the user asks you to review a filesystem workspace (for example `/home/user`, a lab directory, or a project root) and summarize what the person is actually capable of, especially for research, engineering, or experimental work.

## When to use
- The user asks for a summary of their skills based on files/repos/projects.
- The user wants career-direction advice grounded in their existing work.
- The user wants a read-only audit of a research or engineering workspace.
- The user asks what themes or strengths are visible across many repos.

## Core principle
Only claim capabilities that are supported by filesystem evidence. Distinguish clearly between:
1. **Observed evidence** — directly supported by files, scripts, READMEs, reports, manuscripts, outputs.
2. **Strong inference** — repeated patterns across multiple repositories or documents.
3. **Unverified execution depth** — where documents show design/organization ability but not necessarily independent bench execution.

## Evidence hierarchy
Prefer stronger evidence in this order:
1. Grant proposals, manuscripts, response letters, integrated reports
2. Run scripts, pipeline wrappers, notebooks, analysis scripts
3. Result tables, figures, output directories, logs
4. Installed repos and cloned tool collections
5. Environment caches and model weights (weakest evidence)

Do not over-weight a cloned repository unless there is evidence of active use, customization, outputs, or project-specific scripts.

## Workflow

### 1. Set scope and assumptions
- Treat the audit as read-only unless the user asks otherwise.
- Write assumptions/evidence plan to `DEBUG.md` if local workflow policy requires it.
- Clarify that career advice will be grounded in observed work patterns, not personality speculation.

### 2. Inventory the workspace
- List top-level directories and identify likely research/project roots.
- Use a compact tree or scripted directory summary for the first 1–2 levels.
- Ignore low-value noise when possible: caches, package directories, virtualenvs, compiled artifacts.
- Flag high-signal directories such as `projects/`, `biobank/`, `md/`, `manuscript/`, `proposal/`, `scripts/`, `results/`.

### 3. Pull representative evidence
Read a targeted sample of files from the strongest-signal directories:
- `README.md`
- `*_Proposal*.md`, `*_Manuscript*.md`, `response_letter*.md`
- domain-specific run scripts (`run_*.sh`, `infer.py`, `train.py`)
- result summaries and figure reports
- methodology docs that show actual pipeline structure

Aim to cover:
- scientific/problem domain
- tooling stack
- validation methods
- scale/rigor of outputs
- evidence of end-to-end ownership

### 4. Build capability clusters
Group findings into reusable skill clusters, for example:
- computational discovery / AI design
- structural biology / MD / docking
- wet-lab experiment design
- multi-omics / statistical analysis
- scientific visualization / manuscript packaging
- automation / infrastructure / workflow design

For each cluster, cite concrete path evidence.

### 5. Calibrate claims carefully
Use these phrasing rules:
- **“Clearly demonstrated”** when multiple files/outputs show real execution.
- **“Strongly suggests”** when repeated project scaffolding implies real familiarity.
- **“Shows experiment-design literacy”** when documents specify detailed assays, controls, sample sizes, and QC, but independent execution is not directly proven.
- Avoid saying the user personally performed every experiment unless the evidence is explicit.

### 6. Translate into career direction
Recommend directions based on the intersection of:
- strongest evidence-backed skills
- rarity/market value of the combined profile
- coherence of existing projects
- where the user appears to have an emerging research narrative

Usually recommend:
- one primary direction
- one or two secondary directions
- explicit warnings against over-dispersion if the workspace is fragmented

### 7. End with actionable synthesis
Provide:
- one-sentence positioning statement
- strongest capability areas
- likely ceiling/role type
- top 2–3 next-step career moves
- any key gap to strengthen

## Output structure

```markdown
# 基于工作区证据的能力审阅

## 一句话判断
[总体定位]

## 核心证据来源
- `[path]`: [为什么重要]
- `[path]`: [为什么重要]

## 能力画像
### 1. [能力簇]
- 证据：`[path]`
- 判断：[明确区分直接证据 / 强推断 / 仅显示方案设计能力]

### 2. [能力簇]
...

## 事业方向建议
### 主方向
[最匹配方向 + 原因]

### 次方向
[可延伸方向 + 原因]

## 需要补强的短板
- [短板1]
- [短板2]

## 最终评价
[角色定位 + 下一步建议]
```

## Practical heuristics learned
- A home directory audit is most informative when you first map the top-level workspace, then read a small number of high-signal documents rather than many low-signal files.
- Proposal/manuscript files are often the best evidence for whether the user can connect computation, biology, experiments, and publication strategy.
- Distinguish between **tool possession**, **pipeline operation**, and **research leadership/experimental design**.
- Repeated cross-links between design outputs, retrieval analyses, MD workflows, and validation plans indicate a higher-level systems researcher profile rather than isolated tool usage.
- When giving career advice, emphasize the user's most differentiated combination of skills rather than every domain they touched.

## Pitfalls
- Do not confuse installed software or cloned repos with real competence.
- Do not overstate wet-lab independence from proposal text alone.
- Do not give generic career advice detached from observed evidence.
- Do not drown the user in exhaustive directory listings; synthesize.

## Success criteria
A good audit should let the user feel:
- “Yes, this is grounded in what I actually work on.”
- “You distinguished what I’ve clearly done from what is only implied.”
- “The career advice follows from my evidence, not from generic motivational talk.”
