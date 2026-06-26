from ..providers.base import BaseProvider
from ..providers.claude_provider import ClaudeProvider
from ..providers.local_provider import LocalProvider


def make_provider(cfg: dict) -> BaseProvider:
    system = cfg.get("system_prompt", "")
    provider = cfg.get("provider", "claude")

    if provider == "claude":
        return ClaudeProvider(model=cfg["claude_model"], system=system)
    elif provider == "local":
        return LocalProvider(
            model=cfg["local_model"],
            base_url=cfg["local_url"],
            system=system,
        )
    else:
        raise ValueError(f"Unknown provider '{provider}'. Choose 'claude' or 'local'.")
