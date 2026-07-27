from shark.providers.synthetic import SyntheticProvider
from shark.scanner import composite_score, scan
from shark.signals import Signal


def test_synthetic_provider_is_deterministic():
    a = SyntheticProvider().fetch("DEMO1", days=200)
    b = SyntheticProvider().fetch("DEMO1", days=200)
    assert a.equals(b)
    c = SyntheticProvider().fetch("DEMO2", days=200)
    assert not a["close"].equals(c["close"])


def test_scan_returns_ranked_results():
    provider = SyntheticProvider()
    results = scan(provider, days=250)
    assert len(results) == len(provider.default_symbols)
    scores = [r.score for r in results if r.error is None]
    assert scores == sorted(scores, reverse=True)
    for r in results:
        assert r.error is None
        assert r.price > 0
        assert len(r.sparkline) == 30


def test_composite_score_empty_and_capped():
    assert composite_score([]) == 0.0
    sigs = [
        Signal("breakout", "bullish", 100.0, "x"),
        Signal("golden_cross", "bullish", 100.0, "x"),
        Signal("macd_cross", "bullish", 100.0, "x"),
    ]
    assert composite_score(sigs) == 100.0
    single = [Signal("breakout", "bullish", 60.0, "x")]
    assert composite_score(single) == 60.0


def test_scan_reports_errors_without_crashing():
    class Boom(SyntheticProvider):
        def fetch(self, symbol, days=365):
            if symbol == "BAD":
                raise ValueError("no data")
            return super().fetch(symbol, days)

    results = scan(Boom(), ["DEMO1", "BAD"], days=250)
    by_symbol = {r.symbol: r for r in results}
    assert by_symbol["BAD"].error == "no data"
    assert by_symbol["DEMO1"].error is None
