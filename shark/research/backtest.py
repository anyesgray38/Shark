from dataclasses import dataclass
from typing import Callable
from ..data.models import Candle

@dataclass(frozen=True)
class Trade:
    entry_index: int
    exit_index: int
    side: str
    entry: float
    exit: float
    r_multiple: float

@dataclass(frozen=True)
class BacktestResult:
    trades: tuple[Trade, ...]
    equity: tuple[float, ...]


def run(candles: list[Candle], signal: Callable[[int, list[Candle]], str | None], stop_distance: float, target_r: float = 2.0) -> BacktestResult:
    if stop_distance <= 0:
        raise ValueError("stop_distance must be positive")
    trades=[]; equity=[0.0]
    for i in range(len(candles)-1):
        side=signal(i, candles[:i+1])
        if side not in ("long", "short"):
            continue
        entry=candles[i+1].open
        stop=entry-stop_distance if side=="long" else entry+stop_distance
        target=entry+stop_distance*target_r if side=="long" else entry-stop_distance*target_r
        exit_i=None; exit_px=None
        for j in range(i+1, len(candles)):
            c=candles[j]
            if side=="long":
                if c.low <= stop: exit_i,exit_px=j,stop; break
                if c.high >= target: exit_i,exit_px=j,target; break
            else:
                if c.high >= stop: exit_i,exit_px=j,stop; break
                if c.low <= target: exit_i,exit_px=j,target; break
        if exit_i is None:
            exit_i=len(candles)-1; exit_px=candles[-1].close
        r=(exit_px-entry)/stop_distance if side=="long" else (entry-exit_px)/stop_distance
        trades.append(Trade(i+1,exit_i,side,entry,exit_px,r))
        equity.append(equity[-1]+r)
    return BacktestResult(tuple(trades),tuple(equity))
