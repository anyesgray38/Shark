# 🦈 Shark

A technical setup scanner: point it at a watchlist and it hunts for
tradeable setups — breakouts, oversold bounces, MACD crosses, golden
crosses, volume spikes, and Bollinger squeezes — then ranks everything by a
composite score. Results come out as a CLI table, JSON, or a live web
dashboard.

Shark is the front of the trading funnel: it finds candidates worth a
closer look. It doesn't place trades.

## Quick start

```bash
pip install -r requirements.txt

# Scan the default crypto watchlist (Coinbase public data, no API key)
python -m shark scan

# Scan stocks via Yahoo Finance
python -m shark scan --provider yahoo --symbols AAPL,NVDA,TSLA --detail

# Only show strong setups, as JSON
python -m shark scan --min-score 50 --json

# Offline demo with deterministic synthetic data (no network)
python -m shark scan --provider synthetic
```

## Web dashboard

```bash
uvicorn shark.server:app --port 8000
```

Open http://localhost:8000 — pick a data source, enter symbols (or use the
default watchlist), and scan. Rows with signals expand on click to show the
reasoning behind each detection.

API endpoints:

- `GET /api/scan?provider=coinbase&symbols=BTC-USD,ETH-USD&min_score=40`
- `GET /api/providers`

Scan results are cached for 5 minutes per (provider, symbols, days) key;
pass `refresh=true` to bypass.

## Data providers

| Provider | Assets | Auth | Notes |
|-----------|--------|------|-------|
| `coinbase` | Crypto | none | Coinbase Exchange public candles API |
| `yahoo` | Stocks/ETFs | none | via `yfinance`; Yahoo rate-limits shared/cloud IPs |
| `synthetic` | Demo | none | Deterministic seeded data for tests and offline demos |

Adding a provider means subclassing `shark.providers.base.DataProvider`
with one method: `fetch(symbol, days) -> DataFrame[open, high, low, close,
volume]`.

## Signal detectors

| Detector | Fires when |
|----------|------------|
| `breakout` | Close breaks the prior 20-day high on elevated volume |
| `oversold_bounce` | RSI dipped below 30 and has turned up with price |
| `macd_cross` | MACD line crossed above its signal line in the last 2 bars |
| `golden_cross` | SMA50 crossed above SMA200 in the last 5 bars |
| `volume_spike` | Volume z-score ≥ 2.5 with a directional close |
| `squeeze` | Bollinger bandwidth in the bottom decile of the last 120 bars |

Each detector returns a 0–100 score with a human-readable reason. The
composite score lets the strongest signal dominate and adds a 25% bonus for
each confirming signal, capped at 100.

## Tests

```bash
pytest
```

The test suite runs entirely offline against the synthetic provider.

## Disclaimer

Shark surfaces technical patterns for research. Nothing it outputs is
financial advice.
