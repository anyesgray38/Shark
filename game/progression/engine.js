const MILESTONES = [
  { level: 1, capital: 1000, unlock: 'manual-trading' },
  { level: 2, capital: 2500, unlock: 'risk-controls' },
  { level: 3, capital: 10000, unlock: 'analyst-agent' },
  { level: 4, capital: 50000, unlock: 'automated-strategy' },
  { level: 5, capital: 250000, unlock: 'trading-desk' },
  { level: 6, capital: 1000000, unlock: 'fund-management' }
];

export function applyProgression(state) {
  const unlocked = [...state.progression.unlocked];
  let level = state.progression.level;

  for (const milestone of MILESTONES) {
    if (state.equity >= milestone.capital) {
      level = Math.max(level, milestone.level);
      if (!unlocked.includes(milestone.unlock)) unlocked.push(milestone.unlock);
    }
  }

  const reputation = Math.min(1000, state.stats.wins * 10 + state.stats.trades * 2);
  return { ...state, progression: { level, reputation, unlocked } };
}

export { MILESTONES };
