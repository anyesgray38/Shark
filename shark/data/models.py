from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Candle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0

@dataclass(frozen=True)
class MarketSnapshot:
    symbol: str
    timeframe: str
    candles: tuple[Candle, ...]
