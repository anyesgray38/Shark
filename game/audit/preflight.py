"""Static self-audit for the browser game layer.

This audit intentionally runs before game tests/build steps. It catches structural,
accounting, and safety regressions before a proposed game change is accepted.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
GAME = ROOT / "game"
REQUIRED = [
    "core/state.js",
    "core/simulation.js",
    "core/persistence.js",
    "core/offline.js",
    "market/engine.js",
    "trading/engine.js",
    "trading/risk.js",
    "progression/engine.js",
    "ui/app.js",
    "ui/styles.css",
]

ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def read(rel: str) -> str:
    path = GAME / rel
    if not path.exists():
        fail(f"missing required file: game/{rel}")
        return ""
    return path.read_text(encoding="utf-8")


def audit_structure() -> None:
    for rel in REQUIRED:
        read(rel)
    index = read("index.html")
    if index and "./ui/app.js" not in index:
        fail("game/index.html must load ./ui/app.js")


def audit_accounting() -> None:
    trading = read("trading/engine.js")
    if trading:
        for token in ("realizedPnl", "unrealizedPnl", "cash", "equity"):
            if token not in trading:
                fail(f"trading engine missing accounting field: {token}")
        if "cash + pnl" not in trading:
            fail("close-position accounting must settle P&L into cash")
        if "cash + unrealizedPnl" not in trading:
            fail("mark-to-market must derive equity from cash + unrealized P&L")
        if "risk" not in trading.lower():
            fail("trading engine must integrate the risk guard")

    risk = read("trading/risk.js")
    if risk and not all(token in risk for token in ("riskPerTrade", "stopDistance", "maxLoss")):
        fail("risk module must calculate size from riskPerTrade, stopDistance, and maxLoss")


def audit_persistence() -> None:
    persistence = read("core/persistence.js")
    if persistence and not all(token in persistence for token in ("localStorage", "snapshot", "version")):
        fail("persistence must use versioned snapshots in localStorage")


def audit_determinism() -> None:
    simulation = read("core/simulation.js")
    if simulation and "random = Math.random" not in simulation:
        fail("simulation must accept an injectable RNG for deterministic testing")


def audit_dangerous_patterns() -> None:
    for path in GAME.rglob("*.js"):
        text = path.read_text(encoding="utf-8")
        if "eval(" in text or "new Function(" in text:
            fail(f"dynamic code execution found in {path.relative_to(ROOT)}")
        if re.search(r"fetch\s*\(", text) and "game/" in str(path):
            fail(f"unexpected network fetch in game layer: {path.relative_to(ROOT)}")


def main() -> int:
    audit_structure()
    audit_accounting()
    audit_persistence()
    audit_determinism()
    audit_dangerous_patterns()
    if ERRORS:
        print("SHARK SELF-AUDIT: FAIL")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    print("SHARK SELF-AUDIT: PASS")
    print(f"Checked {len(REQUIRED)} required game modules plus static safety rules.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
