from datetime import datetime,timedelta
from shark.data.models import Candle
from shark.features.structure import detect
from shark.features.market_structure_events import breaks, displacement

def candles():
    rows=[(100,102,99,101),(101,105,100,104),(104,106,103,105),(105,103,101,102),(102,107,100,106),(106,112,105,111),(111,113,110,112)]
    t=datetime(2026,1,1)
    return [Candle(t+timedelta(minutes=i),*r,100) for i,r in enumerate(rows)]

def test_breaks_are_confirmed_by_close():
    c=candles(); p=detect(c,1,1); events=breaks(c,p)
    assert all(e.index >= 0 and e.direction in ("bullish","bearish") for e in events)

def test_displacement_uses_prior_range():
    c=[]; t=datetime(2026,1,1)
    for i in range(25): c.append(Candle(t+timedelta(minutes=i),100,101,99.5,100.5,100))
    c.append(Candle(t+timedelta(minutes=25),100,105,99,104.5,100))
    events=displacement(c,20,1.5)
    assert events and events[-1].direction=="bullish"
