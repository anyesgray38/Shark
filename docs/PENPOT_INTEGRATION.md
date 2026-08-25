# Shark + Penpot Integration

Shark uses the official Penpot MCP architecture as its design integration boundary.

## Architecture

`Design Agent -> Penpot MCP Server -> Penpot MCP Plugin -> Penpot Plugin API -> Penpot design file`

The upstream Penpot project provides the MCP server and plugin. Shark does not copy the Penpot monorepo into the trading engine.

## Why Penpot is part of Shark

Penpot provides design tokens, components, variants, libraries, responsive layout, and design-to-code workflows. Its official MCP server enables AI clients to query, transform, and create design elements in a connected design file.

## Shark routing

```text
validated requirement
        ↓
   Design Agent
        ↓
 Penpot specification
        ↓
 Penpot MCP
        ↓
 connected design
        ↓
 implementation
        ↓
 design validation
```

## Connection states

- `UNCONNECTED` — no Penpot project is connected.
- `DESIGN_SPEC_ONLY` — Shark produced a design specification but did not modify Penpot.
- `CONNECTED_READ` — Penpot context was successfully inspected.
- `CONNECTED_WRITE` — Penpot was successfully modified.
- `VALIDATED` — implementation was checked against the design contract.

No agent may claim a connected read or write without the corresponding successful operation.
