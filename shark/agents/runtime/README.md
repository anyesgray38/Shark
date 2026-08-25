# Runtime

The runtime is the enforcement layer for Markdown-defined agents.

## Guarantees

- Discovers `AGENT.md` recursively.
- Loads Markdown as data/configuration, never executable code.
- Provides deterministic routing.
- Provides structured handoffs.
- Preserves provenance and failure state.
- Prevents unvalidated artifacts from being treated as production-ready signals.
- Represents disconnected Penpot operations as `DESIGN_SPEC_ONLY`.

## Extension points

Agent folders can add scripts and Markdown contracts without modifying discovery.
