---
name: dependency-intelligence
description: Analyze project dependencies for outdated packages, duplicate capabilities, compatibility risks, supply-chain concerns, and better alternatives.
---

# Dependency Intelligence

## Workflow

1. Identify package manifests and lockfiles.
2. Inventory direct and important transitive dependencies.
3. Detect duplicate libraries solving the same problem.
4. Check compatibility with the project's runtime.
5. Research maintained alternatives when a dependency is weak, abandoned, oversized, or redundant.
6. Evaluate migration cost and breaking changes.
7. Recommend upgrades only when evidence supports them.
8. Validate with tests and build commands.

## Output

Return a dependency matrix containing:
- package
- current role
- risk/opportunity
- alternative or upgrade
- migration effort
- validation required

Avoid upgrades solely because a newer version exists.
