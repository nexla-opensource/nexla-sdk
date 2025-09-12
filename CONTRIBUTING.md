Contributing to nexla-sdk
=========================

Thanks for your interest in contributing!

Setup
- Python 3.8+ is required.
- Install dev deps: `pip install -e .[dev]`
- Run unit tests: `pytest -m unit`

Coding standards
- Pydantic v2 models.
- Keep public API stable; deprecate before breaking.
- Run pre-commit: `pre-commit install` then commit.

Testing
- Prefer unit tests with mocks.
- Avoid network in unit tests.
- Add integration tests only when necessary.

Release
- Versions are driven by setuptools_scm.
- Update CHANGELOG.md and docs for user-facing changes.

