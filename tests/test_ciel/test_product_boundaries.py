import pytest
from pathlib import Path
from ciel.skills.detect_product_boundaries import identify_boundaries

@pytest.fixture
def mock_monorepo(tmp_path):
    repo = tmp_path / "monorepo"
    repo.mkdir()
    
    # Frontend (React)
    frontend = repo / "apps" / "frontend-web"
    frontend.mkdir(parents=True)
    (frontend / "package.json").write_text('{"name": "frontend-web"}')
    
    # Backend (Python API)
    backend = repo / "services" / "backend-api"
    backend.mkdir(parents=True)
    (backend / "pyproject.toml").write_text('[tool.poetry]\nname = "backend-api"')
    
    # Infrastructure
    infra = repo / "deploy"
    infra.mkdir(parents=True)
    (infra / "Dockerfile").write_text('FROM python:3.9')
    
    return repo

def test_identify_boundaries_heuristic(mock_monorepo, monkeypatch):
    # Mock route_inference to avoid calling LLM during basic tests
    def mock_route_inference(prompt):
        return "[]" # Empty array forces fallback to heuristics
    
    import ciel.skills.detect_product_boundaries
    monkeypatch.setattr(ciel.skills.detect_product_boundaries, "route_inference", mock_route_inference)

    boundaries = identify_boundaries(mock_monorepo)
    
    assert len(boundaries) >= 3
    
    # Check frontend
    frontend_b = next((b for b in boundaries if b.id == "frontend-web"), None)
    assert frontend_b is not None
    assert frontend_b.language == "JavaScript/TypeScript"
    assert frontend_b.role == "frontend"
    assert "apps/frontend-web" in frontend_b.path
    
    # Check backend
    backend_b = next((b for b in boundaries if b.id == "backend-api"), None)
    assert backend_b is not None
    assert backend_b.language == "Python"
    assert backend_b.role == "backend"
    assert "services/backend-api" in backend_b.path
    
    # Check infrastructure
    infra_b = next((b for b in boundaries if b.id == "deploy"), None)
    assert infra_b is not None
    assert infra_b.language == "Dockerfile"
    assert infra_b.role == "infrastructure"
    assert "deploy" in infra_b.path
