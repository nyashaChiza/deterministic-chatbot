# Contributing

## Setup

```bash
pip install -r requirements-dev.txt
cp .env.example .env
```

## Before opening a PR

Run the test suite, linter, and typechecker, and make sure all three are clean:

```bash
pytest
flake8 .
mypy src/ main.py
```

CI (`.github/workflows/python-app.yml`) runs the same checks, plus `pip-audit`, on every push and PR.

## Commit style

- Keep each commit focused on one change, with the tests that pin its behavior included in the same commit.
- Avoid bundling unrelated formatting, refactors, and features together.

## Updating dependencies

`requirements.txt` and `requirements-dev.txt` are compiled from `requirements.in` and `requirements-dev.in` via [pip-tools](https://pypi.org/project/pip-tools/) - see [Dependency updates](README.md#dependency-updates) in the README.
