"""Technical indicators as pure pandas functions.

All functions take price/volume Series (oldest row first) and return Series
aligned to the input index. No external TA library required.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window, min_periods=window).mean()


def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False, min_periods=span).mean()


def rsi(close: pd.Series, window: int = 14) -> pd.Series:
    """Wilder's RSI, 0-100."""
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1.0 / window, adjust=False, min_periods=window).mean()
    avg_loss = loss.ewm(alpha=1.0 / window, adjust=False, min_periods=window).mean()
    rs = avg_gain / avg_loss.replace(0.0, np.nan)
    out = 100.0 - 100.0 / (1.0 + rs)
    # All-gain windows have avg_loss == 0 -> RSI 100
    out = out.where(avg_loss != 0.0, 100.0)
    out[avg_gain.isna() | avg_loss.isna()] = np.nan
    return out


def macd(
    close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9
) -> pd.DataFrame:
    macd_line = ema(close, fast) - ema(close, slow)
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return pd.DataFrame(
        {
            "macd": macd_line,
            "macd_signal": signal_line,
            "macd_hist": macd_line - signal_line,
        }
    )


def bollinger(close: pd.Series, window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    mid = sma(close, window)
    std = close.rolling(window, min_periods=window).std(ddof=0)
    upper = mid + num_std * std
    lower = mid - num_std * std
    bandwidth = (upper - lower) / mid
    return pd.DataFrame(
        {"bb_upper": upper, "bb_mid": mid, "bb_lower": lower, "bb_bandwidth": bandwidth}
    )


def atr(df: pd.DataFrame, window: int = 14) -> pd.Series:
    """Average True Range. Expects columns: high, low, close."""
    prev_close = df["close"].shift(1)
    tr = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr.ewm(alpha=1.0 / window, adjust=False, min_periods=window).mean()


def volume_zscore(volume: pd.Series, window: int = 20) -> pd.Series:
    mean = volume.rolling(window, min_periods=window).mean()
    std = volume.rolling(window, min_periods=window).std(ddof=0)
    return (volume - mean) / std.replace(0.0, np.nan)


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of an OHLCV frame with all indicator columns added.

    Expects columns: open, high, low, close, volume. Oldest row first.
    """
    out = df.copy()
    close = out["close"]
    out["sma20"] = sma(close, 20)
    out["sma50"] = sma(close, 50)
    out["sma200"] = sma(close, 200)
    out["rsi14"] = rsi(close, 14)
    out = out.join(macd(close))
    out = out.join(bollinger(close))
    out["atr14"] = atr(out, 14)
    out["vol_z"] = volume_zscore(out["volume"], 20)
    return out
