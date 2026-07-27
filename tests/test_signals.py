import numpy as np
import pandas as pd

from shark.indicators import enrich
from shark.signals import (
    detect_breakout,
    detect_macd_cross,
    detect_oversold_bounce,
    detect_volume_spike,
)


def make_frame(close, volume=None, days=None):
    close = np.asarray(close, dtype=float)
    n = len(close)
    volume = np.asarray(volume, dtype=float) if volume is not None else np.full(n, 1e6)
    df = pd.DataFrame(
        {
            "open": close * 0.995,
            "high": close * 1.01,
            "low": close * 0.99,
            "close": close,
            "volume": volume,
        },
        index=pd.bdate_range(end="2026-07-24", periods=n),
    )
    return enrich(df)


def test_breakout_detected_on_new_high_with_volume():
    close = np.concatenate([np.full(60, 100.0) + np.sin(np.arange(60)), [108.0]])
    volume = np.concatenate([np.full(60, 1e6), [4e6]])
    df = make_frame(close, volume)
    sig = detect_breakout(df)
    assert sig is not None
    assert sig.direction == "bullish"
    assert sig.score > 55


def test_no_breakout_in_flat_market():
    close = np.full(80, 100.0) + np.sin(np.arange(80))
    assert detect_breakout(make_frame(close)) is None


def test_oversold_bounce_detected():
    # Steady decline drives RSI under 30, then two up days.
    close = np.concatenate([np.linspace(100, 60, 40), [61.0, 63.0]])
    df = make_frame(close)
    sig = detect_oversold_bounce(df)
    assert sig is not None
    assert sig.direction == "bullish"


def test_no_oversold_bounce_in_uptrend():
    close = np.linspace(100, 160, 60)
    assert detect_oversold_bounce(make_frame(close)) is None


def test_macd_cross_detected_after_reversal():
    # Long decline, then a 3-bar recovery — the cross lands 2 bars ago,
    # inside the detector's window.
    close = np.concatenate([np.linspace(100, 70, 50), [70.0, 71.1, 72.2]])
    df = make_frame(close)
    sig = detect_macd_cross(df)
    assert sig is not None
    assert sig.direction == "bullish"


def test_volume_spike_detected():
    close = np.full(40, 100.0) + np.linspace(0, 1, 40)
    volume = np.concatenate([np.random.default_rng(0).uniform(9e5, 1.1e6, 39), [5e6]])
    sig = detect_volume_spike(make_frame(close, volume))
    assert sig is not None
    assert sig.score > 40
