from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote_plus

ROOT = Path(__file__).resolve().parent


def load_registry() -> dict:
    return json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))


def query_variants(product: str, country: str) -> list[str]:
    return [
        product,
        f"{product} manufacturer",
        f"{product} factory",
        f"{product} OEM",
        f"{product} ODM private label",
        f"{country} {product} manufacturer",
        f"{country} {product} factory",
    ]


def plan(product: str, countries: list[str], vertical: str | None = None) -> dict:
    registry = load_registry()
    sources = registry["sources"]
    by_id = {s["id"]: s for s in sources}
    selected: list[str] = []
    for country in countries:
        key = country.strip().lower().replace(" ", "_")
        for sid in registry.get("regions", {}).get(key, []):
            if sid not in selected:
                selected.append(sid)
    for sid in registry["regions"].get("global", []):
        if sid not in selected:
            selected.append(sid)
    if vertical:
        for s in sources:
            if vertical.lower() in [v.lower() for v in s.get("verticals", [])] and s["id"] not in selected:
                selected.append(s["id"])

    searches = []
    for sid in selected:
        source = by_id[sid]
        for country in countries:
            for q in query_variants(product, country):
                template = source.get("search")
                if template:
                    searches.append({
                        "source_id": sid,
                        "source": source["name"],
                        "country": country,
                        "query": q,
                        "url": template.format(query=quote_plus(q)),
                    })
    return {
        "product": product,
        "countries": countries,
        "vertical": vertical,
        "source_ids": selected,
        "searches": searches,
        "evidence_required": ["identity", "capability", "product", "commercial", "compliance", "trade", "reputation"],
    }
