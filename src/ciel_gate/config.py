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
    enable_exec: bool = False
    allowed_commands: Tuple[str, ...] = ("pytest", "python", "git")
    exec_timeout_seconds: int = 30
    ledger_path: str = ".ciel/decisions.log"
    require_approval_tty: bool = True

    @classmethod
    def from_env(cls) -> "CielSettings":
        return cls(
            enable_exec=env_bool("CIEL_GATE_ENABLE_EXEC", cls.enable_exec),
            allowed_commands=env_tuple("CIEL_GATE_ALLOWED_COMMANDS", cls.allowed_commands),
            exec_timeout_seconds=env_int("CIEL_GATE_EXEC_TIMEOUT", cls.exec_timeout_seconds, 1, 600),
            ledger_path=os.getenv("CIEL_GATE_LEDGER_PATH", cls.ledger_path),
            require_approval_tty=env_bool("CIEL_GATE_REQUIRE_APPROVAL_TTY", cls.require_approval_tty),
        )
