from collections import defaultdict
from datetime import datetime
from ..data.models import Candle

_MINUTES = {"1m":1,"3m":3,"5m":5,"15m":15,"1h":60,"4h":240,"1d":1440}

def aggregate(candles: list[Candle], timeframe: str) -> list[Candle]:
    if timeframe not in _MINUTES: raise ValueError(f"Unsupported timeframe: {timeframe}")
    minutes = _MINUTES[timeframe]
    buckets = {}
    for c in candles:
        epoch = int(c.timestamp.timestamp() // 60)
        bucket = epoch - (epoch % minutes)
        if bucket not in buckets: buckets[bucket] = [c, c.high, c.low, c.volume]
        else:
            b=buckets[bucket]; b[1]=max(b[1],c.high); b[2]=min(b[2],c.low); b[3]+=c.volume; b[0]=c
    out=[]
    for bucket in sorted(buckets):
        last, high, low, vol = buckets[bucket]
        first_candidates=[c for c in candles if int(c.timestamp.timestamp()//60) - (int(c.timestamp.timestamp()//60)%minutes)==bucket]
        first=first_candidates[0]
        out.append(Candle(first.timestamp, first.open, high, low, last.close, vol))
    return out
