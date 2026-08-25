"""Structured handoff contract shared by Shark agents."""
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AgentHandoff:
    status: str
    evidence: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)
    next_action: str = ""
    provenance: list[str] = field(default_factory=list)

    def is_promotable(self) -> bool:
        return self.status.upper() == "PASS" and not self.failures

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "evidence": self.evidence,
            "assumptions": self.assumptions,
            "metrics": self.metrics,
            "failures": self.failures,
            "next_action": self.next_action,
            "provenance": self.provenance,
        }
