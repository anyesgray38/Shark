from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class ModelRecord:
    model_id: str
    features: tuple[str, ...]
    status: str = "candidate"
    metrics: dict = field(default_factory=dict)
    history: list[dict] = field(default_factory=list)
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class ModelRegistry:
    def __init__(self):
        self.models = {}

    def upsert(self, record: ModelRecord):
        self.models[record.model_id] = record

    def promote(self, model_id: str, status: str):
        self.models[model_id].status = status

    def reject(self, model_id: str, reason: str):
        model = self.models[model_id]
        model.status = "rejected"
        model.history.append({"reason": reason})

    def leaderboard(self):
        return sorted(
            self.models.values(),
            key=lambda model: model.metrics.get("score", float("-inf")),
            reverse=True,
        )
