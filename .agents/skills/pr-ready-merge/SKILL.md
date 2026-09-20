---
name: pr-ready-merge
description: Take completed repository work through validation, commit, push, pull request, review, CI repair, and merge readiness.
---

# PR Ready Merge

## Workflow

1. Inspect the diff and changed files.
2. Run the repository's relevant tests, lint, type checks, and build.
3. Fix failures caused by the change.
4. Review the diff for accidental changes, secrets, debug code, and incomplete work.
5. Create a focused commit.
6. Push the branch.
7. Open a pull request with:
   - summary
   - implementation details
   - tests run
   - risks
   - follow-up work
8. Monitor CI and review feedback.
9. Repair failures, re-run validation, and update the PR.
10. Merge only when required checks and review conditions are satisfied.

## Guardrails

- Never claim CI passed without checking it.
- Never merge failing or unreviewed work.
- Prefer squash merges for focused changes unless repository conventions require otherwise.
- Preserve a clean audit trail.
