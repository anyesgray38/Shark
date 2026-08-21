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


def run(
    candles: list[Candle],
    signal: Callable[[int, list[Candle]], str | None],
    stop_distance: float,
    target_r: float = 2.0,
) -> BacktestResult:
    """Run a deterministic next-bar backtest without look-ahead bias.

    A signal generated from candle ``i`` is filled at candle ``i + 1``'s
    open. Because the entry occurs at that open, the entry candle itself is
    excluded from stop/target evaluation; only subsequent candles can exit
    the position. If both stop and target are touched in the same future
    candle, the stop is treated as first (conservative OHLC assumption).
    """
    if stop_distance <= 0:
        raise ValueError("stop_distance must be positive")
    if target_r <= 0:
        raise ValueError("target_r must be positive")

    trades: list[Trade] = []
    equity = [0.0]
    i = 0

    while i < len(candles) - 1:
        side = signal(i, candles[: i + 1])
        if side not in ("long", "short"):
            i += 1
            continue

        entry_index = i + 1
        entry = candles[entry_index].open
        stop = entry - stop_distance if side == "long" else entry + stop_distance
        target = entry + stop_distance * target_r if side == "long" else entry - stop_distance * target_r

        exit_i: int | None = None
        exit_px: float | None = None

        # The entry candle's OHLC occurred before/at the entry transaction.
        # Never use its high/low to trigger a post-entry exit.
        for j in range(entry_index + 1, len(candles)):
            c = candles[j]
            if side == "long":
                if c.low <= stop:
                    exit_i, exit_px = j, stop
                    break
                if c.high >= target:
                    exit_i, exit_px = j, target
                    break
            else:
                if c.high >= stop:
                    exit_i, exit_px = j, stop
                    break
                if c.low <= target:
                    exit_i, exit_px = j, target
                    break

        if exit_i is None:
            exit_i = len(candles) - 1
            exit_px = candles[-1].close

        assert exit_px is not None
        r = ((exit_px - entry) / stop_distance) if side == "long" else ((entry - exit_px) / stop_distance)
        trades.append(Trade(entry_index, exit_i, side, entry, exit_px, r))
        equity.append(equity[-1] + r)

        # Do not generate another signal from candles consumed by this trade.
        i = max(i + 1, exit_i)

    return BacktestResult(tuple(trades), tuple(equity))
