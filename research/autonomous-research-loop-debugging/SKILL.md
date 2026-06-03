---
name: autonomous-research-loop-debugging
description: Debug and operate autonomous research/Bayesian optimization loops that run batches of simulations. Covers path mismatches, variable scoping bugs, data structure errors, and long-running process management.
version: 1.0.0
tags:
  - research
  - bayesian-optimization
  - debugging
  - batch-processing
  - automation
---

# Autonomous Research Loop Debugging & Operation

## When to Use

Use this skill when running an autonomous research/Bayesian optimization loop that:
- Calls a sub-script repeatedly in batches (like `run_batches.py` → `autoresearch_loop.py`)
- Needs to run 10-100+ simulations with checkpointing/resuming
- Has parent/child script architecture with shared state (logs, best configs)

## Common Pitfalls & Fixes

### 1. Path Inconsistency Between Parent and Child Scripts

**Symptom**: Batch runner reports "0/50 done" repeatedly, log file never grows, best config never updates.

**Cause**: Parent script (`run_batches.py`) and child script (`*_loop.py`) use different `RESULTS_DIR` definitions. Parent expects `PROJECT_ROOT/results/` but child writes to `scripts/results/` (relative to its location).

**Fix**: Make child script's `RESULTS_DIR` point to project root:
```python
# In child script (in scripts/ subdirectory)
HERE = Path(__file__).resolve().parent
# WRONG: RESULTS_DIR = HERE / "results" / "autoresearch"
# RIGHT:
RESULTS_DIR = HERE.parent / "results" / "autoresearch"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
```

**Verification**: After first simulation completes, check both locations. Log should appear in parent's expected path.

---

### 2. Variable Not Defined in All Code Paths

**Symptom**: `UnboundLocalError: cannot access local variable 'X' where it is not associated with a value` after N simulations (often when N < initial batch size).

**Cause**: Variable defined only inside conditional branch (e.g., BO phase) but used unconditionally later (in report generation).

**Fix**: Initialize variable at function start, before any branching:
```python
def main():
    strain_names_ordered = sorted(STRAIN_LIST)  # Initialize early
    
    if n_done < N_INITIAL:
        pass  # sampling phase
    else:
        # BO phase - already defined
        pass
    
    # Safe to use here
    generate_figures(history, strain_names_ordered)
```

**Pattern**: Variables used after `if/else` must be defined in both branches OR before the conditional.

---

### 3. Passing Wrong Data Structure to Function

**Symptom**: `AttributeError: 'str' object has no attribute 'get'` when function expects dict.

**Cause**: Passing `pd.DataFrame(valid_hist)` to a function that iterates expecting dictionaries. Iterating a DataFrame yields column names (strings), not row dicts.

**Fix**: Pass the list directly:
```python
# WRONG:
generate_figures(pd.DataFrame(valid_hist), strain_names_ordered)

# RIGHT (if function expects List[Dict]):
generate_figures(valid_hist, strain_names_ordered)
```

**Check**: Verify function signature matches what's passed. If function needs DataFrame, iterate with `.iterrows()`.

---

### 4. Docstring Syntax Error

**Symptom**: `SyntaxError: unterminated triple-quoted string literal`.

**Cause**: Missing closing `"""` or stray backslash in docstring.

**Fix**: Check docstring and next line for completeness:
```bash
python3 -m py_compile file.py  # quick syntax check
```

---

### 5. Long-Running Script Timeouts

**Symptom**: Tool timeout after 300s while script still running.

**Cause**: Default tool timeout is 5 minutes; autonomous loops take 60-120 minutes.

**Fix**: Use `terminal(background=True, timeout=7200, notify_on_complete=True)`.

**Monitoring**: Check progress via log file line count:
```bash
wc -l results/autoresearch/autoresearch_log.jsonl  # lines = simulations completed
```

---

## Diagnostic Checklist

Ordered troubleshooting steps:

1. **Log file exists and grows?** → Path mismatch if missing
2. **Log file contains valid JSON?** → Parse error if invalid  
3. **Best config file updates?** → `save_final_report()` may not be running
4. **Child process still alive?** → `pstree -p <parent_pid>` to see grandchildren
5. **stderr output available?** → Redirect child stderr to logfile

---

## Monitoring Pattern

```bash
# Start in background
nohup python3 run_batches.py > /tmp/batch.log 2>&1 &

# Monitor loop
while true; do
  clear
  echo "=== $(date) ==="
  echo "Completed: $(wc -l < results/autoresearch/autoresearch_log.jsonl)/50"
  python3 -c "import json; d=json.load(open('results/autoresearch/autoresearch_best.json')); print(f'Best: {d[\"best_configuration\"][\"arg_titer_g_L\"]:.2f} g/L')"
  echo "Process: $(ps -p <PID> -o stat=)"
  sleep 60
done
```

---

## Report Generation Template

Final Markdown report should include:
- Total runs & wall-clock time
- Optimal configuration (all 12+ parameters)
- Per-strain statistics (n, max, mean titer)
- Top-5 designs table
- Parameter sensitivity (correlation with objective)
- Baseline vs optimal comparison
- File paths to all artifacts

See `results/autoresearch/OPTIMIZATION_REPORT.md` for a complete example.

---

## Key Principles

1. **Paths must align**: Parent and child must agree on results location. Use `HERE.parent` from `scripts/` subdirectory to reach project root.
2. **Initialize before branching**: Variables used after `if/else` must be defined in all paths.
3. **Match data structures**: Function argument types must match expectations (list vs DataFrame).
4. **Check subprocess exit codes**: `result.returncode != 0` indicates failure.
5. **Monitor files, not just stdout**: The log file is the ground truth of progress.

---

## Related Scripts

- `run_batches.py`: Parent batch runner (orchestrates N runs, tracks progress)
- `scripts/autoresearch_loop.py`: Child optimization loop (BO, simulation, reporting)
- `scripts/two_stage_simulation.py`: The actual FBA simulator called by the loop