from itertools import combinations

BASE_FEATURES = [
    "fvg", "liquidity_sweep", "displacement", "market_structure",
    "order_block", "ifvg", "bpr", "premium_discount", "candlestick_patterns",
    "vix_regime", "mag7_alignment", "session", "atr_regime",
]

def generate(max_features: int = 4):
    for n in range(2, max_features + 1):
        yield from combinations(BASE_FEATURES, n)
