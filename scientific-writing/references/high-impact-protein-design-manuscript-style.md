# High-impact protein/enzyme-design manuscript style

Use this reference when revising manuscript-style work in protein design, enzyme design, or computational catalysis toward a Nature / Science / ACS Catalysis / JACS / Protein Science tone.

## Core framing moves

1. Frame the field-level contrast early: protein folding, backbone generation, and binder design have advanced rapidly, whereas catalysis remains harder because it requires a reactive microenvironment rather than binding alone.
2. Explain why enzymes matter beyond method development: green chemistry, mild conditions, chemo-/regio-/stereoselectivity, and central biological function.
3. Position directed evolution correctly: powerful once weak activity exists, but bottlenecked by finding the first active starting point.
4. Use classical computational enzyme-design methods as background, not as the manuscript's narrative center: theozyme placement, motif scaffolding, and transition-state-anchored design are baselines that also expose the limits of two-stage structure-then-sequence workflows.
5. Present multimodal / chemistry-conditioned generation as an attempt to make chemistry a first-class conditioning signal, not as a routine extension of binder design.

## Style decontamination rules

If the user says the deliverable is an academic paper rather than a technical article, remove or rename audit-style sections and phrases.

### Red-flag phrases to remove from main text
- This manuscript is based on ...
- accessible outputs / accessible evidence / accessible workflow
- current working directory / local design files / package / repository
- authoritative source document
- reproducibility note
- methods and source basis
- file-generation notes

### Better replacements
- "Study basis" instead of "Methods and source basis"
- "Data and document availability" instead of "Reproducibility note"
- "The workflow specifications define ..." instead of "The accessible workflow specifications define ..."
- "campaign outputs" or simply "outputs" instead of "accessible outputs"
- "No wet-lab validation data are reported" instead of "No wet-lab validation data were accessible"

## Citation support pattern for the introduction

When the introduction has strong logic but weak support, add a small set of recent citations that map directly onto the main claims rather than padding the bibliography.

Useful categories:
- structure prediction / modern protein design progress
- sequence design / diffusion or generative design
- ML-assisted enzyme engineering / directed evolution
- functional sequence-space expansion / generative protein models

A compact supporting set used successfully in session work:
1. Jumper et al., *Nature* (2021) — AlphaFold
2. Dauparas et al., *Science* (2022) — ProteinMPNN
3. Singh, *Nature Methods* (2024) — Chroma
4. Yang, Li & Arnold, *ACS Central Science* (2024) — ML-assisted enzyme engineering
5. Repecka et al., *Nature Machine Intelligence* (2021) — generative functional sequence expansion

## Transcript / slide / notes handling

If the user provides a talk transcript, slide export, or auto-generated notes and asks to "follow the format" or "add background", do not copy spoken prose. Extract:
- field tensions
- motivating contrasts
- method framing
- background examples

Then rewrite into compact manuscript paragraphs in venue voice. Remove speaker intros, presentation-stage narration, verbal fillers, and transcript artifacts.

## Chinese-manuscript synchronization

When maintaining matched English and Chinese manuscripts, keep the introduction logically isomorphic:
- same paragraph functions
- same evidence hierarchy
- same candidate-positioning logic
- same citation groupings where possible

Translate for scholarly tone, not sentence-by-sentence literalism.
