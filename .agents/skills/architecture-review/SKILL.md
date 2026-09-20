---
name: architecture-review
description: Review a repository's architecture for coupling, boundaries, data flow, extensibility, failure modes, and maintainability before or after implementation.
---

# Architecture Review

## Workflow

1. Inventory entry points, packages, agents, data providers, storage, external services, and deployment surfaces.
2. Trace the main data/control flows.
3. Identify duplicated responsibilities and hidden coupling.
4. Check interfaces between modules.
5. Evaluate:
   - separation of concerns
   - dependency direction
   - configuration
   - observability
   - error propagation
   - testability
   - extensibility
6. Propose the smallest architectural change that solves the identified problem.
7. Validate with tests or static inspection.

## Deliverable

Produce:
- architecture map
- strengths
- concrete failure points
- proposed changes
- migration risk
- validation steps

Do not redesign merely for style.
