import { createInitialState } from '../core/state.js';
import { step } from '../core/simulation.js';
import { calculatePositionSize } from '../trading/risk.js';
import { closePosition, openPosition } from '../trading/engine.js';
import { loadState, saveState } from '../core/persistence.js';

const root = document.querySelector('#game');
let state = loadState() ?? createInitialState();

function money(value) {
  return `$${value.toFixed(2)}`;
}

function render() {
  const p = state.position;
  const risk = state.settings.riskPerTrade * 100;
  const suggested = calculatePositionSize(state.equity, state.settings.riskPerTrade, state.market.price, state.market.price * 0.01);

  root.innerHTML = `
    <section class="hud">
      <div><span>Capital</span><strong>${money(state.equity)}</strong></div>
      <div><span>Market</span><strong>${money(state.market.price)}</strong></div>
      <div><span>Regime</span><strong>${state.market.regime}</strong></div>
      <div><span>Level</span><strong>${state.progression.level}</strong></div>
    </section>
    <section class="panel">
      <h2>Trading Desk</h2>
      <p>Risk: ${risk.toFixed(1)}% · Suggested size: ${suggested.toFixed(3)}</p>
      <div class="controls">
        <button data-action="buy" ${p.qty ? 'disabled' : ''}>BUY</button>
        <button data-action="sell" ${p.qty ? 'disabled' : ''}>SELL</button>
        <button data-action="close" ${p.qty ? '' : 'disabled'}>CLOSE</button>
        <button data-action="tick">NEXT TICK</button>
      </div>
      <p>Position: ${p.side} ${p.qty ? p.qty.toFixed(3) : ''} · Unrealized: ${money(state.unrealizedPnl)}</p>
    </section>
    <section class="panel">
      <h2>Track Record</h2>
      <p>Trades ${state.stats.trades} · Wins ${state.stats.wins} · Losses ${state.stats.losses} · Reputation ${state.progression.reputation}</p>
    </section>`;
}

function act(action) {
  const price = state.market.price;
  if (action === 'tick') state = step(state);
  if (action === 'buy' || action === 'sell') {
    const stopDistance = price * 0.01;
    const qty = calculatePositionSize(state.equity, state.settings.riskPerTrade, price, stopDistance);
    state = openPosition(state, action === 'buy' ? 'long' : 'short', qty, price, stopDistance);
  }
  if (action === 'close') state = closePosition(state, price);
  saveState(state);
  render();
}

root.addEventListener('click', (event) => {
  const action = event.target.dataset.action;
  if (action) act(action);
});

render();
