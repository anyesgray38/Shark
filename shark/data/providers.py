from abc import ABC, abstractmethod
from pathlib import Path
import csv
from datetime import datetime
from .models import Candle

class MarketDataProvider(ABC):
    @abstractmethod
    def candles(self, symbol: str, timeframe: str, start: datetime | None = None, end: datetime | None = None) -> list[Candle]:
        raise NotImplementedError

class CSVMarketDataProvider(MarketDataProvider):
    """Reads normalized OHLCV CSV files; no external API required."""
    def __init__(self, root: str = "data"):
        self.root = Path(root)

    def candles(self, symbol, timeframe, start=None, end=None):
        path = self.root / f"{symbol}_{timeframe}.csv"
        if not path.exists():
            return []
        out = []
        with path.open(newline="") as f:
            for row in csv.DictReader(f):
                ts = datetime.fromisoformat(row["timestamp"])
                if start and ts < start: continue
                if end and ts > end: continue
                out.append(Candle(ts, float(row["open"]), float(row["high"]), float(row["low"]), float(row["close"]), float(row.get("volume", 0))))
        return out
