# ASTRALIS Architecture

> "Simple architecture scales better than complicated architecture."

## Overview

ASTRALIS is a modular AI Operating System designed around separation of responsibilities, dependency injection, and extensibility.

Every subsystem has a clearly defined responsibility and communicates through explicit dependencies.

The architecture follows one guiding principle:

> **Assist. Don't Control.**

- The Engine coordinates the application.
- The Pipeline coordinates request processing.
- The Brain owns intelligence.
- Capabilities perform actions.
- Providers generate language.
- Memory manages state.
- Storage manages persistence.

---

# High-Level Architecture

```text
                     User
                       │
                       ▼
          Command Line Interface (CLI)
                       │
                       ▼
              Request Pipeline
                       │
                       ▼
              Memory Retrieval
                       │
                       ▼
                 Brain Context
                       │
                       ▼
                    Brain
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
 Interpreter      Planner     Capability Manager
                                       │
                                       ▼
                              Capability Registry
                                       │
                                       ▼
                                 Capabilities
                              ┌──────┼──────┐
                              │      │      │
                              ▼      ▼      ▼
                           Memory  Tools Providers
                                       │
                                       ▼
                                External Services
```

---

# Composition Root

ASTRALIS uses a composition root to construct the application.

```text
main.py
    │
    ▼
Bootstrap
    │
    ▼
Application
    │
    ▼
Engine
```

Bootstrap constructs every shared dependency and assembles a complete application before execution begins.

---

# Startup Flow

```text
main.py
    │
    ▼
Bootstrap.build()
    │
    ▼
Application
    │
    ▼
Engine.start()
    │
    ├── Initialize lifecycle
    ├── Load modules
    ├── Run health checks
    ├── Transition to RUNNING
    └── Start CLI
```

Once startup completes:

```text
CLI
 │
 ▼
RequestPipeline
 │
 ▼
MemoryRetriever
 │
 ▼
BrainContext
 │
 ▼
Brain
 │
 ▼
Capability Manager
```

---

# Core Components

## Engine

Coordinates the application lifecycle.

Responsibilities:

- Startup
- Lifecycle transitions
- Health checks
- Module loading
- Starting the user interface

The Engine contains no business logic.

---

## Bootstrap

Bootstrap is the application's composition root.

Responsibilities:

- Create shared services
- Create providers
- Create memory components
- Create the Brain
- Create the Request Pipeline
- Create the user interface
- Register capabilities
- Assemble the Application

Bootstrap owns dependency construction.

---

## Application

Application is a lightweight dependency container.

It stores shared application components that are constructed during bootstrap and used throughout the system.

Application performs no logic.

---

## Request Pipeline

The Request Pipeline is the single entry point for every request.

Responsibilities:

- Receive requests from interfaces
- Retrieve relevant memory
- Build the BrainContext
- Coordinate request processing
- Delegate execution to the Brain

The pipeline contains no intelligence.

It assembles the context required for reasoning while isolating cross-cutting concerns from the Brain and user interfaces.

---

## Brain

The Brain coordinates intelligent request processing.

Responsibilities:

- Consume BrainContext
- Request validation
- Conversation management
- Request interpretation
- Planning
- Capability execution
- Response generation

The Brain receives all information required for reasoning through a BrainContext.

It never retrieves persistent memory directly.

---

# Brain Context

BrainContext represents the complete reasoning context supplied to the Brain.

Current contents:

- Request
- Retrieved Memory

Future versions may extend BrainContext with:

- Working Memory
- Active Project
- Vision Context
- Environment
- User Context

The Brain API should evolve through BrainContext rather than by expanding the Brain.process() signature.

---

# Capability Architecture

```text
Brain
   │
   ▼
Capability Manager
   │
   ▼
Capability Registry
   │
   ▼
Capability
   │
   ├── Memory
   ├── Tool
   └── Provider
```

Capabilities represent everything ASTRALIS can do.

Every capability implements the same interface and is independently testable.

---

# Provider Layer

Providers generate natural language.

Current providers:

- Gemini
- OpenAI
- Mock

Providers:

- do not store memory
- do not plan requests
- do not execute capabilities

Their only responsibility is language generation.

---

# Memory

Memory manages knowledge rather than persistence.

Current components:

- MemoryManager
- MemoryRetriever
- EntityStore
- JsonEntityStore

Memory is responsible for:

- Managing persistent entities
- Retrieving relevant knowledge
- Abstracting storage

Storage determines where information is stored.

Memory determines what information is available for reasoning.

---

# Storage

Storage provides persistence for memory modules.

Current implementation:

- JSON Storage

Storage is independent from memory implementations.

---

# Interfaces

Interfaces communicate with users.

Current interface:

- Command Line Interface (CLI)

Interfaces never contain business logic or intelligence.

They forward requests to the Request Pipeline.

---

# Monitoring

ASTRALIS includes a monitoring module.

Current components:

- Timer
- Monitor

Monitoring is implemented independently from the Brain and capabilities.

---

# Design Principles

ASTRALIS is designed around:

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

# Engineering Rules

Every architectural decision should reinforce these rules.

- Bootstrap owns object construction.
- Application stores shared dependencies.
- Engine coordinates the application lifecycle.
- Request Pipeline assembles reasoning context.
- Brain owns reasoning and decision making.
- Brain never retrieves or persists memory directly.
- Capabilities perform actions.
- Memory manages knowledge.
- Storage manages persistence.
- Providers generate language.
- Interfaces remain thin.
- Prefer composition over inheritance.
- Keep modules independent.
- Favor explicit dependencies over hidden coupling.
- Catch specific exceptions.
- Design before implementation.
- Keep documentation synchronized with the code.
- Preserve user autonomy.
---

Project: **ASTRALIS**

Release: **v0.3.1**

Codename: **Engineering Stability**

Philosophy:

> **Assist. Don't Control.**