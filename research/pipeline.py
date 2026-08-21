from dataclasses import dataclass
from shark.models import Candle
from .indicators import candle_features, detect_fvg, liquidity_sweep

@dataclass
class FeatureSnapshot:
    candles: int
    fvgs: int
    sweeps: int
    latest_candle: dict


def discover(candles: list[Candle]) -> FeatureSnapshot:
    """Run deterministic feature extraction on closed candles."""
    fvgs = detect_fvg(candles)
    sweeps = liquidity_sweep(candles)
    latest = candle_features(candles[-1]) if candles else {}
    return FeatureSnapshot(len(candles), len(fvgs), len(sweeps), latest)
