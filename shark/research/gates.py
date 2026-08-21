from dataclasses import dataclass

@dataclass(frozen=True)
class ValidationMetrics:
    trades: int
    expectancy: float
    profit_factor: float
    max_drawdown: float
    oos_expectancy: float
    walk_forward_expectancy: float
    monte_carlo_drawdown_p95: float
    permutation_p_value: float

@dataclass(frozen=True)
class GatePolicy:
    min_trades: int = 100
    min_expectancy: float = 0.0
    min_oos_expectancy: float = 0.0
    min_walk_forward_expectancy: float = 0.0
    max_drawdown: float = 0.30
    max_mc_drawdown: float = 0.40
    max_permutation_p: float = 0.05

def passes(metrics: ValidationMetrics, policy: GatePolicy = GatePolicy()) -> bool:
    return (
        metrics.trades >= policy.min_trades and
        metrics.expectancy > policy.min_expectancy and
        metrics.oos_expectancy > policy.min_oos_expectancy and
        metrics.walk_forward_expectancy > policy.min_walk_forward_expectancy and
        metrics.max_drawdown <= policy.max_drawdown and
        metrics.monte_carlo_drawdown_p95 <= policy.max_mc_drawdown and
        metrics.permutation_p_value <= policy.max_permutation_p
    )
