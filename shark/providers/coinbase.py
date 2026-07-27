from __future__ import annotations

import time
from typing import List

import pandas as pd
import requests

from .base import DataProvider

_API = "https://api.exchange.coinbase.com"
_MAX_CANDLES = 300  # Coinbase per-request limit
_DAY = 86400


class CoinbaseProvider(DataProvider):
    """Daily candles from Coinbase Exchange's public market data API (no auth)."""

    name = "coinbase"
    default_symbols: List[str] = [
        "BTC-USD",
        "ETH-USD",
        "SOL-USD",
        "XRP-USD",
        "ADA-USD",
        "DOGE-USD",
        "AVAX-USD",
        "LINK-USD",
        "LTC-USD",
        "DOT-USD",
    ]

    def __init__(self, session: requests.Session | None = None, retries: int = 3):
        self._session = session or requests.Session()
        self._retries = retries

    def _get_with_retry(self, url: str, params: dict) -> list:
        for attempt in range(self._retries + 1):
            try:
                resp = self._session.get(url, params=params, timeout=30)
                resp.raise_for_status()
                return resp.json()
            except (requests.ConnectionError, requests.Timeout):
                if attempt == self._retries:
                    raise
                time.sleep(1.5 * (attempt + 1))
        raise RuntimeError("unreachable")

    def fetch(self, symbol: str, days: int = 365) -> pd.DataFrame:
        end = int(time.time())
        rows: list[list[float]] = []
        remaining = days
        while remaining > 0:
            batch = min(remaining, _MAX_CANDLES)
            start = end - batch * _DAY
            data = self._get_with_retry(
                f"{_API}/products/{symbol}/candles",
                {
                    "granularity": _DAY,
                    "start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(start)),
                    "end": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(end)),
                },
            )
            if not data:
                break
            rows.extend(data)
            remaining -= batch
            end = start
        if not rows:
            raise ValueError(f"{symbol}: no candles returned")
        # Rows are [time, low, high, open, close, volume], newest first.
        df = pd.DataFrame(
            rows, columns=["time", "low", "high", "open", "close", "volume"]
        )
        df.index = pd.to_datetime(df["time"], unit="s")
        df.index.name = "date"
        return self.validate(df, symbol)
