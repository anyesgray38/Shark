from dataclasses import dataclass

from ..data.providers import MarketDataProvider
from ..features.smc import find_fvgs, find_sweeps
from ..features.structure import classify, detect_structure, find_order_blocks
from .backtest import BacktestResult, run
from .hypotheses import generate


@dataclass(frozen=True)
class ResearchResult:
    symbol: str
    timeframe: str
    features: tuple[str, ...]
    backtest: BacktestResult
    structure_events: int = 0
    fvg_events: int = 0
    liquidity_sweeps: int = 0
    order_blocks: int = 0


def run_hypothesis_search(
    provider: MarketDataProvider,
    symbol: str,
    timeframe: str,
    max_features: int = 3,
) -> list[ResearchResult]:
    candles = provider.candles(symbol, timeframe)
    if len(candles) < 3:
        return []

    raw_structure = detect_structure(candles)
    structure = classify(raw_structure)
    fvgs = find_fvgs(candles)
    sweeps = find_sweeps(candles)
    order_blocks = find_order_blocks(candles, structure)

    results: list[ResearchResult] = []
    for features in generate(max_features=max_features):
        feature_set = set(features)

        def signal(i: int, history, feature_set=feature_set):
            if i < 2:
                return None
            if "fvg" in feature_set:
                if history[-2].high < history[-1].low:
                    return "long"
                if history[-2].low > history[-1].high:
                    return "short"
            if "liquidity_sweep" in feature_set:
                recent = sweeps[-1] if sweeps else None
                if recent is not None and recent.index == i:
                    return "long" if recent.direction == "buy" else "short"
            if "market_structure" in feature_set or "choch_mss" in feature_set:
                recent = structure[-1] if structure else None
                if recent is not None and recent.index == i:
                    return recent.direction
            if "order_block" in feature_set:
                recent = order_blocks[-1] if order_blocks else None
                if recent is not None and recent.index == i - 1:
                    return recent.direction
            return None

        result = run(
            candles,
            signal,
            stop_distance=max(candles[-1].close * 0.001, 0.0001),
        )
        results.append(
            ResearchResult(
                symbol,
                timeframe,
                tuple(features),
                result,
                len(structure),
                len(fvgs),
                len(sweeps),
                len(order_blocks),
            )
        )
    return results
