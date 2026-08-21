from datetime import UTC, datetime, timedelta

from shark.data.models import Candle
from shark.features.candles import extract
from shark.features.smc import find_fvgs, find_sweeps
from shark.research.gates import ValidationMetrics, passes


def candle(index, open_, high, low, close):
    return Candle(datetime(2026, 1, 1, tzinfo=UTC) + timedelta(minutes=index), open_, high, low, close)


def test_candle_features():
    features = extract(candle(0, 100, 110, 99, 109))
    assert features.bullish and features.body_ratio > 0


def test_fvg_and_sweep():
    candles = [
        candle(0, 100, 102, 99, 101),
        candle(1, 101, 103, 100, 102),
        candle(2, 104, 106, 104, 105),
    ]
    assert find_fvgs(candles)
    sweep = [candle(i, 100, 101, 99, 100) for i in range(6)] + [
        candle(6, 100, 103, 99, 100.2)
    ]
    assert find_sweeps(sweep)


def test_validation_gate():
    metrics = ValidationMetrics(150, 0.2, 1.4, 0.18, 0.1, 0.08, 0.25, 0.02)
    assert passes(metrics)
