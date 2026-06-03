# Briefings in Bioinformatics review framing for generative protein design

Use this note when a review on de novo / generative protein design should be reshaped for a bioinformatics audience rather than a protein-science or broad narrative audience.

## Core shift in framing
Do not organize the review primarily as:
- historical story of the field
- list of model families
- protein-engineering success showcase

Instead organize it as a methods-comparison review answering:
1. What computational object is the method acting on?
2. Where in the design pipeline does it operate?
3. What proxy metrics does it optimize or report?
4. What do those metrics actually support?
5. Under what task definitions are cross-paper comparisons valid?

## Recommended top-level structure
1. Why a bioinformatics-style reframing is needed
2. Unified pipeline for generative protein design
   - input representation
   - generation/search module
   - sequence realization
   - proxy evaluation
   - triage / robustness
   - experimental evidence
3. Method taxonomy
   - prediction-guided search / hallucination / inversion
   - diffusion and geometric generation
   - flow-based generation
   - language-model and latent-space methods
   - inverse folding / sequence realization
4. Benchmarking and evaluation problems
5. Task-specific evidence ladders
   - fold generation
   - binder design
   - enzyme design
   - dynamic/multistate design
   - membrane / GPCR / special environments
6. Open protocol and benchmarking recommendations

## Tables BIB-style readers expect
### Table A: method comparison
Columns:
- method family
- input representation
- output object
- conditioning signal
- sequence generation strategy
- main proxy metrics
- validation depth
- main failure mode

### Table B: metric / evidence mapping
Columns:
- metric
- what it measures
- what it does NOT prove
- valid task scope
- common misuse

### Table C: task-specific minimum evidence
Columns:
- task type
- minimum acceptable evidence
- strong evidence
- common overclaim pattern

## Language shift
Prefer:
- comparability
- benchmark discipline
- protocol heterogeneity
- proxy metric
- evidence ladder
- robustness audit
- task-specific validity

Avoid overusing:
- revolutionary
- breakthrough
- superior
- state-of-the-art
unless the claim is tightly bounded and benchmark-backed.

## Editorial heuristic
If a paragraph could fit equally well in a protein-science narrative review and does not help compare methods, benchmarks, or evidence standards, it is not yet BIB-optimized.
