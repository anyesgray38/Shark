"""Setup detectors.

Each detector inspects the tail of an indicator-enriched OHLCV frame
(see indicators.enrich) and returns a Signal when the setup is present.
Scores are 0-100 within each detector; the scanner combines them.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Signal:
    name: str
    direction: str  # "bullish" | "bearish" | "neutral"
    score: float  # 0-100
    reason: str


def _last(df: pd.DataFrame, col: str, offset: int = 0) -> float:
    return float(df[col].iloc[-1 - offset])


def detect_breakout(df: pd.DataFrame, lookback: int = 20) -> Optional[Signal]:
    """Close breaks above the prior N-day high on real volume."""
    if len(df) < lookback + 2 or np.isnan(_last(df, "vol_z")):
        return None
    close = _last(df, "close")
    prior_high = float(df["high"].iloc[-1 - lookback : -1].max())
    if close <= prior_high:
        return None
    margin = (close - prior_high) / prior_high
    vol_z = _last(df, "vol_z")
    score = min(100.0, 55.0 + margin * 800.0 + max(vol_z, 0.0) * 10.0)
    return Signal(
        "breakout",
        "bullish",
        round(score, 1),
        f"close {close:.2f} above {lookback}-day high {prior_high:.2f} "
        f"(+{margin * 100:.1f}%), volume z={vol_z:.1f}",
    )


def detect_oversold_bounce(df: pd.DataFrame) -> Optional[Signal]:
    """RSI dipped below 30 recently and has turned up with price."""
    if len(df) < 20 or df["rsi14"].iloc[-6:].isna().any():
        return None
    recent_min = float(df["rsi14"].iloc[-6:-1].min())
    rsi_now = _last(df, "rsi14")
    price_up = _last(df, "close") > _last(df, "close", 1)
    if recent_min >= 30.0 or rsi_now <= recent_min or not price_up:
        return None
    score = min(100.0, 45.0 + (30.0 - recent_min) * 2.5 + (rsi_now - recent_min))
    return Signal(
        "oversold_bounce",
        "bullish",
        round(score, 1),
        f"RSI bottomed at {recent_min:.0f} and recovered to {rsi_now:.0f} "
        "with price turning up",
    )


def detect_macd_cross(df: pd.DataFrame) -> Optional[Signal]:
    """MACD line crossed above its signal line within the last 2 bars."""
    if len(df) < 3 or df["macd"].iloc[-3:].isna().any():
        return None
    for offset in (0, 1):
        now = _last(df, "macd", offset) - _last(df, "macd_signal", offset)
        before = _last(df, "macd", offset + 1) - _last(df, "macd_signal", offset + 1)
        if before <= 0.0 < now:
            below_zero = _last(df, "macd", offset) < 0.0
            score = 55.0 + (15.0 if below_zero else 0.0) - offset * 5.0
            where = "below zero (early)" if below_zero else "above zero"
            return Signal(
                "macd_cross",
                "bullish",
                round(score, 1),
                f"MACD crossed above signal {offset + 1} bar(s) ago, {where}",
            )
    return None


def detect_golden_cross(df: pd.DataFrame, within: int = 5) -> Optional[Signal]:
    """SMA50 crossed above SMA200 within the last few bars."""
    if len(df) < 200 + within or df["sma200"].iloc[-(within + 1) :].isna().any():
        return None
    diff = df["sma50"] - df["sma200"]
    for offset in range(within):
        if diff.iloc[-2 - offset] <= 0.0 < diff.iloc[-1 - offset]:
            return Signal(
                "golden_cross",
                "bullish",
                round(70.0 - offset * 3.0, 1),
                f"SMA50 crossed above SMA200 {offset + 1} bar(s) ago",
            )
    return None


def detect_volume_spike(df: pd.DataFrame, threshold: float = 2.5) -> Optional[Signal]:
    """Unusual volume with a directional close."""
    if len(df) < 21 or np.isnan(_last(df, "vol_z")):
        return None
    vol_z = _last(df, "vol_z")
    if vol_z < threshold:
        return None
    up = _last(df, "close") >= _last(df, "open")
    direction = "bullish" if up else "bearish"
    score = min(100.0, 40.0 + (vol_z - threshold) * 15.0)
    return Signal(
        "volume_spike",
        direction,
        round(score, 1),
        f"volume z-score {vol_z:.1f} on a{'n up' if up else ' down'} day",
    )


def detect_squeeze(df: pd.DataFrame, lookback: int = 120) -> Optional[Signal]:
    """Bollinger bandwidth at a long-term low — volatility coiling."""
    if len(df) < lookback or df["bb_bandwidth"].iloc[-lookback:].isna().any():
        return None
    bw = df["bb_bandwidth"].iloc[-lookback:]
    now = float(bw.iloc[-1])
    pct_rank = float((bw <= now).mean())
    if pct_rank > 0.10:
        return None
    return Signal(
        "squeeze",
        "neutral",
        round(35.0 + (0.10 - pct_rank) * 150.0, 1),
        f"Bollinger bandwidth in the bottom {pct_rank * 100:.0f}% "
        f"of the last {lookback} bars",
    )


DETECTORS: List[Callable[[pd.DataFrame], Optional[Signal]]] = [
    detect_breakout,
    detect_oversold_bounce,
    detect_macd_cross,
    detect_golden_cross,
    detect_volume_spike,
    detect_squeeze,
]


def detect_all(df: pd.DataFrame) -> List[Signal]:
    signals = []
    for detector in DETECTORS:
        sig = detector(df)
        if sig is not None:
            signals.append(sig)
    return signals
