from dataclasses import dataclass
from ..data.models import Candle
from .market_structure_events import StructureBreak

@dataclass(frozen=True)
class OrderBlock:
    direction: str
    index: int
    low: float
    high: float


def detect(candles: list[Candle], breaks: list[StructureBreak], search_back: int = 5) -> list[OrderBlock]:
    if search_back < 1: raise ValueError("search_back must be positive")
    out=[]
    for event in breaks:
        start=max(0,event.index-search_back)
        for i in range(event.index-1,start-1,-1):
            c=candles[i]
            if event.direction=="bullish" and c.close < c.open:
                out.append(OrderBlock("bullish",i,c.low,c.high)); break
            if event.direction=="bearish" and c.close > c.open:
                out.append(OrderBlock("bearish",i,c.low,c.high)); break
    return out
