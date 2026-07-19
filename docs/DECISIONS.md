# Architecture Decision Records (ADR)

This document records significant architectural and engineering decisions made during the development of ASTRALIS.

The purpose of these records is to document not only **what** decisions were made, but also **why** they were made and the trade-offs considered. As the project evolves, new decisions will be added to preserve the reasoning behind the architecture.

---

## ADR-0001

### Title

Use Python as the Primary Programming Language

### Decision

ASTRALIS will be developed primarily in Python.

### Rationale

Python provides an excellent ecosystem for Artificial Intelligence, automation, computer vision, speech processing, and rapid prototyping.

It also enables seamless integration with modern AI frameworks while remaining highly readable and maintainable.

### Consequences

- Python becomes the primary language for all core development.
- Performance-critical components may be implemented in lower-level languages if necessary.
- Contributors should prioritize Python-first solutions.

---

## ADR-0002

### Title

Adopt a Modular Architecture

### Decision

ASTRALIS will be divided into independent modules coordinated by a central Core Engine.

### Rationale

A modular architecture improves maintainability, scalability, testing, and future expansion.

Each module owns a single responsibility and communicates through well-defined interfaces.

### Consequences

- Modules remain independent.
- New capabilities can be added without major architectural changes.
- Individual modules can be tested and maintained separately.

---

## ADR-0003

### Title

Project Philosophy

### Decision

The guiding philosophy of ASTRALIS is:

> **Assist. Don't Control.**

### Rationale

AI should empower users rather than replace their judgment.

Every feature should respect user autonomy, provide transparency, and keep humans in control of important decisions.

### Consequences

- User permission takes priority over automation.
- Features that reduce user autonomy should be reconsidered.
- Safety and transparency remain core design principles.

---

## ADR-0004

### Title

Documentation Before Development

### Decision

Project philosophy, architecture, roadmap, and engineering principles should be established before implementing major functionality.

### Rationale

Good software begins with clear thinking.

Strong documentation reduces ambiguity, improves onboarding, and preserves architectural reasoning throughout the project's lifetime.

### Consequences

- Documentation evolves alongside the codebase.
- Significant architectural changes should be documented.
- Future contributors can understand design decisions quickly.

---

## ADR-0005

### Title

Centralized Configuration Management

### Decision

Application-wide configuration is managed through a single Config object owned by the Core Engine.

### Rationale

Maintaining a single source of truth prevents configuration inconsistencies and simplifies application maintenance.

Configuration describes application behavior, while user-specific preferences remain separate.

### Consequences

- Core services receive configuration from the Engine.
- Duplicate configuration across modules is avoided.
- User preferences are stored independently.

---

## ADR-0006

### Title

Centralized Logging

### Decision

All application logging is performed through a centralized logging service rather than direct `print()` statements.

### Rationale

Centralized logging provides consistent formatting, simplifies debugging, and allows future support for multiple logging destinations without changing application modules.

### Consequences

- Modules use the shared logger.
- Log formatting remains consistent.
- Future logging improvements require minimal architectural changes.

---

## ADR-0007

### Title

Incremental Development

### Decision

ASTRALIS is developed through small, complete, and reviewable capabilities rather than large feature drops.

### Rationale

Incremental development improves software quality, reduces complexity, simplifies debugging, and ensures the project remains stable throughout development.

### Consequences

- Each commit introduces one meaningful capability.
- Every feature leaves the project in a working state.
- Documentation evolves alongside implementation.

---

## ADR-0008

### Title

Core Engine Owns Core Services

### Decision

The Core Engine creates and coordinates shared application services including Configuration, Logging, Module Registry, and Module Loader.

### Rationale

Centralizing ownership provides a predictable startup sequence while avoiding unnecessary duplication of shared services.

### Consequences

- A single Engine instance manages application startup.
- Shared services are initialized once.
- Responsibilities remain clearly separated.

---

## ADR-0009

### Title

Use a Module Registry

### Decision

ASTRALIS maintains a centralized Module Registry responsible for tracking initialized application modules.

### Rationale

The registry decouples the Engine from individual modules, making the architecture easier to extend as new capabilities are introduced.

### Consequences

- New modules can be registered without modifying the Engine.
- Module discovery remains centralized.
- Future plugin support becomes easier to implement.

---

## ADR-0010

### Title

Delegate Module Initialization to the Module Loader

### Decision

The Core Engine delegates module initialization to a dedicated Module Loader.

### Rationale

Separating module initialization from the Engine keeps the Engine focused on coordinating the application lifecycle while allowing the loading process to evolve independently.

### Consequences

- The Engine remains lightweight.
- Module initialization follows a single, consistent process.
- Future loading strategies can evolve without redesigning the Engine.

---

## ADR-0011

### Title

User-Controlled Module Activation

### Decision

Modules may be discovered automatically, but activation should occur only through explicit user intent or application configuration.

### Rationale

Automatically executing newly discovered modules conflicts with ASTRALIS's guiding philosophy.

Users should remain in control of what capabilities become active.

### Consequences

- Plugin discovery is separate from plugin activation.
- Users explicitly enable new capabilities.
- Security and transparency are improved.
- The architecture remains aligned with **Assist. Don't Control.**

---

## ADR-0012

### Title

Introduce a Dedicated Lifecycle Manager

### Decision

The application lifecycle is represented by a dedicated Lifecycle Manager. The Core Engine controls lifecycle transitions.

### Rationale

Separating lifecycle state from application orchestration keeps responsibilities clear and maintains a single source of truth for application state.

### Consequences

- The Engine remains the orchestrator.
- Lifecycle state is centralized.
- Future state validation can be added without redesigning the Engine.

---

---

## ADR-0013

### Title

Introduce a Dedicated Health Checker

### Decision

ASTRALIS introduces a dedicated Health Checker responsible for verifying the readiness of core application services.

The Health Checker reports the health of the system but does not determine application behavior.

### Rationale

Separating health verification from application orchestration keeps responsibilities clearly defined and allows the health system to evolve independently of the startup process.

### Consequences

- Health verification is centralized.
- The Health Checker reports system readiness.
- Startup decisions remain the responsibility of the Core Engine.
- Core services can be validated through a consistent interface.

---

## ADR-0014

### Title

Introduce the Brain Module

### Decision

ASTRALIS introduces a dedicated Brain module responsible for coordinating intelligence across the system.

The Brain exposes a single public interface for processing user requests while remaining independent of specific AI providers and supporting modules.

### Rationale

Separating intelligence coordination from application orchestration keeps responsibilities clear and allows the Brain to evolve independently of the Core Engine.

### Consequences

- The Engine communicates only with the Brain.
- The Brain becomes the central coordinator for intelligent behavior.
- Future integrations with Memory, Vision, Tools, and AI providers remain isolated from the Engine.

---

## ADR-0015

### Title

Core Engine Owns the Brain

### Decision

The Core Engine owns and initializes the Brain during application startup.

### Rationale

Centralizing ownership of the Brain keeps startup orchestration within the Engine and maintains a single point of coordination for core application services.

### Consequences

- The Engine becomes the entry point to intelligence.
- Other components interact with the Brain through the Engine.
- The Brain remains independent of the application lifecycle.

---

Project: **ASTRALIS**

Current Release: **v0.0.1 "Genesis"**

Current Milestone: **v0.1.0 "Foundation"**

Philosophy: **Assist. Don't Control.**