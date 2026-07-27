from __future__ import annotations

import hashlib
from typing import List

import numpy as np
import pandas as pd

from .base import DataProvider


class SyntheticProvider(DataProvider):
    """Deterministic simulated OHLCV data — for demos and tests, no network.

    Each symbol gets a reproducible regime-switching random walk seeded from
    its name, so 'DEMO1' always produces the same chart.
    """

    name = "synthetic"
    default_symbols: List[str] = [f"DEMO{i}" for i in range(1, 9)]

    def fetch(self, symbol: str, days: int = 365) -> pd.DataFrame:
        seed = int.from_bytes(
            hashlib.sha256(symbol.encode()).digest()[:4], "big"
        )
        rng = np.random.default_rng(seed)
        base_price = 20.0 + rng.uniform(0, 480)

        # Regime-switching drift: alternating trend blocks of 20-60 days.
        drifts = []
        while len(drifts) < days:
            block = int(rng.integers(20, 61))
            drifts.extend([rng.normal(0.0005, 0.0015)] * block)
        drift = np.array(drifts[:days])

        vol = rng.uniform(0.012, 0.035)
        returns = drift + rng.normal(0.0, vol, days)
        close = base_price * np.exp(np.cumsum(returns))

        open_ = np.empty(days)
        open_[0] = base_price
        open_[1:] = close[:-1] * (1 + rng.normal(0, vol / 4, days - 1))
        spread = np.abs(rng.normal(0, vol, days)) * close
        high = np.maximum(open_, close) + spread
        low = np.minimum(open_, close) - spread

        base_volume = rng.uniform(1e5, 5e6)
        volume = base_volume * np.exp(rng.normal(0, 0.4, days))
        # Occasional volume spikes on big-move days
        big_moves = np.abs(returns) > 2 * vol
        volume[big_moves] *= rng.uniform(2.5, 5.0, big_moves.sum())

        index = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=days)
        df = pd.DataFrame(
            {
                "open": open_,
                "high": high,
                "low": low,
                "close": close,
                "volume": volume,
            },
            index=index,
        )
        df.index.name = "date"
        return self.validate(df, symbol)
