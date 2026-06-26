import json
from datetime import datetime
from pathlib import Path

SESSIONS_DIR = Path(__file__).parent.parent.parent / "sessions"


def _ensure_dir() -> Path:
    SESSIONS_DIR.mkdir(exist_ok=True)
    return SESSIONS_DIR


def save(messages: list[dict], provider_name: str) -> Path:
    d = _ensure_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = d / f"session_{ts}.json"
    with open(path, "w") as f:
        json.dump({"provider": provider_name, "messages": messages}, f, indent=2)
    return path


def load(path: str) -> list[dict]:
    with open(path) as f:
        data = json.load(f)
    return data["messages"]


def list_sessions() -> list[Path]:
    d = _ensure_dir()
    return sorted(d.glob("session_*.json"))
