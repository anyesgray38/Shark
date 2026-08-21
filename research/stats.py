import math
import random
from statistics import mean, stdev


def summarize(pnls: list[float]) -> dict[str, float]:
    if not pnls:
        return {"trades": 0, "win_rate": 0.0, "net_pnl": 0.0, "profit_factor": 0.0, "sharpe_like": 0.0}
    wins = [x for x in pnls if x > 0]
    losses = [-x for x in pnls if x < 0]
    pf = sum(wins) / sum(losses) if losses else math.inf
    s = stdev(pnls) if len(pnls) > 1 else 0.0
    return {
        "trades": len(pnls),
        "win_rate": len(wins) / len(pnls),
        "net_pnl": sum(pnls),
        "profit_factor": pf,
        "sharpe_like": mean(pnls) / s * math.sqrt(len(pnls)) if s else 0.0,
    }


def permutation_p_value(pnls: list[float], trials: int = 2000, seed: int = 7) -> float:
    """Two-sided sign permutation test against zero mean."""
    if not pnls:
        return 1.0
    rng = random.Random(seed)
    observed = abs(sum(pnls) / len(pnls))
    exceed = 0
    for _ in range(trials):
        sample = [x if rng.random() < 0.5 else -x for x in pnls]
        if abs(sum(sample) / len(sample)) >= observed:
            exceed += 1
    return (exceed + 1) / (trials + 1)


def monte_carlo_drawdown(pnls: list[float], trials: int = 2000, seed: int = 7) -> dict[str, float]:
    if not pnls:
        return {"median_max_drawdown": 0.0, "p95_max_drawdown": 0.0}
    rng = random.Random(seed)
    dds = []
    for _ in range(trials):
        sample = pnls[:]
        rng.shuffle(sample)
        equity = peak = dd = 0.0
        for x in sample:
            equity += x
            peak = max(peak, equity)
            dd = max(dd, peak - equity)
        dds.append(dd)
    dds.sort()
    return {"median_max_drawdown": dds[len(dds)//2], "p95_max_drawdown": dds[int(len(dds)*0.95)]}
