from abc import ABC, abstractmethod
from datetime import datetime
from shark.models import Candle

class MarketDataSource(ABC):
    """Provider-neutral interface. API, file, broker, or web-backed adapters can implement this."""

    @abstractmethod
    def candles(self, symbol: str, timeframe: str, start: datetime, end: datetime) -> list[Candle]:
        raise NotImplementedError

class CsvDataSource(MarketDataSource):
    def __init__(self, root: str):
        self.root = root

    def candles(self, symbol: str, timeframe: str, start: datetime, end: datetime) -> list[Candle]:
        raise NotImplementedError("CSV adapter is the next data-layer implementation.")
