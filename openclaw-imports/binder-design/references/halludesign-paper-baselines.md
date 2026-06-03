# HalluDesign paper baselines and safe wording

Use this note when the user asks what HalluDesign is "compared against" or wants a concise Chinese summary grounded in the HalluDesign paper (`2025.11.08.686881v1.full.pdf`).

## Core reading

In the HalluDesign paper, the comparison target is task-dependent, not a single universal baseline.

### Explicit baselines named in the paper

1. Chroma
- Used as an initial monomer scaffold source for optimization.
- HalluDesign is applied to improve Chroma-generated scaffolds.

2. RSO
- Explicitly described as a state-of-the-art backpropagation-based AlphaFold2 design method.
- Used as a strong monomer-generation baseline/challenging refinement test case.

3. RFdiffusion partial diffusion
- Used as a refinement comparison for RSO-generated scaffolds.
- Paper states RFdiffusion partial diffusion could not refine the same RSO scaffolds that HalluDesign improved.

4. RFdiffusion protein binders / RFdiffusion PPI benchmark
- HalluDesign refines RFdiffusion-generated binders from the published PPI benchmark.
- This is the main protein-protein binder baseline/rescue setting.

5. RFdiffusion all-atom
- Explicit diffusion-based baseline for small-molecule binder tasks.

6. BoltzDesign
- Explicit backpropagation baseline in scaffold-based de novo ligand-binder design.

7. AF3 used as an external oracle
- Methodological baseline: the common workflow where generative models propose many candidates and AF3 only filters/selects them.
- HalluDesign contrasts itself with this by turning AF3-style models into active iterative refinement engines.

8. Original fixed-ligand generative mode
- Important ligand-design comparison.
- HalluDesign claims an advantage because it co-optimizes protein structure and ligand conformation simultaneously, unlike fixed-ligand generation.

9. Protenix
- Not a classic baseline but an alternate AF3-style engine used when AF3-based HalluDesign collapses on larger from-scratch protein tasks.
- Important for limitations language: HalluDesign depends on the quality/smoothness of the underlying AF3-style engine.

## Safe answer pattern

Prefer wording like:

- "HalluDesign在论文中不是只对比单一模型，而是按任务分别对比 backpropagation 方法、diffusion-based 方法，以及把 AF3 仅作为外部筛选器的常规流程。"
- "具体基线包括 Chroma、RSO、RFdiffusion partial diffusion、RFdiffusion all-atom、BoltzDesign，以及 fixed-ligand generative mode。"

Avoid overstating:
- Do NOT say HalluDesign has one single universal baseline across all tasks.
- Do NOT collapse ProteinHunter transcript baselines into HalluDesign paper baselines unless the user explicitly asks for a cross-document synthesis.

## Compact Chinese summary

Suggested concise wording:

- "HalluDesign 主要对比 RFdiffusion、RSO、BoltzDesign 等 diffusion/backprop 路线，以及 AF3 仅作外部筛选器的常规流程。"

## Strengths supported by the paper

- Forward-pass-only iterative sequence-structure co-optimization
- Can refine suboptimal or failed designs instead of only filtering them
- Strong rescue/refinement performance for RFdiffusion binders
- Simultaneous protein-ligand co-optimization is a key ligand-design advantage
- Can bypass initial docking in some scaffold-based ligand-binder tasks

## Limitations supported by the paper

- AF3-based HalluDesign can collapse on larger from-scratch protein design tasks
- Success drops for larger, more polar ligands/targets
- Still depends strongly on the underlying AF3-style engine
- Structure-update step remains the main compute bottleneck
- Best framed as a refinement/co-optimization engine, not a universal replacement for broad topology exploration
