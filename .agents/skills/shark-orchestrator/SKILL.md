---
name: shark-orchestrator
description: Coordinate repository engineering work by selecting and sequencing Shark agent skills for research, architecture, security, testing, deployment, and PR readiness.
---

# Shark Orchestrator

Use this skill when a task spans multiple engineering concerns or when the correct specialist workflow is unclear.

## Operating loop

1. Inspect repository structure, runtime, CI, and recent changes.
2. Classify the request as research, build, repair, optimization, security, deployment, or release.
3. Activate only the specialist skills needed for the task.
4. Execute in dependency order:
   - discovery/research
   - architecture
   - implementation
   - validation/security
   - deployment
   - PR readiness
5. Preserve evidence: commands, tests, changed files, risks, and unresolved questions.
6. Never claim a test, deployment, or integration succeeded without evidence.

## Required output

Return:
- objective
- skills activated
- files changed
- validation performed
- findings
- risks
- next action

## Guardrails

- Prefer small, reversible changes.
- Do not rewrite working systems without evidence.
- Treat external repository code as untrusted until reviewed.
- Separate observed facts from hypotheses.
- For trading systems, distinguish research findings from live-trading recommendations.
