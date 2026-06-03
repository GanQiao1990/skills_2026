---
name: journal-readiness-audit
category: research
description: Systematic evaluation of research projects for top-tier journal suitability (Nature/Science/Cell family). Identifies critical gaps, provides concrete remediation roadmap with timelines, and estimates publication success probability.
usage: Use when user asks "Can this project冲击 [journal]?" or requests evaluation of research for high-impact publication. NOT for general paper writing or literature review (use academic-research-workflow instead).
---
# Research Project Journal Readiness Audit

## 📋 Skill Overview

Systematic evaluation of computational/experimental research projects for top-tier journal suitability (Nature/Science/Cell family). Identifies critical gaps, provides concrete remediation roadmap, and estimates success probability.

**Use when**: User asks "Can this project冲击 X journal?" or "Evaluate this project for Nature/Science/Cell publication"

**Not for**: Literature reviews, paper drafting, or general research advice (use `academic-research-workflow` instead)

---

## 🎯 Core Methodology

### Phase 1: Project Reconnaissance (15-30 min)
**Goal**: Understand what the project actually is

```
1. Directory structure mapping
   Command: find <project_root> -type f -name "*.md" -o -name "*.pdf" -o -name "*.csv" | head -50
   Purpose: Identify key documents (reports, proposals, data)

2. Document classification
   Categories:
   - Computational reports (methods, metrics, validation)
   - Experimental plans (wetlab protocols, validation schemes)
   - Grant proposals (target journal often embedded)
   - Preliminary results (data files, figures)
   - Code/scripts (reproducibility evidence)

3. Quick scan for red flags
   - ❌ No experimental validation (computational-only)
   - ❌ Missing key metrics (no quantitative evaluation)
   - ❌ Incomplete narratives (fragmented documents)
   - ✅ Comprehensive documentation (organized reports)
```

---

### Phase 2: Evidence Extraction & Cross-Validation (30-60 min)
**Goal**: Build factual foundation, separate claims from evidence

```
Step 1: Extract quantitative metrics
   Sources:
   - ranked_candidates.csv (binder design metrics)
   - master_metrics.csv (composite scores)
   - JSON outputs (structure confidence: ipTM, pLDDT, PAE)
   - Performance tables (accuracy, recall, runtime)
   
   Key metrics to capture:
   • Design success rate (% high-confidence candidates)
   • Cross-model consistency (correlation between predictors)
   • Physical feasibility (clash penalties, pocket coverage)
   • Throughput (number of designs, time per design)

Step 2: Verify narrative claims
   Compare stated achievements vs documented evidence:
   "We designed 100 binders" → Check: ranked_candidates rows = ?
   "High specificity" → Check: off-target analysis exists?
   "Validated by SPR" → Check: actual SPR data files
   
Step 3: Identify missing links
   Gap analysis:
   Computation → [missing] → Experimental validation
   Design → [missing] → Mechanism insight
   Method → [missing] → Biological application
```

---

### Phase 3: Journal-Specific Criteria Mapping (15 min)
**Goal**: Match project strengths/weaknesses to target journal preferences

#### Nature Biotechnology (IF ~47) checklist:
```
 ✅ METHODOLOGICAL INNOVATION (must-have)
    • New algorithm/workflow? 
    • Integration of multiple methods?
    • Demonstrable improvement over state-of-art?
    • Reproducibility evidence (code/data availability)?

 ✅ BIOLOGICAL/ENGINEERING IMPACT (must-have)
    • Addresses important biomedical/industrial problem?
    • Shows real-world application potential?
    • Demonstrates utility beyond proof-of-concept?

 ✅ EXPERIMENTAL VALIDATION (critical for computational work)
    • Biophysical characterization (SPR/BLI/ITC)?
    • Structural validation (crystal/EM)?
    • Cellular/animal functional assays?
    • At least 1-2 key experiments completed?

 ✅ MECHANISTIC INSIGHT (differentiates tool paper from insight paper)
    • Not just "it works" but "why it works"?
    • Reveals something about biological system?
    • Unexpected findings or mechanistic explanations?

 ❌ COMMON DEAL-BREAKERS:
    • Pure computation without wetlab (usually → Nature Methods/Comm)
    • Incremental improvement (<2x performance gain)
    • Narrow applicability (only works on 1-2 test cases)
    • Poor documentation/irreproducible
```

