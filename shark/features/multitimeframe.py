from ..data.models import Candle

_SECONDS={"1m":60,"3m":180,"5m":300,"15m":900,"1h":3600,"4h":14400,"1d":86400}

def aggregate(candles: list[Candle], timeframe: str) -> list[Candle]:
    if timeframe not in _SECONDS: raise ValueError(f"unsupported timeframe: {timeframe}")
    if not candles: return []
    if any(candles[i].timestamp > candles[i+1].timestamp for i in range(len(candles)-1)):
        raise ValueError("candles must be chronological")
    seconds=_SECONDS[timeframe]; out=[]; bucket_start=None; bucket=[]
    for c in candles:
        start=c.timestamp.replace(second=0,microsecond=0)
        epoch=int(start.timestamp())
        start=start.fromtimestamp(epoch - epoch % seconds, tz=start.tzinfo)
        if bucket_start is None: bucket_start=start
        if start != bucket_start:
            out.append(_merge(bucket)); bucket=[c]; bucket_start=start
        else: bucket.append(c)
    if bucket: out.append(_merge(bucket))
    return out

def _merge(bucket):
    return Candle(bucket[0].timestamp,bucket[0].open,max(x.high for x in bucket),min(x.low for x in bucket),bucket[-1].close,sum(x.volume for x in bucket))
