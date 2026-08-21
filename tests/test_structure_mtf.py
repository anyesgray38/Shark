from datetime import datetime,timedelta
from shark.data.models import Candle
from shark.features.structure import detect
from shark.features.multitimeframe import aggregate

def cs():
    t=datetime(2026,1,1)
    rows=[(100,102,99,101),(101,105,100,104),(104,106,103,105),(105,103,101,102),(102,107,100,106),(106,109,105,108)]
    return [Candle(t+timedelta(minutes=i),*r,100) for i,r in enumerate(rows)]

def test_structure_detects_pivots():
    events=detect(cs(),1,1)
    assert events
    assert all(e.kind in ("pivot_high","pivot_low") for e in events)

def test_aggregate_3m():
    out=aggregate(cs(),"3m")
    assert len(out)==2
    assert out[0].open==100 and out[0].close==105
    assert out[0].high==106 and out[0].low==99
    assert out[0].volume==300
