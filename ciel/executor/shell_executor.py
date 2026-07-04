import shlex
import subprocess
from pathlib import Path
from typing import Iterable, Optional

from ciel.config import CielSettings
from ciel.executor.approval_gate import request_approval


DANGEROUS_TOKENS = {
    "rm",
    "sudo",
    "su",
    "mkfs",
    "dd",
    "shutdown",
    "reboot",
    "curl",
    "wget",
    "nc",
    "netcat",
}


def _parse_command(command: str) -> list[str]:
    try:
        return shlex.split(command)
    except ValueError:
        return []


def _is_allowed(argv: Iterable[str], allowed_commands: tuple[str, ...]) -> tuple[bool, str]:
    args = list(argv)
    if not args:
        return False, "empty or invalid command"

    executable = Path(args[0]).name
    if executable not in allowed_commands:
        return False, f"command '{executable}' is not in the allowlist"

    lowered = {Path(arg).name.lower() for arg in args}
    if lowered & DANGEROUS_TOKENS:
        return False, "command contains a blocked token"

    return True, "allowed"


def execute_command(
    command: str,
    cwd: Path,
    require_approval: bool = True,
    settings: Optional[CielSettings] = None,
) -> dict:
    """Execute an allowlisted command without invoking a shell.

    Execution is disabled unless CIEL_ENABLE_EXEC=1 is set. This keeps the audit
    pipeline safe by default and prevents LLM-generated strings from being run
    as shell scripts.
    """
    runtime = settings or CielSettings.from_env()
    if not runtime.enable_shell:
        return {"status": "denied", "output": "Command execution is disabled. Set CIEL_ENABLE_EXEC=1 to enable it."}

    argv = _parse_command(command)
    allowed, reason = _is_allowed(argv, runtime.allowed_commands)
    if not allowed:
        return {"status": "denied", "output": reason}

    if require_approval:
        approved = request_approval(f"Execute command: `{command}` in {cwd}")
        if not approved:
            return {"status": "denied", "output": "Execution denied by user."}

    try:
        result = subprocess.run(
            argv,
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
            timeout=runtime.shell_timeout_seconds,
        )
        status = "success" if result.returncode == 0 else "error"
        output = result.stdout if result.returncode == 0 else result.stderr
        return {"status": status, "output": output, "returncode": result.returncode}
    except subprocess.TimeoutExpired as exc:
        return {"status": "error", "output": f"Command timed out after {exc.timeout} seconds."}
