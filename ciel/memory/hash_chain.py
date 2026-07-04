import hashlib
import json
from typing import Any, Dict

def hash_data(data: str) -> str:
    """Computes a SHA-256 hash of a string."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def compute_entry_hash(entry: Dict[str, Any]) -> str:
    """
    Computes a deterministic hash for a ledger entry.
    Removes the 'entry_hash' key itself if present to avoid recursion,
    and sorts keys to ensure stability across platforms.
    """
    entry_copy = dict(entry)
    entry_copy.pop('entry_hash', None)
    
    # Sort keys for deterministic JSON output
    serialized = json.dumps(entry_copy, sort_keys=True)
    return hash_data(serialized)
