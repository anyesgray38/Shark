# Research Workflow

```text
observe
  -> research
  -> feature analysis
  -> hypothesis generation
  -> backtest
  -> out-of-sample
  -> walk-forward
  -> Monte Carlo / permutation
  -> cost + slippage stress
  -> validation
  -> report
  -> promote / reject
```

## Routing rule
If an upstream stage fails, downstream stages must not present the result as validated.

## Promotion rule
Only artifacts with explicit validation status may feed the Signal Agent.
