const STORAGE_KEY = 'shark-idle-trading-state-v1';

export function saveState(state, storage = globalThis.localStorage) {
  if (!storage) return false;
  storage.setItem(STORAGE_KEY, JSON.stringify(snapshot(state)));
  return true;
}

export function loadState(storage = globalThis.localStorage) {
  if (!storage) return null;
  try {
    const raw = storage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const state = JSON.parse(raw);
    return state?.version === 1 ? state : null;
  } catch {
    return null;
  }
}

export function snapshot(state) {
  return structuredClone(state);
}

export function clearState(storage = globalThis.localStorage) {
  storage?.removeItem(STORAGE_KEY);
}
