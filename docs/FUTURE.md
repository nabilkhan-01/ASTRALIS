# ASTRALIS Future Decisions

This document records architectural decisions that have been intentionally deferred.

These are **not bugs** or **technical debt**.

They represent improvements or capabilities that will be implemented when the project reaches the appropriate stage.

Following the principle:

> **Simple today. Extensible tomorrow.**

---

# Engine

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

# Brain

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

Users should always be able to override the selected provider when desired.

Until this capability is implemented, ASTRALIS falls back to the configured default provider.

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

# Storage

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

## Context-Aware Assistance

ASTRALIS should eventually understand and use relevant context before deciding how to assist the user.

Context may include:

- Conversation history
- Long-term memory
- User preferences
- Current project
- Active application
- Time and schedule
- Previous work
- Environmental context

This context should improve reasoning, planning, and recommendations without becoming intrusive or reducing user autonomy.

Reasoning should not depend solely on the current request, but on the broader context available to ASTRALIS.

**Status:** Planned

**Reason:** Enables more coherent, personalized, and context-aware assistance while preserving user privacy, transparency, and control.

## Explainability

ASTRALIS should be able to explain significant decisions and recommendations.

Users should understand:

- Why an action was suggested.
- Which information influenced the decision.
- Any assumptions made.

**Status:** Planned

**Reason:** Supports transparency and trust.

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

Future shared abstractions should only be introduced after repeated implementation patterns emerge.

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

# Documentation Policy

Whenever a feature is intentionally postponed, evaluate whether it belongs in this document.

Only record items that would meaningfully affect the future architecture if forgotten.

This document should remain intentionally small and contain only significant architectural decisions that have been deliberately deferred.

---

## Plugin Framework

Capabilities should eventually support external plugins without requiring modifications to the core application.

Plugins should be:

- Discoverable
- Independently installable
- Sandboxed when practical
- Explicitly enabled by users

Status: Planned

Reason: Enables ecosystem growth while preserving modularity.

---

Project: **ASTRALIS**

Current Release: **v0.3.1 – Engineering Stability**

Current Milestone: **v0.4.0 "Memory"**

Philosophy: **Assist. Don't Control.**