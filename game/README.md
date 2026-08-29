# Shark Idle Trading Game

Browser-based incremental trading simulator built as a separate game layer from the quantitative research engine.

## Phase 1 — Economy Foundation

The first playable layer models capital, market price movement, trades, realized/unrealized P&L, risk limits, and deterministic progression.

## Architecture

- `core/` — simulation state and game clock
- `market/` — synthetic market generation
- `trading/` — orders, positions, and P&L
- `progression/` — capital milestones and unlocks
- `ui/` — browser presentation

The game does not import the HTML5GameArchive. The archive is treated as external research/reference material only.
