from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Tuple


def env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def env_int(name: str, default: int, minimum: int = 1, maximum: int = 300) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return max(minimum, min(value, maximum))


def env_tuple(name: str, default: Tuple[str, ...]) -> Tuple[str, ...]:
    raw = os.getenv(name)
    if not raw:
        return default
    values = tuple(part.strip() for part in raw.split(",") if part.strip())
    return values or default


@dataclass(frozen=True)
class CielSettings:
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    llm_provider: str = "auto"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-haiku-latest"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    llm_timeout_seconds: int = 10
    disable_llm: bool = False
    enable_shell: bool = False
    shell_timeout_seconds: int = 30
    allowed_commands: Tuple[str, ...] = ("python", "pytest", "git", "pip")

    @classmethod
    def from_env(cls) -> "CielSettings":
        return cls(
            ollama_url=os.getenv("CIEL_OLLAMA_URL", cls.ollama_url).rstrip("/"),
            ollama_model=os.getenv("CIEL_OLLAMA_MODEL", cls.ollama_model),
            llm_provider=os.getenv("CIEL_LLM_PROVIDER", cls.llm_provider),
            openai_api_key=os.getenv("CIEL_OPENAI_API_KEY", cls.openai_api_key),
            openai_model=os.getenv("CIEL_OPENAI_MODEL", cls.openai_model),
            anthropic_api_key=os.getenv("CIEL_ANTHROPIC_API_KEY", cls.anthropic_api_key),
            anthropic_model=os.getenv("CIEL_ANTHROPIC_MODEL", cls.anthropic_model),
            gemini_api_key=os.getenv("CIEL_GEMINI_API_KEY", cls.gemini_api_key),
            gemini_model=os.getenv("CIEL_GEMINI_MODEL", cls.gemini_model),
            llm_timeout_seconds=env_int("CIEL_LLM_TIMEOUT", cls.llm_timeout_seconds),
            disable_llm=env_bool("CIEL_DISABLE_LLM", cls.disable_llm),
            enable_shell=env_bool("CIEL_ENABLE_EXEC", cls.enable_shell),
            shell_timeout_seconds=env_int("CIEL_EXEC_TIMEOUT", cls.shell_timeout_seconds, 1, 600),
            allowed_commands=env_tuple("CIEL_ALLOWED_COMMANDS", cls.allowed_commands),
        )
