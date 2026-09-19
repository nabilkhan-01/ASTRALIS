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

The request path is therefore:

```text
User
  │
  ▼
Interface
  │
  ▼
Request Pipeline
  │
  ├── Retrieve relevant knowledge
  │
  ├── Assemble Context
  │
  ▼
BrainContext
  │
  ▼
Brain
  │
  ├── Interpret
  ├── Plan
  ├── Execute capabilities
  └── Generate response
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
- Assemble request-scoped Context
- Build the BrainContext
- Coordinate request processing
- Delegate execution to the Brain
- Provide read-only context inspection

The pipeline contains no intelligence.

It assembles the context required for reasoning while isolating cross-cutting concerns from the Brain and user interfaces.

The Pipeline does not directly manage persistent storage.

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

## Context

Context represents the request-scoped reasoning information assembled for the Brain.

Context is immutable and ephemeral.

Current contents:

- Relevant ContextItems
- Persistent Entities
- Deterministic relevance scores

Context may expose entity metadata such as:

- Entity identity
- Entity type
- Properties
- Provenance
- Temporal metadata
- Confidence

Context is not persistent storage.

A new Context is assembled for each retrieval operation and is not reused as persistent memory.

---

## ContextItem

ContextItem is an immutable wrapper connecting a persistent Entity with its relevance to the current request.

Current structure:

```text
ContextItem
├── Entity
└── Relevance
```

Relevance is calculated deterministically by the context relevance engine.

ContextItem does not own persistence or retrieval.

---

## BrainContext

BrainContext represents the complete reasoning context supplied to the Brain.

Current contents:

- Request
- Retrieved Memory

The Brain API should evolve through BrainContext rather than by expanding the Brain.process() signature.

Future versions may extend BrainContext with:

- Working Memory
- Active Project
- Vision Context
- Environment
- User Context

The Brain should consume context rather than retrieve it independently.

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
- LocalProvider (abstract base for local runtimes)

Future providers may include concrete local inference providers such as Ollama.

The Brain depends on the provider abstraction rather than a
specific model or model runtime.

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
- Updating entities
- Deleting entities
- Retrieving relevant knowledge
- Applying retrieval policies
- Abstracting storage

Memory also supports knowledge metadata such as:

- Provenance
- Temporal metadata
- Confidence
- Decision state
- Project context

Storage determines where information is stored.

Memory determines what information is available for reasoning.

---

# Storage

Storage provides persistence for Memory.

Current implementation:

- JSON Storage

Storage is independent from memory behavior.

The storage layer is responsible for persistence mechanics.

Memory remains responsible for managing knowledge and determining what is available for reasoning.

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

Monitoring does not own memory or reasoning.

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
- Explicit Context
- Provider Independence

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
- Context represents ephemeral request-scoped reasoning state.
- Context remains separate from persistent Memory.
- Providers generate language.
- Providers remain independent from Memory and Context.
- Interfaces remain thin.
- Prefer composition over inheritance.
- Keep modules independent.
- Favor explicit dependencies over hidden coupling.
- Catch specific exceptions.
- Design before implementation.
- Keep documentation synchronized with the code.
- Preserve user autonomy.
- Never silently mutate persistent context.
- Prefer deterministic behavior where possible.
- Treat provenance, freshness, confidence, and conflict state as explicit context metadata.
- Separate knowledge, context, reasoning, and action.

---

Project: **ASTRALIS**

Release: **v0.4.0**

Codename: **Context Foundation**

Philosophy:

> **Assist. Don't Control.**