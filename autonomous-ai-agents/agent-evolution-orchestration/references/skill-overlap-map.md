# Skill overlap map for agent evolution work

This note captures the overlap observed during the review of the current Hermes skill library.

## Skills reviewed
- autoskill: mines repeated user workflows from screenpipe and drafts new skills or composition recipes.
- subagent-driven-development: executes plans with fresh subagents and two-stage review.
- agents-orchestrator: orchestrates multi-stage pipelines with QA loops.
- engineering-autonomous-optimization-architect: manages autonomous optimization, shadow testing, and guardrailed routing.

## Durable takeaways
- There is no single Hermes-native, class-level agent-evolution umbrella yet.
- The existing skills cover adjacent parts of the problem, but they are split by function:
  - workflow mining
  - task execution with delegation
  - pipeline orchestration and QA
  - optimization/routing of AI systems
- Future updates should prefer one umbrella plus support references, rather than a new narrow skill for each session.

## Promotion heuristic
- If the work is about observing user behavior and proposing reusable skills, start with autoskill.
- If the work is about executing a plan through subagents, start with subagent-driven-development.
- If the work is about managing a multi-stage pipeline with gates, start with agents-orchestrator.
- If the work is about improving model routing, cost controls, or autonomous optimization, start with engineering-autonomous-optimization-architect.
- If the work is about improving the skill library itself, use the new agent-evolution-orchestration umbrella.
