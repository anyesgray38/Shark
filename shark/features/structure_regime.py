from dataclasses import dataclass
from .market_structure_events import StructureBreak

@dataclass(frozen=True)
class RegimeEvent:
    kind: str
    direction: str
    index: int
    level: float


def classify(events: list[StructureBreak]) -> list[RegimeEvent]:
    """Classify confirmed directional breaks into BOS, MSS, and CHoCH."""
    out=[]
    state=None
    reversal_seen=False
    for e in sorted(events, key=lambda x: x.index):
        if state is None:
            state=e.direction
            out.append(RegimeEvent("BOS", e.direction, e.index, e.broken_level))
            continue
        if e.direction == state:
            kind="BOS"
        else:
            kind="CHoCH" if reversal_seen else "MSS"
            reversal_seen=True
            state=e.direction
        out.append(RegimeEvent(kind,e.direction,e.index,e.broken_level))
    return out
