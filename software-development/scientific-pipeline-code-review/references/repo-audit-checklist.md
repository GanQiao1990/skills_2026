# Repository-wide scientific project audit checklist

Use this when the user asks to "review the project", "audit the repo", or review the current directory for a scientific codebase.

## Review scope
- Structure: top-level layout, true entrypoints, runners, orchestration scripts
- Reproducibility: declared dependencies vs imported packages; external repos/data; absolute paths
- Portability: machine-specific interpreters, `/home/...` paths, `sys.path` hacks, env assumptions
- Verification: tests, smoke checks, syntax checks, artifact existence checks
- Manuscript consistency: canonical paper, canonical figure family, canonical metrics
- Release hygiene: debug files, stale logs, duplicate reports, legacy outputs in main tree

## High-value findings to look for
1. Missing runtime dependencies that break README quick-start
2. Hard-coded workstation paths in runners and figure scripts
3. Sibling repository coupling not documented as prerequisite
4. Conflicting headline numbers across manuscript/report files
5. Stale references to missing outputs from older pipeline versions
6. No test suite or smoke-test harness for major entrypoints
7. Generated figures/results presented as canonical without a locked source dataset

## Suggested output headings
- Overall verdict
- What looks strong
- Highest-priority findings
- Issues by category: reproducibility, portability, testing, manuscript consistency, release hygiene
- Priority action plan (P0/P1/P2)
- Bottom line
