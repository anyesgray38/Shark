const MAX_OFFLINE_SECONDS = 8 * 60 * 60;

export function calculateOfflineSeconds(savedAt, now = Date.now()) {
  const elapsed = Math.max(0, (now - savedAt) / 1000);
  return Math.min(elapsed, MAX_OFFLINE_SECONDS);
}

export function applyOfflineProgress(state, savedAt, now = Date.now()) {
  const seconds = calculateOfflineSeconds(savedAt, now);
  if (seconds <= 0) return { state, seconds: 0 };

  // Offline progress advances the market without creating trades.
  const ticks = Math.floor(seconds * (state.settings?.speed ?? 1));
  const next = { ...state, market: { ...state.market, tick: state.market.tick + ticks } };
  return { state: next, seconds };
}
