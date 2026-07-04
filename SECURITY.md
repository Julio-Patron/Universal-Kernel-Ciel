# Security Policy

## Supported versions

Only the latest commit on `master` and active release-candidate branches are supported.

## Reporting issues

Open a private security advisory or contact the maintainer directly. Do not publish exploit details in a public issue before a fix is available.

## Current security posture

- Command execution is disabled by default.
- Local inference is local-first and can be disabled with `CIEL_DISABLE_LLM=1`.
- No repository content is sent to cloud providers by default.
- Local runtime files such as ledgers, keys, and analysis output are ignored by Git.
