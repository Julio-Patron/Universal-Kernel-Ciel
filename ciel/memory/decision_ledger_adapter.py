import json
from pathlib import Path
from datetime import datetime
from ciel.executor.filesystem_manager import create_directory, append_file

def log_decision(memory_dir: Path, context: str, decision: str, reason: str):
    """Appends an immutable decision record to the decisions.log file."""
    log_path = memory_dir / "decisions.log"
    # Internal writes are permitted without explicit user approval
    create_directory(log_path.parent, require_approval=False)
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "context": context,
        "decision": decision,
        "reason": reason
    }
    
    # Internal writes are permitted without explicit user approval
    append_file(log_path, json.dumps(entry) + "\n", require_approval=False)
