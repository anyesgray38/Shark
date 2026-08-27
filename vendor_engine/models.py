from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Evidence:
    kind: str
    source: str
    url: str
    observation: str = ""
    confidence: float = 0.0
    captured_at: str | None = None


@dataclass
class Supplier:
    name: str
    country: str = ""
    website: str = ""
    supplier_type: str = "unknown"
    product: str = ""
    source_ids: list[str] = field(default_factory=list)
    moq: str = ""
    price: str = ""
    oem: bool | None = None
    odm: bool | None = None
    private_label: bool | None = None
    certifications: list[str] = field(default_factory=list)
    contacts: list[str] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)
    score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
