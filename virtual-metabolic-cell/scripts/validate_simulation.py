#!/usr/bin/env python3
"""Quick validation test for virtual metabolic cell simulation."""

import sys
from pathlib import Path

# Adjust path as needed
sys.path.insert(0, str(Path(__file__).parent.parent))

from aivm_va_cell import load_model, simulate_scenario, Scenario, StepCondition, summarize
import pandas as pd

# Create a single baseline scenario
test_scenario = Scenario(
    scenario_id='validation_test',
    product='arginine',
    label='Low O2 shift',  # Must match baseline label for summarize()
    steps=[
        StepCondition(0.0, -18.0, 0.0, 'growth_high_o2'),
        StepCondition(2.0, -2.0, 0.0, 'production_low_o2'),
    ],
    total_h=4.0,
    dt_h=2.0
)

print("Loading model...", flush=True)
model = load_model()

print("Running validation scenario...", flush=True)
df = simulate_scenario(model, test_scenario)

print("\nSimulation results:", flush=True)
print(df[['time_h', 'phase', 'status', 'biomass_proxy', 'product_flux']].to_string(index=False), flush=True)

# Create summary
summary = summarize(df)

print("\nSummary:", flush=True)
print(summary.to_string(index=False), flush=True)

# Check for expected results
if len(summary) > 0:
    print("\n✓ Validation passed!", flush=True)
else:
    print("\n✗ Validation failed!", flush=True)
    sys.exit(1)
