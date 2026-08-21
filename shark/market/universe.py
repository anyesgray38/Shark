MARKET_UNIVERSE = {
    "primary": ["XAUUSD"],
    "forex": ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD"],
    "futures": ["ES", "NQ", "YM", "RTY", "GC", "SI", "CL", "ZN"],
    "mag7": ["AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "TSLA"],
    "volatility": ["VIX"],
    "crypto": ["BTCUSD", "ETHUSD", "SOLUSD"],
}

FEATURES = [
    "market_structure", "bos", "choch_mss", "liquidity_sweep",
    "equal_high_low", "fvg", "ifvg", "bpr", "order_block",
    "breaker_block", "premium_discount", "displacement", "vwap",
    "atr_regime", "volume_regime", "session", "kill_zone",
    "candlestick_patterns", "multi_candle_sequences", "trend_regime",
    "range_regime", "vix_regime", "mag7_alignment", "dxy_relationship",
    "cross_market_momentum",
]
