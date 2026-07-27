from __future__ import annotations

from typing import List

import pandas as pd

from .base import DataProvider


class YahooProvider(DataProvider):
    """Daily stock data via yfinance.

    yfinance is an optional dependency; install with `pip install yfinance`.
    """

    name = "yahoo"
    default_symbols: List[str] = [
        "AAPL",
        "MSFT",
        "NVDA",
        "TSLA",
        "AMZN",
        "GOOGL",
        "META",
        "AMD",
        "NFLX",
        "SPY",
    ]

    def fetch(self, symbol: str, days: int = 365) -> pd.DataFrame:
        try:
            import yfinance as yf
        except ImportError as exc:
            raise RuntimeError(
                "yfinance is required for the yahoo provider: pip install yfinance"
            ) from exc
        df = yf.Ticker(symbol).history(period=f"{days}d", auto_adjust=True)
        df = df.rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            }
        )
        if isinstance(df.index, pd.DatetimeIndex):
            df.index = df.index.tz_localize(None)
        return self.validate(df, symbol)
