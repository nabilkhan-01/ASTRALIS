# ASTRALIS Future Decisions

This document records architectural decisions that have been intentionally deferred.

These are **not bugs** or **technical debt**.

They represent architectural improvements that should be implemented when the project reaches the appropriate stage.

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

Future versions should determine the most appropriate provider for each request rather than relying solely on a predefined default.

Provider selection may consider:

- Task complexity
- Required capabilities
- Privacy requirements
- User preferences
- Provider availability
- Cost
- Latency
- Local versus cloud execution
- Model availability

Users should always be able to override the selected provider.

**Status:** Planned

**Reason:** Improves flexibility while preserving user autonomy.

---

## Response Model Expansion

The current Response model intentionally remains minimal.

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

If these models become shared across multiple subsystems, they may be extracted into a common package.

This should only occur when they become genuinely shared.

**Status:** Deferred

**Reason:** Avoids premature abstraction.

---

## BrainContext Evolution

BrainContext currently carries the information required by the Brain for request processing.

Future versions may extend BrainContext with additional contextual information such as:

- Working Memory
- Active Project
- Vision Context
- Environmental Context
- User Context

The Brain's public API should evolve by extending BrainContext rather than expanding the `Brain.process()` method signature.

**Status:** Planned

**Reason:** Preserves a stable Brain interface while allowing contextual reasoning to evolve.

---

# Memory

## Working and Long-Term Memory

Memory should eventually consist of two distinct layers.

### Working Memory

Temporary information used while reasoning.

Examples include:

- Current conversation
- Active project
- Current task
- Recently referenced information

Working memory should naturally expire as context changes.

### Long-Term Memory

Persistent information that remains useful across conversations.

Examples include:

- User preferences
- Projects
- Goals
- Frequently used technologies
- Important relationships
- Personal profile

Long-term memory should remain user-visible and user-editable.

**Status:** Planned

**Reason:** Mirrors natural human memory while preserving user control.

---

## Memory Policy

The Brain should identify observations but should not directly decide what becomes long-term memory.

Future versions should introduce a Memory Policy responsible for determining whether information should be:

- Ignored
- Remembered
- Updated
- Strengthened
- Forgotten

The policy may consider:

- Frequency
- Confidence
- Importance
- User feedback
- Recency
- Explicit user instructions

The Brain should emit observations.

The Memory Policy should decide what is ultimately stored.

**Status:** Planned

**Reason:** Separates reasoning from persistence while enabling intelligent long-term learning.

---

# Storage

## Stable Entity Identity

Persistent entities should use stable internal identifiers that never change.

Future implementations should migrate from human-readable identifiers to generated UUIDs to support:

- Relationships
- Synchronization
- Database storage
- Distributed systems

User-facing names should remain presentation data rather than persistent identity.

**Status:** Deferred

**Reason:** Enables future scalability while preserving stable references.

---

## PostgreSQL Migration

JSON storage is intentionally used during early development.

Future versions should migrate persistent storage to PostgreSQL through the Storage abstraction.

Higher application layers should remain unchanged.

Potential benefits include:

- Transactions
- Relationships
- Efficient querying
- Indexing
- Concurrent access
- Synchronization

**Status:** Planned

**Reason:** Provides scalable persistence while preserving architectural separation.

---

# Security

## Permission System

Every action capable of modifying user data or interacting with external systems should pass through a centralized Permission Manager.

Examples include:

- File deletion
- Sending emails
- Running terminal commands
- Browser automation
- Cloud synchronization

**Status:** Planned

**Reason:** Preserves user autonomy.

---

# Intelligence

## Explainability

ASTRALIS should explain significant decisions and recommendations.

Users should understand:

- Why an action was suggested
- Which information influenced the decision
- Why information was remembered
- Why information was forgotten
- Any assumptions made

**Status:** Planned

**Reason:** Improves transparency and trust.

---

## Conversation Window

The current Conversation stores every message in the active session.

Future versions should support configurable context windows, summarization, and pruning to prevent unbounded growth.

**Status:** Planned

---

## ASTRALIS Language Model

ASTRALIS currently relies on interchangeable external language providers.

Future versions should support one or more language models developed specifically for ASTRALIS while preserving the provider abstraction.

External providers should remain optional.

**Status:** Planned

**Reason:** Reduces dependence on external providers while preserving flexibility.

---

## Provider Resilience

Language providers should tolerate temporary failures.

Future implementations may include:

- Automatic retries
- Exponential backoff
- Model fallback
- Provider fallback
- Health monitoring
- Cached provider availability

**Status:** Planned

**Reason:** Improves reliability.

---

# Automation

## Background Scheduler

Future versions should introduce a scheduler responsible for executing time-based automation.

Examples include:

- Alarms
- Reminders
- Scheduled tasks
- Recurring jobs

Capabilities should manage user data.

Execution belongs to the Automation layer.

**Status:** Planned

**Reason:** Separates user interaction from background execution.

---

# Engineering

## Application Services

As ASTRALIS grows, application-wide subsystems should be grouped into an Application Services layer rather than being injected individually throughout the application.

Future structure:

```text
Application
├── Core
├── Brain
├── Services
│   ├── Memory
│   ├── Monitoring
│   ├── Automation
│   ├── Permissions
│   └── ...
├── Capabilities
└── Interfaces
```

This refactor should only occur when multiple cross-cutting services justify the additional abstraction.

**Status:** Deferred

**Reason:** Prevents Application and RequestPipeline from accumulating excessive dependencies while avoiding premature abstraction.

---

## Pipeline Stages

If the request pipeline grows beyond a small number of responsibilities, it should evolve into a stage-based architecture.

Possible stages include:

- Monitoring
- Memory Retrieval
- Brain Processing
- Memory Policy
- Memory Update
- Permissions
- Automation

The current pipeline should remain intentionally simple until this abstraction becomes justified.

**Status:** Deferred

**Reason:** Prevents unnecessary complexity while providing a clear evolution path.

---

## Shared Base Components

As the number of Memory and Capability implementations grows, common behavior may be extracted into shared base classes.

These abstractions should only be introduced after repeated implementation patterns clearly emerge.

**Status:** Deferred

**Reason:** Avoids premature abstraction.

---

## Plugin Framework

Capabilities should eventually support external plugins without requiring modifications to the core application.

Plugins should be:

- Discoverable
- Independently installable
- Sandboxed when practical
- Explicitly enabled by users

**Status:** Planned

**Reason:** Enables ecosystem growth while preserving modularity.

---

# Documentation Policy

Whenever a feature is intentionally postponed, evaluate whether it belongs in this document.

Only record architectural decisions that would be difficult to reconstruct later.

This document should remain intentionally small and focused on significant deferred architectural decisions.

---

Project: **ASTRALIS**

Current Release: **v0.4.0 "Context Foundation"**

Current Milestone: **v0.5.0 "Local Intelligence"**

Philosophy:

> **Assist. Don't Control.**