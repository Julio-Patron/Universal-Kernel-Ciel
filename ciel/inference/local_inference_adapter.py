import json
import urllib.request
from typing import Dict, Any

def query_ollama(prompt: str, model: str = "llama3") -> str:
    """Queries a local Ollama instance for offline inference."""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            return result.get("response", "")
    except Exception as e:
        return f"Error connecting to local inference: {e}"
