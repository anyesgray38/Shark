---
name: trading-system-review
description: Review trading research and market-engine code for data integrity, timeframe consistency, signal leakage, backtest validity, risk controls, and production reliability.
---

# Trading System Review

Use for Shark market research, SMC engines, backtests, signal generation, intermarket models, or live market pipelines.

## Workflow

1. Trace data from provider to feature generation to signal to execution/reporting.
2. Verify timestamp, timezone, symbol, timeframe, and candle-boundary consistency.
3. Check for lookahead bias, survivorship bias, leakage, duplicated observations, and unstable indicators.
4. Separate:
   - liquidity narrative
   - structure
   - displacement
   - PDA/confluence
   - regime
   - intermarket confirmation
5. Review multi-timeframe joins for future information contamination.
6. Review backtest assumptions, slippage, spread, fees, execution timing, and position sizing.
7. Test edge cases around missing data, market closures, gaps, and provider failures.
8. Treat research results as hypotheses until independently validated.

## Output

Return:
- data integrity findings
- timeframe findings
- signal logic findings
- statistical/backtest findings
- risk findings
- production findings
- tests required

Never turn an unvalidated research result into a guaranteed trading outcome.
