# ecGEM asset validation before running tuning pipelines

Use this when a local optimisation repo depends on a separate model-assets checkout.

Checklist
1. Verify the upstream asset root exists and contains the expected model + priors.
   - Example: `data/model/eciML1515.xml`
   - Example: `data/model/eciML1515.mat`
   - Example: `data/E.coli/mapped_kcats.csv`
2. Resolve the runtime config to concrete paths before the first run; do not trust placeholder `repo_root: ./Something` values.
3. Confirm the model is actually an ecGEM, not just a plain GEM with a familiar organism/model name.
   - Positive signals: `prot_` / `draw_prot_` reactions, non-zero enzyme-metabolite discovery, non-zero tunable kcat space.
   - Failure signal: the workflow reports 0 enzyme metabolites and 0 tunable parameters. That run may still finish, but it is not performing meaningful kcat tuning.
4. If both XML and MAT assets exist, try the XML/SBML first when the MAT loader fails on malformed identifiers or whitespace-containing reaction names.
5. For long Phase B/C/D runs without an explicit parallelism flag, set:
   - `OMP_NUM_THREADS=<n>`
   - `OPENBLAS_NUM_THREADS=<n>`
   - `MKL_NUM_THREADS=<n>`
   - `NUMEXPR_NUM_THREADS=<n>`
   and run in a tracked background process.

EnzymeTuning / E. coli example
- A plain `iML1515.mat` from a non-ecGEM source can load and benchmark, but may yield:
  - 0 discovered enzyme metabolites
  - 0 tunable kcat parameters
  This means the pipeline is only exercising the wrapper code, not real enzyme-capacity tuning.
- The EnzymeTuning-backed `eciML1515.xml` can load successfully and produce a real kcat space (thousands of tunable parameters), even when direct MAT loading is brittle.
- If Phase A shows a large non-zero tunable space and mapped-kcat priors load successfully, the run has crossed the threshold into a real ecGEM tuning workflow.
