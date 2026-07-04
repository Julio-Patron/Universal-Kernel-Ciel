import json
import pytest
from pathlib import Path
from ciel.memory.decision_ledger import DecisionLedger

def test_ledger_append_and_verify(tmp_path: Path):
    ledger = DecisionLedger(tmp_path)
    assert ledger.verify_chain() is True
    
    # Write first decision
    entry1 = ledger.record_decision("gap_analysis", {"foo": "bar"}, {"status": "ok"})
    assert ledger.verify_chain() is True
    
    # Write second decision
    entry2 = ledger.record_decision("maturity_audit", {"baz": 1}, {"score": 0.9})
    assert ledger.verify_chain() is True
    
    # Check linkage
    assert entry2["previous_hash"] == entry1["entry_hash"]
    
def test_ledger_detects_corruption(tmp_path: Path):
    ledger = DecisionLedger(tmp_path)
    
    # Setup chain
    ledger.record_decision("event1", {"a": 1}, {"b": 2})
    ledger.record_decision("event2", {"a": 2}, {"b": 3})
    
    # Corrupt log
    log_content = ledger.log_path.read_text(encoding="utf-8").splitlines()
    corrupt_line = log_content[0].replace('"event_type": "event1"', '"event_type": "hacked"')
    log_content[0] = corrupt_line
    ledger.log_path.write_text("\n".join(log_content) + "\n", encoding="utf-8")
    
    # Should detect mismatch
    assert ledger.verify_chain() is False
