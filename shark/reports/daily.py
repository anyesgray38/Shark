from dataclasses import dataclass, asdict
from datetime import date
import json

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

    def to_json(self): return json.dumps(asdict(self), indent=2)

def empty_report():
    return DailyReport(str(date.today()), 0, 0, 0, 0, 0, "PENDING", [])
