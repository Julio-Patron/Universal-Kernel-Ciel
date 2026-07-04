import json
from pathlib import Path
from datetime import datetime
from ciel.schemas.gap_report import ImplementationGapReport

def write_project_profile(report: ImplementationGapReport, memory_dir: Path):
    """Writes the project profile snapshot to the memory directory."""
    profiles_dir = memory_dir / "project_profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)
    
    # Simple sanitized filename
    safe_name = report.project.name.replace(" ", "_").replace("/", "_").replace("\\", "_")
    profile_path = profiles_dir / f"{safe_name}.json"
    
    profile_data = {
        "last_analyzed": datetime.now().isoformat(),
        "stage": report.verdict.stage,
        "bottleneck": report.verdict.main_bottleneck,
        "maturity_scores": report.maturity_score.model_dump()
    }
    
    profile_path.write_text(json.dumps(profile_data, indent=2), encoding="utf-8")
