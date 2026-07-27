"""Command line interface: python -m shark scan [options]"""
from __future__ import annotations

import argparse
import json
import sys
from typing import List

from .providers import PROVIDERS, get_provider
from .scanner import ScanResult, scan


def _format_table(results: List[ScanResult]) -> str:
    header = f"{'SYMBOL':<10} {'PRICE':>12} {'1D%':>7} {'20D%':>7} {'RSI':>5} {'TREND':<6} {'SCORE':>6}  SIGNALS"
    lines = [header, "-" * len(header)]
    for r in results:
        if r.error:
            lines.append(f"{r.symbol:<10} ERROR: {r.error}")
            continue
        sigs = ", ".join(f"{s.name}({s.score:.0f})" for s in r.signals) or "-"
        rsi = f"{r.rsi:.0f}" if r.rsi is not None else "-"
        lines.append(
            f"{r.symbol:<10} {r.price:>12,.2f} {r.change_1d:>+7.2f} "
            f"{r.change_20d:>+7.2f} {rsi:>5} {r.trend:<6} {r.score:>6.1f}  {sigs}"
        )
    return "\n".join(lines)


def _format_detail(results: List[ScanResult]) -> str:
    lines = []
    for r in results:
        if r.error or not r.signals:
            continue
        lines.append(f"\n{r.symbol} — score {r.score:.1f}")
        for s in r.signals:
            lines.append(f"  [{s.direction:>7}] {s.name}: {s.reason}")
    return "\n".join(lines)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="shark", description="Shark — technical setup scanner"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="scan a watchlist for setups")
    p_scan.add_argument(
        "--provider",
        choices=sorted(PROVIDERS),
        default="coinbase",
        help="data source (default: coinbase)",
    )
    p_scan.add_argument(
        "--symbols",
        help="comma-separated symbols (default: provider watchlist)",
    )
    p_scan.add_argument("--days", type=int, default=365, help="history depth")
    p_scan.add_argument(
        "--min-score", type=float, default=0.0, help="hide results scoring below this"
    )
    p_scan.add_argument("--json", action="store_true", help="emit JSON")
    p_scan.add_argument(
        "--detail", action="store_true", help="print signal reasons after the table"
    )

    args = parser.parse_args(argv)

    provider = get_provider(args.provider)
    symbols = (
        [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
        if args.symbols
        else None
    )
    results = scan(provider, symbols, days=args.days, min_score=args.min_score)

    if args.json:
        print(json.dumps([r.to_dict() for r in results], indent=2))
    else:
        print(_format_table(results))
        if args.detail:
            print(_format_detail(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
