---
name: transcript-to-method-positioning-note
description: Turn a noisy auto-generated talk transcript or paper dump into a clean internal method-positioning note, especially when comparing existing methods to your own pipeline.
---

# Transcript to Method Positioning Note

## When to use
Use this skill when the user gives you:
- an auto-generated English transcript, seminar dump, or OCR-like notes
- a request such as "review this and summarize the weaknesses of method A/B and our advantages"
- a local project/repo whose internal docs should be used to frame the comparison
- a requirement to write the result directly into the current working directory or a specified folder

Typical examples:
- Compare BindCraft / diffusion methods vs our pipeline
- Read a seminar transcript and extract the speaker's critique of current methods
- Turn messy source text into a discussion-ready or manuscript-ready positioning memo

## Core idea
Do **not** read the transcript linearly end-to-end first. Auto-generated transcripts are noisy. Instead:
1. locate the file and working directory
2. identify keywords and claims with targeted search
3. read only the dense relevant windows around those hits
4. cross-check the framing against local project docs
5. write a clean summary that distinguishes **source-derived claims** from **our project framing**

## Workflow

### 1) Resolve the target path first
- Run `pwd` if the user says "write it in pwd"
- Search for the exact file or folder pattern
- Confirm the final output folder before drafting

### 2) Log assumptions in `DEBUG.md`
Before substantive work, append or patch `DEBUG.md` with:
- task
- source file path
- likely output path
- assumptions about language/style
- pending evidence to collect

Do not overwrite unrelated prior findings; patch if `DEBUG.md` already exists.

### 3) Mine the transcript with keyword search before deep reading
For noisy transcripts, first grep conceptually using file search for terms like:
- method names: `BindCraft`, `RFdiffusion`, `ProteinHunter`, `AlphaProteo`
- critique terms: `hard`, `challenging`, `0%`, `time consuming`, `computationally heavy`, `dynamic`, `multimer`, `small molecule`, `DNA`, `RNA`
- speed theory terms: `pair trunk`, `distogram`, `contact loss`, `proxy`, `back propagate`, `confidence`

Then read local windows around those hits rather than the whole file.

### 4) Separate three layers of content
When extracting notes, sort each claim into one of these bins:

#### A. What the source explicitly says
Examples:
- single-model / backprop methods are computationally heavy
- AF3-style full diffusion backprop is expensive
- oligomeric / dynamic / ligand-constrained targets are harder
- ProteinHunter uses pair/contact proxies for faster optimization

#### B. What our repo/docs explicitly say
Search local docs for:
- `Double Hallucination`
- `orthogonal validation`
- `single-model bias`
- `Chai-1`
- `go/no-go`
- `wet-lab entry`

Use these to ground statements about our own approach.

#### C. The synthesis
This is the actual deliverable:
- weaknesses of prior methods
- why ProteinHunter is faster
- why our full pipeline is better for decision-making, not just proposal generation

Never present synthesis as if it were a direct quote from the transcript.

### 5) Preferred output structure
Write the summary as a markdown memo with these sections:
1. one-paragraph conclusion
2. strengths and limits of existing methods
3. diffusion / AF3-style backprop bottlenecks
4. ProteinHunter's speed intuition
5. why Double Hallucination + multi-model validation is better
6. a short manuscript-ready paragraph
7. an ultra-short version for slides/chat

If the user provides an explicit **staged pipeline** (e.g., `Stage 0–6`) with counts (e.g., `200→20→400→Top-5`) or bracketed internal pointers (e.g., `[1c][6g]`), **preserve their stage numbering, funnel numbers, and bracket tokens verbatim** and only improve clarity/wording around them.

This structure works well for both internal notes and later manuscript reuse.

### 5.1) Recommended structure for staged multi-model pipelines
When the input is already organized as a pipeline, prefer:
- “Method overview” (include the stage code-block diagram)
- “Design philosophy” (3–5 crisp axioms)
- “Why it is fast” (compute scheduling + funnel)
- “Why it is accurate” (orthogonal audit + multi-signal scoring)
- “Metrics & composite score” (table: ipTM/pLDDT/clash/pocket coverage)
- “Comparison table” (1 table instead of long prose)
- “Reproducibility & engineering” (YAML/config, directories, one-command run)

### 6) Wording guidance
Prefer these distinctions:
- `proposal generator` vs `decision system`
- `single-model consistency` vs `true transferability`
- `candidate generation` vs `candidate compression`
- `high score under one model` vs `orthogonal agreement across models`
- `worthy of wet-lab entry` rather than `best overall`

These phrases make the comparison sharper without overclaiming.

## Important cautions
- Auto-generated transcripts are error-prone; do not over-quote garbled lines.
- Only use exact numbers if they clearly appear in the source or repo docs.
- If the transcript is noisy, summarize claims conservatively.
- Cross-check local project claims before attributing advantages to "our method".
- Do not say our approach is globally superior; say it is better suited for reducing single-model bias and improving wet-lab entry decisions.
- **Encoding/legibility pitfall:** if you generate a markdown file programmatically, verify the file is UTF-8 plain text (no hidden control characters). If you see gibberish characters like `\u0011` in the rendered output, rewrite the file cleanly and re-open it to confirm.

## Reusable query patterns
Good transcript searches:
- `(BindCraft|diffusion|back propagation|ProteinHunter|small molecule|DNA|RNA|dynamic|multimer|0%|time consuming)`
- `(pair trunk|distogram|contact loss|proxy|confidence)`

Good repo searches:
- `(Double Hallucination|orthogonal validation|single-model bias|Chai-1|go/no-go|wet-lab entry)`

## Deliverable expectation
A strong final note should let the user immediately reuse the text in one of three places:
- internal method note
- grant/manuscript Discussion/Introduction
- slide or meeting summary

Reference: see `references/staged-multi-model-binder-pipeline-outline.md` for a reusable outline, metric table template, and quality checkpoints for staged multi-model pipelines.
