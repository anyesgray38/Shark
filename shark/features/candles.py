from dataclasses import dataclass
from .types import CandleFeatures

def extract(candle) -> CandleFeatures:
    body = abs(candle.close - candle.open)
    rng = max(candle.high - candle.low, 1e-12)
    upper = candle.high - max(candle.open, candle.close)
    lower = min(candle.open, candle.close) - candle.low
    bullish = candle.close > candle.open
    return CandleFeatures(
        body_ratio=body/rng,
        upper_wick_ratio=max(upper,0)/rng,
        lower_wick_ratio=max(lower,0)/rng,
        bullish=bullish,
        doji=body/rng <= 0.1,
        long_upper_wick=max(upper,0)/rng >= 0.6,
        long_lower_wick=max(lower,0)/rng >= 0.6,
    )
