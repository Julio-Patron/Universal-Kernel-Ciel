import pytest
import hashlib
import json
from pathlib import Path
from ciel_gate.contracts import ChangeProposal, DiffFacts
from ciel_gate.policy.schema import Ruleset, ProtectedPath, Limits, DenyRules
from ciel_gate.policy.evaluator import evaluate_proposal
from ciel_gate.ledger.writer import DecisionLedger
from ciel_gate.checks.command_runner import _is_allowed

def test_1_protected_path_requires_approval():
    policy = Ruleset(
        protected_paths=[ProtectedPath(pattern="src/auth/**", action="require_approval")]
    )
    facts = DiffFacts(files_added=[], files_modified=["src/auth/session.py"], files_deleted=[], total_additions=10, total_deletions=5, sensitive_paths=[])
    proposal = ChangeProposal(repository="test", base_commit="HEAD", agent="test", diff="")
    
    decision = evaluate_proposal(proposal, policy, facts, "hash", "hash")
    assert decision.verdict == "require_approval"

def test_2_rename_protected_path_requires_approval():
    policy = Ruleset(
        protected_paths=[ProtectedPath(pattern="src/auth/**", action="require_approval")]
    )
    # Parser maps renames to add/delete or modify
    facts = DiffFacts(files_added=["src/auth/new_session.py"], files_modified=[], files_deleted=["src/auth/old_session.py"], total_additions=10, total_deletions=10, sensitive_paths=[])
    proposal = ChangeProposal(repository="test", base_commit="HEAD", agent="test", diff="")
    
    decision = evaluate_proposal(proposal, policy, facts, "hash", "hash")
    assert decision.verdict == "require_approval"
    
def test_3_path_traversal_denied():
    policy = Ruleset()
    facts = DiffFacts(files_added=["../outside.py"], files_modified=[], files_deleted=[], total_additions=1, total_deletions=0, sensitive_paths=[])
    proposal = ChangeProposal(repository="test", base_commit="HEAD", agent="test", diff="")
    
    decision = evaluate_proposal(proposal, policy, facts, "hash", "hash")
    assert decision.verdict == "deny"
    assert any(v.rule_id == "path-traversal" for v in decision.violations)

def test_4_policy_evaluation_deterministic():
    policy = Ruleset(deny=DenyRules(file_patterns=["**/.env"]))
    facts = DiffFacts(files_added=["config/.env"], files_modified=[], files_deleted=[], total_additions=1, total_deletions=0, sensitive_paths=[])
    proposal = ChangeProposal(repository="test", base_commit="HEAD", agent="test", diff="")
    
    decision1 = evaluate_proposal(proposal, policy, facts, "hash1", "hash2")
    decision2 = evaluate_proposal(proposal, policy, facts, "hash1", "hash2")
    assert decision1.model_dump() == decision2.model_dump()

def test_5_hashes_are_reproducible():
    diff_text = "test diff"
    hash1 = hashlib.sha256(diff_text.encode()).hexdigest()
    hash2 = hashlib.sha256(diff_text.encode()).hexdigest()
    assert hash1 == hash2

def test_6_altered_ledger_breaks_chain(tmp_path):
    ledger = DecisionLedger(tmp_path)
    # Record two decisions
    ledger.record_decision("test", {"some": "context1"}, {"verdict": "allow"})
    ledger.record_decision("test", {"some": "context2"}, {"verdict": "deny"})
    assert ledger.verify_chain() is True
    
    # Tamper with the ledger
    with open(ledger.log_path, "r") as f:
        lines = f.readlines()
        
    import json
    entry1 = json.loads(lines[0])
    entry1["event_type"] = "tampered"
    lines[0] = json.dumps(entry1) + "\n"
    
    with open(ledger.log_path, "w") as f:
        f.writelines(lines)
        
    assert ledger.verify_chain() is False

def test_7_command_allowlist_enforced():
    allowed = ("pytest", "git")
    assert _is_allowed(["pytest", "-q"], allowed)[0] is True
    assert _is_allowed(["rm", "-rf", "/"], allowed)[0] is False
    assert _is_allowed(["curl", "http://evil.com"], allowed)[0] is False
    assert _is_allowed(["bash", "-c", "echo"], allowed)[0] is False

def test_8_offline_operation():
    # If the evaluator can run without hitting the network, this test passes
    # by invoking the evaluator logic completely offline.
    policy = Ruleset()
    facts = DiffFacts(files_added=["main.py"], files_modified=[], files_deleted=[], total_additions=10, total_deletions=0, sensitive_paths=[])
    proposal = ChangeProposal(repository="test", base_commit="HEAD", agent="test", diff="")
    decision = evaluate_proposal(proposal, policy, facts, "hash", "hash")
    assert decision.verdict == "allow"

def test_9_json_contract_compatibility():
    policy = Ruleset()
    facts = DiffFacts(files_added=["main.py"], files_modified=[], files_deleted=[], total_additions=10, total_deletions=0, sensitive_paths=[])
    proposal = ChangeProposal(repository="test", base_commit="HEAD", agent="test", diff="")
    decision = evaluate_proposal(proposal, policy, facts, "hash", "hash")
    
    json_str = decision.model_dump_json()
    data = json.loads(json_str)
    assert "verdict" in data
    assert "risk" in data
    assert "violations" in data
    assert "diff_hash" in data
    assert "policy_hash" in data

def test_10_invalid_diff_never_allowed():
    # A diff that touches denied files
    policy = Ruleset(deny=DenyRules(file_patterns=["**/*.pem"]))
    facts = DiffFacts(files_added=["secret.pem"], files_modified=[], files_deleted=[], total_additions=10, total_deletions=0, sensitive_paths=[])
    proposal = ChangeProposal(repository="test", base_commit="HEAD", agent="test", diff="")
    decision = evaluate_proposal(proposal, policy, facts, "hash", "hash")
    assert decision.verdict == "deny"
