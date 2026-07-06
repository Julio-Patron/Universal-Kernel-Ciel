import json
from datetime import datetime
import pytest
from pathlib import Path
from typer.testing import CliRunner
from ciel.cli.main import app
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
    assert entry1["repo"] == tmp_path.name
    commit_sha = entry1["commit_sha"]
    if commit_sha != "unknown":
        assert len(commit_sha) == 40
        int(commit_sha, 16)
    assert datetime.fromisoformat(entry1["timestamp"]).tzinfo is not None
    
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


def test_memory_verify_command_fails_for_corrupt_ledger(tmp_path: Path):
    ledger = DecisionLedger(tmp_path)
    ledger.record_decision("event", {"input": 1}, {"output": 2})
    ledger.log_path.write_text("not-json\n", encoding="utf-8")

    result = CliRunner().invoke(app, ["memory", "verify", str(tmp_path)])

    assert result.exit_code == 1
    assert "verification failed" in result.stdout.lower()


def test_ledger_does_not_fail_when_git_is_unavailable(tmp_path: Path, monkeypatch):
    def unavailable(*args, **kwargs):
        raise OSError("git unavailable")

    monkeypatch.setattr("ciel.memory.decision_ledger.subprocess.run", unavailable)

    entry = DecisionLedger(tmp_path).record_decision("event", {}, {})

    assert entry["commit_sha"] == "unknown"


def test_ledger_stores_hashes_not_sensitive_context(tmp_path: Path):
    secret = "api-key-that-must-not-be-persisted"
    ledger = DecisionLedger(tmp_path)

    ledger.record_decision("inference", {"api_key": secret}, {"result": "ok"})

    assert secret not in ledger.log_path.read_text(encoding="utf-8")
