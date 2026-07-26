# Contributing to ASTRALIS

Thank you for contributing to ASTRALIS.

## Development Setup

1. Clone the repository.

2. Create a virtual environment.

```bash
python -m venv .venv
```

3. Activate the virtual environment.

### Windows

```powershell
.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source .venv/bin/activate
```

4. Install development dependencies.

```bash
pip install -r requirements-dev.txt
```

---

## Before Every Commit

Run the project quality checks.

```bash
python scripts/check.py
```

This verifies:

- Ruff
- MyPy
- Pytest

All checks must pass before committing changes.

---

## Project Architecture

Follow these architectural principles.

- Bootstrap owns object creation.
- Engine coordinates the application lifecycle.
- Capabilities implement application features.
- Memory stores and retrieves data.
- Providers communicate with external AI services.
- Tools perform system-level operations.
- Models are immutable data objects whenever possible.

---

## Coding Standards

- Follow PEP 8.
- Format and lint using Ruff.
- Public classes and methods should include docstrings.
- Prefer dependency injection over creating dependencies inside classes.
- Prefer composition over inheritance.
- Keep functions focused on a single responsibility.
- Avoid global state.

---

## Error Handling

- Never use broad `except Exception` unless there is a strong reason.
- Catch the most specific exception possible.
- Return meaningful error messages.
- Do not silently ignore errors.

---

## Testing

Every new feature should include appropriate tests.

Run tests with:

```bash
pytest -v
```

---

## Pull Requests

Before opening a pull request, ensure:

- All quality checks pass.
- Tests pass.
- Documentation is updated when behavior changes.
- CHANGELOG.md is updated for user-facing changes.

---

## Project Philosophy

ASTRALIS is built around one core principle:

> **Assist. Don't Control.**

Every feature should respect user autonomy, remain transparent, and prioritize reliability over unnecessary complexity.