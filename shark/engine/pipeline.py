from dataclasses import dataclass
from typing import Callable, Iterable

@dataclass
class ResearchJob:
    symbol: str
    timeframe: str
    hypothesis: tuple[str, ...]

@dataclass
class ResearchResult:
    job: ResearchJob
    status: str
    metrics: dict
    evidence: list[str]

class AdaptiveResearchPipeline:
    """Orchestrates research stages; execution is intentionally absent."""
    def __init__(self, detector: Callable, tester: Callable, validator: Callable):
        self.detector, self.tester, self.validator = detector, tester, validator

    def run(self, jobs: Iterable[ResearchJob]):
        for job in jobs:
            features = self.detector(job)
            metrics = self.tester(job, features)
            status = self.validator(metrics)
            yield ResearchResult(job, status, metrics, ["detected", "tested", "validated"])
