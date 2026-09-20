# Shark Agent Skills

Reusable engineering workflows for the Shark repository.

## Skills

| Skill | Purpose |
|---|---|
| shark-orchestrator | Select and sequence specialist workflows |
| github-intelligence | Research GitHub for better implementations |
| architecture-review | Review system boundaries and design |
| security-audit | Find application and supply-chain risks |
| dependency-intelligence | Analyze dependencies and alternatives |
| trading-system-review | Validate market-engine and research logic |
| pr-ready-merge | Move completed work through validation and PR readiness |

## Design

Skills follow the Agent Skills format: each capability is a directory containing a required SKILL.md, with optional scripts and references.

The skills are repository-focused. They provide procedures, not hidden state, and should load only when the task requires them.

## Standard lifecycle

DISCOVER -> RESEARCH -> DESIGN -> BUILD -> VERIFY -> REVIEW -> SHIP

The orchestrator activates only the stages required by the task.
