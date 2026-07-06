import pytest
from ciel.schemas.gap_report import GapMatrixItem
from ciel.skills.auto_refactor_planner import generate_refactor_plan

@pytest.fixture
def mock_gaps():
    return [
        GapMatrixItem(
            claim_id="gap-001",
            claim="Needs Memory Ledger implementation",
            status="technical_debt",
            classification="missing_feature",
            evidence=["Not found"],
            severity="high",
            interpretation="Core functionality missing",
            recommended_action="Implement memory ledger schema and tests"
        ),
        GapMatrixItem(
            claim_id="gap-002",
            claim="Is fully tested",
            status="implemented",
            classification="production_ready",
            evidence=["tests/ passed"],
            severity="low",
            interpretation="OK",
            recommended_action="None"
        )
    ]

def test_generate_refactor_plan_fallback(mock_gaps, monkeypatch):
    def mock_route_inference(prompt):
        return "Error: LLM Disabled"
        
    import ciel.skills.auto_refactor_planner
    monkeypatch.setattr(ciel.skills.auto_refactor_planner, "route_inference", mock_route_inference)
    
    plans = generate_refactor_plan(mock_gaps)
    
    assert len(plans) == 1
    assert plans[0].target_gap_id == "gap-001"
    assert len(plans[0].steps) == 1
    assert plans[0].steps[0].action == "modify_file"
    assert plans[0].steps[0].path == "ciel/memory/decision_ledger.py"
    assert plans[0].steps[0].evidence_id == "gap-001"
    assert plans[0].risk == "high"
    assert plans[0].suggested_tests

def test_generate_refactor_plan_with_target(mock_gaps, monkeypatch):
    def mock_route_inference(prompt):
        return "Error: LLM Disabled"
        
    import ciel.skills.auto_refactor_planner
    monkeypatch.setattr(ciel.skills.auto_refactor_planner, "route_inference", mock_route_inference)
    
    plans = generate_refactor_plan(mock_gaps, target_gap_id="gap-002")
    
    assert len(plans) == 0 # because gap-002 is 'implemented' and not 'technical_debt' or 'missing_feature'

def test_generate_refactor_plan_valid_json(mock_gaps, monkeypatch):
    def mock_route_inference(prompt):
        return '''```json
        {
            "plan_id": "plan_123",
            "target_gap_id": "gap-001",
            "risk": "medium",
            "steps": [
                {
                    "order": 1,
                    "action": "create_file",
                    "path": "ciel/memory/decision_ledger.py",
                    "reason": "Create ledger",
                    "evidence_id": "ev-01"
                }
            ],
            "suggested_tests": ["Test ledger"]
        }
        ```'''
        
    import ciel.skills.auto_refactor_planner
    monkeypatch.setattr(ciel.skills.auto_refactor_planner, "route_inference", mock_route_inference)
    
    plans = generate_refactor_plan(mock_gaps)
    
    assert len(plans) == 1
    assert plans[0].plan_id == "plan_123"
    assert plans[0].risk == "medium"
    assert plans[0].steps[0].action == "create_file"
