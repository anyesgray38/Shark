# Shark Adaptive Research Engine

Adaptive quantitative research platform for XAUUSD, forex, futures, MAG 7, VIX and crypto.

## Architecture

AI proposes and challenges research hypotheses. Python/statistical code measures them. No model becomes production-ready from backtest performance alone.

### Research loop

`observe -> discover features -> generate hypotheses -> backtest -> out-of-sample -> walk-forward -> Monte Carlo -> permutation -> cost/slippage stress -> paper validation -> promote/reject`

### Markets

- Primary: XAUUSD
- Forex: EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, USDCAD, NZDUSD
- Futures: ES, NQ, YM, RTY, GC, SI, CL, ZN
- MAG 7: AAPL, MSFT, NVDA, AMZN, META, GOOGL, TSLA
- Volatility: VIX
- Crypto: BTCUSD, ETHUSD, SOLUSD

## Start the dashboard

```bash
python run.py
```

The starter runs in research/paper mode only. Live trading is intentionally not enabled.

## Radium / Hal

Set `RADIUM_API_KEY` in your environment to enable the optional OpenAI-compatible Radium reasoning layer. Keep secrets out of Git.
