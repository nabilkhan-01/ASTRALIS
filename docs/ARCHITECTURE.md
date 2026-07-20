# ASTRALIS Architecture

> "Simple architecture scales better than complicated architecture."

## Overview

ASTRALIS is designed as a modular AI Operating System.

Its architecture emphasizes **modularity, maintainability, extensibility, and user autonomy**.

Every capability is implemented as an independent module coordinated by a shared Core Engine.

The architecture follows the philosophy:

> **Assist. Don't Control.**

The Brain owns intelligence.

Other components provide specialized capabilities while remaining independent and replaceable.

---

# High-Level Architecture

```text
                          User
                            │
          ┌─────────────────┴─────────────────┐
          │                                   │
        CLI                              Future Interfaces
                                              │
                 ┌────────────────────────────┘
                 │
            Core Engine
                 │
      ┌──────────┼──────────┐
      │          │          │
   Brain      Memory    Security
      │
      ▼
 Interpreter
      │
      ▼
 Planner
      │
      ▼
 Capability Manager
      │
      ▼
 Capability Registry
      │
      ▼
 Language Capability
      │
      ▼
 Provider
      │
      ▼
 Language Model
```

Future versions will replace the direct Provider connection with a Capability Framework.

---

# Current Brain Architecture

```text
Request
    │
    ▼
Validate
    │
    ▼
Conversation Update
    │
    ▼
Interpret
    │
    ▼
Planner
    │
    ▼
Execution Plan
    │
    ▼
Capability Manager
    │
    ▼
Capability
    │
    ▼
Provider
    │
    ▼
Response
    │
    ▼
Conversation Update
```

The Brain coordinates every stage of request processing while remaining independent of any specific language model.

---

# Core Architecture

```text
Core Engine
│
├── Configuration
├── Logger
├── Module Registry
├── Module Loader
├── Lifecycle Manager
├── Health Checker
└── Brain
```

The Core Engine coordinates startup, shutdown, lifecycle management, and shared infrastructure.

It intentionally contains no AI-specific logic.

---

# Startup Flow

```text
main.py
    │
    ▼
Engine.start()
    │
    ├── Initialize Configuration
    ├── Initialize Logger
    ├── Load Modules
    ├── Run Health Checks
    ├── Transition to RUNNING
    └── Start User Interface
```

Startup remains predictable and deterministic.

Future modules should integrate without modifying this sequence.

---

# Core Components

## Core Engine

Coordinates application startup, shutdown, lifecycle, and shared services.

The Engine contains no intelligence.

---

## Brain

Coordinates intelligence across ASTRALIS.

Responsibilities include:

- Request validation
- Conversation coordination
- Request interpretation
- Planning coordination
- Capability coordination
- Response coordination

The Brain does not directly execute tools, store memory, or interact with external systems.

---

## Provider Layer

Provides interchangeable language generation.

Current implementations include:

- Gemini
- OpenAI
- Mock Provider

Future providers may include:

- Claude
- Ollama
- Local Models
- ASTRALIS Language Model

Providers generate language only.

They do not own intelligence or conversation state.
Providers are implementation details behind the Language Capability and are never accessed directly by the Brain.

---

## Memory

Responsible for remembering user information, conversations, and long-term knowledge.

Memory decides what should be remembered.

Storage decides where it is persisted.

---

## Security

Responsible for permissions, authentication, and sensitive operations.

Every capability that affects user data or external systems should pass through the Security layer.

---

## Voice

Provides speech recognition and speech synthesis.

---

## Vision

Processes screenshots, images, and visual context.

---

## Capability System

Provides independent capabilities that allow ASTRALIS to interact with the world.

Current implementation:
- Language

Planned:
- Browser
- Weather
- Memory
- Calendar
- Email
- Automation
- Calculator

Every capability should expose a common interface.

---

## User Interfaces

ASTRALIS should remain independent of any interface.

Current:

- Command-Line Interface

Future:

- Desktop
- Voice
- Mobile
- API
- Web

Changing the interface should never change how ASTRALIS thinks.

---

# Design Principles

The architecture follows these principles:

- Single Responsibility
- Modularity
- Extensibility
- Low Coupling
- Maintainability
- Transparency
- Security
- Interface Independence
- User Autonomy

---

# Architectural Principles

Every architectural decision should support the project's philosophy.

- The Brain owns intelligence.
- Providers generate language.
- Capabilities remain modular.
- The user remains in control.
- Build simple today.
- Extend tomorrow.
- Design before implementation.
- Keep documentation synchronized with the codebase.

---

# Future Evolution

The architecture is intentionally incremental.

Future milestones will introduce:

- Context Engine
- Event Bus
- Plugin System
- Awareness Engine
- Multi-Agent Communication
- ASTRALIS Language Model

Each addition should strengthen the existing architecture rather than replace it.

---

Project: **ASTRALIS**

Current Release: **v0.2.0 "Brain Architecture"**

Current Milestone: **v0.3.0 "Capabilities"**

Philosophy: **Assist. Don't Control.**