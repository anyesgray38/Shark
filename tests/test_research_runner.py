from datetime import UTC, datetime, timedelta

from shark.data.models import Candle
from shark.data.providers import CSVMarketDataProvider
from shark.research.runner import run_hypothesis_search


def test_research_runner_returns_no_results_without_data(tmp_path):
    provider = CSVMarketDataProvider(str(tmp_path))
    assert run_hypothesis_search(provider, "XAUUSD", "1h") == []


def test_research_runner_reads_normalized_csv_and_tests_hypotheses(tmp_path):
    path = tmp_path / "XAUUSD_1h.csv"
    rows = ["timestamp,open,high,low,close,volume"]
    base = datetime(2026, 1, 1, tzinfo=UTC)
    for i in range(20):
        price = 100 + i
        rows.append(f"{(base + timedelta(hours=i)).isoformat()},{price},{price + 1},{price - 1},{price},100")
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")

    provider = CSVMarketDataProvider(str(tmp_path))
    results = run_hypothesis_search(provider, "XAUUSD", "1h", max_features=2)

    assert results
    assert all(result.symbol == "XAUUSD" for result in results)
    assert all(result.timeframe == "1h" for result in results)
