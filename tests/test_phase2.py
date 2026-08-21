from datetime import datetime, timedelta
from shark.data.models import Candle
from shark.features.candles import extract
from shark.features.smc import find_fvgs, find_sweeps
from shark.research.gates import ValidationMetrics, passes

def c(i,o,h,l,cl): return Candle(datetime(2026,1,1)+timedelta(minutes=i),o,h,l,cl)

def test_candle_features():
    x=extract(c(0,100,110,99,109))
    assert x.bullish and x.body_ratio > 0

def test_fvg_and_sweep():
    candles=[c(0,100,102,99,101),c(1,101,103,100,102),c(2,104,106,104,105)]
    assert find_fvgs(candles)
    sweep=[c(i,100,101,99,100) for i in range(6)] + [c(6,100,103,99,100.2)]
    assert find_sweeps(sweep)

def test_validation_gate():
    m=ValidationMetrics(150,.2,1.4,.18,.1,.08,.25,.02)
    assert passes(m)
