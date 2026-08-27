from __future__ import annotations

from .models import Supplier


def score_supplier(s: Supplier) -> float:
    evidence_kinds = {e.kind for e in s.evidence}
    source_count = len(set(s.source_ids))
    score = 0.0
    score += 20 if s.supplier_type.lower() in {"manufacturer", "factory", "oem", "odm"} else 8 if s.supplier_type.lower() in {"exporter", "distributor"} else 3
    score += 15 if s.product else 0
    score += 15 if s.website else 0
    score += 10 if s.certifications or "compliance" in evidence_kinds else 0
    score += 10 if "trade" in evidence_kinds else 0
    score += 8 if s.moq else 0
    score += 8 if s.price else 0
    score += 5 if s.contacts else 0
    score += 5 if "reputation" in evidence_kinds else 0
    score += min(4, source_count)
    score -= min(20, 20 if s.contradictions else 0)
    score -= 15 if "unsupported_certification" in evidence_kinds else 0
    score -= 10 if s.supplier_type.lower() in {"reseller", "trading_company"} else 0
    score -= min(10, max(0, 3 - len(evidence_kinds)) * 3)
    return round(max(0.0, min(100.0, score)), 2)


def rank(suppliers: list[Supplier]) -> list[Supplier]:
    for supplier in suppliers:
        supplier.score = score_supplier(supplier)
    return sorted(suppliers, key=lambda x: x.score, reverse=True)
