from dataclasses import dataclass

from ..data.providers import MarketDataProvider
from .backtest import BacktestResult, run
from .hypotheses import generate


@dataclass(frozen=True)
class ResearchResult:
    symbol: str
    timeframe: str
    features: tuple[str, ...]
    backtest: BacktestResult


def run_hypothesis_search(
    provider: MarketDataProvider,
    symbol: str,
    timeframe: str,
    max_features: int = 3,
) -> list[ResearchResult]:
    candles = provider.candles(symbol, timeframe)
    if len(candles) < 3:
        return []

    results: list[ResearchResult] = []
    for features in generate(max_features=max_features):
        feature_set = set(features)

        def signal(i: int, history, feature_set=feature_set):
            if i < 2:
                return None
            if "fvg" in feature_set and history[-2].high < history[-1].low:
                return "long"
            if "fvg" in feature_set and history[-2].low > history[-1].high:
                return "short"
            return None

        result = run(candles, signal, stop_distance=max(candles[-1].close * 0.001, 0.0001))
        results.append(ResearchResult(symbol, timeframe, tuple(features), result))
    return results
