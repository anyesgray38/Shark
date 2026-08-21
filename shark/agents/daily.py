import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from ..data.providers import CSVMarketDataProvider
from ..data.quality import validate_candles
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


def _run_research(provider: CSVMarketDataProvider) -> tuple[list[dict], list[dict]]:
    findings: list[dict] = []
    quality: list[dict] = []
    for group_markets in MARKET_UNIVERSE.values():
        for symbol in group_markets:
            for timeframe in ("1m", "5m", "15m", "1h", "4h", "1d"):
                candles = provider.candles(symbol, timeframe)
                check = validate_candles(candles, timeframe)
                quality.append(
                    {
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "valid": check.valid,
                        "candles": check.candles,
                        "duplicates": check.duplicates,
                        "out_of_order": check.out_of_order,
                        "invalid_ohlc": check.invalid_ohlc,
                        "gaps": check.gaps,
                        "errors": check.errors,
                    }
                )
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
                            "structure_events": result.structure_events,
                            "fvg_events": result.fvg_events,
                            "liquidity_sweeps": result.liquidity_sweeps,
                            "order_blocks": result.order_blocks,
                        }
                    )
    return findings, quality


def run(data_root: str = "data") -> dict:
    provider = CSVMarketDataProvider(data_root)
    results = []
    markets = sum(len(v) for v in MARKET_UNIVERSE.values())
    hypothesis_count = sum(1 for _ in generate(max_features=3))
    research, quality = _run_research(provider)

    for name in AGENTS:
        status = "COMPLETE" if name in {"market_scanner", "strategy_researcher", "quant_validator"} else "READY"
        findings = {"role": name}
        if name == "data_auditor":
            findings["quality_checks"] = len(quality)
            findings["invalid_series"] = sum(not item["valid"] for item in quality)
        if name == "market_scanner":
            findings["research_results"] = len(research)
        if name == "smc_researcher":
            findings["structure_events"] = sum(item["structure_events"] for item in research)
            findings["fvg_events"] = sum(item["fvg_events"] for item in research)
            findings["liquidity_sweeps"] = sum(item["liquidity_sweeps"] for item in research)
            findings["order_blocks"] = sum(item["order_blocks"] for item in research)
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
        "data_quality": quality,
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
