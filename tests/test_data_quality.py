from datetime import UTC, datetime, timedelta

from shark.data.models import Candle
from shark.data.quality import validate_candles


def candles(count=4, step=1):
    start = datetime(2026, 1, 1, tzinfo=UTC)
    return [
        Candle(start + timedelta(minutes=i * step), 100 + i, 101 + i, 99 + i, 100.5 + i, 1)
        for i in range(count)
    ]


def test_quality_accepts_clean_series():
    result = validate_candles(candles(), "1m")
    assert result.valid
    assert result.gaps == 0


def test_quality_rejects_bad_ohlc_and_gaps():
    rows = candles()
    rows[2] = Candle(rows[2].timestamp + timedelta(minutes=2), 100, 99, 98, 98.5, 1)
    result = validate_candles(rows, "1m")
    assert not result.valid
    assert result.invalid_ohlc == 1
    assert result.gaps == 1


def test_quality_detects_duplicates_and_naive_timestamps():
    rows = candles(2)
    rows.append(Candle(rows[-1].timestamp, 102, 103, 101, 102, 1))
    rows.append(Candle(datetime(2026, 1, 1, 0, 3), 103, 104, 102, 103, 1))
    result = validate_candles(rows, "1m")
    assert not result.valid
    assert result.duplicates == 1
    assert any("naive timestamp" in error for error in result.errors)
