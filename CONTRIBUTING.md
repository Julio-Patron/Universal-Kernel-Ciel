# Contributing

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Test locally

```bash
CIEL_DISABLE_LLM=1 CIEL_ENABLE_EXEC=0 python -m pytest
python -m build
python -m twine check dist/*
```

## Quality rules

- Keep the CLI usable without Ollama by preserving deterministic fallbacks.
- Do not enable shell execution by default.
- Every release-facing claim must be backed by implementation evidence and tests.
- Keep schemas stable or document schema version changes.
