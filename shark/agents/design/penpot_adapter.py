"""Deterministic boundary for Shark -> Penpot design tasks.

The adapter intentionally does not pretend to be a Penpot client. It produces
validated task specifications that can be handed to the configured Penpot MCP
runtime when one is connected.
"""
from dataclasses import dataclass, asdict
from enum import Enum
import json


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
    target: str = "shark"
    state: PenpotState = PenpotState.UNCONNECTED


def prepare_task(operation: str, requirement: str, target: str = "shark") -> PenpotTask:
    if not operation.strip():
        raise ValueError("operation is required")
    if not requirement.strip():
        raise ValueError("requirement is required")
    if not target.strip():
        raise ValueError("target is required")
    return PenpotTask(operation.strip(), requirement.strip(), target.strip())


def to_json(task: PenpotTask) -> str:
    payload = asdict(task)
    payload["state"] = task.state.value
    return json.dumps(payload, indent=2)


if __name__ == "__main__":
    print(to_json(prepare_task("design", "Create the XAUUSD signal dashboard")))
