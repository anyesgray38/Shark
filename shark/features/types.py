from dataclasses import dataclass

@dataclass(frozen=True)
class CandleFeatures:
    body_ratio: float
    upper_wick_ratio: float
    lower_wick_ratio: float
    bullish: bool
    doji: bool
    long_upper_wick: bool
    long_lower_wick: bool
