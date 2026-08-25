"""Deterministic Markdown-agent router.

Markdown defines policy and workflow; this module only discovers, loads, validates,
and routes contracts. It never executes Markdown as code.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
AGENTS_ROOT = ROOT.parent


@dataclass(frozen=True)
class AgentContract:
    name: str
    path: Path
    instructions: str


def discover() -> dict[str, AgentContract]:
    found: dict[str, AgentContract] = {}
    for path in AGENTS_ROOT.rglob("AGENT.md"):
        if path.parent == ROOT:
            continue
        name = path.parent.relative_to(AGENTS_ROOT).as_posix()
        found[name] = AgentContract(name, path, path.read_text(encoding="utf-8"))
    return dict(sorted(found.items()))


def load_workflow(agent: AgentContract) -> str | None:
    path = agent.path.parent / "workflow.md"
    return path.read_text(encoding="utf-8") if path.exists() else None


def route(task: str, preferred: str | None = None) -> list[AgentContract]:
    agents = discover()
    if preferred:
        if preferred not in agents:
            raise KeyError(f"Unknown agent: {preferred}")
        return [agents[preferred]]

    text = task.lower()
    order = []
    if any(x in text for x in ("research", "macro", "geopolitical", "intermarket")):
        order += ["research"]
    if any(x in text for x in ("smc", "fvg", "liquidity", "structure", "hypothesis")):
        order += ["analyst"]
    if any(x in text for x in ("backtest", "validate", "falsify", "oos", "walk-forward")):
        order += ["validator"]
    if any(x in text for x in ("signal", "entry", "setup")):
        order += ["signal"]
    if any(x in text for x in ("report", "summary", "findings")):
        order += ["reporter"]
    if any(x in text for x in ("ui", "dashboard", "penpot", "design")):
        order += ["design"]
    if not order:
        order = ["orchestrator"]

    unique = []
    for name in order:
        if name in agents and name not in unique:
            unique.append(name)
    return [agents[name] for name in unique]


def validate_contract(contract: AgentContract) -> list[str]:
    errors = []
    if not contract.instructions.strip():
        errors.append("empty AGENT.md")
    if not re.search(r"^#\s+", contract.instructions, re.MULTILINE):
        errors.append("AGENT.md must contain a Markdown heading")
    return errors


if __name__ == "__main__":
    for name, contract in discover().items():
        errors = validate_contract(contract)
        print(f"{name}: {'PASS' if not errors else 'FAIL: ' + '; '.join(errors)}")
