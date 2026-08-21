from collections.abc import Callable
from dataclasses import dataclass

from ..data.models import Candle


@dataclass(frozen=True)
class BacktestConfig:
    initial_equity: float = 100_000.0
    risk_per_trade: float = 0.01
    reward_risk: float = 2.0
    spread: float = 0.0
    slippage: float = 0.0


@dataclass(frozen=True)
class Trade:
    index: int
    side: str
    entry: float
    stop: float
    target: float
    exit: float
    pnl_r: float


@dataclass(frozen=True)
class BacktestResult:
    trades: tuple[Trade, ...]
    equity_curve: tuple[float, ...]


_DEFAULT_CONFIG = BacktestConfig()


def run(
    candles: list[Candle],
    signal: Callable[[list[Candle], int], str | None],
    config: BacktestConfig | None = None,
) -> BacktestResult:
    config = _DEFAULT_CONFIG if config is None else config
    equity = config.initial_equity
    curve = [equity]
    trades = []
    for i in range(1, len(candles)):
        side = signal(candles, i - 1)  # signal uses only candles closed before execution
        if side not in {"long", "short"}:
            curve.append(equity)
            continue
        c = candles[i]
        entry = c.open + (
            config.spread + config.slippage
            if side == "long"
            else -(config.spread + config.slippage)
        )
        risk = max(abs(c.close - c.open), 1e-9)
        stop = entry - risk if side == "long" else entry + risk
        target = (
            entry + risk * config.reward_risk
            if side == "long"
            else entry - risk * config.reward_risk
        )
        exit_price = c.close
        if side == "long" and c.low <= stop:
            exit_price = stop
        elif side == "long" and c.high >= target:
            exit_price = target
        elif side == "short" and c.high >= stop:
            exit_price = stop
        elif side == "short" and c.low <= target:
            exit_price = target
        pnl_r = (
            (exit_price - entry) / risk
            if side == "long"
            else (entry - exit_price) / risk
        )
        equity *= 1.0 + config.risk_per_trade * pnl_r
        trades.append(Trade(i, side, entry, stop, target, exit_price, pnl_r))
        curve.append(equity)
    return BacktestResult(tuple(trades), tuple(curve))
