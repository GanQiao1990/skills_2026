---
name: agent-evolution-orchestration
description: "Class-level umbrella for reviewing, updating, and composing agent workflows and skill libraries from observed behavior, session learnings, and overlapping agent skills. Use when a task is about improving the agent itself, not just completing one user deliverable."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, skills, delegation, orchestration, evolution, self-improvement, workflow, review]
---

# Agent Evolution Orchestration

Use this skill when the work is about improving the agent's reusable behavior: reviewing an existing skill library, identifying overlaps, converting repeated workflows into class-level skills, or updating orchestration patterns for future sessions.

This skill is intentionally umbrella-shaped. Prefer adding one durable class-level skill or support file rather than creating narrow one-session artifacts.

## When to use

Trigger this skill when the user asks to:
- review the current skill library for gaps, overlap, or stale patterns
- update skills based on a session or repeated workflow
- turn repeated agent behavior into reusable procedures
- improve orchestration across subagents, review gates, or skill promotion steps
- design a self-improvement loop for Hermes or another agent system

## Core principles

1. Start from the current skill ecosystem.
   - Identify loaded skills and existing umbrella skills before creating anything new.
   - If an existing umbrella already covers the class, patch it first.

2. Prefer class-level skills over narrow session artifacts.
   - Capture durable workflow patterns, not one-off task narratives.
   - Use references/ for session-specific detail, examples, or evidence.

3. Keep overlaps explicit.
   - If two skills overlap, say so in the output.
   - Note whether the right move is patch, add a reference, or create a new umbrella.

4. Use subagents for decomposition when the task spans discovery, drafting, and review.
   - One worker can inspect the library.
   - One can draft changes.
   - One can review for gaps, duplication, or tone issues.

5. Preserve guardrails.
   - Do not edit protected skills.
   - Do not encode environment-specific failures as durable rules.
   - Do not turn transient setup problems into permanent policy.

## Recommended workflow

1. Inspect the relevant skill(s) and surrounding umbrellas.
2. Decide whether the learning belongs in:
   - an existing skill body,
   - a new reference file,
   - or a new umbrella skill.
3. Update the smallest durable surface that captures the lesson.
4. Add a one-line pointer in the umbrella skill to any new reference or script.
5. If the update reveals overlap, call it out explicitly in the final response.

## Common patterns this skill should absorb

- skill-library review and pruning
- agent workflow retrospectives
- delegation and review sequencing
- reuse vs compose vs novel decision-making
- skill promotion and consolidation
- maintenance of orchestration personas

## Pitfalls

- Do not create a skill named after a single session, issue, PR, or error string.
- Do not copy an entire long transcript into a skill body.
- Do not treat a one-off diagnostic as a lasting rule unless it is clearly generalizable.
- Do not update bundled or pinned skills unless the change is truly durable and the skill is editable.
- Do not bury overlap; make the relationship between skills visible.

## Supporting notes

- See `references/skill-overlap-map.md` for the overlap map and promotion heuristics discovered in this session.
- See `references/promotion-checklist.md` for a compact review checklist when deciding patch vs create.
