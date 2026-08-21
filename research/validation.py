from dataclasses import dataclass, field
from .stats import monte_carlo_drawdown, permutation_p_value, summarize

@dataclass
class ValidationPolicy:
    min_trades: int = 100
    min_profit_factor: float = 1.20
    min_win_rate: float = 0.35
    max_permutation_p: float = 0.05
    max_p95_drawdown: float = 0.20

@dataclass
class ValidationReport:
    metrics: dict[str, float]
    permutation_p: float
    monte_carlo: dict[str, float]
    gates: dict[str, bool] = field(default_factory=dict)

    @property
    def eligible(self) -> bool:
        return all(self.gates.values()) if self.gates else False


def validate_pnls(pnls: list[float], policy: ValidationPolicy | None = None) -> ValidationReport:
    policy = policy or ValidationPolicy()
    metrics = summarize(pnls)
    p = permutation_p_value(pnls)
    mc = monte_carlo_drawdown(pnls)
    gates = {
        "minimum_trades": metrics["trades"] >= policy.min_trades,
        "profit_factor": metrics["profit_factor"] >= policy.min_profit_factor,
        "win_rate": metrics["win_rate"] >= policy.min_win_rate,
        "permutation": p <= policy.max_permutation_p,
        "drawdown": mc["p95_max_drawdown"] <= policy.max_p95_drawdown,
    }
    return ValidationReport(metrics, p, mc, gates)
