---
name: virtual-metabolic-mimic
category: metabolic-engineering
description: Test mechanistic hypotheses about metabolic regulation (NarL/NarX, redox, cofactor balancing) in amino acid overproduction using the project's dFBA pipeline + literature synthesis. Produces structured Chinese reports with quantitative evidence tables.
tags: [dFBA, NarL, two-stage-fermentation, amino-acid-production, hypothesis-testing]
version: 0.1.0
---

# Virtual Metabolic Mimic for Amino Acid Production Hypotheses

Use this skill when the user wants to test mechanistic hypotheses about metabolic regulation (especially two-component systems like NarL/NarX, redox engineering, or cofactor balancing) in amino acid overproduction using the project's internal dynamic flux balance analysis (dFBA) pipeline combined with literature synthesis.

## When to Use
- User asks whether a specific regulator (e.g. NarL phosphorylation) can improve amino acid titer.
- User wants to evaluate two-stage fermentation strategies (high-DO growth → low-DO + alternative electron acceptor).
- User provides or references existing simulation outputs (strain_comparison.csv, narl_phospho_control tables, NarL~P trajectories).
- The task requires both quantitative evidence from the virtual cell model AND mechanistic literature grounding.

## Core Workflow
1. **Inspect project artifacts first**
   - Read key reports: `NarL_NADPH_Arginine_Production_Report.md`, `NARL_NO3_NADPH_ARGININE_HYPOTHESIS_REVIEW.md`
   - Load quantitative tables: `results/strain_comparison.csv`, `results/narl_phospho_control/narl_control_comparison_table.csv`
   - Extract NarL~P dynamics, NADPH fluxes (PntAB vs PPP vs SthA), NO₂ peaks, and arginine titers across chassis vs engineered strains.

2. **Reconstruct the mechanistic circuit**
   - Identify the three axes the model captures:
     - pmf maintenance via NarGHI/FdnGHI nitrate respiration
     - PntAB-driven NADPH regeneration under O₂ limitation
     - NarL~P-mediated repression of astCADBE (arginine catabolism)
   - Note any missing elements (e.g. explicit NirBD overexpression for NO₂ detoxification).

3. **Synthesize literature + simulation evidence**
   - Map simulation outcomes back to published mechanisms (Sauer 2004 PntAB contribution, Chen 2022 C. crenatum nitrate data, Constantinidou 2006 NarL regulon).
   - Explicitly state what the virtual model supports vs what remains hypothetical.

4. **Produce structured deliverable**
   - Default output: concise Chinese markdown report with one-sentence conclusion, evidence table, simulation numbers, and engineering recommendations.
   - Always include a "trade-off / limitation" section (e.g. NO₂ toxicity window, requirement for配套 redox engineering).

## Multi-repo local-learning pattern
When the user says to "learn from" several local directories and then complete a NarL / virtual-metabolic deliverable in a target folder, treat it as a repo-grounded synthesis task rather than a generic literature summary.

1. Inspect each provided directory and assign it a role before writing:
   - dynamic simulation engine / dFBA scaffold
   - product or chassis GEM
   - functional-annotation / nitrogen-cycle capability reference
   - prior local evidence bank (reports, patent summaries, hypothesis notes)
2. Pull exact local evidence that supports the final plan, not just high-level impressions. Good examples include:
   - dFBA workflow lines showing time-step simulation, manual flux-bound overrides, and scenario loops
   - GEM reactions for nitrate reduction, nitrite reduction, amino-acid synthesis, and export
   - local notes that distinguish what is directly supported vs still hypothetical for NarL
3. In the final markdown, add a short section explaining what was learned from each directory so the deliverable reads as an integrated project artifact rather than free-floating advice.
4. If the requested output directory does not exist, create it and place an authoritative `README.md` there unless the user specified a different filename.
5. For this task class, prefer a platform-style conclusion: NarL should usually be framed as a dynamic growth-to-production switch coupled to nitrate / redox / nitrogen-state reprogramming, not as a standalone always-on overexpression recommendation.
6. When the user explicitly asks to extend beyond NarL, preserve one shared virtual-cell state machine for all target amino acids—oxygen state, nitrate input, nitrite risk, redox redistribution, and product output—and swap only the execution-layer modules for arginine, lysine, glutamate/glutamine, threonine, or other target products.