#### Adaptation for other journals:
- **Nature Methods**: Emphasize method validation, benchmarks, usability
- **Science**: Broad interdisciplinary impact, paradigm-shifting
- **Cell**: Deep biological mechanism, disease relevance
- **Nature Communications**: Solid work but narrower impact

---

### Phase 4: Gap Analysis & Risk Assessment (15 min)
**Goal**: Quantify what's missing and how hard to fix

**Gap typology**:
```
TYPE A - FATAL (cannot publish without)
   Example: No experimental data for NBT
   Fix: 6-12 months wetlab work
   Risk: Experiment may fail (30-50% success rate)

TYPE B - CRITICAL (severely limits impact)
   Example: Weak biology, only tool demo
   Fix: 3-6 months additional experiments/analysis
   Risk: May uncover negative results

TYPE C - IMPORTANT (enhances but not essential)
   Example: Missing structural validation
   Fix: 2-4 months (if crystals available)
   Risk: Low, but time-consuming

TYPE D - NICE-TO-HAVE (polishing)
   Example: Additional control experiments
   Fix: 1-2 months
   Risk: Minimal
```

**Risk scoring**:
```
Experimental feasibility risk:
  Low (70%+ success): Expression/purification work, standard assays
  Medium (50%): Structural biology, complex cellular phenotypes
  High (<30%): Novel mechanism requiring unknown conditions

Timeline risk:
  Conservative estimate × 1.5 = realistic timeline
  "It never works the first time" factor
```

---

### Phase 5: Strategic Roadmap Creation (15 min)
**Goal**: Concrete, prioritized action plan

**Template**:

```
PROJECT: <Name>
TARGET: Nature Biotechnology
CURRENT SCORE: <X>/10
FEASIBILITY (with full experiments): <Y>%

CRITICAL GAPS (Must-fix before submission):
  [Gap 1: Missing experimental validation]
    Required: SPR data for top 3 binders + cellular assay
    Timeline: 6-8 months
    Resources: Protein purification setup, SPR access, cell culture
    Success probability: 60%
    Priority: 🔴 P0 (blocks submission)
  
  [Gap 2: Weak biological insight]
    Required: Transcriptomics to reveal NarL downstream effects
    Timeline: 3-4 months
    Resources: RNA-seq, bioinformatics
    Success probability: 90%
    Priority: 🟡 P1 (strengthens story)

IMPORTANT ENHANCEMENTS:
  [Enhancement 1: Structural validation]
    Nice-to-have: Co-crystal structure
    Timeline: 4-6 months (if crystals)
    Priority: 🟢 P2 (boost credibility)

STRATEGIC RECOMMENDATIONS:
  1. Storyline focus: Emphasize ClpX degradation as main narrative
  2. Cut: CarB-PknB system (separate paper)
  3. Method framing: "Orthogonal validation framework" not just "we used 3 models"
  4. Competitive positioning: First integrated design→validation→application pipeline

TIMELINE TO SUBMISSION:
  Month 1-3:  Critical experiments
  Month 4-6:  Impact experiments + analysis
  Month 7:    Draft paper (Methods + Results)
  Month 8-9:  Supplement experiments (transcriptomics if needed)
  Month 10:   Internal review + revisions
  Month 11:   Target journal selection + submission
  
TOTAL TIME: 11-12 months (optimistic)
```

---

## 🔄 Skill Workflow: Step-by-Step

When user asks "Can this project冲击 Nature Biotechnology?":

