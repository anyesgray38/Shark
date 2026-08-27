# Shark Global Vendor Intelligence Engine

A multi-agent, source-diverse vendor discovery and verification framework for international product sourcing.

## Pipeline

`intake -> source_plan -> discovery -> normalize -> dedupe -> verification -> scoring -> shortlist -> RFQ`

Agents live under `vendor_engine/agents/`; deterministic orchestration lives in Python.

## Run

```bash
python -m vendor_engine.cli plan "commercial LED lighting" --countries China,India,USA
python -m vendor_engine.cli search "custom heavyweight hoodies" --countries China,India,Turkey,Vietnam --limit 50
python -m vendor_engine.cli score examples/suppliers.json
python -m vendor_engine.cli rfq examples/suppliers.json --quantity 1000
```

The engine emits JSON/JSONL so it can feed other agent systems, dashboards, or workflows.

## Evidence model

Supplier claims remain evidence-backed records: source, URL, observation, date, and confidence. Marketplace badges are signals, not proof. Final verification should use multiple independent evidence classes and, for material purchases, human document review and sample orders.

## Source strategy

The registry covers global B2B marketplaces, manufacturer directories, country-specific sources, trade-show/exhibitor sources, and trade-intelligence sources. Initial coverage includes Alibaba, Global Sources, Made-in-China, HKTDC, IndiaMART, TradeIndia, EC21, TradeKey, Kompass, Europages, Thomasnet, Fibre2Fashion, Panjiva, and Volza.

Source coverage is configuration rather than hard-coded business logic, so new countries and vertical sources can be added without changing the scoring engine.
