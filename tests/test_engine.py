from datetime import datetime, timedelta
from shark.models import Candle
from research.indicators import detect_fvg, liquidity_sweep, candle_features
from research.stats import summarize, permutation_p_value


def candles(rows):
    t = datetime(2026, 1, 1)
    return [Candle(t + timedelta(minutes=i), *r) for i, r in enumerate(rows)]


def test_bullish_fvg():
    cs = candles([(100, 101, 99, 100.5), (100.5, 103, 100, 102.5), (102.5, 105, 102, 104.5)])
    assert detect_fvg(cs)[0].direction == 1


def test_liquidity_sweep():
    cs = candles([(100, 101, 99, 100)] * 10 + [(100, 102, 99.5, 100.5)])
    assert liquidity_sweep(cs, 10) == [10]


def test_candle_features():
    c = candles([(100, 105, 99, 104)])[0]
    f = candle_features(c)
    assert f["bullish"] is True
    assert 0 < f["body_ratio"] < 1


def test_stats():
    s = summarize([1, 2, -1, 3])
    assert s["trades"] == 4
    assert s["net_pnl"] == 5
    assert 0 < permutation_p_value([1, 2, 3, 4], 200) <= 1
