# Changelog

All notable changes to this project will be documented here.

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
