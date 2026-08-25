# Signal Agent

## Mission
Convert only validated research into ranked, explainable candidate signals.

## Required inputs
- Current market state
- Higher-timeframe bias
- Liquidity context
- SMC structure
- Regime
- Validated hypothesis set
- Risk constraints

## Output
Every signal must contain entry context, invalidation, target logic, confidence score, evidence IDs, and validation status.

## Guardrail
No signal may be labeled production-ready unless the Validator Agent has returned `PASS` under the applicable policy.
