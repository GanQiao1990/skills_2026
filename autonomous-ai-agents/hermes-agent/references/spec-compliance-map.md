# Compliance map for pasted specification

Source specification:
- `/root/.hermes/pastes/paste_1_090129.txt`

Target skill files:
- `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/SKILL.md`
- `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/local-environment-and-visualization.md`

## Read/interpretation evidence

The full pasted specification file was read directly from:
- `/root/.hermes/pastes/paste_1_090129.txt`

The main skill now explicitly states that it follows that pasted specification:
- `SKILL.md:35`

## Traceable requirement mapping

### Execution defaults

1. `export HF_ENDPOINT=https://hf-mirror.com`
- Spec: `paste_1_090129.txt:1`
- Implemented in main skill: `SKILL.md:43`
- Implemented in reference: `local-environment-and-visualization.md:9`

2. `npx skills`
- Spec: `paste_1_090129.txt:2`
- Implemented in main skill: `SKILL.md:46-49`
- Implemented in reference: `local-environment-and-visualization.md:12-16`
- Ambiguity note preserved in reference: `local-environment-and-visualization.md:238-240`

3. Aliyun torch install command
- Spec: `paste_1_090129.txt:4`
- Implemented in main skill: `SKILL.md:56-59`
- Implemented in reference: `local-environment-and-visualization.md:18-21`

4. Conda python path `/home/qiao/anaconda3/bin/python`
- Spec: `paste_1_090129.txt:102`
- Implemented in main skill: `SKILL.md:51-54`
- Implemented in reference: `local-environment-and-visualization.md:23-26`

### Visualization palette and style

5. Section title `## Global visualization palette and style`
- Spec: `paste_1_090129.txt:7`
- Implemented in reference: `local-environment-and-visualization.md:28`

6. Explanatory text about palette cleanup and 15 core colors
- Spec: `paste_1_090129.txt:9`
- Implemented in reference: `local-environment-and-visualization.md:30`

7. Color table entries
- Spec: `paste_1_090129.txt:13-22`
- Implemented in reference: `local-environment-and-visualization.md:34-43`

8. Threshold emphasis color `#D0021B`
- Spec: `paste_1_090129.txt:24`
- Implemented in reference: `local-environment-and-visualization.md:45`
- Mentioned in main skill summary: `SKILL.md:70`

9. Exact `PALETTE` block
- Spec: `paste_1_090129.txt:32-38`
- Implemented in reference: `local-environment-and-visualization.md:53-59`

10. Exact `AUX_PALETTE` block
- Spec: `paste_1_090129.txt:40-46`
- Implemented in reference: `local-environment-and-visualization.md:61-67`

11. Exact Matplotlib / seaborn style block
- Spec: `paste_1_090129.txt:28-61`
- Implemented in main skill: `SKILL.md:83-116`
- Implemented in reference: `local-environment-and-visualization.md:49-82`

### Plot templates

12. Exact `plot_iptm(...)` template
- Spec: `paste_1_090129.txt:68-77`
- Implemented in main skill: `SKILL.md:123-132`
- Implemented in reference: `local-environment-and-visualization.md:89-98`

13. Exact `plot_cycles(...)` template
- Spec: `paste_1_090129.txt:83-90`
- Implemented in main skill: `SKILL.md:138-145`
- Implemented in reference: `local-environment-and-visualization.md:104-111`

### Usage guidelines

14. All usage guideline bullets
- Spec: `paste_1_090129.txt:94-99`
- Implemented in main skill: `SKILL.md:149-154`
- Implemented in reference: `local-environment-and-visualization.md:115-120`

### Mermaid flowchart template

15. Mermaid graph root `graph TB`
- Spec: `paste_1_090129.txt:107`
- Implemented in main skill: `SKILL.md:161`
- Implemented in reference: `local-environment-and-visualization.md:127`

16. Inference subgraph
- Spec: `paste_1_090129.txt:108-116`
- Implemented in main skill: `SKILL.md:162-170`
- Implemented in reference: `local-environment-and-visualization.md:128-136`

17. Data subgraph
- Spec: `paste_1_090129.txt:118-126`
- Implemented in main skill: `SKILL.md:172-180`
- Implemented in reference: `local-environment-and-visualization.md:138-146`

18. Model subgraph
- Spec: `paste_1_090129.txt:128-136`
- Implemented in main skill: `SKILL.md:182-190`
- Implemented in reference: `local-environment-and-visualization.md:148-156`

19. Diffusion subgraph
- Spec: `paste_1_090129.txt:138-147`
- Implemented in main skill: `SKILL.md:192-201`
- Implemented in reference: `local-environment-and-visualization.md:158-167`

20. Pairformer subgraph
- Spec: `paste_1_090129.txt:149-157`
- Implemented in main skill: `SKILL.md:203-211`
- Implemented in reference: `local-environment-and-visualization.md:169-177`

21. Application subgraph
- Spec: `paste_1_090129.txt:159-168`
- Implemented in main skill: `SKILL.md:213-222`
- Implemented in reference: `local-environment-and-visualization.md:179-188`

22. Mermaid edge definitions
- Spec: `paste_1_090129.txt:170-215`
- Implemented in main skill: `SKILL.md:224-269`
- Implemented in reference: `local-environment-and-visualization.md:190-235`

## Validation evidence

A programmatic validation pass checked that key required strings from the pasted specification appear in the final skill files, including:
- `export HF_ENDPOINT=https://hf-mirror.com`
- `npx skills`
- the exact Aliyun `uv pip install ...` command
- `/home/qiao/anaconda3/bin/python`
- `PALETTE = [`
- `AUX_PALETTE = [`
- `def plot_iptm(...)`
- `def plot_cycles(...)`
- `graph TB`
- `subgraph Inference["Inference Runner (Trace 1)"]`
- `1f -->|produces| 5f`

It also verified that the exact `PALETTE`, `AUX_PALETTE`, `plot_iptm`, and `plot_cycles` blocks are present in the reference file.

## Limits / impossible items in this environment

The pasted specification mainly defines skill content and conventions, not an executable runtime protocol with a dedicated test harness. In this environment I can:
- read the source specification
- patch the skill files
- read them back
- validate string/block presence programmatically

I cannot honestly prove runtime properties that the spec does not define as executable behavior, such as performance targets, sandbox enforcement, or command entrypoint behavior beyond the skill text itself, because the specification is content-oriented rather than a runnable software contract.
