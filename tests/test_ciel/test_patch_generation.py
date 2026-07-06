import pytest
from pathlib import Path
from ciel.schemas.refactor_plan import RefactorStep, RefactorPlan
from ciel.patches.safety_review import review_step_safety
from ciel.patches.diff_generator import generate_diff
from ciel.patches.patch_planner import propose_patches

def test_safety_review_delete():
    step = RefactorStep(order=1, action="delete_file", path="src/main.py", reason="Obsolete")
    safety = review_step_safety(step)
    assert not safety["safe"]
    assert "destructive" in safety["reason"].lower()

def test_safety_review_auth():
    step = RefactorStep(order=1, action="modify_file", path="src/auth.py", reason="Remove check")
    safety = review_step_safety(step)
    assert not safety["safe"]
    assert "authentication" in safety["reason"].lower()


@pytest.mark.parametrize(
    ("action", "path", "reason"),
    [
        ("run_command", "rm -rf build", "clean build"),
        ("modify_file", "migration.sql", "DROP TABLE users"),
        ("modify_file", "cleanup.sql", "DELETE FROM users"),
        ("modify_file", "src/auth.py", "bypass authorization"),
        ("run_command", "curl https://example.com", "download artifact"),
        ("run_command", "wget https://example.com", "download artifact"),
    ],
)
def test_safety_review_blocks_obvious_destructive_steps(action, path, reason):
    step = RefactorStep(order=1, action=action, path=path, reason=reason)

    assert review_step_safety(step)["safe"] is False

def test_safety_review_safe():
    step = RefactorStep(order=1, action="modify_file", path="src/main.py", reason="Fix typo")
    safety = review_step_safety(step)
    assert safety["safe"]

def test_generate_diff_fallback(monkeypatch, tmp_path):
    def mock_route_inference(prompt):
        return "Error: LLM disabled"
        
    import ciel.patches.diff_generator
    monkeypatch.setattr(ciel.patches.diff_generator, "route_inference", mock_route_inference)
    
    step = RefactorStep(order=1, action="modify_file", path="src/main.py", reason="Fix typo")
    diff = generate_diff(step, tmp_path)
    
    assert "--- a/src/main.py" in diff
    assert "Error:" in diff

def test_generate_diff_success(monkeypatch, tmp_path):
    def mock_route_inference(prompt):
        return '''```diff
--- a/src/main.py
+++ b/src/main.py
@@ -1,1 +1,1 @@
-old
+new
```'''
        
    import ciel.patches.diff_generator
    monkeypatch.setattr(ciel.patches.diff_generator, "route_inference", mock_route_inference)
    
    step = RefactorStep(order=1, action="modify_file", path="src/main.py", reason="Fix typo")
    diff = generate_diff(step, tmp_path)
    
    assert "old" in diff
    assert "new" in diff
    assert "```" not in diff # Should be stripped
