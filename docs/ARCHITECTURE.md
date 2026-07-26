# ASTRALIS Architecture

> "Simple architecture scales better than complicated architecture."

## Overview

ASTRALIS is a modular AI Operating System designed around separation of responsibilities, dependency injection, and extensibility.

Every major subsystem has a single responsibility and communicates through well-defined interfaces.

The architecture follows one guiding principle:

> **Assist. Don't Control.**

The Brain owns intelligence.

Capabilities perform work.

Providers generate language.

Memory stores information.

The Engine coordinates the application.

---

# High-Level Architecture

```text
                           User
                             │
                 ┌───────────┴───────────┐
                 │                       │
                CLI             Future Interfaces
                                         │
                                         ▼
                                   Bootstrap
                                         │
                                         ▼
                                  Application
                                         │
                                         ▼
                                   Core Engine
                                         │
      ┌───────────────┬──────────────────┬──────────────────┐
      │               │                  │                  │
   Lifecycle       Health            Brain          Capability System
      │                                 │                  │
      │                                 │                  ▼
      │                           Interpreter      Capability Manager
      │                                 │                  │
      │                             Planner               ▼
      │                                 │          Capability Registry
      │                                 │                  │
      │                                 └──────────┬───────┘
      │                                            │
      ▼                                            ▼
 Module Loader                               Capabilities
      │                                            │
 Module Registry                                  │
                                                   ▼
                                               Providers
                                                   │
                                                   ▼
                                           External Services
```

---

# Composition Root

ASTRALIS uses a composition root.

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

Bootstrap is responsible for:

- Constructing application components
- Injecting dependencies
- Registering capabilities
- Returning a fully configured application

No other component should create application-wide dependencies.

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
    └── Start user interface
```

Startup is deterministic and centralized.

---

# Core Components

## Engine

Coordinates the application's lifecycle.

Responsibilities include:

- Startup
- Shutdown
- Lifecycle transitions
- Health checks
- Module loading

The Engine contains no business logic.

---

## Bootstrap

Bootstrap is the application's composition root.

Responsibilities:

- Create shared services
- Create providers
- Create memories
- Create the Brain
- Create the CLI
- Register capabilities
- Assemble the Application

Bootstrap owns dependency construction.

---

## Application

Application is a lightweight container that groups all shared dependencies.

It allows the Engine to receive a fully configured application rather than constructing objects itself.

---

## Brain

The Brain coordinates intelligence.

Responsibilities include:

- Conversation management
- Request interpretation
- Planning
- Capability selection
- Response generation

The Brain never directly accesses external services.

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
   ▼
Tool / Memory / Provider
```

Capabilities represent everything ASTRALIS can do.

Current capabilities include:

- Language
- Search
- Weather
- Browser
- Calculator
- Notes
- Calendar
- Alarm
- File System
- Email
- Time

Every capability implements the same interface and can be independently tested.

---

# Provider Layer

Providers generate language.

Current providers:

- Gemini
- OpenAI
- Mock Provider

Providers never:

- store memory
- make decisions
- coordinate execution

They only generate language.

---

# Memory

Memory manages persistent information.

Current memories:

- Notes
- Calendar
- Alarm

Memory decides **what** is remembered.

Storage decides **where** it is stored.

---

# Storage

Storage provides persistence.

Memory components remain independent of the underlying storage implementation.

---

# User Interfaces

Interfaces remain independent from application logic.

Current:

- Command-Line Interface (CLI)

Future:

- Desktop
- Voice
- Mobile
- Web
- API

Changing the interface should never require changes to the Brain.

---

# Design Principles

The architecture follows these principles.

- Single Responsibility
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
- Engine coordinates the application.
- Brain owns intelligence.
- Capabilities perform actions.
- Providers generate language.
- Memory manages state.
- Storage manages persistence.
- Keep modules independent.
- Catch specific exceptions.
- Prefer composition over inheritance.
- Design before implementation.
- Keep documentation synchronized with the code.

---

# Future Evolution

Future milestones may introduce:

- Voice Interface
- Vision System
- Plugin Framework
- Event Bus
- Context Engine
- Multi-Agent Coordination
- Local Language Models

Each addition should extend the existing architecture rather than replace it.

---

Project: **ASTRALIS**

Release: **v0.3.0 – Capability Platform**

Philosophy:

> **Assist. Don't Control.**