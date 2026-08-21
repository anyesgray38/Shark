from dataclasses import dataclass

@dataclass(frozen=True)
class Regime:
    trend: str
    volatility: str
    risk: str

def classify(returns: list[float], volatility: float, vix: float | None = None) -> Regime:
    if not returns:
        return Regime("unknown", "unknown", "unknown")
    momentum = sum(returns[-20:])
    trend = "up" if momentum > 0 else "down" if momentum < 0 else "range"
    vol = "high" if volatility > 0.02 else "low"
    risk = "risk_off" if vix is not None and vix >= 25 else "risk_on" if vix is not None and vix < 18 else "neutral"
    return Regime(trend, vol, risk)
