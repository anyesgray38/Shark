from fastapi.testclient import TestClient

from shark.server import app

client = TestClient(app)


def test_index_serves_dashboard():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Shark" in resp.text


def test_providers_endpoint():
    resp = client.get("/api/providers")
    assert resp.status_code == 200
    body = resp.json()
    assert set(body) == {"coinbase", "yahoo", "synthetic"}
    assert body["synthetic"]["default_symbols"]


def test_scan_endpoint_with_synthetic_provider():
    resp = client.get("/api/scan", params={"provider": "synthetic", "days": 250})
    assert resp.status_code == 200
    body = resp.json()
    assert body["provider"] == "synthetic"
    assert len(body["results"]) > 0
    first = body["results"][0]
    for key in ("symbol", "price", "score", "signals", "sparkline"):
        assert key in first


def test_scan_rejects_unknown_provider():
    resp = client.get("/api/scan", params={"provider": "nope"})
    assert resp.status_code == 400
