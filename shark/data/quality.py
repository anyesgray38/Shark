from dataclasses import dataclass
from datetime import timedelta

from .models import Candle


_TIMEFRAME_MINUTES = {
    "1m": 1,
    "3m": 3,
    "5m": 5,
    "15m": 15,
    "1h": 60,
    "4h": 240,
    "1d": 1440,
}


@dataclass(frozen=True)
class DataQuality:
    valid: bool
    candles: int
    duplicates: int
    out_of_order: int
    invalid_ohlc: int
    gaps: int
    errors: tuple[str, ...]


def validate_candles(candles: list[Candle], timeframe: str) -> DataQuality:
    if timeframe not in _TIMEFRAME_MINUTES:
        raise ValueError(f"Unsupported timeframe: {timeframe}")

    duplicates = 0
    out_of_order = 0
    invalid_ohlc = 0
    gaps = 0
    errors: list[str] = []
    seen = set()
    expected = timedelta(minutes=_TIMEFRAME_MINUTES[timeframe])

    previous = None
    for candle in candles:
        if candle.timestamp in seen:
            duplicates += 1
        seen.add(candle.timestamp)

        if candle.timestamp.tzinfo is None or candle.timestamp.utcoffset() is None:
            errors.append(f"naive timestamp at {candle.timestamp!s}")

        if not (
            candle.low <= candle.open <= candle.high
            and candle.low <= candle.close <= candle.high
            and candle.low <= candle.high
        ):
            invalid_ohlc += 1

        if previous is not None:
            delta = candle.timestamp - previous.timestamp
            if delta <= timedelta(0):
                out_of_order += 1
            elif delta > expected:
                gaps += 1
        previous = candle

    if duplicates:
        errors.append(f"duplicate timestamps: {duplicates}")
    if out_of_order:
        errors.append(f"out-of-order timestamps: {out_of_order}")
    if invalid_ohlc:
        errors.append(f"invalid OHLC rows: {invalid_ohlc}")
    if gaps:
        errors.append(f"timeframe gaps: {gaps}")

    return DataQuality(
        valid=not errors,
        candles=len(candles),
        duplicates=duplicates,
        out_of_order=out_of_order,
        invalid_ohlc=invalid_ohlc,
        gaps=gaps,
        errors=tuple(errors),
    )
