from abc import ABC, abstractmethod
from typing import Iterator


class BaseProvider(ABC):
    """All providers implement this — swap Claude for local with zero changes elsewhere."""

    @abstractmethod
    def chat(self, messages: list[dict], stream: bool = True) -> Iterator[str]:
        """Yield response text chunks. messages = [{"role": "user"|"assistant", "content": str}]"""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...
