from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent


def discover_agents() -> dict[str, Path]:
    """Discover Markdown-defined agents beneath this directory."""
    agents: dict[str, Path] = {}
    for contract in ROOT.rglob("AGENT.md"):
        if contract.parent == ROOT:
            continue
        name = contract.parent.relative_to(ROOT).as_posix()
        agents[name] = contract
    return dict(sorted(agents.items()))


def load_contract(agent_path: Path) -> str:
    return agent_path.read_text(encoding="utf-8")


def main() -> None:
    for name, path in discover_agents().items():
        print(f"{name}: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
