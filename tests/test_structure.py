from datetime import UTC, datetime, timedelta

from shark.data.models import Candle
from shark.features.structure import classify, find_order_blocks, find_swings


def candle(index, open_, high, low, close):
    return Candle(datetime(2026, 1, 1, tzinfo=UTC) + timedelta(minutes=index), open_, high, low, close)


def test_find_swings():
    rows = [
        candle(0, 100, 101, 99, 100),
        candle(1, 100, 102, 99, 101),
        candle(2, 101, 106, 100, 105),
        candle(3, 105, 103, 98, 99),
        candle(4, 99, 101, 97, 98),
    ]
    swings = find_swings(rows, left=1, right=1)
    assert any(point.kind == "high" and point.index == 2 for point in swings)
    assert any(point.kind == "low" and point.index == 4 for point in swings) is False


def test_classify_reversal_sequence():
    from shark.features.structure import StructureBreak

    events = [
        StructureBreak("BOS", "bullish", 5, 100),
        StructureBreak("BOS", "bullish", 8, 105),
        StructureBreak("BOS", "bearish", 12, 98),
        StructureBreak("BOS", "bullish", 16, 106),
    ]
    out = classify(events)
    assert [event.kind for event in out] == ["BOS", "MSS", "CHoCH"]


def test_order_block_uses_last_opposite_candle():
    rows = [
        candle(0, 100, 101, 99, 100),
        candle(1, 100, 102, 98, 99),
        candle(2, 99, 106, 99, 105),
    ]
    from shark.features.structure import StructureBreak

    blocks = find_order_blocks(rows, [StructureBreak("BOS", "bullish", 2, 102)])
    assert blocks == [blocks[0]]
    assert blocks[0].direction == "bullish"
    assert blocks[0].index == 1
