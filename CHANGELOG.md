# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `/health/` and `/readiness/` endpoints (the latter checks DB connectivity when `STATE_BACKEND=sqlite`).
- Structured (JSON) logging via loguru when `DEBUG=False`.
- mypy typechecking and `pip-audit` dependency scanning in CI.
- `docker-compose.yml`.
- Hash-locked lockfiles (`pip-compile --generate-hashes`); CI now installs with `--require-hashes`.

### Fixed
- `webhook()`'s exception handler referenced `form_data` before it was guaranteed to be assigned, raising a fresh `NameError` instead of the intended fallback response if `await request.form()` itself failed.
- Every webhook request logged *all* users' stored conversation state (`state.get_all()`), not just the current sender's - a per-request unbounded read and a PII leak into logs. Now logs only the current sender's state.
- `logger.critical` was used for routine intent-detection logging and for an ordinary Twilio delivery failure (the latter also logging the full message body) - both downgraded, the message body dropped from the log line.
- `requirements.txt` pinned `SQLAlchemy==2.0.40`, which has no wheel for the Python version this project targets and failed to install from a fresh clone.
- `model.py`'s untyped `declarative_base()`/`Column()` style masked several real type errors in `state.py` once mypy was added; migrated to SQLAlchemy 2.0's typed `DeclarativeBase`/`Mapped`/`mapped_column`.
- `BaseState.get_all`'s abstract signature declared `-> None` while both implementations return `dict`.
- `tests/test_main.py`'s `test_read_root` didn't call the app at all (just asserted `1 + 1 == 2`); replaced with a real test of `GET /`.

## [0.1.0] - 2026-09-03

Initial tagged release.

### Added
- FastAPI backend with a Twilio WhatsApp `/webhook/` endpoint and `/status-callback/` for delivery status.
- Pattern-matching intent detection (greeting, goodbye, reset, unknown) with pluggable intent handlers.
- Conversational state, backed by either an in-memory store or SQLite (`STATE_BACKEND`).
- CI (pytest, flake8), Dependabot, and Docker support.
