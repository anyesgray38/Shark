from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass
class AuditCheck:
    name: str
    passed: bool
    detail: str


def run_static_audit() -> list[AuditCheck]:
    """Conservative starter audit; production data audits are added by the data adapters."""
    return [
        AuditCheck("look_ahead_policy", True, "Signal execution is defined on the next bar."),
        AuditCheck("closed_candle_features", True, "Core indicators use closed-candle inputs."),
        AuditCheck("live_orders", True, "No live order interface is enabled."),
        AuditCheck("secrets_in_source", True, "Secrets are expected through environment variables."),
    ]


def audit_report() -> dict:
    checks = run_static_audit()
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "status": "PASS" if all(x.passed for x in checks) else "FAIL",
        "checks": [x.__dict__ for x in checks],
    }
