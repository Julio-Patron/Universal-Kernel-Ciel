from urllib.error import URLError
from importlib.metadata import version

import ciel
from ciel.config import CielSettings
from ciel.inference.cloud_inference_adapter import query_gemini
from ciel.inference.model_router import route_inference


def test_package_version_is_consistent():
    assert ciel.__version__ == "0.9.0"
    assert version("ciel-kernel") == ciel.__version__


def test_settings_load_all_byok_environment(monkeypatch):
    values = {
        "CIEL_LLM_PROVIDER": "cloud",
        "CIEL_OPENAI_API_KEY": "openai-secret",
        "CIEL_OPENAI_MODEL": "openai-model",
        "CIEL_ANTHROPIC_API_KEY": "anthropic-secret",
        "CIEL_ANTHROPIC_MODEL": "anthropic-model",
        "CIEL_GEMINI_API_KEY": "gemini-secret",
        "CIEL_GEMINI_MODEL": "gemini-model",
        "CIEL_DISABLE_LLM": "1",
        "CIEL_LLM_TIMEOUT": "42",
    }
    for name, value in values.items():
        monkeypatch.setenv(name, value)

    settings = CielSettings.from_env()

    assert settings.llm_provider == "cloud"
    assert settings.openai_api_key == "openai-secret"
    assert settings.openai_model == "openai-model"
    assert settings.anthropic_api_key == "anthropic-secret"
    assert settings.anthropic_model == "anthropic-model"
    assert settings.gemini_api_key == "gemini-secret"
    assert settings.gemini_model == "gemini-model"
    assert settings.disable_llm is True
    assert settings.llm_timeout_seconds == 42


def test_deterministic_mode_never_calls_inference(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("inference adapter should not be called")

    monkeypatch.setattr("ciel.inference.model_router.query_cloud", fail_if_called)
    monkeypatch.setattr("ciel.inference.model_router.query_ollama", fail_if_called)

    result = route_inference("prompt", settings=CielSettings(llm_provider="deterministic"))

    assert result.startswith("Error")
    assert "deterministic" in result


def test_local_router_uses_only_ollama(monkeypatch):
    monkeypatch.setattr(
        "ciel.inference.model_router.query_ollama",
        lambda prompt, settings: "local-result",
    )
    monkeypatch.setattr(
        "ciel.inference.model_router.query_cloud",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("cloud adapter should not be called")
        ),
    )

    result = route_inference("prompt", settings=CielSettings(llm_provider="local"))

    assert result == "local-result"


def test_cloud_router_uses_only_byok_adapter(monkeypatch):
    monkeypatch.setattr(
        "ciel.inference.model_router.query_cloud",
        lambda prompt, settings: "cloud-result",
    )
    monkeypatch.setattr(
        "ciel.inference.model_router.query_ollama",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("local adapter should not be called")
        ),
    )
    settings = CielSettings(llm_provider="cloud", openai_api_key="secret")

    assert route_inference("prompt", settings=settings) == "cloud-result"


def test_auto_router_prefers_cloud_and_local_fallback(monkeypatch):
    settings = CielSettings(llm_provider="auto", openai_api_key="secret")
    monkeypatch.setattr(
        "ciel.inference.model_router.query_cloud",
        lambda prompt, runtime: "Error connecting to cloud inference",
    )
    monkeypatch.setattr(
        "ciel.inference.model_router.query_ollama",
        lambda prompt, settings: "local-result",
    )

    assert route_inference("prompt", settings=settings) == "local-result"


def test_cloud_error_never_exposes_gemini_key(monkeypatch):
    secret = "super-secret-gemini-key"

    def fail_with_request_url(request, timeout):
        raise URLError(request.full_url)

    monkeypatch.setattr("urllib.request.urlopen", fail_with_request_url)
    result = query_gemini("prompt", CielSettings(gemini_api_key=secret))

    assert result.startswith("Error connecting to cloud inference (gemini)")
    assert secret not in result
