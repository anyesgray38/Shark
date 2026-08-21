from dataclasses import dataclass
from shark.models import Candle, Trade

@dataclass
class BacktestConfig:
    risk_per_trade: float = 1.0
    fee_per_trade: float = 0.0
    slippage: float = 0.0

@dataclass
class BacktestResult:
    trades: list[Trade]
    equity_curve: list[float]

    @property
    def net_pnl(self) -> float:
        return self.equity_curve[-1] if self.equity_curve else 0.0


def run_signal_backtest(candles: list[Candle], signals: list[int], config: BacktestConfig | None = None) -> BacktestResult:
    """Simple next-bar execution model. signals[i] executes at i+1 open."""
    config = config or BacktestConfig()
    trades, equity = [], [0.0]
    for i, side in enumerate(signals[:-1]):
        if side not in (-1, 1):
            continue
        entry_bar = candles[i + 1]
        exit_bar = candles[i + 1]
        entry = entry_bar.open + config.slippage * side
        exit_price = exit_bar.close - config.slippage * side
        pnl = (exit_price - entry) * side - config.fee_per_trade
        trades.append(Trade(entry_bar.timestamp, exit_bar.timestamp, entry, exit_price, side))
        equity.append(equity[-1] + pnl)
    return BacktestResult(trades, equity)
