from shark.features.market_structure_events import StructureBreak
from shark.features.structure_regime import classify

def test_first_directional_reversal_is_mss_then_choch():
    events=[
        StructureBreak("BOS","bullish",5,100),
        StructureBreak("BOS","bullish",8,105),
        StructureBreak("BOS","bearish",12,98),
        StructureBreak("BOS","bullish",16,106),
    ]
    out=classify(events)
    assert [x.kind for x in out]==["BOS","MSS","CHoCH"]
    assert [x.direction for x in out]==["bullish","bearish","bullish"]
