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

## Provider Abstraction

The Brain communicates only through the Provider interface.

Concrete AI providers remain interchangeable implementations behind this abstraction.

Possible providers include:

- OpenAI
- Gemini
- Claude
- Ollama
- Local Models

This abstraction allows new providers to be introduced without modifying the Brain.

**Status:** Implemented

---

## Intelligent Provider Selection

The current implementation uses a default AI provider selected through configuration.

In future versions, ASTRALIS should determine the most appropriate provider for each request instead of relying solely on a predefined default.

Provider selection may consider:

- Task complexity
- Required capabilities (reasoning, vision, coding, etc.)
- Privacy requirements
- User preferences
- Provider availability
- Cost
- Latency
- Local versus cloud execution
- Model availability
- Automatic retries
- Fallback models

Users should always be able to override the selected provider when desired.

Until this capability is implemented, ASTRALIS falls back to the configured default provider.

Future implementations should transparently retry temporary provider failures and fall back to another compatible model or provider whenever practical.

Users should interact with ASTRALIS rather than managing provider availability themselves.

**Status:** Planned

**Reason:** Enables intelligent provider selection while preserving user autonomy.


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

## Context-Aware Reasoning

The Brain should eventually consider conversation history, user preferences, memory, and environmental context before generating a response.

Reasoning should not depend solely on the current request.

**Status:** Planned

**Reason:** Enables coherent long-term assistance and more personalized interactions.


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

## Conversation Window

The Conversation currently stores every message in the active session.

Future versions should support configurable context windows, summarization, and pruning to prevent unbounded conversation growth while preserving important context.

**Status:** Planned

---

## ASTRALIS Language Model

ASTRALIS currently relies on external language models through interchangeable providers.

Future versions should support one or more language models developed specifically for ASTRALIS while preserving the existing provider abstraction.

External providers should remain optional so users can choose the most appropriate language engine for their needs.

**Status:** Planned

**Reason:** Reduces dependency on external AI providers while preserving architectural flexibility.

---

## Context Awareness

ASTRALIS should eventually understand the user's current context before deciding how to assist.

Context may include:

- Current project
- Active application
- Conversation history
- User preferences
- Time and schedule
- Previous work

ASTRALIS should use context to provide relevant assistance without becoming intrusive.

**Status:** Planned

**Reason:** Enables proactive, context-aware assistance while respecting user autonomy and privacy.

---

## Provider Resilience

Language providers should remain resilient to temporary service failures.

Future implementations may include:

- Automatic retries
- Exponential backoff
- Model fallback
- Provider fallback
- Health monitoring
- Cached provider availability

ASTRALIS should recover from temporary provider failures whenever possible without requiring user intervention.

**Status:** Planned

**Reason:** Improves reliability while allowing users to interact with ASTRALIS instead of individual AI providers.

---


# Documentation Policy

Whenever a feature is intentionally postponed, evaluate whether it belongs in this document.

Only record items that would meaningfully affect the future architecture if forgotten.

This document should remain intentionally small and contain only significant architectural decisions that have been deliberately deferred.

---

Project: **ASTRALIS**

Current Release: **v0.2.0 "Brain Architecture"**

Current Milestone: **v0.3.0 "Capabilities"**

Philosophy: **Assist. Don't Control.**