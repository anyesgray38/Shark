from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class Candle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0

    @property
    def body(self) -> float:
        return abs(self.close - self.open)

    @property
    def range(self) -> float:
        return self.high - self.low

@dataclass(frozen=True)
class Trade:
    entry_time: datetime
    exit_time: datetime
    entry: float
    exit: float
    side: int
    size: float = 1.0

    @property
    def pnl(self) -> float:
        return (self.exit - self.entry) * self.side * self.size

@dataclass
class ResearchResult:
    model_id: str
    trades: list[Trade]
    score: float = 0.0
    status: str = "RESEARCH_ONLY"
    notes: Optional[str] = None
