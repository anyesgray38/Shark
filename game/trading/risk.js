export function calculatePositionSize(equity, riskPerTrade, entry, stopDistance) {
  if (![equity, riskPerTrade, entry, stopDistance].every(Number.isFinite)) return 0;
  if (equity <= 0 || riskPerTrade <= 0 || stopDistance <= 0 || entry <= 0) return 0;
  const maxLoss = equity * riskPerTrade;
  return maxLoss / stopDistance;
}

export function riskCheck(state, side, qty, entry, stopDistance) {
  const riskPerTrade = state.settings?.riskPerTrade ?? 0.02;
  const maxLoss = state.equity * riskPerTrade;
  const requestedLoss = qty * stopDistance;
  const validSide = side === 'long' || side === 'short';
  const valid = validSide && qty > 0 && stopDistance > 0 && requestedLoss <= maxLoss + Number.EPSILON;
  return { valid, maxLoss, requestedLoss, riskPerTrade };
}
