import { riskCheck } from './risk.js';

export function openPosition(state, side, qty, price, stopDistance) {
  if (!['long', 'short'].includes(side) || qty <= 0 || price <= 0) return state;
  if (state.position.qty > 0) return state;

  const risk = riskCheck(state, side, qty, price, stopDistance);
  if (!risk.valid) return state;

  return {
    ...state,
    position: { side, qty, entry: price, stopDistance }
  };
}

export function closePosition(state, price) {
  const p = state.position;
  if (p.qty <= 0 || !Number.isFinite(price) || price <= 0) return state;

  const direction = p.side === 'long' ? 1 : -1;
  const pnl = (price - p.entry) * p.qty * direction;
  const cash = state.cash + pnl;

  return {
    ...state,
    cash,
    equity: cash,
    realizedPnl: state.realizedPnl + pnl,
    unrealizedPnl: 0,
    peakEquity: Math.max(state.peakEquity, cash),
    position: { side: 'flat', qty: 0, entry: 0, stopDistance: 0 },
    stats: {
      ...state.stats,
      trades: state.stats.trades + 1,
      wins: state.stats.wins + (pnl > 0 ? 1 : 0),
      losses: state.stats.losses + (pnl <= 0 ? 1 : 0)
    }
  };
}

export function markToMarket(state, price) {
  const p = state.position;
  if (p.qty <= 0) return { ...state, equity: state.cash, unrealizedPnl: 0 };
  const direction = p.side === 'long' ? 1 : -1;
  const unrealizedPnl = (price - p.entry) * p.qty * direction;
  return { ...state, unrealizedPnl, equity: state.cash + unrealizedPnl };
}
