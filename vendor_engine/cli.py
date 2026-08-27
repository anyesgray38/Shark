from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import Evidence, Supplier
from .planner import plan
from .scoring import rank


def load_suppliers(path: str) -> list[Supplier]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        Supplier(
            name=x["name"], country=x.get("country", ""), website=x.get("website", ""),
            supplier_type=x.get("supplier_type", "unknown"), product=x.get("product", ""),
            source_ids=x.get("source_ids", []), moq=x.get("moq", ""), price=x.get("price", ""),
            oem=x.get("oem"), odm=x.get("odm"), private_label=x.get("private_label"),
            certifications=x.get("certifications", []), contacts=x.get("contacts", []),
            contradictions=x.get("contradictions", []),
            evidence=[Evidence(**e) for e in x.get("evidence", [])],
        ) for x in raw
    ]


def main() -> None:
    parser = argparse.ArgumentParser(prog="shark-vendors")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("plan")
    p.add_argument("product")
    p.add_argument("--countries", default="China,India,Turkey,Vietnam,USA")
    p.add_argument("--vertical")
    p.add_argument("--out")
    s = sub.add_parser("score")
    s.add_argument("file")
    s.add_argument("--limit", type=int, default=20)
    r = sub.add_parser("rfq")
    r.add_argument("file")
    r.add_argument("--quantity", type=int, required=True)
    args = parser.parse_args()

    if args.command == "plan":
        result = plan(args.product, [x.strip() for x in args.countries.split(",") if x.strip()], args.vertical)
        text = json.dumps(result, indent=2)
        if args.out:
            Path(args.out).write_text(text + "\n", encoding="utf-8")
        else:
            print(text)
    elif args.command == "score":
        ranked = rank(load_suppliers(args.file))
        print(json.dumps([x.to_dict() for x in ranked[:args.limit]], indent=2))
    elif args.command == "rfq":
        ranked = rank(load_suppliers(args.file))
        for i, supplier in enumerate(ranked, 1):
            print(f"{i}. {supplier.name} | {supplier.country} | score={supplier.score} | qty={args.quantity} | contact={', '.join(supplier.contacts) or 'UNKNOWN'}")


if __name__ == "__main__":
    main()
