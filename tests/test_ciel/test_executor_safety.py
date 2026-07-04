from pathlib import Path

from ciel.config import CielSettings
from ciel.executor.shell_executor import execute_command


def test_shell_is_off_by_default():
    result = execute_command("python --version", Path("."), require_approval=False, settings=CielSettings())
    assert result["status"] == "denied"


def test_shell_uses_allowlist():
    settings = CielSettings(enable_shell=True, allowed_commands=("python",))
    result = execute_command("unknown-tool --version", Path("."), require_approval=False, settings=settings)
    assert result["status"] == "denied"
