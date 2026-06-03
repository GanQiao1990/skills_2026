---
name: financial-services
description: Use when the task should leverage Anthropic's financial-services repository cloned locally at /home/qiao/qiao_design/financial-services. Routes Hermes to the appropriate financial-services vertical or agent skill files for investment banking, financial analysis, equity research, private equity, wealth management, fund admin, and KYC workflows.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [finance, financial-services, investment-banking, equity-research, wealth-management, private-equity, fund-admin, kyc]
---

# Financial Services

Use this skill when the user wants Hermes to use the Anthropic financial-services repo that is cloned locally at:

`/home/qiao/qiao_design/financial-services`

Important:
- This repository is not laid out as a native Hermes `skills/` tap.
- Its actual skill files live under `plugins/vertical-plugins/*/skills/` and bundled agent copies live under `plugins/agent-plugins/*/skills/`.
- Therefore this wrapper skill is the Hermes entrypoint for that repository.

## Repository map

Core repo layout:
- `plugins/vertical-plugins/financial-analysis/skills/`
- `plugins/vertical-plugins/investment-banking/skills/`
- `plugins/vertical-plugins/equity-research/skills/`
- `plugins/vertical-plugins/private-equity/skills/`
- `plugins/vertical-plugins/wealth-management/skills/`
- `plugins/vertical-plugins/fund-admin/skills/`
- `plugins/vertical-plugins/operations/skills/`
- `plugins/agent-plugins/<agent>/skills/`

## Default routing

When a user request matches one of these domains, inspect the corresponding source skill files in the repo before acting:

- Financial modeling, comps, DCF, LBO, 3-statement, deck refresh, Excel audit
  - `plugins/vertical-plugins/financial-analysis/skills/`
- Teasers, CIMs, buyer lists, merger models, deal tracking
  - `plugins/vertical-plugins/investment-banking/skills/`
- Earnings, model updates, sector overviews, thesis tracking
  - `plugins/vertical-plugins/equity-research/skills/`
- Deal screening, IC memos, due diligence, portfolio monitoring
  - `plugins/vertical-plugins/private-equity/skills/`
- Client reviews, financial plans, portfolio rebalance, tax-loss harvesting
  - `plugins/vertical-plugins/wealth-management/skills/`
- GL recon, break tracing, accrual schedules, roll-forward, NAV tie-out
  - `plugins/vertical-plugins/fund-admin/skills/`
- KYC document parsing and KYC rules
  - `plugins/vertical-plugins/operations/skills/`

## Agent bundles

If the user asks for a named end-to-end workflow, inspect the matching agent bundle first:
- `plugins/agent-plugins/pitch-agent/`
- `plugins/agent-plugins/meeting-prep-agent/`
- `plugins/agent-plugins/market-researcher/`
- `plugins/agent-plugins/earnings-reviewer/`
- `plugins/agent-plugins/model-builder/`
- `plugins/agent-plugins/valuation-reviewer/`
- `plugins/agent-plugins/gl-reconciler/`
- `plugins/agent-plugins/month-end-closer/`
- `plugins/agent-plugins/statement-auditor/`
- `plugins/agent-plugins/kyc-screener/`

## Working method

1. Start from `/home/qiao/qiao_design/financial-services/README.md` to identify the correct vertical or agent.
2. Read the relevant `SKILL.md` inside the repo.
3. Follow that file's domain instructions as closely as the current Hermes environment allows.
4. Prefer source skills in `plugins/vertical-plugins/.../skills/` over duplicated agent copies when both exist.
5. If repo-specific constraints conflict with Hermes tools, state the limitation explicitly and adapt conservatively.

## Good first files to inspect

- `/home/qiao/qiao_design/financial-services/README.md`
- `/home/qiao/qiao_design/financial-services/CLAUDE.md`
- `/home/qiao/qiao_design/financial-services/plugins/vertical-plugins/financial-analysis/skills/comps-analysis/SKILL.md`
- `/home/qiao/qiao_design/financial-services/plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md`
- `/home/qiao/qiao_design/financial-services/plugins/vertical-plugins/equity-research/skills/earnings-analysis/SKILL.md`
- `/home/qiao/qiao_design/financial-services/plugins/vertical-plugins/fund-admin/skills/gl-recon/SKILL.md`
- `/home/qiao/qiao_design/financial-services/plugins/vertical-plugins/wealth-management/skills/financial-plan/SKILL.md`
- `/home/qiao/qiao_design/financial-services/plugins/vertical-plugins/wealth-management/skills/investment-proposal/SKILL.md`
- `/home/qiao/qiao_design/financial-services/plugins/vertical-plugins/wealth-management/skills/portfolio-rebalance/SKILL.md`

## Wealth-management adaptation notes

When the repo is used for personal or household wealth questions (for example: inflation protection, family capital preservation, or a long-horizon household investment framework), route to the `wealth-management` source skills first even if the user is not asking for a formal advisor deliverable.

Practical adaptation:
- Use `financial-plan` for goal hierarchy, cash-flow safety, liabilities, and scenario framing.
- Use `investment-proposal` for allocation rationale, expected-outcome framing, and clear caveats.
- Use `portfolio-rebalance` for target bands, drift thresholds, and annual review rules.
- If the user asks to "write the decision process" rather than just give an allocation, produce a narrative decision memo that explains goals, layers of capital, allocation logic, implementation sequence, and rebalancing/governance rules.
- In household contexts, avoid pretending to give regulated individualized advice when key inputs are missing; explicitly state assumptions and present a conservative base-case framework that can be tightened once age, income, liabilities, and risk tolerance are known.
- When the user wants China-listed ETF implementation, use a function-first ETF sleeve model (cash / core beta / defensive dividend / treasury bond / gold / optional satellite growth), ground current facts with live public quote/history tools, and express timing as staged-entry rules rather than bottom-calling. See `references/china-etf-household-execution.md`.
- Preserve the repo's safety posture: emphasize process, suitability limits, and human review rather than claiming certainty or guaranteed returns.

## Notes

- The repo was tapped in Hermes as `anthropics/financial-services`, but native discovery does not expose its nested skill layout automatically.
- This wrapper skill exists so Hermes can reliably use the repository in future sessions.
