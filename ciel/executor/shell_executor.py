import subprocess
from pathlib import Path
from ciel.executor.approval_gate import request_approval

def execute_command(command: str, cwd: Path, require_approval: bool = True) -> dict:
    """Executes a shell command in the specified directory."""
    if require_approval:
        approved = request_approval(f"Execute shell command: `{command}` in {cwd}")
        if not approved:
            return {"status": "denied", "output": "Execution denied by user."}
            
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return {"status": "success", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "output": e.stderr}
