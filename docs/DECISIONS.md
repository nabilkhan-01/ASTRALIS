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

Bootstrap Constructs Core Services

### Decision

Bootstrap constructs shared application services and assembles the Application container.

The Engine coordinates these services but does not construct them.

### Rationale

Separating dependency construction from application orchestration keeps the Engine lightweight, improves testability, and centralizes dependency injection.

### Consequences

- Bootstrap becomes the application's composition root.
- Shared services are initialized exactly once.
- Application stores shared dependencies.
- Engine focuses exclusively on orchestration.

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

## ADR-0017

### Title

Depend on AI Provider Abstractions

### Decision

The Brain communicates exclusively through a Provider interface rather than depending directly on any specific AI provider.

### Rationale

Separating the Brain from provider implementations preserves modularity and allows AI providers to be replaced without affecting Brain logic.

### Consequences

- The Brain remains provider-agnostic.
- New providers can be added without modifying the Brain.
- Switching AI providers requires changes only within the provider layer.

---

## ADR-0018

### Title

Instantiate Providers Through a Factory

### Context

The Engine previously instantiated concrete provider implementations directly.

As additional AI providers are introduced, this would increase coupling between the Engine and provider implementations.

### Decision

Provider instances are created through a centralized `ProviderFactory`.

The Engine requests a provider from the factory instead of instantiating provider implementations directly.

### Rationale

- Keeps the Engine provider-agnostic.
- Centralizes provider creation logic.
- Simplifies adding new AI providers.
- Preserves the separation between application orchestration and provider instantiation.

### Consequences

- The Engine no longer depends on concrete provider implementations.
- New providers require updates only to the factory.
- Provider selection is centralized in a single location.

---

## ADR-0019

### Title

Delegate Execution Planning to the Planner

### Decision

The Brain delegates execution planning to a dedicated Planner component. The Planner produces an Plan, allowing the Brain to remain focused on orchestration.

### Rationale

- Separates planning from orchestration.
- Keeps the Brain small and maintainable.
- Allows planning strategies to evolve independently.

### Consequences

- The Brain coordinates planning instead of implementing it.
- Future planning logic remains isolated.
- New planning strategies can be introduced without modifying the Brain.

---

## ADR-0020

### Title

Request Interpretation Is Delegated

### Context

As the Brain grows, request interpretation will become increasingly complex.

Future capabilities such as intent recognition, entity extraction, language detection, conversation context, and confidence scoring should remain separate from orchestration logic.

### Decision

The Brain delegates request interpretation to a dedicated `Interpreter` component.

The `Interpreter` produces an `Interpretation` object representing the Brain's understanding of the request without modifying the original `Request`.

### Rationale

- Separates interpretation from orchestration.
- Preserves the original request.
- Allows interpretation to evolve independently.
- Supports future expansion without increasing Brain complexity.

### Consequences

- The Brain coordinates interpretation rather than implementing it.
- Interpretation can expand with additional metadata over time.
- Future planning stages consume an `Interpretation` instead of the raw request.

---

## ADR-0021

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

## ADR-0022

### Title

Execute Requests Through Capabilities

### Decision

The Brain executes requests through a Capability Framework rather than communicating directly with AI providers or external systems.

### Rationale

- Separates reasoning from execution.
- Allows Browser, Memory, Email, Weather and future features to be implemented independently.
- Keeps the Brain provider-independent.

### Consequences

- New capabilities implement a common interface.
- The Capability Manager coordinates execution.
- Language generation becomes one capability among many.

----

## ADR-0023

### Title

Introduce Bootstrap as the Composition Root

### Decision

Object construction and dependency wiring are centralized in Bootstrap.

### Rationale

Keeps the Engine focused on orchestration, improves testability, and simplifies dependency management.

### Consequences

The Engine no longer constructs application-wide dependencies; Bootstrap owns composition.

---

## ADR-0024

### Title

Introduce a Request Pipeline

### Decision

ASTRALIS introduces a dedicated Request Pipeline positioned between user interfaces and the Brain.

Every user request passes through the Request Pipeline before reaching the Brain.

### Rationale

Separating request processing from both interfaces and the Brain provides a dedicated location for cross-cutting concerns without increasing the responsibilities of either component.

The Brain remains focused exclusively on intelligent request processing, while interfaces remain focused on user interaction.

### Consequences

- User interfaces communicate with the Request Pipeline instead of the Brain.
- The Brain remains independent of interface-specific concerns.
- Cross-cutting concerns can be introduced without modifying Brain logic.
- The request flow becomes consistent across all interfaces.

---

## ADR-0025

### Title

The Brain Consumes Context Rather Than Raw Requests

### Decision

The Brain receives a BrainContext instead of a raw Request.

BrainContext represents all information available for reasoning while remaining independent of how that information was collected.

The Request Pipeline is responsible for constructing the BrainContext.

### Rationale

As ASTRALIS evolves, the Brain requires more than the current user request.

Future reasoning may depend on:

- Retrieved memory
- Working memory
- Active project
- Vision
- Environmental context
- User preferences

Passing these independently would continually expand the Brain API.

A dedicated BrainContext provides a stable interface that can evolve without changing the Brain's public contract.

### Consequences

- The Brain consumes a single immutable reasoning context.
- Request Pipeline assembles reasoning context.
- Future contextual information can be added without redesigning the Brain API.
- The Brain remains independent from memory retrieval and other context providers.

---

## ADR-0026

### Title

Separate Memory Retrieval from Memory Persistence

### Decision

Memory retrieval and memory persistence are separate responsibilities.

The Brain never retrieves or persists memory directly.

Memory retrieval occurs before reasoning.

Memory persistence occurs after reasoning through a dedicated Memory Policy.

### Rationale

Reasoning and persistence evolve independently.

The Brain should focus exclusively on understanding requests and coordinating intelligent behavior.

Determining what should become long-term memory is a separate concern requiring different policies and heuristics.

Separating these responsibilities preserves modularity and aligns with the project philosophy.

### Consequences

- Memory retrieval becomes part of the request pipeline.
- The Brain remains independent of storage implementations.
- Future Memory Policies can evolve without modifying Brain logic.
- Automatic learning and explicit user memory can coexist through a common persistence policy.


## ADR Guidelines

Architecture Decision Records (ADRs) document significant architectural decisions that have a long-term impact on ASTRALIS.

An ADR should be created only when a decision:

- Significantly influences the overall architecture.
- Is difficult or expensive to reverse.
- Establishes a long-term engineering principle.
- Affects multiple modules or future development.

Implementation details, helper classes, refactorings, naming changes, and other low-level design decisions should be documented through code, commit history, or project documentation rather than ADRs.

ADRs should record why the architecture is the way it is, not how individual components are implemented.

When in doubt, prefer documenting the decision in code or project documentation rather than creating a new ADR.

The goal is to preserve the reasoning behind major architectural decisions—not to record every implementation detail.

--- 

Project: **ASTRALIS**

Current Release: **v0.3.1 – Engineering Stability**

Current Milestone: **v0.4.0 "Memory"**

Philosophy: **Assist. Don't Control.**