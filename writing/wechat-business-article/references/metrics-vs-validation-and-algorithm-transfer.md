# Metrics vs. validation, and how to translate a paper into design guidance

Use this reference when a user wants a scientific paper turned into a 公众号 article and asks questions like:
- '这个标题可以吗？'
- 'X = 物理模型吗？'
- '突出某个子系统标题呢？'
- '把核心算法写进去'
- '对我们做蛋白设计有什么启发？'

## 1. Separate benchmark metrics from real-world validation

Do not blur these categories.

### Evaluation metrics
These are scoring or comparison devices, not the physical world:
- DockQ
- LDDT / pLDDT
- AUROC / AUPRC
- pass rate
- top-k accuracy
- perplexity
- correlation coefficients

Recommended wording:
- 'DockQ is a complex-structure quality metric, not a physical model.'
- 'This result shows benchmark improvement, not by itself experimental confirmation.'

### Stronger validation layers
These are closer to reality and should carry more rhetorical weight in the article:
- cryo-EM / X-ray / NMR structural confirmation
- BLI / SPR / ITC affinity measurements
- competition / epitope assays
- selectivity or off-target tests
- cell-based functional assays
- in vivo validation

Recommended article move:
After mentioning a metric, immediately ask: 'What is the strongest reality-check in this paper?' Then build the headline around that layer if possible.

## 2. Title selection rule
If a user proposes a title, test it against the strongest evidence chain.

### Good title pattern
Center the title on the subsystem or claim that is actually validated.
Example:
- Better: 'ESMFold2 的真正突破：不只是更准，而是更快、更能设计、也更能被实验验证'
- Worse: a very broad title that implies the whole paper is fully validated when the evidence mainly supports one module.

### Decision heuristic
Ask internally:
1. What exact component does the paper most directly validate?
2. Is the title naming that component, or a broader concept around it?
3. If broader, would a reader infer stronger evidence than the paper really provides?
4. If yes, narrow the title to the validated component.

## 3. Algorithm-to-practice extraction template
When the user asks to 'write in the core algorithm' or connect the paper to their own work, add a dedicated section.

### Minimum structure
1. Problem factorization
   - Write the paper's decomposition or objective in plain language.
   - If there is a formal factorization, include it.

2. Major modules
   - What each module is
   - What it contributes
   - What failure mode it is trying to reduce

3. Search / optimization loop
   - Sampling vs. gradient-based optimization vs. ranking ensemble
   - What is optimized directly
   - What is only used as a screening score

4. Practical takeaways for the user's workflow
   - 3-5 bullets
   - Prefer statements like:
     - separate sequence prior from interface scoring
     - do not collapse all objectives into one black-box score
     - speed is part of design capability when screening at scale
     - judge value by experimental hit rate, not only by benchmark scores

## 4. Protein-design-specific translation pattern
For protein design papers, one useful compression is:
- sequence prior
- conditional structure/interface model
- search loop
- validation ladder

### Validation ladder example
1. benchmark metric
2. structural confirmation
3. affinity confirmation
4. epitope/selectivity confirmation
5. functional confirmation

This helps avoid overstating what the paper actually proved.

## 5. Compact wording snippets
Use or adapt these when useful.

- 'X is a quality metric, not a physical model.'
- 'The stronger evidence in this paper comes from structure/affinity/function, not from the benchmark score alone.'
- 'The title should track the most directly validated subsystem, not the broadest ambition statement in the paper.'
- 'For design work, the main lesson is not just that the model is stronger, but how the paper decomposes prior, structure scoring, and search.'
