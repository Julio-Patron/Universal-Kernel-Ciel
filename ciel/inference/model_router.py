from typing import Optional

from ciel.config import CielSettings
from ciel.inference.local_inference_adapter import query_ollama


def route_inference(
    prompt: str,
    requires_cloud: bool = False,
    settings: Optional[CielSettings] = None,
) -> str:
    """Route inference requests.

    Ciel is local-first. Cloud routing is deliberately not implicit because a
    production tool must not send repository content to remote providers without
    explicit configuration and user consent.
    """
    if requires_cloud:
        return "Cloud inference is not configured. Use local Ollama or disable LLM mode."
    return query_ollama(prompt, settings=settings)
