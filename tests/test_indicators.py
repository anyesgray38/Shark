import numpy as np
import pandas as pd
import pytest

from shark.indicators import bollinger, enrich, macd, rsi, sma, volume_zscore
from shark.providers.synthetic import SyntheticProvider


@pytest.fixture
def frame():
    return SyntheticProvider().fetch("TEST", days=300)


def test_sma_matches_manual(frame):
    got = sma(frame["close"], 20)
    expected = frame["close"].iloc[-20:].mean()
    assert got.iloc[-1] == pytest.approx(expected)
    assert got.iloc[:19].isna().all()


def test_rsi_bounds(frame):
    r = rsi(frame["close"]).dropna()
    assert len(r) > 0
    assert ((r >= 0) & (r <= 100)).all()


def test_rsi_all_gains_is_100():
    close = pd.Series(np.linspace(10, 50, 60))
    assert rsi(close).iloc[-1] == pytest.approx(100.0)


def test_rsi_all_losses_is_0():
    close = pd.Series(np.linspace(50, 10, 60))
    assert rsi(close).iloc[-1] == pytest.approx(0.0, abs=1e-6)


def test_macd_columns_and_identity(frame):
    m = macd(frame["close"])
    assert list(m.columns) == ["macd", "macd_signal", "macd_hist"]
    diff = (m["macd"] - m["macd_signal"] - m["macd_hist"]).dropna().abs()
    assert (diff < 1e-9).all()


def test_bollinger_ordering(frame):
    bb = bollinger(frame["close"]).dropna()
    assert (bb["bb_upper"] >= bb["bb_mid"]).all()
    assert (bb["bb_mid"] >= bb["bb_lower"]).all()


def test_volume_zscore_flags_spike():
    vol = pd.Series([100.0] * 40 + [1000.0])
    noise = np.linspace(0, 1, 41)  # avoid zero std
    z = volume_zscore(vol + noise)
    assert z.iloc[-1] > 3


def test_enrich_adds_columns(frame):
    df = enrich(frame)
    for col in ["sma20", "sma50", "sma200", "rsi14", "macd", "bb_upper", "atr14", "vol_z"]:
        assert col in df.columns
    assert len(df) == len(frame)
