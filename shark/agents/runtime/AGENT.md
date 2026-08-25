# Agent Runtime

The runtime treats Markdown as the agent contract and Python as the execution layer.

## Discovery
An agent directory is valid when it contains `AGENT.md`. The runtime discovers agents recursively and exposes their instruction paths to the orchestrator.

## Safety
Markdown is configuration and policy, not executable code. Scripts remain responsible for deterministic execution, validation, and I/O.

## Future extension
Agent folders can add `workflow.md`, `scoring.md`, `sources.md`, or additional scripts without changing the core discovery contract.
