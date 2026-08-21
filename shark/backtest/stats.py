from math import sqrt
from .engine import BacktestResult

def summarize(result: BacktestResult) -> dict:
    r = [t.pnl_r for t in result.trades]
    wins = [x for x in r if x > 0]
    losses = [x for x in r if x < 0]
    equity = list(result.equity_curve)
    peak = equity[0] if equity else 0.0
    max_dd = 0.0
    for x in equity:
        peak = max(peak, x)
        if peak: max_dd = max(max_dd, (peak-x)/peak)
    expectancy = sum(r)/len(r) if r else 0.0
    gross_win = sum(wins)
    gross_loss = abs(sum(losses))
    pf = gross_win/gross_loss if gross_loss else (float('inf') if gross_win else 0.0)
    mean = expectancy
    variance = sum((x-mean)**2 for x in r)/max(len(r)-1,1) if r else 0.0
    sharpe = mean/sqrt(variance) if variance > 0 else 0.0
    return {"trades": len(r), "win_rate": len(wins)/len(r) if r else 0.0, "expectancy_r": expectancy, "profit_factor": pf, "max_drawdown": max_dd, "sharpe_like": sharpe}
