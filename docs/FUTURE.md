# ASTRALIS Future Decisions

This document records architectural decisions that have been intentionally deferred.

These are **not bugs** or **technical debt**.

They represent improvements or capabilities that will be implemented when the project reaches the appropriate stage.

Following the principle:

> **Simple today. Extensible tomorrow.**

---

# Core

## Lifecycle Manager

### Validate Lifecycle Transitions

Current implementation allows any lifecycle transition.

Future versions should validate transitions such as:

- STOPPED → INITIALIZING ✅
- INITIALIZING → RUNNING ✅
- RUNNING → STOPPING ✅
- STOPPING → STOPPED ✅

Invalid transitions should be rejected.

**Status:** Deferred

**Reason:** The current implementation is intentionally simple.

---

## Engine

### Core Service Initialization

As additional core services are introduced, Engine initialization may eventually be extracted into dedicated helper methods to improve readability.

This refactoring should occur only when it meaningfully improves maintainability.

**Status:** Deferred

---

## Health System

Differentiate between:

- Required core services
- Optional modules

Startup should abort only when required services fail.

Optional modules may fail without preventing application startup.

**Status:** Planned

---

# Module System

## Configuration-Based Module Loading

The current Module Loader initializes modules directly.

Future versions should support enabling or disabling modules through configuration.

Example:

```yaml
modules:
  brain: true
  memory: true
  vision: false
```

**Status:** Deferred

**Reason:** There are currently no optional application modules.

---

## Plugin Discovery

Future versions should automatically discover available plugins.

Discovery should remain separate from activation.

**Status:** Deferred

---

## User-Controlled Plugin Activation

Discovered plugins should never be activated automatically.

Users must explicitly enable new capabilities.

This supports the project philosophy:

> **Assist. Don't Control.**

**Status:** Deferred

---

# Brain

## Provider Independence

Introduce an abstraction layer between the Brain and AI providers.

Future providers may include:

- OpenAI
- Gemini
- Claude
- Ollama
- Local Models

The Brain should communicate only with the provider interface.

**Status:** Planned

---

## Response Model Expansion

The initial Response model intentionally remains minimal.

Future versions may include:

- Tool results
- Suggested actions
- Attachments
- Explanations
- Metadata

These additions should only be introduced when required by real functionality.

**Status:** Deferred

---

## Shared Data Models

Request and Response currently belong to the Brain module.

If these models become shared across multiple modules, they may be extracted into a common package.

This decision should only be made when the models become genuinely shared.

**Status:** Deferred

**Reason:** Avoid introducing shared abstractions before they are necessary.

---

# Memory

## Memory Independence

Memory is responsible for deciding what should be remembered.

Storage is responsible only for persistence.

The Brain should never write directly to storage.

**Status:** Planned

**Reason:** Maintains separation between reasoning, memory, and persistence.

---

# Storage

## Storage Abstraction

Introduce a dedicated storage layer that separates persistence technology from application logic.

Possible implementations may include:

- SQLite
- PostgreSQL
- JSON
- Cloud storage

Other components should communicate only with the storage interface.

**Status:** Planned

---

# Security

## Permission System

Every action capable of changing user data or interacting with external systems should pass through a centralized Permission Manager.

Examples:

- File deletion
- Sending emails
- Running terminal commands
- Browser automation
- Cloud synchronization

**Status:** Planned

**Reason:** Required to preserve user autonomy.

---

# Intelligence

## Explainability

ASTRALIS should be able to explain significant decisions and recommendations.

Users should understand:

- Why an action was suggested.
- Which information influenced the decision.
- Any assumptions made.

**Status:** Planned

**Reason:** Supports transparency and trust.

---

## Local-First Design

Whenever practical, ASTRALIS should process and store information locally before relying on cloud services.

Cloud providers should remain optional rather than mandatory.

**Status:** Planned

**Reason:** Improves privacy, reliability, and user control.

---

# Documentation Policy

Whenever a feature is intentionally postponed, evaluate whether it belongs in this document.

Only record items that would meaningfully affect the future architecture if forgotten.

This document should remain intentionally small and contain only significant architectural decisions that have been deliberately deferred.

---

Project: **ASTRALIS**

Current Release: **v0.1.0 "Foundation"**

Current Milestone: **v0.2.0 "Brain Architecture"**

Philosophy: **Assist. Don't Control.**