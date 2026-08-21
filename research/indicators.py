from dataclasses import dataclass
from shark.models import Candle

@dataclass(frozen=True)
class FVG:
    index: int
    direction: int
    low: float
    high: float

def detect_fvg(candles: list[Candle]) -> list[FVG]:
    """Three-candle imbalance detector using only closed candles."""
    out = []
    for i in range(2, len(candles)):
        a, _, c = candles[i-2], candles[i-1], candles[i]
        if c.low > a.high:
            out.append(FVG(i, 1, a.high, c.low))
        elif c.high < a.low:
            out.append(FVG(i, -1, c.high, a.low))
    return out

def liquidity_sweep(candles: list[Candle], lookback: int = 10) -> list[int]:
    """Detect prior-range sweeps that close back inside the range."""
    hits = []
    for i in range(lookback, len(candles)):
        window = candles[i-lookback:i]
        prior_high = max(x.high for x in window)
        prior_low = min(x.low for x in window)
        c = candles[i]
        if (c.high > prior_high and c.close < prior_high) or (c.low < prior_low and c.close > prior_low):
            hits.append(i)
    return hits

def candle_features(c: Candle) -> dict[str, float | bool]:
    rng = c.range
    if rng <= 0:
        return {"body_ratio": 0.0, "bullish": c.close > c.open, "upper_wick_ratio": 0.0, "lower_wick_ratio": 0.0}
    return {
        "body_ratio": c.body / rng,
        "bullish": c.close > c.open,
        "upper_wick_ratio": (c.high - max(c.open, c.close)) / rng,
        "lower_wick_ratio": (min(c.open, c.close) - c.low) / rng,
    }