```
STEP 1: Project reconnaissance (explore files)
  $ find /path/to/project -type f \( -name "*.md" -o -name "*.pdf" -o -name "*.csv" \) | head -100
  $ tree -L 3 /path/to/project
  Goal: Create project inventory

STEP 2: Evidence gathering (read key documents)
  Priority order:
  1. Grant proposal (if exists) → reveals target journal & expected results
  2. Academic reports (methodology, metrics)
  3. Experimental validation plan (what they plan to do)
  4. Ranked candidates / data tables (actual outputs)
  5. Methods documentation (reproducibility)
  
  Extract:
  • Quantitative results (metrics, success rates)
  • Claims about achievements
  • Gaps acknowledged in documents
  • Timeline/status information

STEP 3: Journal criteria matching
  For NBT specifically check:
  ☐ Experimental validation (any wetlab data?)
  ☐ Mechanism + application (both present?)
  ☐ Methodology novelty (new algorithm/workflow?)
  ☐ Impact scope (broad bioscience/engineering?)
  ☐ Data integrity (complete metrics, controls)

STEP 4: Gap quantification
  List ALL missing components:
  - Experimental: [SPR/BLI/ITC, structural data, cellular assays]
  - Biological: [mechanism, pathway analysis, phenotype]
  - Methodological: [benchmarking, comparison to prior art]
  - Narrative: [focused story, clear take-home message]
  
  For each gap:
  • Estimate time to complete
  • Estimate success probability
  • Identify resource needs
  • Mark as P0/P1/P2 priority

STEP 5: Strategic recommendations
  Provide:
  • "Must-have" experiments (non-negotiable for target journal)
  • "Should-have" enhancements (increase acceptance odds)
  • "Nice-to-have" polish (if time permits)
  • Story tightening advice (what to emphasize/cut)
  • Competitive positioning (vs. recent papers in journal)
  • Timeline with milestones
  • Resource/personnel needs
  • A **single mainline narrative** when the project currently has multiple parallel ideas
  • A **Figure 1–6 manuscript skeleton** when the user needs help converging a broad platform story

  IMPORTANT NARRATIVE RULE:
  If the project has several promising branches (e.g. method, validation platform, flagship application, future translational direction), do NOT preserve them as equal-weight parallel stories for Nature Biotechnology. Collapse them into:
  1. **one platform/method engine**,
  2. **one validation or enabling platform innovation**,
  3. **one flagship biological/engineering application**,
  while moving broader extensions (for example eukaryotic therapy or distant disease applications without direct data) into Discussion/Outlook. This "platform + validation paradigm + flagship application" compression is often the difference between an ambitious but diffuse project and an NBT-shaped manuscript.

STEP 6: Final verdict with confidence intervals
  Format:
  "Current state: <journal> readiness = X/10"
  "With full experiments: readiness = Y/10, success probability = Z%"
  "Recommended target journal (if no additional data): <weaker journal>"
  "Best-case timeline to <target>: N months"
```

---

## 📊 Evaluation Matrix Template

Use this standardized scoring for consistency:

```
Journal Target: Nature Biotechnology

I. METHODOLOGY (30%)
   Score: __/10
   - Novelty of approach
   - Rigor of validation (orthogonal methods)
   - Reproducibility (code/data availability)
   
II. EXPERIMENTAL VALIDATION (30%) 
   Score: __/10
   - Biophysical characterization (SPR/BLI/ITC)
   - Structural confirmation (crystal/EM/cryo-EM)
   - Cellular functional assays
   - In vivo/application demonstration (if applicable)
   
III. BIOLOGICAL INSIGHT (25%)
   Score: __/10
   - Mechanistic understanding (not just phenotype)
   - New biological knowledge revealed
   - Integration with existing paradigms
   
IV. IMPACT & STORY (15%)
   Score: __/10
   - Importance of problem addressed
   - Clarity of narrative
   - Breadth of potential applications
   - Compelling figures/data presentation

OVERALL: ___/40 → Journal Suitability: 
  >32: Excellent fit (pursue immediately)
  26-32: Good fit (with gap fixes)
  20-25: Marginal (consider tier-2 journal first)
  <20: Major revisions needed
```

---

## ⚠️ Common Pitfalls to Check

**Computational Biology-specific red flags**:

1. **"Evaluation on synthetic data only"**
   - Real biological targets? Or toy examples?
   - NBT wants real-world impact

2. **"Single-model validation"**
   - Only using AF3's own scores? Red flag for overfitting
   - Need orthogonal validation (different predictor/experiment)

3. **"Success rate inflation"**
   - "90% success" on trivial cases?
   - Check: How restrictive are success criteria?

4. **"Missing controls"**
   - Negative controls (non-binding variants)?
   - Baseline comparisons (prior methods)?

