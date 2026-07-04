import json
import urllib.request
from typing import Optional

from ciel.config import CielSettings


def query_ollama(prompt: str, model: Optional[str] = None, settings: Optional[CielSettings] = None) -> str:
    """Query a configured local Ollama instance.

    The function returns an explicit error string instead of raising so callers
    can fall back to deterministic parsers without requiring Ollama in CI.
    """
    runtime = settings or CielSettings.from_env()
    if runtime.disable_llm:
        return "Error connecting to local inference: disabled by CIEL_DISABLE_LLM"

    url = f"{runtime.ollama_url}/api/generate"
    payload = {
        "model": model or runtime.ollama_model,
        "prompt": prompt,
        "stream": False,
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=runtime.llm_timeout_seconds) as response:
            result = json.loads(response.read().decode())
            return result.get("response", "")
    except Exception as exc:
        return f"Error connecting to local inference: {exc}"
