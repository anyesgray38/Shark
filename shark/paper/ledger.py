from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class PaperTrade:
    model_id: str
    symbol: str
    side: str
    entry: float
    stop: float
    target: float
    timestamp: str
    status: str = "open"

class PaperLedger:
    def __init__(self): self.trades=[]
    def record(self, trade: PaperTrade): self.trades.append(trade)
    def open_trades(self): return [t for t in self.trades if t.status == "open"]
