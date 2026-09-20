---
name: security-audit
description: Audit application code, dependencies, workflows, secrets handling, permissions, and external integrations for security weaknesses.
---

# Security Audit

## Workflow

1. Identify secrets, credentials, tokens, webhooks, external APIs, filesystem/network access, and privileged workflows.
2. Inspect authentication and authorization boundaries.
3. Check input validation, command execution, path handling, serialization, dependency use, and logging.
4. Review GitHub Actions permissions and supply-chain exposure.
5. Check for credentials accidentally committed to source.
6. Classify findings by severity and exploitability.
7. Provide remediation with minimal scope.
8. Re-run relevant tests or static checks after changes.

## Rules

- Never print secrets.
- Do not weaken security controls to make tests pass.
- Treat third-party code and CI actions as supply-chain dependencies.
- Distinguish confirmed vulnerabilities from potential risks.

## Output

For each finding:
- severity
- evidence
- affected component
- impact
- remediation
- verification
