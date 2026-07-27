from __future__ import annotations

from typing import Dict, Type

from .base import DataProvider
from .coinbase import CoinbaseProvider
from .synthetic import SyntheticProvider
from .yahoo import YahooProvider

PROVIDERS: Dict[str, Type[DataProvider]] = {
    CoinbaseProvider.name: CoinbaseProvider,
    YahooProvider.name: YahooProvider,
    SyntheticProvider.name: SyntheticProvider,
}


def get_provider(name: str) -> DataProvider:
    try:
        return PROVIDERS[name]()
    except KeyError:
        raise ValueError(
            f"unknown provider {name!r}; choose from {sorted(PROVIDERS)}"
        ) from None
