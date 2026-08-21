from datetime import UTC, datetime, timedelta

from shark.data.models import Candle
from shark.research.runner import run_hypothesis_search


class Provider:
    def __init__(self, candles):
        self._candles = candles

    def candles(self, symbol, timeframe, start=None, end=None):
        return self._candles


def test_runner_exposes_smc_counts():
    start = datetime(2026, 1, 1, tzinfo=UTC)
    rows = [
        Candle(start + timedelta(minutes=i), 100, 101, 99, 100, 1)
        for i in range(8)
    ]
    rows[2] = Candle(start + timedelta(minutes=2), 104, 106, 104, 105, 1)
    rows[3] = Candle(start + timedelta(minutes=3), 105, 108, 105, 107, 1)
    rows[4] = Candle(start + timedelta(minutes=4), 107, 109, 107, 108, 1)
    results = run_hypothesis_search(Provider(rows), "XAUUSD", "1m", max_features=2)
    assert results
    assert all(result.symbol == "XAUUSD" for result in results)
    assert all(result.timeframe == "1m" for result in results)
    assert all(result.fvg_events >= 0 for result in results)
    assert all(result.structure_events >= 0 for result in results)
