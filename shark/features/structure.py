from dataclasses import dataclass
from ..data.models import Candle

@dataclass(frozen=True)
class StructureEvent:
    kind: str
    direction: str
    index: int
    level: float


def _pivot_high(candles, i, left, right):
    h=candles[i].high
    return h > max(c.high for c in candles[i-left:i]) and h >= max(c.high for c in candles[i+1:i+right+1])


def _pivot_low(candles, i, left, right):
    l=candles[i].low
    return l < min(c.low for c in candles[i-left:i]) and l <= min(c.low for c in candles[i+1:i+right+1])


def detect(candles: list[Candle], left: int = 2, right: int = 2) -> list[StructureEvent]:
    if left < 1 or right < 1:
        raise ValueError("left and right must be positive")
    events=[]
    last_high=None
    last_low=None
    for i in range(left, len(candles)-right):
        if _pivot_high(candles,i,left,right):
            direction="HH" if last_high is None or candles[i].high > last_high else "LH"
            events.append(StructureEvent("pivot_high",direction,i,candles[i].high)); last_high=candles[i].high
        if _pivot_low(candles,i,left,right):
            direction="LL" if last_low is None or candles[i].low < last_low else "HL"
            events.append(StructureEvent("pivot_low",direction,i,candles[i].low)); last_low=candles[i].low
    return events