5. **"Application theater"**
   - Vague "this could be used for drug design" 
   - NBT wants concrete demonstration, not speculation

5. **"No failure analysis"**
   - Only showing successes, hiding failures
   - NBT appreciates understanding limitations

6. **Big-data-to-disease target indication without causal proof**
   - If a project moves from GWAS/PWAS/omics/ML to disease targets, require a separate target-indication layer instead of letting biomarker evidence become causal language.
   - Good upgrade: code-generated `causal_target_indication_table.csv` plus a readable report that scores every candidate by genetic support, replication, direction consistency, SHAP/feature importance, stability, drug-perturbation concordance, known biology, and explicit caution flags.
   - Add a second readiness-audit layer before claiming formal causality: check whether packaged files contain SNP-level exposure and outcome summary statistics with variant ID, alleles, EAF, beta, SE, P, and sample size. If only protein-level/model-level rows exist, export required schemas and state that coloc/MR is blocked instead of fabricating causal results.
   - Publication boundary: call outputs "target indications", "causal validation priorities", or "genetically anchored hypotheses" until locus-level colocalization, MR/sensitivity analyses, and/or perturbation evidence exist.
   - See `references/big-data-causal-target-indication.md` for a reusable scoring/report and readiness-audit pattern.

7. **Big-data-to-disease target indication without causal proof**
   - If a project moves from GWAS/PWAS/omics/ML to disease targets, require a separate target-indication layer instead of letting biomarker evidence become causal language.
   - Good upgrade: code-generated `causal_target_indication_table.csv` plus a readable report that scores every candidate by genetic support, replication, direction consistency, SHAP/feature importance, stability, drug-perturbation concordance, known biology, and explicit caution flags.
   - Publication boundary: call outputs "target indications", "causal validation priorities", or "genetically anchored hypotheses" until locus-level colocalization, MR/sensitivity analyses, and/or perturbation evidence exist.
   - See `references/big-data-causal-target-indication.md` for a reusable scoring/report pattern.

   - Distinguish real computational artifacts (ranked candidates, run reports, predictor outputs) from manuscript-level claimed results
   - Verify whether root-level outputs actually reproduce headline claims, or are only toy/minimal examples
   - Treat metric collapse (e.g. a ranking feature degenerates to 0.0 for all candidates) as a target-definition or evaluation-pipeline risk, not just a cosmetic issue
   - For multi-model workflows, weak cross-model coupling can be a substantive red flag for generalizability

---

## 🎯 Journal-Specific Adjustments

### For Nature Methods:
```
Emphasize:
  • Benchmarking against existing methods
  • Usability/user experience
  • Open-source implementation quality
  • Community adoption potential
  
De-emphasize:
  • Specific biological application (can be 1-2 examples only)
  • Deep mechanistic insight (nice but not required)
  
Minimum bar:
  • Must have: Method + validation on ≥3 diverse datasets
  • Should have: Comparison to ≥3 state-of-art methods
  • Could have: Simple biological example (1 case study)
```

### For Science:
```
Emphasize:
  • Cross-disciplinary impact
  • Paradigm-shifting potential
  • Broad scientific community interest
  
De-emphasize:
  • Technical minutiae (put in SI)
  • Extensive validation (one compelling example enough)
  
Minimum bar:
  • Must have: Fundamental insight that transcends single field
  • Should have: At least one "wow" result that captures imagination
```

### For Cell:
```
Emphasize:
  • Deep molecular/cellular mechanism
  • Disease relevance if medical
  • Confocal/imaging evidence
  • Multiple lines of orthogonal evidence
  
Minimum bar:
  • Must have: Mechanism (not just phenotype)
  • Must have: Multiple experimental modalities
  • Computational work must directly enable biology
```

---

## 📝 Output Format Template

When delivering verdict to user:

