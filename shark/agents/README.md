# Shark Agent System

Shark uses Markdown files as agent contracts and scripts as deterministic execution layers.

## Architecture

```text
user request
  -> orchestrator
  -> Markdown contract discovery
  -> workflow routing
  -> specialized agent
  -> structured handoff
  -> validation gate
  -> downstream agent
  -> artifact/report
```

## Agent folders

Each agent folder may contain:

- `AGENT.md` — mission, rules, inputs, outputs
- `workflow.md` — execution sequence
- `scoring.md` — scoring methodology
- `sources.md` — evidence policy
- scripts — deterministic execution
- schemas — machine-readable contracts

Existing specialized research roles remain supported; the new runtime provides a common contract and routing layer around them.

## Penpot

The Design Agent is the bridge between validated Shark requirements and Penpot. Penpot is an external design-system integration, not a copied dependency.
