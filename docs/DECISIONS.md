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

## ADR-0016

### Title

Represent User Requests with a Request Model

### Decision

The Brain communicates using structured Request models instead of primitive data types.

### Rationale

Using a dedicated request model creates a stable interface between user-facing components and the Brain while allowing the request to evolve without changing the Brain's public API.

### Consequences

- All user input is represented consistently.
- Future fields can be added without redesigning the Brain interface.
- Voice, UI, CLI, and API can all produce the same request type.

---

## ADR-0016

### Title

Separate Behavior from Data Models

### Decision

Behavior-oriented components are implemented as regular classes.

Structured data exchanged between major components is represented using dedicated data models. In Python, these models should normally be implemented as dataclasses.

### Rationale

ASTRALIS separates components that perform work from objects that represent information.

This distinction improves readability, reduces boilerplate, and keeps responsibilities clear as the project grows.

### Consequences

- Engine, Brain, Module Loader, Health Checker, and similar components remain regular classes.
- Request, Response, and future domain models are represented as data models.
- The architecture maintains a clear distinction between behavior and data.

---

## ADR-0018

## Title

Depend on AI Provider Abstractions

## Decision

The Brain communicates exclusively through a Provider interface rather than depending directly on any specific AI provider.

## Rationale

Separating the Brain from provider implementations preserves modularity and allows AI providers to be replaced without affecting Brain logic.

## Consequences

- The Brain remains provider-agnostic.
- New providers can be added without modifying the Brain.
- Switching AI providers requires changes only within the provider layer.

---

# ADR-0019

## Title

Instantiate Providers Through a Factory

## Context

The Engine previously instantiated concrete provider implementations directly.

As additional AI providers are introduced, this would increase coupling between the Engine and provider implementations.

## Decision

Provider instances are created through a centralized `ProviderFactory`.

The Engine requests a provider from the factory instead of instantiating provider implementations directly.

## Rationale

- Keeps the Engine provider-agnostic.
- Centralizes provider creation logic.
- Simplifies adding new AI providers.
- Preserves the separation between application orchestration and provider instantiation.

## Consequences

- The Engine no longer depends on concrete provider implementations.
- New providers require updates only to the factory.
- Provider selection is centralized in a single location.

---

# ADR-0020

## Title

Brain Produces Execution Plans

## Context

As ASTRALIS grows, request processing will involve more than simply forwarding requests to an AI provider.

Future capabilities such as memory, tools, permissions, and provider selection require an intermediate planning stage.

## Decision

The Brain produces an `ExecutionPlan` before executing a request.

Execution follows the plan rather than embedding decision logic directly into the execution stage.

## Rationale

- Separates planning from execution.
- Supports future capabilities without increasing coupling.
- Keeps request execution predictable and extensible.

## Consequences

- The Brain becomes responsible for planning.
- Execution follows the generated plan.
- Future capabilities can extend the plan without changing the overall processing pipeline.

---

# ADR-0021

## Title

Request Interpretation Is Delegated

## Context

As the Brain grows, request interpretation will become increasingly complex.

Future capabilities such as intent recognition, entity extraction, language detection, conversation context, and confidence scoring should remain separate from orchestration logic.

## Decision

The Brain delegates request interpretation to a dedicated `Interpreter` component.

The `Interpreter` produces an `Interpretation` object representing the Brain's understanding of the request without modifying the original `Request`.

## Rationale

- Separates interpretation from orchestration.
- Preserves the original request.
- Allows interpretation to evolve independently.
- Supports future expansion without increasing Brain complexity.

## Consequences

- The Brain coordinates interpretation rather than implementing it.
- Interpretation can expand with additional metadata over time.
- Future planning stages consume an `Interpretation` instead of the raw request.

---

## ADR Guidelines

Architecture Decision Records (ADRs) document significant architectural decisions that have a long-term impact on ASTRALIS.

An ADR should be created only when a decision:

- Significantly influences the overall architecture.
- Is difficult or expensive to reverse.
- Establishes a long-term engineering principle.
- Affects multiple modules or future development.

Implementation details, internal algorithms, logging changes, helper classes, and other low-level design choices should be documented through code, commit history, or project documentation rather than ADRs.
When in doubt, prefer documenting the decision in code or project documentation rather than creating a new ADR.

The goal is to preserve the reasoning behind major architectural decisions—not to record every implementation detail.

--- 

## ADR-0022

### Title

The Brain Owns Conversation State

### Context

ASTRALIS supports multiple AI providers including Gemini, OpenAI, and future local models.

Different providers expose different APIs and conversation formats. Storing conversation history inside provider implementations would tightly couple conversation management to a specific provider and make switching providers more difficult.

### Decision

The Brain owns the active conversation.

Conversation history is represented using dedicated `Conversation`, `Message`, and `Role` models.

AI providers receive the current conversation, generate the next assistant response, and return it to the Brain.

Providers remain stateless and never own conversation history.

### Rationale

- Preserves provider independence.
- Maintains a single source of truth for conversation state.
- Allows providers to be replaced without losing context.
- Enables future integration with memory, tools, permissions, and planning.
- Keeps conversation management independent of provider-specific APIs.

### Consequences

- The Brain becomes responsible for conversation lifecycle.
- Providers only generate responses from the supplied conversation.
- Conversation can evolve independently of AI providers.
- Future interfaces (CLI, Desktop, Voice, Mobile, API) share the same conversation model.

---

Project: **ASTRALIS**

Current Release: **v0.1.0 "Foundation"**

Current Milestone: **v0.2.0 "Brain Architecture"**

Philosophy: **Assist. Don't Control.**