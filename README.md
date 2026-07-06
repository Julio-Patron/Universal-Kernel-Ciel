# Ciel Kernel 🧠⚙️

[![CI](https://github.com/JPatronC92/universal-ai-kernel/actions/workflows/ci.yml/badge.svg)](https://github.com/JPatronC92/universal-ai-kernel/actions/workflows/ci.yml)

Ciel Kernel is a local-first repository audit CLI for comparing documented intent against code reality. It scans a repository, classifies files, extracts implementation evidence, detects gaps, and emits structured reports.

Local or cloud inference can improve semantic extraction when available, but deterministic fallbacks are part of the core contract. Cloud inference is optional and uses bring-your-own-key (BYOK) credentials.

## Features

- Purpose resolution from prompts and repository documentation.
- Evidence extraction from source code and project metadata.
- Gap detection with specific evidence IDs.
- Repository maturity scoring based on claims, implementation evidence, tests, and operational manifests.
- Multi-product boundary detection for monorepos.
- Policy Rulesets enforcement (YAML based governance).
- Automated Safe Patch Generation and step-by-step refactoring plans.
- Offline-safe fallback mode for CI and machines without Ollama.

## Install before the PyPI release

```bash
pip install -e .
```

After `v0.9.0` is published to PyPI, installation will be:

```bash
pip install ciel-kernel
```

## Run

```bash
ciel analyze ./path/to/repo
ciel analyze ./path/to/repo --scope frontend --ruleset release-readiness
ciel boundaries ./path/to/repo
ciel report ./path/to/repo --format markdown
ciel gap ./path/to/repo
ciel sources ./path/to/repo
ciel purpose "audit this repo for release readiness"
ciel plan-refactor ./path/to/repo --gap <id>
ciel propose-patch ./path/to/repo --gap <id>
ciel memory init ./path/to/repo
ciel memory status ./path/to/repo
ciel memory verify ./path/to/repo
```

## Runtime configuration

```bash
CIEL_OLLAMA_URL=http://localhost:11434
CIEL_OLLAMA_MODEL=llama3
CIEL_LLM_PROVIDER=auto
CIEL_LLM_TIMEOUT=10
CIEL_DISABLE_LLM=0
CIEL_OPENAI_API_KEY=
CIEL_OPENAI_MODEL=gpt-4o-mini
CIEL_ANTHROPIC_API_KEY=
CIEL_ANTHROPIC_MODEL=claude-3-5-haiku-latest
CIEL_GEMINI_API_KEY=
CIEL_GEMINI_MODEL=gemini-1.5-flash
CIEL_ENABLE_EXEC=0
CIEL_EXEC_TIMEOUT=30
```

`CIEL_LLM_PROVIDER` accepts `auto`, `local`, `cloud`, or `deterministic`. In `auto` mode, configured cloud credentials are tried before local Ollama. API keys remain runtime-only and are not written to reports or the decision ledger.

Deterministic/offline CI does not require Ollama or API keys:

```bash
CIEL_DISABLE_LLM=1 CIEL_ENABLE_EXEC=0 python -m pytest
```

## Core structure

- `ciel/cli/`: Typer CLI entrypoints.
- `ciel/rag/`: repository scanning and evidence extraction.
- `ciel/orchestrator/`: purpose and reasoning orchestration.
- `ciel/skills/`: gap detection, maturity audit, product boundary detection, and planning helpers.
- `ciel/schemas/`: Pydantic schemas for purpose, evidence, and reports.
- `ciel/inference/`: local and optional BYOK cloud inference adapters.
- `ciel/executor/`: approval-gated command and filesystem helpers.
- `ciel/patches/`: safe diff generation and step validation logic.
