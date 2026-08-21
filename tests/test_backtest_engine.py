from datetime import datetime, timedelta
from shark.data.models import Candle
from shark.research.backtest import run
from shark.research.statistics import summary

def candles():
    out=[]
    prices=[100,101,102,104,106,108,107,106]
    for i,p in enumerate(prices):
        out.append(Candle(datetime(2026,1,1)+timedelta(minutes=i),p,p+1,p-1,p,100))
    return out

def test_backtest_uses_next_open():
    result=run(candles(),lambda i,_: "long" if i==0 else None,1,2)
    assert result.trades[0].entry == 101
    assert result.trades[0].r_multiple == 2

def test_statistics():
    s=summary([2,-1,2,-1])
    assert s["trades"] == 4
    assert s["win_rate"] == 0.5
    assert s["expectancy"] == 0.5
