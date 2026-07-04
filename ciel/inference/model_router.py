from ciel.inference.local_inference_adapter import query_ollama

def route_inference(prompt: str, requires_cloud: bool = False) -> str:
    """Routes the inference request to the appropriate model (local first by default)."""
    if requires_cloud:
        # Placeholder for cloud router (e.g. Gemini, OpenAI)
        return "Cloud inference not yet configured."
    else:
        return query_ollama(prompt)
