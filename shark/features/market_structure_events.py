from dataclasses import dataclass
from ..data.models import Candle
from .structure import StructureEvent

@dataclass(frozen=True)
class StructureBreak:
    kind: str
    direction: str
    index: int
    broken_level: float

@dataclass(frozen=True)
class Displacement:
    direction: str
    index: int
    body_ratio: float
    range_ratio: float


def breaks(candles: list[Candle], pivots: list[StructureEvent]) -> list[StructureBreak]:
    events=[]
    highs=[p for p in pivots if p.kind=="pivot_high"]
    lows=[p for p in pivots if p.kind=="pivot_low"]
    for i,c in enumerate(candles):
        prior_highs=[p for p in highs if p.index < i]
        prior_lows=[p for p in lows if p.index < i]
        if prior_highs:
            h=prior_highs[-1]
            if c.close > h.level:
                events.append(StructureBreak("BOS","bullish",i,h.level))
        if prior_lows:
            l=prior_lows[-1]
            if c.close < l.level:
                events.append(StructureBreak("BOS","bearish",i,l.level))
    return _dedupe_breaks(events)


def _dedupe_breaks(events):
    seen=set(); out=[]
    for e in events:
        key=(e.kind,e.direction,e.index,e.broken_level)
        if key not in seen: seen.add(key); out.append(e)
    return out


def displacement(candles: list[Candle], lookback: int = 20, multiple: float = 1.5) -> list[Displacement]:
    if lookback < 1 or multiple <= 0: raise ValueError("invalid displacement parameters")
    out=[]
    for i in range(lookback,len(candles)):
        c=candles[i]; rng=c.high-c.low
        if rng <= 0: continue
        prior=[x.high-x.low for x in candles[i-lookback:i] if x.high>x.low]
        avg=sum(prior)/len(prior) if prior else 0
        body=abs(c.close-c.open)
        if avg and rng >= avg*multiple:
            out.append(Displacement("bullish" if c.close>c.open else "bearish",i,body/rng,rng/avg))
    return out
