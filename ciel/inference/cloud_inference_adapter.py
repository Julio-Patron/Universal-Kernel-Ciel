import json
import urllib.request
from typing import Optional

from ciel.config import CielSettings

def _handle_error(exc: Exception, provider: str) -> str:
    # Exception messages from HTTP clients may contain request URLs. Gemini
    # authenticates in its query string, so returning/logging the raw message
    # could expose the caller's API key.
    return (
        f"Error connecting to cloud inference ({provider}): "
        f"request failed ({type(exc).__name__})"
    )

def query_openai(prompt: str, settings: CielSettings) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": settings.openai_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.openai_api_key}"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=settings.llm_timeout_seconds) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except Exception as exc:
        return _handle_error(exc, "openai")

def query_anthropic(prompt: str, settings: CielSettings) -> str:
    url = "https://api.anthropic.com/v1/messages"
    payload = {
        "model": settings.anthropic_model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
        "temperature": 0.0
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": settings.anthropic_api_key,
            "anthropic-version": "2023-06-01"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=settings.llm_timeout_seconds) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["content"][0]["text"]
    except Exception as exc:
        return _handle_error(exc, "anthropic")

def query_gemini(prompt: str, settings: CielSettings) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:generateContent?key={settings.gemini_api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.0}
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=settings.llm_timeout_seconds) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as exc:
        return _handle_error(exc, "gemini")

def query_cloud(prompt: str, settings: CielSettings) -> str:
    if settings.openai_api_key:
        return query_openai(prompt, settings)
    elif settings.anthropic_api_key:
        return query_anthropic(prompt, settings)
    elif settings.gemini_api_key:
        return query_gemini(prompt, settings)
    return "Error connecting to cloud inference: No API keys configured."
