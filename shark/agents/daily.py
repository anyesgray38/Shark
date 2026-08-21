import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from ..data.providers import CSVMarketDataProvider
from ..market.universe import MARKET_UNIVERSE
from ..research.hypotheses import generate
from ..research.runner import run_hypothesis_search


@dataclass(frozen=True)
class AgentResult:
    name: str
    status: str
    findings: dict


AGENTS = (
    "data_auditor",
    "market_scanner",
    "smc_researcher",
    "candlestick_researcher",
    "intermarket_researcher",
    "regime_researcher",
    "strategy_researcher",
    "falsification_agent",
    "quant_validator",
    "code_auditor",
    "risk_auditor",
    "reporter",
)


def _run_research(provider: CSVMarketDataProvider) -> list[dict]:
    findings: list[dict] = []
    for group_markets in MARKET_UNIVERSE.values():
        for symbol in group_markets:
            for timeframe in ("1m", "5m", "15m", "1h", "4h", "1d"):
                results = run_hypothesis_search(
                    provider, symbol, timeframe, max_features=3
                )
                for result in results:
                    findings.append(
                        {
                            "symbol": result.symbol,
                            "timeframe": result.timeframe,
                            "features": result.features,
                            "trades": len(result.backtest.trades),
                            "total_r": sum(
                                trade.r_multiple for trade in result.backtest.trades
                            ),
                        }
                    )
    return findings


def run(data_root: str = "data") -> dict:
    provider = CSVMarketDataProvider(data_root)
    results = []
    markets = sum(len(v) for v in MARKET_UNIVERSE.values())
    hypothesis_count = sum(1 for _ in generate(max_features=3))
    research = _run_research(provider)

    for name in AGENTS:
        status = "COMPLETE" if name in {"market_scanner", "strategy_researcher", "quant_validator"} else "READY"
        findings = {"role": name}
        if name == "market_scanner":
            findings["research_results"] = len(research)
        if name == "strategy_researcher":
            findings["hypotheses_evaluated"] = len(research)
        if name == "quant_validator":
            findings["nonempty_backtests"] = sum(item["trades"] > 0 for item in research)
        results.append(AgentResult(name, status, findings))

    report = {
        "timestamp": datetime.now(UTC).isoformat(),
        "markets_in_universe": markets,
        "hypothesis_space_sample": hypothesis_count,
        "hypotheses_evaluated": len(research),
        "research_results": research,
        "agents": [asdict(result) for result in results],
        "mode": "research_only",
        "live_execution": "disabled",
    }
    out = Path("reports")
    out.mkdir(exist_ok=True)
    path = out / "daily-agent-report.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
