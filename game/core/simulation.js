import { tickMarket } from '../market/engine.js';
import { markToMarket } from '../trading/engine.js';
import { applyProgression } from '../progression/engine.js';

export function step(state, random = Math.random) {
  const market = tickMarket(state.market, random);
  const marked = markToMarket({ ...state, market }, market.price);
  return applyProgression(marked);
}

export function runSteps(state, count, random = Math.random) {
  let next = state;
  for (let i = 0; i < count; i += 1) next = step(next, random);
  return next;
}
