"""FastAPI server: JSON scan API plus the dashboard at /.

Run with:  uvicorn shark.server:app --reload
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

from .providers import PROVIDERS, get_provider
from .scanner import scan

app = FastAPI(title="Shark", description="Technical setup scanner")

_WEB_DIR = Path(__file__).parent / "web"
_CACHE_TTL = 300  # seconds
_cache: dict[str, tuple[float, list[dict]]] = {}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(_WEB_DIR / "index.html")


@app.get("/api/providers")
def providers() -> dict:
    return {
        name: {"default_symbols": cls.default_symbols}
        for name, cls in PROVIDERS.items()
    }


@app.get("/api/scan")
def api_scan(
    provider: str = Query("coinbase"),
    symbols: Optional[str] = Query(None, description="comma-separated"),
    days: int = Query(365, ge=60, le=2000),
    min_score: float = Query(0.0, ge=0.0, le=100.0),
    refresh: bool = Query(False, description="bypass the cache"),
) -> dict:
    symbol_list = (
        [s.strip().upper() for s in symbols.split(",") if s.strip()]
        if symbols
        else None
    )
    try:
        prov = get_provider(provider)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    key = f"{provider}:{','.join(symbol_list or prov.default_symbols)}:{days}"
    now = time.time()
    if not refresh and key in _cache and now - _cache[key][0] < _CACHE_TTL:
        ts, results = _cache[key]
    else:
        results = [r.to_dict() for r in scan(prov, symbol_list, days=days)]
        ts = now
        _cache[key] = (ts, results)

    return {
        "provider": provider,
        "generated_at": ts,
        "results": [
            r
            for r in results
            if r["error"] is not None or r["score"] >= min_score
        ],
    }
