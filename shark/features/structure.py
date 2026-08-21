from dataclasses import dataclass

from ..data.models import Candle


@dataclass(frozen=True)
class StructureBreak:
    kind: str
    direction: str
    index: int
    level: float


@dataclass(frozen=True)
class SwingPoint:
    kind: str
    index: int
    price: float


@dataclass(frozen=True)
class OrderBlock:
    direction: str
    index: int
    low: float
    high: float


def find_swings(candles: list[Candle], left: int = 2, right: int = 2) -> list[SwingPoint]:
    if left < 1 or right < 1:
        raise ValueError("left and right must be positive")
    out: list[SwingPoint] = []
    for i in range(left, len(candles) - right):
        current = candles[i]
        window = candles[i - left : i + right + 1]
        highs = [c.high for c in window]
        lows = [c.low for c in window]
        if current.high == max(highs) and highs.count(current.high) == 1:
            out.append(SwingPoint("high", i, current.high))
        if current.low == min(lows) and lows.count(current.low) == 1:
            out.append(SwingPoint("low", i, current.low))
    return out


def detect_structure(candles: list[Candle], left: int = 2, right: int = 2) -> list[StructureBreak]:
    swings = find_swings(candles, left, right)
    highs = [s for s in swings if s.kind == "high"]
    lows = [s for s in swings if s.kind == "low"]
    events: list[StructureBreak] = []
    broken_highs: set[int] = set()
    broken_lows: set[int] = set()
    for i, candle in enumerate(candles):
        prior_highs = [s for s in highs if s.index < i and s.index not in broken_highs]
        prior_lows = [s for s in lows if s.index < i and s.index not in broken_lows]
        if prior_highs:
            level = prior_highs[-1]
            if candle.close > level.price:
                events.append(StructureBreak("BOS", "bullish", i, level.price))
                broken_highs.add(level.index)
        if prior_lows:
            level = prior_lows[-1]
            if candle.close < level.price:
                events.append(StructureBreak("BOS", "bearish", i, level.price))
                broken_lows.add(level.index)
    return sorted(events, key=lambda event: event.index)


def classify(events: list[StructureBreak]) -> list[StructureBreak]:
    if not events:
        return []
    out: list[StructureBreak] = []
    trend: str | None = None
    reversed_once: set[str] = set()
    for event in events:
        if trend is None:
            trend = event.direction
            out.append(event)
            continue
        if event.direction == trend:
            continue
        if event.direction not in reversed_once:
            kind = "MSS" if not reversed_once else "CHoCH"
            reversed_once.add(event.direction)
            trend = event.direction
            out.append(StructureBreak(kind, event.direction, event.index, event.level))
        else:
            trend = event.direction
    return out


def find_order_blocks(candles: list[Candle], structure: list[StructureBreak] | None = None) -> list[OrderBlock]:
    events = structure if structure is not None else detect_structure(candles)
    out: list[OrderBlock] = []
    for event in events:
        if event.index < 1:
            continue
        source = candles[event.index - 1]
        if event.direction == "bullish" and source.close < source.open:
            out.append(OrderBlock("bullish", event.index - 1, source.low, source.high))
        elif event.direction == "bearish" and source.close > source.open:
            out.append(OrderBlock("bearish", event.index - 1, source.low, source.high))
    return out
