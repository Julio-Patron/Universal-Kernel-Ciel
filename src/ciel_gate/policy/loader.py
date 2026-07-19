import yaml
import hashlib
from pathlib import Path
from ciel_gate.policy.schema import Ruleset

def load_ruleset(ruleset_id: str, search_paths: list[Path] = None) -> Ruleset:
    """Carga un ruleset YAML, calcula su hash y lo valida."""
    if not search_paths:
        # Default to current dir rulesets folder and kernel default rulesets
        search_paths = [Path.cwd() / "rulesets"]
        
    for base_path in search_paths:
        yaml_path = base_path / f"{ruleset_id}.yaml"
        if yaml_path.exists() and yaml_path.is_file():
            content = yaml_path.read_bytes()
            # Calcular SHA-256
            file_hash = hashlib.sha256(content).hexdigest()
            
            # Parsear YAML
            data = yaml.safe_load(content)
            if not isinstance(data, dict):
                raise ValueError(f"Formato YAML inválido en {yaml_path}")
                
            ruleset = Ruleset(**data)
            ruleset.hash = file_hash
            return ruleset
            
    raise FileNotFoundError(f"No se encontró el ruleset '{ruleset_id}.yaml' en las rutas configuradas.")
