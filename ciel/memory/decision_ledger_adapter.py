import json
from pathlib import Path
from datetime import datetime

def log_decision(memory_dir: Path, context: str, decision: str, reason: str):
    """Appends an immutable decision record to the decisions.log file."""
    log_path = memory_dir / "decisions.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "context": context,
        "decision": decision,
        "reason": reason
    }
    
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
