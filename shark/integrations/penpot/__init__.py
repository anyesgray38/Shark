from dataclasses import dataclass
from enum import Enum

class PenpotState(str, Enum):
    UNCONNECTED = "UNCONNECTED"
    DESIGN_SPEC_ONLY = "DESIGN_SPEC_ONLY"
    CONNECTED_READ = "CONNECTED_READ"
    CONNECTED_WRITE = "CONNECTED_WRITE"
    VALIDATED = "VALIDATED"

@dataclass(frozen=True)
class PenpotTask:
    operation: str
    requirement: str
    state: PenpotState = PenpotState.UNCONNECTED

def prepare_task(operation: str, requirement: str) -> PenpotTask:
    if not operation.strip() or not requirement.strip():
        raise ValueError("operation and requirement are required")
    return PenpotTask(operation, requirement)