## Required Inputs from User / Project
- Target amino acid (arginine, glutamate, lysine, etc.)
- Whether the user already has simulation results or wants a new virtual experiment
- Any specific constraints (nitrate concentration range, DO setpoints, switching time)

## Pitfalls to Avoid
- Do not claim "NarL phosphorylation always increases titer" — the model shows it only helps when combined with ΔsthA + pntAB↑ and within a narrow NO₃⁻ window.
- Never treat nitrate as a direct NADPH source; it is always an indirect pmf → PntAB mechanism.
- Do not ignore the biphasic nitrate response (toxicity above ~60–80 mM).
- Avoid proposing standalone narL overexpression without redox engineering.

## Output Format Preference
- Chinese markdown report
- One-sentence core conclusion at the top
- Evidence table (命题 | 仓库证据 | 结论)
- Quantitative simulation comparison table
- Clear engineering recommendations with "must-have" vs "optional" components
- References to exact file paths and line numbers in the project
- When the user explicitly asks for a journal-like deliverable, prefer concise, manuscript-ready language and Nature-style figures over exploratory commentary.

## Adapting an Existing dFBA Codebase for NarL/NO3 Hypotheses
When the user asks you to not only write the NarL strategy but also start modifying an existing dynamic-metabolism repository, prefer a minimal-change extension path instead of rewriting the repo's main entrypoint.

1. Keep the original `main.R` or baseline workflow intact whenever possible.
2. Add a separate regime generator for NarL/NO3 time-series inputs (for example a new `generating_narl_no3_regimes.R`) rather than overloading the original carbon-only generator.
3. Extend the smallest shared interfaces first:
   - init function to accept nitrate initial state
   - execution wrapper to accept alternate regime subdirectories, init values, and result tags
4. Generate separate compiled-model variants for hypothesis states (for example NarL-off, NarL-on + nitrate, NarL-on + stronger nitrite clearance) by changing reaction bounds, instead of mutating one compiled model repeatedly by hand.
5. Prefer a dedicated runner script for the hypothesis grid (`variant × regime`) so the experiment remains reproducible and easy to inspect.
6. If the repo's convenience import script pulls in many optional packages, write the new hypothesis scripts with only the packages they actually need. This reduces setup friction and makes first-pass validation easier.
7. In the deliverable, explicitly label first-pass limitations when the PN / GSPN layer still lacks formal nitrate or nitrite places/transitions. Do not overclaim full mechanistic coupling if only the FBA-constraint layer has been extended.
8. If a Python/cobra virtual-cell runner appears to produce no output, first test whether it is actually timing out rather than crashing: profile a few scenarios, estimate total runtime, add explicit progress prints (`Loaded model`, `Running N scenarios`, `[i/N] scenario_id`) and then rerun with a long enough timeout before debugging stack traces. When results are delivered, verify whether outputs are only CSV/JSON tables or whether figure artifacts were also generated; if figures are missing, create publication-style PNG/PDF summaries from the summary and timecourse tables.

## References Directory
Also see `references/aivm-timeout-and-visualization-pattern.md` for the runtime-diagnosis + figure-generation pattern that distinguishes timeout from crash, adds explicit progress logging, and generates summary figures from CSV outputs.
See `references/` for session-specific evidence transcripts and condensed mechanism banks.
Also see `references/virtual-cell-literature-bank.md` for the compact whole-cell / dFBA literature base and project-facing takeaways used in this session.
Also see `references/ecoli-narl-no3-first-pass.md` for the first-pass integration pattern used to graft NarL/NO3 hypothesis testing onto an existing E. coli dFBA repository.
Also see `references/narl-no3-python-cobra-first-pass.md` for the fallback pattern that uses the existing `.mat` GEM backbone to deliver a runnable Python/cobra first-pass experiment, figures, and a scientific report when the canonical R/dFBA path is not yet running end-to-end.
Also see `references/ecoli-narl-no3-r-path-repair.md` for the durable R-path repair pattern: install sequence (`R.matlab` -> `fdatest` -> `strex` -> `epimod`), the `carbon_reg` fallback fix, explicit `library(epimod)` loading, and how to distinguish repaired R code from remaining epimod Docker-image runtime blockers.
Also see `references/multi-amino-acid-virtual-cell-proposal.md` for the proposal-level pattern that expands a NarL/NO3 virtual-cell mimic into a reusable multi-amino-acid production framework with shared oxygen/NO3/NO2/redox/product-output state variables.
