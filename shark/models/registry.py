from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class ModelRecord:
    model_id: str
    features: tuple[str, ...]
    status: str = "candidate"
    metrics: dict = field(default_factory=dict)
    history: list[dict] = field(default_factory=list)
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ModelRegistry:
    def __init__(self): self.models={}
    def upsert(self, record: ModelRecord): self.models[record.model_id]=record
    def promote(self, model_id: str, status: str): self.models[model_id].status=status
    def reject(self, model_id: str, reason: str):
        m=self.models[model_id]; m.status="rejected"; m.history.append({"reason":reason})
    def leaderboard(self):
        return sorted(self.models.values(), key=lambda m:m.metrics.get("score", float("-inf")), reverse=True)
