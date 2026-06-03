# High-DO Fermentation Visualization and Carbon Accounting

Context: E. coli virtual-cell fermentation project where the user clarified that the real process keeps high dissolved oxygen throughout the entire run, including late production phase.

Key durable lessons

1. Process assumption alignment
- If the user says there is no low-oxygen fermentation, remove low-O2 assumptions everywhere, not just in the main scenario builder.
- Update main scenarios, tests, helper scripts, autoresearch baselines, labels in summaries, and figure/report titles together.
- In this project, the stable baseline label is `High O2 constant`, not `Low O2 shift`.
- Use explicit phase names such as `growth_high_o2` and `production_high_o2` to avoid ambiguity.

2. What to persist in time-course outputs
To support downstream visualization cleanly, save these columns directly from simulation:
- `o2_bound`
- `o2_uptake_flux`
- `co2_release_flux`
- `product_pool_mmol`
- `co2_pool_mmol`

Pool variables prevent downstream code from having to reconstruct cumulative state from noisy per-step fluxes.

3. Visualization logic that worked
- DO curve: use an oxygen-uptake-based proxy, not only categorical phase labels.
- OD curve: `OD_proxy = biomass_proxy * 20` was used as a coarse display proxy.
- Product concentration: derive from `product_pool_mmol`, not a second cumulative sum over `product_flux_auc_step`.
- Yield: compute from product mass / consumed glucose mass.
- Carbon allocation: compare glucose carbon input vs product carbon + biomass carbon + CO2/other sink.

4. Carbon-accounting pitfall
A bad pattern is:
- simulation emits `product_flux_auc_step = product_flux * dt`
- visualization then does `cumsum(product_flux_auc_step)` while the simulation already effectively tracked integrated output elsewhere
This can inflate product accumulation and produce impossible carbon efficiencies above 100%.

Preferred fix
- track `product_pool_mmol` during the simulation loop
- track `co2_pool_mmol` during the simulation loop
- compute product carbon from product-specific carbon number:
  - arginine: 6
  - lysine: 6
  - glutamate: 5
- use a biomass carbon estimate explicitly documented in code (here: 24.6 mmol-C per gDW proxy)

5. Reporting conventions
For this workflow, reports/figures should make explicit when values are proxies, e.g.:
- `g/L (proxy)`
- `OD600 proxy`
- `carbon allocation` using modeled pools and sink proxies

6. Verification checklist after changing oxygen assumptions
- no formal scenario still uses `production_low_o2`
- no baseline lookup still expects `Low O2 shift`
- time-course CSV includes oxygen and cumulative product/CO2 fields
- carbon efficiency does not exceed 100% unless the model explicitly justifies external carbon not counted in glucose pool
- figure titles and report text state full high-DO fermentation consistently

7. Non-blocking issue observed
Matplotlib may still emit Chinese glyph warnings even when figures are successfully written. Treat this as a presentation-quality improvement task, not a reason to distrust the numeric outputs.
