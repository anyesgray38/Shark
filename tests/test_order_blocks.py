from datetime import datetime,timedelta
from shark.data.models import Candle
from shark.features.order_blocks import detect
from shark.features.market_structure_events import StructureBreak

def test_bullish_order_block_uses_last_bearish_candle():
    t=datetime(2026,1,1)
    c=[Candle(t,100,101,99,100.5,1),Candle(t+timedelta(minutes=1),100.5,101,98.5,99,1),Candle(t+timedelta(minutes=2),99,104,98.8,103,1)]
    e=[StructureBreak("BOS","bullish",2,101)]
    ob=detect(c,e)
    assert len(ob)==1 and ob[0].index==1 and ob[0].direction=="bullish"
