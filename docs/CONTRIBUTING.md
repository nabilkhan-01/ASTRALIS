# Contributing to ASTRALIS

Thank you for contributing to ASTRALIS.

Please read this guide before making changes.

---

# Development Setup

## 1. Clone the repository

```bash
git clone <repository-url>
cd ASTRALIS
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

## 3. Activate the virtual environment

### Windows

```powershell
.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## 4. Install development dependencies

```bash
pip install -r requirements-dev.txt
```

---

# Quality Checks

Before every commit, run:

```bash
python scripts/check.py
```

This executes:

- Ruff
- MyPy
- Pytest

Every check must pass before code is committed.

---

# Architecture

ASTRALIS follows a modular architecture built around clearly separated responsibilities.

## Core Responsibilities

- Bootstrap constructs application dependencies.
- Application stores shared dependencies.
- Engine coordinates the application lifecycle.
- Request Pipeline coordinates request processing.
- Brain owns intelligence.
- Capability Manager executes capabilities.
- Capability Registry manages capability registration.
- Capabilities perform actions.
- Providers generate language.
- Memory manages persistent state.
- Storage provides persistence.
- Interfaces communicate with users.

Every component should have a single responsibility.

---

# Dependency Injection

Dependencies should be injected through constructors.

Prefer:

```python
class SearchCapability:
    def __init__(
        self,
        api: SearchApi,
    ) -> None:
        self.api = api
```

Avoid:

```python
class SearchCapability:
    def __init__(
        self,
    ) -> None:
        self.api = SearchApi()
```

Bootstrap is responsible for constructing shared dependencies.

---

# Coding Standards

- Follow PEP 8.
- Use Ruff for formatting and linting.
- Use MyPy type annotations.
- Public classes and methods should include docstrings.
- Keep functions focused on a single responsibility.
- Prefer composition over inheritance.
- Prefer explicit dependencies over global state.
- Keep modules independent.

---

# Error Handling

- Catch the most specific exception possible.
- Never silently ignore exceptions.
- Return meaningful error messages.
- Avoid broad `except Exception` unless absolutely necessary.

---

# Testing

Every new feature should include tests.

Tests should be:

- Independent
- Deterministic
- Fast
- Readable

Run tests with:

```bash
pytest -v
```

---

# Documentation

Whenever behavior or architecture changes:

- Update relevant documentation.
- Keep architectural diagrams synchronized with the implementation.
- Update the CHANGELOG for user-visible changes.

Documentation should always describe the current implementation.

---

# Pull Requests

Before opening a pull request, ensure:

- All quality checks pass.
- All tests pass.
- Documentation has been updated where necessary.
- CHANGELOG.md has been updated for user-facing changes.

---

# Design Principles

ASTRALIS is built around these engineering principles:

- Single Responsibility Principle
- Dependency Injection
- Composition over Inheritance
- Low Coupling
- High Cohesion
- Modularity
- Extensibility
- Testability
- Interface Independence
- User Autonomy

---

# Philosophy

ASTRALIS is built around one guiding principle:

> **Assist. Don't Control.**

Every contribution should prioritize simplicity, transparency, reliability, and respect for user autonomy.