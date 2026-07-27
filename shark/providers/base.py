from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

import pandas as pd

REQUIRED_COLUMNS = ["open", "high", "low", "close", "volume"]


class DataProvider(ABC):
    """Fetches daily OHLCV history for a symbol.

    Returned frames have columns open/high/low/close/volume, a DatetimeIndex,
    and rows sorted oldest first.
    """

    name: str = "base"
    default_symbols: List[str] = []

    @abstractmethod
    def fetch(self, symbol: str, days: int = 365) -> pd.DataFrame:
        ...

    @staticmethod
    def validate(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(f"{symbol}: missing columns {missing}")
        if df.empty:
            raise ValueError(f"{symbol}: no data returned")
        df = df[REQUIRED_COLUMNS].sort_index()
        return df[~df.index.duplicated(keep="last")]
