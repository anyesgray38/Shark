export function createInitialState() {
  return {
    version: 1,
    cash: 1000,
    equity: 1000,
    peakEquity: 1000,
    realizedPnl: 0,
    unrealizedPnl: 0,
    position: { side: 'flat', qty: 0, entry: 0, stopDistance: 0 },
    market: { price: 100, volatility: 0.008, regime: 'balanced', tick: 0 },
    stats: { trades: 0, wins: 0, losses: 0 },
    progression: { level: 1, reputation: 0, unlocked: ['manual-trading'] },
    settings: { riskPerTrade: 0.02, speed: 1 }
  };
}

export function snapshot(state) {
  return structuredClone(state);
}
