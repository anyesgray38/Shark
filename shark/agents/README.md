# Continuous Agent System

The agents operate as a research pipeline under GitHub Actions. Each role has a narrow responsibility and produces evidence for downstream validation.

- data_auditor — data integrity, missing bars, timestamp/order checks
- market_scanner — universe and timeframe coverage
- smc_researcher — structure, liquidity, FVG/IFVG/BPR/OB hypotheses
- candlestick_researcher — candle and multi-candle feature hypotheses
- intermarket_researcher — MAG 7, VIX, futures, forex and cross-market relationships
- regime_researcher — trend/range/volatility/risk regimes
- strategy_researcher — generates testable combinations
- falsification_agent — searches for failure, leakage and regime dependence
- quant_validator — statistical and out-of-sample gates
- code_auditor — regression and implementation checks
- risk_auditor — drawdown/exposure/trade-risk constraints
- reporter — daily evidence report

The workflow is scheduled daily and can also be dispatched manually. AI-assisted reasoning can be connected later through the Radium adapter; credentials remain GitHub Secrets and are never committed.

No agent is allowed to place live orders. Production execution remains a separate disabled boundary.
