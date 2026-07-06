# Changelog

All notable changes to this project will be documented here.

## 0.9.0 - 2026-07-05

### Added

- Optional BYOK cloud inference adapters for OpenAI, Anthropic, and Gemini.
- Model routing modes for `auto`, `local`, `cloud`, and `deterministic` execution.
- Append-only decision ledger with hash-chain verification.
- Memory CLI commands: `memory init`, `memory status`, and `memory verify`.
- Multi-product boundary detection for mixed-language monorepositories.
- Versioned YAML policy rulesets and CLI ruleset selection.
- Auto-refactor planning with deterministic fallback plans.
- Safe patch proposal workflow with destructive-operation review and no automatic apply.
- Tag-triggered PyPI trusted-publishing workflow.

### Changed

- Consolidated CI into one test/build workflow with Python 3.10 and 3.11 coverage gates.
- Hardened cloud error handling so provider credentials cannot appear in returned errors.
- Aligned package and ledger metadata with the `0.9.0` Safe Patch Generation milestone.

### Removed

- Tracked local runtime decision ledger at `.ciel/decisions.log`.

## 0.3.0 - 2026-07-04

### Added

- Central runtime configuration through `ciel.config.CielSettings`.
- Offline CI mode with `CIEL_DISABLE_LLM=1`.
- Distribution build validation using `python -m build` and `twine check`.
- Focused hardening tests for static evidence extraction, gap matching, maturity scoring, and shell safety.
- License declaration and release support documents.

### Changed

- Local Ollama calls now use environment-configured URL, model, and timeout.
- Gap fallback now matches claims to specific fact IDs instead of attaching every fact to every claim.
- Maturity fallback now derives scores from evidence counts, tests, and operational manifests.
- Shell executor is opt-in, allowlisted, timeout-bound, and does not invoke a system shell.

### Removed

- Stale intelligence test expectations that assumed the old optimistic fallback behavior.
