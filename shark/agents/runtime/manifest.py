"""Generate a machine-readable registry of Markdown-defined agents."""
from __future__ import annotations
import json
from pathlib import Path
from .router import discover, load_workflow, validate_contract


def build_manifest() -> dict:
    result = {"version": 1, "agents": []}
    for name, contract in discover().items():
        result["agents"].append({
            "name": name,
            "contract": str(contract.path),
            "workflow": bool(load_workflow(contract)),
            "validation_errors": validate_contract(contract),
        })
    return result


def write_manifest(path: str = "agent-manifest.json") -> None:
    Path(path).write_text(json.dumps(build_manifest(), indent=2), encoding="utf-8")


if __name__ == "__main__":
    print(json.dumps(build_manifest(), indent=2))
