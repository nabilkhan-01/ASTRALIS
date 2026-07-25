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

## Brain Processing Pipeline

The Brain currently executes a linear request processing pipeline.

Future versions may introduce additional processing stages such as:

- Authorization
- Memory retrieval
- Context enrichment
- Reasoning
- Post-processing
- Memory persistence

The overall pipeline structure should remain sequential to preserve readability and simplify debugging.

**Status:** Planned

**Reason:** Enables future intelligence while preserving the existing architecture.


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

Future provider implementations should remain isolated from application logic so that changing providers never requires modifications to the Brain or Capabilities.

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

Memory components should never depend on Capabilities, Brain, Providers, or Tools.

Memory is responsible for managing application data.

User interaction and reasoning belong to higher layers.

**Status:** Planned

**Reason:** Preserves architectural independence and simplifies future storage migration.

---

# Capability Layer

## Capability Independence

Capabilities should execute user requests but should not directly coordinate other capabilities.

Cross-capability workflows belong to higher orchestration layers such as the Brain or future Automation services.

**Status:** Planned

**Reason:** Maintains loose coupling and simplifies testing.

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

## Stable Entity Identity

The current JSON-based implementation uses sequential identifiers for user-facing collections.

When ASTRALIS migrates to a database (such as PostgreSQL), persistent entities should use stable internal identifiers that are never renumbered or reused.

User-facing numbering should remain presentation logic rather than persistent storage.

Examples include:

- Notes
- Calendar Events
- Alarms
- Future Goals
- Projects
- Tasks

This separation preserves relationships between entities while maintaining a simple user experience.

**Status:** Planned

**Reason:** Supports relational storage, future knowledge graphs, and long-term data integrity.

## PostgreSQL Migration

JSON storage is intentionally used during early development to simplify implementation.

Future versions should migrate persistent application data to PostgreSQL through the Storage abstraction.

The migration should occur without requiring changes to higher application layers.

Potential benefits include:

- Transactions
- Relationships
- Efficient querying
- Indexing
- Concurrent access
- Future synchronization

**Status:** Planned

**Reason:** Provides a scalable persistence layer while preserving architectural separation.

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

# Automation

## Background Scheduler

Future versions should introduce a scheduler responsible for executing time-based automation.

Examples include:

- Alarms
- Reminders
- Scheduled tasks
- Recurring jobs

Capabilities should manage user data only.

Execution should remain the responsibility of the Automation layer.

**Status:** Planned

**Reason:** Separates user interaction from background execution.

---

# Engineering

## Shared Base Components

As the number of Memory and Capability implementations grows, common behavior may be extracted into shared base classes.

Possible candidates include:

- BaseMemory
- Shared capability helpers
- Shared validation helpers

These abstractions should only be introduced after repeated patterns have clearly emerged.

**Status:** Deferred

**Reason:** Avoids premature abstraction while reducing future duplication.

## Service Layer

Future versions may introduce a dedicated Services layer for long-running or application-wide business logic.

Examples include:

- Scheduler
- Notification Service
- Knowledge Graph
- Embedding Service
- Summarization

Services differ from Capabilities in that they are not directly invoked by users.

**Status:** Deferred

**Reason:** Preserves clear architectural boundaries as the project grows.

---

## Bootstrap Layer

As the number of core services and capabilities grows, application initialization may be extracted into dedicated bootstrap modules.

Examples include:

- Capability registration
- Provider initialization
- Service initialization
- Interface initialization

The Engine should remain responsible for application lifecycle rather than detailed construction of every component.

**Status:** Deferred

**Reason:** Keeps the Engine focused on orchestration while maintaining readability as the project grows.

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