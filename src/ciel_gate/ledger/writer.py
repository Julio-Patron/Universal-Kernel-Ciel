import json
import logging
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from ciel_gate.config import CielSettings
from ciel_gate.ledger.hash_chain import compute_entry_hash

logger = logging.getLogger(__name__)

class DecisionLedger:
    """
    An append-only, cryptographically linked log of kernel decisions and findings.
    Serves as the foundation for the Agent Trust Gate.
    """
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.memory_dir = repo_path / ".ciel"
        self.log_path = self.memory_dir / "decisions.log"
        self.version = "0.9.0"
        
    def _ensure_dir(self):
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
    def get_last_hash(self) -> str:
        """Retrieves the hash of the latest entry in the ledger."""
        if not self.log_path.exists():
            return "0" * 64
            
        last_line = ""
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    last_line = line.strip()
                    
        if not last_line:
            return "0" * 64
            
        try:
            data = json.loads(last_line)
            return data.get("entry_hash", "0" * 64)
        except Exception:
            return "0" * 64

    def _resolve_commit_sha(self) -> str:
        """Resolve the current Git commit without making Git a requirement."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            sha = result.stdout.strip()
            if result.returncode == 0 and sha:
                return sha
        except (OSError, subprocess.SubprocessError):
            pass
        return "unknown"

    def record_decision(self, event_type: str, context: Any, decision: Any, commit_sha: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Appends a cryptographically linked decision to the ledger."""
        if CielSettings.from_env().disable_memory:
            return None
            
        self._ensure_dir()
        prev_hash = self.get_last_hash()
        
        context_hash = compute_entry_hash({"data": context})
        decision_hash = compute_entry_hash({"data": decision})
        
        entry = {
            "id": f"decision_{uuid.uuid4().hex}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "repo": self.repo_path.resolve().name or "unknown",
            "commit_sha": commit_sha or self._resolve_commit_sha(),
            "event_type": event_type,
            "input_hash": context_hash,
            "output_hash": decision_hash,
            "previous_hash": prev_hash,
            "ciel_version": self.version
        }
        
        entry["entry_hash"] = compute_entry_hash(entry)
        
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
            
        return entry
        
    def verify_chain(self) -> bool:
        """Verifies the integrity of the entire decision chain."""
        if not self.log_path.exists():
            return True
            
        prev_hash = "0" * 64
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    entry = json.loads(line)
                    
                    if entry.get("previous_hash") != prev_hash:
                        logger.error(f"Chain broken at entry {entry.get('id')} on line {line_number}")
                        return False
                        
                    computed = compute_entry_hash(entry)
                    if entry.get("entry_hash") != computed:
                        logger.error(f"Hash mismatch at entry {entry.get('id')} on line {line_number}")
                        return False
                        
                    prev_hash = entry.get("entry_hash")
                except Exception as e:
                    logger.error(f"Failed to parse ledger line {line_number}: {e}")
                    return False
                    
        return True
