from dataclasses import dataclass

from ..data.models import Candle


@dataclass(frozen=True)
class FVG:
    direction: str
    low: float
    high: float
    index: int


@dataclass(frozen=True)
class LiquiditySweep:
    direction: str
    level: float
    index: int


def find_fvgs(candles: list[Candle]) -> list[FVG]:
    out = []
    for i in range(2, len(candles)):
        a, _, c = candles[i - 2 : i + 1]
        if a.high < c.low:
            out.append(FVG("bullish", a.high, c.low, i))
        if a.low > c.high:
            out.append(FVG("bearish", c.high, a.low, i))
    return out


def find_sweeps(candles: list[Candle], lookback: int = 5) -> list[LiquiditySweep]:
    out = []
    for i in range(lookback, len(candles)):
        c = candles[i]
        highs = [x.high for x in candles[i - lookback : i]]
        lows = [x.low for x in candles[i - lookback : i]]
        if c.high > max(highs) and c.close < max(highs):
            out.append(LiquiditySweep("sell", max(highs), i))
        if c.low < min(lows) and c.close > min(lows):
            out.append(LiquiditySweep("buy", min(lows), i))
    return out
