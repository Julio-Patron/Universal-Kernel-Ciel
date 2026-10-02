import yaml
import hashlib
from pathlib import Path
from ciel_gate.policy.schema import Ruleset

def load_policy(yaml_path: Path | str) -> Ruleset:
    """Carga una política YAML, calcula su hash y la valida."""
    path = Path(yaml_path)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"No se encontró la política '{path}'")
        
    content = path.read_bytes()
    # Calcular SHA-256
    file_hash = hashlib.sha256(content).hexdigest()
    
    # Parsear YAML
    data = yaml.safe_load(content)
    if not isinstance(data, dict):
        raise ValueError(f"Formato YAML inválido en {path}")
        
    ruleset = Ruleset(**data)
    ruleset.hash = file_hash
    return ruleset