```
# Journal Readiness Assessment: <Project Name>

## 🎯 Target Journal: <Journal Name>

### Executive Summary (3 lines)
<One-sentence project description>. <Current status>. <Gap to target>.

---

## 📊 Current State Analysis

### What's Strong ✅
1. **Methodological rigor**: <specific evidence>
2. **Computational results**: <quantitative metrics from data files>
3. **Documentation**: <evidence of organization>
4. **Novelty angle**: <unique selling point>

### Critical Gaps ❌
1. **[Gap Name] - P0 (blocks publication)
   - Current: <what's missing>
   - Required: <what target journal expects>
   - Evidence: <where gap appears in documents>
   
2. **[Gap Name] - P1 (limits impact)
   - ...
   
---

## 🗺️ Remediation Roadmap

### Phase 1: Must-Have Experiments (Timeline: N months)
**Priority**: 🔴 Blockers for submission

**Task 1: <Specific experiment>**
- Purpose: <why needed>
- Success criteria: < measurable outcome>
- Timeline: <X weeks>
- Resources: <equipment/ reagents>
- Risk: <low/medium/high>

**Task 2: ...**

---

### Phase 2: Impact Enhancements (Timeline: M months)
**Priority**: 🟡 Improves acceptance odds

**Task: ...**

---

### Phase 3: Polish & Submit
**Priority**: 🟢 Final touches

---

## 🎯 Strategic Recommendations

### Storyline
**Recommended narrative**: "<One-sentence core message>"
**Why this works**: <alignment with journal readership>
**To cut**: <elements that dilute focus>
**To emphasize**: <unique differentiators>

### Competitive Positioning
**Recent similar papers in <journal>**:
- Paper A (2024): <brief description, how we differ>
- Paper B (2023): <brief description>

**Our unique angle**: <What makes us different/better>

### Journal Selection Strategy
```
Primary target: <journal> (if all gaps fixed)
Timeline: <N> months preparation
Success probability: <X>%

If timeline constrained: Consider <tier-2 journal>
Rationale: <already meets criteria for weaker journal>
```

---

## ⏱️ Realistic Timeline & Resources

**Optimal path** (aggressive):
```
Months 1-3:  Critical experiments
Months 4-6:  Impact experiments + analysis
Months 7-8:  Drafting (methods + results)
Months 9:    Internal review + revisions  
Months 10-11: Submission
TOTAL: 11 months
```

**Conservative path** (including failures):
```
Add 30-50% buffer for:
- Experiment optimization cycles
- Negative results requiring pivots
- Collaborator delays
- Manuscript revisions

TOTAL: 15-18 months
```

**Budget estimate**:
- Wetlab reagents/consumables: ¥XXX,XXX
- Core facility access (SPR, EM): ¥XX,XXX
- Personnel (1 researcher × 15 months): ¥XXX,XXX
- Publication costs (open access): ¥XX,XXX
**Total: ¥XXX,XXX**

---

## 🎲 Success Probability Matrix

| Scenario | Conditions | Probability | Timeline |
|----------|------------|-------------|----------|
| **Best case** | All experiments succeed on first attempt | 70% | 11 months |
| **Realistic** | 1-2 experiments need optimization | 50% | 14 months |
| **Conservative** | Major experimental pivot required | 30% | 18+ months |

---

## 🚨 Risk Mitigation

**Top 3 risks & mitigation**:

1. **Risk**: Key binder fails to express/purify
   **Mitigation**: Have 5-7 backup candidates; small-scale express test early (Month 1)

2. **Risk**: SPR shows weak/no binding despite good metrics
   **Mitigation**: Consider alternate validation (BLI, ITC, MST); design new round if needed

3. **Risk**: Narrative weakens during writing
   **Mitigation**: Draft figure panels first → ensure data tells story; get internal feedback at Month 7

---

## 📋 Immediate Action Items (Next 30 Days)

- [ ] Gap verification: Confirm missing items with lab (are SPR data really absent?)
- [ ] Resource check: Is SPR/BLI equipment accessible? Timeline?
- [ ] Personnel: Who will execute experiments? Availability?
- [ ] Budget: Confirm funding covers wetlab costs
- [ ] Timeline lock: Set concrete date for first data review

---

## 🔍 Confidence Assessment

This assessment confidence: **High/Medium/Low**
- High confidence: Computational completeness, documentation quality
- Medium confidence: Experimental feasibility estimates
- Low confidence: Exact timeline (depends on lab-specific factors)

**Recommendation**: Re-assess after Phase 1 (Month 3) when first experimental data available.

---

*Skill generated based on analysis of narl_project NBT readiness evaluation, 2026-04-24.*