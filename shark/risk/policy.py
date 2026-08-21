from dataclasses import dataclass

@dataclass(frozen=True)
class RiskPolicy:
    max_daily_loss: float = 0.02
    max_position_risk: float = 0.01
    max_open_positions: int = 3
    live_trading_enabled: bool = False

def can_trade(policy: RiskPolicy, daily_loss: float, open_positions: int) -> bool:
    return policy.live_trading_enabled and daily_loss < policy.max_daily_loss and open_positions < policy.max_open_positions
