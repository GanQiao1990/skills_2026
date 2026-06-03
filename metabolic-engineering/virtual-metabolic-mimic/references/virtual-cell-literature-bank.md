# Virtual-cell literature bank for NarL project

## Core references

- Sun, Ahn-Horst, Covert. The E. coli Whole-Cell Modeling Project. EcoSal Plus (2021). DOI: 10.1128/ecosalplus.esp-0001-2020
  - Use for framing a virtual-cell / whole-cell model as a time-resolved state-updating system.
- Mahadevan, Edwards, Doyle. Dynamic Flux Balance Analysis of Diauxic Growth in Escherichia coli. Biophysical Journal (2002). DOI: 10.1016/S0006-3495(02)73903-9
  - Canonical dFBA reference for growth-phase transitions.
- Meadows, Karnik, Lam, Forestell. Application of dynamic flux balance analysis to an industrial Escherichia coli fermentation. Metabolic Engineering (2010). DOI: 10.1016/j.ymben.2009.07.006
  - Useful for process-style dynamic control and fermentation-phase coupling.
- Lee, Chou, Kemp, Voit. Dynamic Metabolic Flux Analysis. Encyclopedia of Systems Biology (2013). DOI: 10.1007/978-1-4419-9863-7_1158
  - Good conceptual reference for time-varying flux interpretation.
- Abreu, Castro, Silva. Simulation step size analysis of a whole-cell computational model of bacteria. AIP Conference Proceedings (2016). DOI: 10.1063/1.4968706
  - Reminder that step size and update logic matter in whole-cell mimic workflows.

## Practical lessons for NarL / amino-acid production

1. Treat the model as a phase-aware virtual cell, not a static endpoint optimizer.
2. Explicitly separate growth, shift, and production states in code, plots, and reports.
3. Use time-step mimic to track oxygen shift, nitrate pulse, nitrite handling, redox proxies, and product export.
4. Present NarL as a switch-like production-phase controller, not a constant overexpression knob.
5. Keep proxy terminology explicit: if a metric is a proxy, say so in the manuscript and figure labels.

## Session-specific note

For the current NarL project, the most useful deliverable was a literature-grounded summary file in the project root:
- /home/qiao/qiao_design/e_coli_model/narl_virtual_metabolic/VIRTUAL_CELL_LITERATURE_NOTES.md

Future runs should consult that project note when improving README text, figure narratives, or the virtual-cell state machine.
