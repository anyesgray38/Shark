import os
from typing import Iterator
import anthropic
from .base import BaseProvider


class ClaudeProvider(BaseProvider):
    def __init__(self, model: str = "claude-sonnet-4-6", system: str = ""):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model
        self._system = system

    @property
    def name(self) -> str:
        return f"Claude ({self._model})"

    def chat(self, messages: list[dict], stream: bool = True) -> Iterator[str]:
        kwargs = dict(
            model=self._model,
            max_tokens=4096,
            messages=messages,
        )
        if self._system:
            kwargs["system"] = self._system

        if stream:
            with self._client.messages.stream(**kwargs) as s:
                for text in s.text_stream:
                    yield text
        else:
            response = self._client.messages.create(**kwargs)
            yield response.content[0].text
