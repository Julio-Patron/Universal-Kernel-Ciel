from pathlib import Path
from typing import List, Dict, Optional
import json

from ciel.schemas.product_boundary import ProductBoundary
from ciel.inference.model_router import route_inference

def identify_boundaries(repo_path: Path) -> List[ProductBoundary]:
    """Identifies potential product boundaries or sub-projects within a monorepo."""
    boundaries = []
    
    if not repo_path.is_dir():
        return boundaries
        
    markers = {
        "package.json": ("JavaScript/TypeScript", None),
        "Cargo.toml": ("Rust", None),
        "pyproject.toml": ("Python", None),
        "requirements.txt": ("Python", None),
        "go.mod": ("Go", None),
        "pom.xml": ("Java", "Maven"),
        "build.gradle": ("Java", "Gradle"),
        "Dockerfile": ("Dockerfile", "Docker")
    }
    
    found_markers = []
    for path in repo_path.rglob("*"):
        if not path.is_file():
            continue
        # Ignorar directorios comunes que no son boundaries per se
        if any(part in {".git", "node_modules", "venv", ".venv", "dist", "build"} for part in path.parts):
            continue
            
        if path.name in markers:
            try:
                rel_path = path.parent.relative_to(repo_path)
                rel_path_str = str(rel_path).replace("\\", "/")
                
                if rel_path_str == ".":
                    rel_path_str = "/"
                    id_name = "root"
                else:
                    id_name = rel_path.name
                
                lang, framework = markers[path.name]
                found_markers.append({
                    "id": id_name,
                    "path": rel_path_str,
                    "language": lang,
                    "framework": framework,
                    "marker": path.name
                })
            except ValueError:
                pass

    boundary_map = {}
    for fm in found_markers:
        bpath = fm["path"]
        if bpath not in boundary_map:
            boundary_map[bpath] = {
                "id": fm["id"],
                "path": fm["path"],
                "language": fm["language"],
                "framework": fm["framework"],
                "role": "unknown"
            }
        else:
            if fm["marker"] == "Dockerfile":
                boundary_map[bpath]["role"] = "infrastructure"
            if not boundary_map[bpath]["framework"] and fm["framework"]:
                boundary_map[bpath]["framework"] = fm["framework"]

    if boundary_map:
        prompt = f"""
        Analyze the following detected project directories in a repository and assign a role (e.g. frontend, backend, sdk, docs, infrastructure, app, library) and refine the framework if possible.
        Return ONLY a JSON array of objects with keys: path, role, framework.
        Do not include markdown blocks, just the raw JSON array.
        Detected: {json.dumps(list(boundary_map.values()))}
        """
        response = route_inference(prompt)
        
        try:
            clean_resp = response.strip()
            if clean_resp.startswith("```json"):
                clean_resp = clean_resp[7:]
            elif clean_resp.startswith("```"):
                clean_resp = clean_resp[3:]
            if clean_resp.endswith("```"):
                clean_resp = clean_resp[:-3]
                
            inferred = json.loads(clean_resp.strip())
            for item in inferred:
                bpath = item.get("path")
                if bpath in boundary_map:
                    if item.get("role"):
                        boundary_map[bpath]["role"] = item.get("role")
                    if item.get("framework"):
                        boundary_map[bpath]["framework"] = item.get("framework")
        except Exception:
            pass

    for bpath, data in boundary_map.items():
        if data["role"] == "unknown":
            low_id = data["id"].lower()
            if "front" in low_id or "ui" in low_id or "web" in low_id:
                data["role"] = "frontend"
            elif "back" in low_id or "api" in low_id or "server" in low_id:
                data["role"] = "backend"
            elif "doc" in low_id:
                data["role"] = "docs"
            elif "infra" in low_id or "deploy" in low_id:
                data["role"] = "infrastructure"
            else:
                data["role"] = "component"

    for data in boundary_map.values():
        boundaries.append(ProductBoundary(**data))
        
    return boundaries
