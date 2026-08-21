from dataclasses import dataclass

@dataclass(frozen=True)
class AgentFinding:
    agent: str
    conclusion: str
    evidence: list[str]
    confidence: float

class ResearchOrchestrator:
    def __init__(self, agents: list): self.agents=agents
    def deliberate(self, context):
        findings=[]
        for agent in self.agents:
            findings.append(agent(context))
        return findings
