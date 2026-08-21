from dataclasses import dataclass
from .market_structure_events import StructureBreak

@dataclass(frozen=True)
class RegimeEvent:
    kind: str
    direction: str
    index: int
    level: float


def classify(events: list[StructureBreak]) -> list[RegimeEvent]:
    """Classify directional breaks without assuming a trade outcome.

    MSS is assigned to the first confirmed break that reverses the most
    recently established break direction; CHoCH is assigned to subsequent
    directional reversals after an established state.
    """
    out=[]
    state=None
    for e in sorted(events, key=lambda x: x.index):
        if state is None:
            state=e.direction
            continue
        if e.direction == state:
            kind="BOS"
        else:
            kind="MSS" if not any(x.kind == "CHoCH" for x in out) else "CHoCH"
            state=e.direction
        out.append(RegimeEvent(kind,e.direction,e.index,e.broken_level))
    return out
