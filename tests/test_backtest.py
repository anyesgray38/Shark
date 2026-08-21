from datetime import datetime, timedelta
from shark.data.models import Candle
from shark.backtest.engine import run, BacktestConfig
from shark.backtest.stats import summarize
from shark.research.splits import holdout, walk_forward
from shark.research.stats_tests import monte_carlo_drawdown, permutation_test

def candles():
    return [Candle(datetime(2026,1,1)+timedelta(minutes=i),100+i,101+i,99+i,100.5+i,1) for i in range(20)]

def signal(cs,i): return "long" if i % 2 == 0 else None

def test_backtest_and_stats():
    r=run(candles(),signal,BacktestConfig(spread=.01,slippage=.01))
    s=summarize(r)
    assert s["trades"] > 0
    assert 0 <= s["win_rate"] <= 1

def test_splits_are_chronological():
    s=holdout(list(range(10)),.7)
    assert s.train == tuple(range(7)) and s.test == tuple(range(7,10))
    wf=list(walk_forward(list(range(12)),4,2))
    assert wf[0].train == (0,1,2,3) and wf[0].test == (4,5)

def test_statistical_tests_are_bounded():
    r=[.1,-.05,.08,-.02,.04]
    mc=monte_carlo_drawdown(r,100)
    p=permutation_test(r,100)
    assert 0 <= mc["p95_drawdown"] <= 1
    assert 0 <= p["p_value"] <= 1
