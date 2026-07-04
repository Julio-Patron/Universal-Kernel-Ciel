from typing import Optional

from ciel.config import CielSettings
from ciel.inference.local_inference_adapter import query_ollama
from ciel.inference.cloud_inference_adapter import query_cloud

def route_inference(
    prompt: str,
    requires_cloud: bool = False,
    settings: Optional[CielSettings] = None,
) -> str:
    """Route inference requests based on configured provider (auto, cloud, local, deterministic)."""
    runtime = settings or CielSettings.from_env()
    
    if runtime.disable_llm:
        return "Error connecting to inference: disabled by CIEL_DISABLE_LLM"
        
    mode = runtime.llm_provider
    has_cloud_keys = any([runtime.openai_api_key, runtime.anthropic_api_key, runtime.gemini_api_key])
    
    if requires_cloud and mode not in ("cloud", "auto"):
        return "Cloud inference is not configured. Use local Ollama or disable LLM mode."
        
    if mode == "deterministic":
        return "Error connecting to inference: deterministic mode enforced"
        
    elif mode == "cloud":
        if has_cloud_keys:
            return query_cloud(prompt, runtime)
        return "Error connecting to cloud inference: No API keys configured."
        
    elif mode == "local":
        return query_ollama(prompt, settings=runtime)
        
    else:  # mode == "auto" (default)
        if has_cloud_keys:
            result = query_cloud(prompt, runtime)
            if not result.startswith("Error"):
                return result
        # Fallback to local Ollama if cloud fails or has no keys
        return query_ollama(prompt, settings=runtime)
