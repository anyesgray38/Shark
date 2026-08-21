from datetime import UTC, datetime, timedelta

from research.indicators import candle_features, detect_fvg, liquidity_sweep
from research.stats import permutation_p_value, summarize
from shark.models import Candle


def candles(rows):
    start = datetime(2026, 1, 1, tzinfo=UTC)
    return [Candle(start + timedelta(minutes=i), *row) for i, row in enumerate(rows)]


def test_bullish_fvg():
    cs = candles(
        [
            (100, 101, 99, 100.5),
            (100.5, 103, 100, 102.5),
            (102.5, 105, 102, 104.5),
        ]
    )
    assert detect_fvg(cs)[0].direction == 1


def test_liquidity_sweep():
    cs = candles([(100, 101, 99, 100)] * 10 + [(100, 102, 99.5, 100.5)])
    assert liquidity_sweep(cs, 10) == [10]


def test_candle_features():
    candle = candles([(100, 105, 99, 104)])[0]
    features = candle_features(candle)
    assert features["bullish"] is True
    assert 0 < features["body_ratio"] < 1


def test_stats():
    stats = summarize([1, 2, -1, 3])
    assert stats["trades"] == 4
    assert stats["net_pnl"] == 5
    assert 0 < permutation_p_value([1, 2, 3, 4], 200) <= 1
