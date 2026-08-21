from datetime import UTC, datetime, timedelta

from shark.backtest.engine import BacktestConfig, run
from shark.backtest.stats import summarize
from shark.data.models import Candle
from shark.research.splits import holdout, walk_forward
from shark.research.stats_tests import monte_carlo_drawdown, permutation_test


def candles():
    start = datetime(2026, 1, 1, tzinfo=UTC)
    return [
        Candle(start + timedelta(minutes=i), 100 + i, 101 + i, 99 + i, 100.5 + i, 1)
        for i in range(20)
    ]


def signal(cs, i):
    return "long" if i % 2 == 0 else None


def test_backtest_and_stats():
    result = run(candles(), signal, BacktestConfig(spread=0.01, slippage=0.01))
    stats = summarize(result)
    assert stats["trades"] > 0
    assert 0 <= stats["win_rate"] <= 1


def test_splits_are_chronological():
    split = holdout(list(range(10)), 0.7)
    assert split.train == tuple(range(7)) and split.test == tuple(range(7, 10))
    walk = list(walk_forward(list(range(12)), 4, 2))
    assert walk[0].train == (0, 1, 2, 3) and walk[0].test == (4, 5)


def test_statistical_tests_are_bounded():
    returns = [0.1, -0.05, 0.08, -0.02, 0.04]
    monte_carlo = monte_carlo_drawdown(returns, 100)
    permutation = permutation_test(returns, 100)
    assert 0 <= monte_carlo["p95_drawdown"] <= 1
    assert 0 <= permutation["p_value"] <= 1
