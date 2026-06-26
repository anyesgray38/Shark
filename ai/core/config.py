import json
import os
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent.parent / "config.json"

DEFAULTS = {
    "provider": "claude",
    "claude_model": "claude-sonnet-4-6",
    "local_model": "llama3",
    "local_url": "http://localhost:11434",
    "system_prompt": "",
    "stream": True,
}


def load() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            data = json.load(f)
        return {**DEFAULTS, **data}
    return dict(DEFAULTS)


def save(cfg: dict) -> None:
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"Config saved to {CONFIG_PATH}")
