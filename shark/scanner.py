"""Scan a watchlist: fetch history, compute indicators, detect and rank setups."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import List, Optional

import pandas as pd

from .indicators import enrich
from .providers.base import DataProvider
from .signals import Signal, detect_all

# How much each detector contributes to the composite score.
_WEIGHTS = {
    "breakout": 1.0,
    "golden_cross": 0.9,
    "macd_cross": 0.8,
    "oversold_bounce": 0.8,
    "volume_spike": 0.6,
    "squeeze": 0.4,
}


@dataclass
class ScanResult:
    symbol: str
    price: float
    change_1d: float  # percent
    change_20d: float  # percent
    rsi: Optional[float]
    trend: str  # "up" | "down" | "flat"
    score: float
    signals: List[Signal] = field(default_factory=list)
    sparkline: List[float] = field(default_factory=list)
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "price": self.price,
            "change_1d": self.change_1d,
            "change_20d": self.change_20d,
            "rsi": self.rsi,
            "trend": self.trend,
            "score": self.score,
            "signals": [vars(s) for s in self.signals],
            "sparkline": self.sparkline,
            "error": self.error,
        }


def composite_score(signals: List[Signal]) -> float:
    """Combine detector scores: strongest signal dominates, extras add a bonus."""
    if not signals:
        return 0.0
    weighted = sorted(
        (s.score * _WEIGHTS.get(s.name, 0.5) for s in signals), reverse=True
    )
    score = weighted[0] + sum(w * 0.25 for w in weighted[1:])
    return round(min(100.0, score), 1)


def _pct(now: float, then: float) -> float:
    if then == 0:
        return 0.0
    return round((now / then - 1.0) * 100.0, 2)


def scan_symbol(provider: DataProvider, symbol: str, days: int = 365) -> ScanResult:
    try:
        raw = provider.fetch(symbol, days=days)
        df = enrich(raw)
    except Exception as exc:  # network / bad symbol — report, don't crash the scan
        return ScanResult(
            symbol=symbol,
            price=0.0,
            change_1d=0.0,
            change_20d=0.0,
            rsi=None,
            trend="flat",
            score=0.0,
            error=str(exc),
        )

    close = df["close"]
    price = float(close.iloc[-1])
    sma50 = df["sma50"].iloc[-1]
    if pd.isna(sma50):
        trend = "flat"
    elif price > sma50 * 1.01:
        trend = "up"
    elif price < sma50 * 0.99:
        trend = "down"
    else:
        trend = "flat"

    rsi_val = df["rsi14"].iloc[-1]
    signals = detect_all(df)
    tail = close.iloc[-30:]
    return ScanResult(
        symbol=symbol,
        price=price,
        change_1d=_pct(price, float(close.iloc[-2])) if len(close) > 1 else 0.0,
        change_20d=_pct(price, float(close.iloc[-21])) if len(close) > 20 else 0.0,
        rsi=None if pd.isna(rsi_val) else round(float(rsi_val), 1),
        trend=trend,
        score=composite_score(signals),
        signals=signals,
        sparkline=[round(float(v), 4) for v in tail],
    )


def scan(
    provider: DataProvider,
    symbols: Optional[List[str]] = None,
    days: int = 365,
    min_score: float = 0.0,
    workers: int = 8,
) -> List[ScanResult]:
    """Scan symbols concurrently, ranked by composite score descending."""
    symbols = symbols or provider.default_symbols
    results: List[ScanResult] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(scan_symbol, provider, sym, days): sym for sym in symbols
        }
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda r: (r.error is None, r.score), reverse=True)
    return [r for r in results if r.error is not None or r.score >= min_score]
