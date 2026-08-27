from __future__ import annotations

import re
from collections import defaultdict

from .models import Supplier


def key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def merge(suppliers: list[Supplier]) -> list[Supplier]:
    groups: dict[str, list[Supplier]] = defaultdict(list)
    for s in suppliers:
        identity = key(s.website) if s.website else key(s.name) + key(s.country)
        groups[identity].append(s)
    result = []
    for group in groups.values():
        base = group[0]
        for other in group[1:]:
            base.source_ids = sorted(set(base.source_ids + other.source_ids))
            base.certifications = sorted(set(base.certifications + other.certifications))
            base.contacts = sorted(set(base.contacts + other.contacts))
            base.evidence.extend(other.evidence)
            base.contradictions.extend(other.contradictions)
            base.moq = base.moq or other.moq
            base.price = base.price or other.price
            base.website = base.website or other.website
            base.product = base.product or other.product
        result.append(base)
    return result
