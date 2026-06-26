import json
import requests
from typing import Iterator
from .base import BaseProvider


class LocalProvider(BaseProvider):
    """
    Connects to a local model via Ollama (http://localhost:11434) or any
    OpenAI-compatible endpoint. No censorship — you control the model.

    Quick start:
        curl -fsSL https://ollama.com/install.sh | sh
        ollama pull llama3          # or mistral, phi3, qwen2, etc.
        Set LOCAL_MODEL=llama3 in config.json, then switch provider to "local".
    """

    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434", system: str = ""):
        self._model = model
        self._base_url = base_url.rstrip("/")
        self._system = system

    @property
    def name(self) -> str:
        return f"Local ({self._model} @ {self._base_url})"

    def chat(self, messages: list[dict], stream: bool = True) -> Iterator[str]:
        payload = {
            "model": self._model,
            "messages": messages,
            "stream": stream,
        }
        if self._system:
            payload["system"] = self._system

        url = f"{self._base_url}/api/chat"
        resp = requests.post(url, json=payload, stream=stream, timeout=120)
        resp.raise_for_status()

        if stream:
            for line in resp.iter_lines():
                if not line:
                    continue
                data = json.loads(line)
                chunk = data.get("message", {}).get("content", "")
                if chunk:
                    yield chunk
                if data.get("done"):
                    break
        else:
            data = resp.json()
            yield data["message"]["content"]
