export function tickMarket(market, random = Math.random) {
  const shock = (random() - 0.5) * 2;
  const drift = market.regime === 'bull' ? 0.0008 : market.regime === 'bear' ? -0.0008 : 0;
  const move = drift + shock * market.volatility;
  const price = Math.max(0.01, market.price * (1 + move));
  const regimes = ['bull', 'balanced', 'bear'];
  const regime = random() < 0.025 ? regimes[Math.floor(random() * regimes.length)] : market.regime;

  return { ...market, price, regime, tick: market.tick + 1 };
}
