import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime


@dataclass
class DailyReport:
    report_date: str
    markets_scanned: int
    hypotheses_tested: int
    candidates: int
    validated: int
    rejected: int
    audit_status: str
    notes: list[str]

    def to_json(self):
        return json.dumps(asdict(self), indent=2)


def empty_report():
    return DailyReport(str(datetime.now(UTC).date()), 0, 0, 0, 0, 0, "PENDING", [])
