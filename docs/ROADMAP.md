# ASTRALIS Roadmap

> *"Build an intelligence people trust—not just another AI."*

This roadmap outlines the planned evolution of ASTRALIS into a modular AI Operating System.

Every milestone builds toward one philosophy:

> **Assist. Don't Control.**

---

# Current Development

**Current Release:** `v0.3.1 – Engineering Stability`

**Current Milestone:** `v0.4.0 – Memory`

---

# v0.0.1 — Genesis ✅

Established the vision for ASTRALIS.

## Completed

- [x] Project foundation
- [x] Engineering principles
- [x] Architecture planning
- [x] Documentation
- [x] Development environment

---

# v0.1.0 — Foundation ✅

Built the core application infrastructure.

## Completed

- [x] Core Engine
- [x] Configuration system
- [x] Logging
- [x] Lifecycle management
- [x] Module system
- [x] Brain foundation
- [x] Command-line interface

### Success Criteria

- [x] Stable application lifecycle
- [x] Modular project structure
- [x] Foundation ready for intelligent features

---

# v0.2.0 — Brain Architecture ✅

Taught ASTRALIS how to think.

## Completed

- [x] Request processing pipeline
- [x] Conversation management
- [x] Interpreter
- [x] Planner
- [x] Capability Framework
- [x] Provider abstraction
- [x] Gemini provider
- [x] OpenAI provider
- [x] Mock provider

### Success Criteria

- [x] Modular reasoning architecture
- [x] Provider-independent intelligence
- [x] Capability-based execution

---

# v0.3.0 — Capability Platform ✅

Enabled ASTRALIS to interact with the world.

## Architecture

- [x] Bootstrap composition root
- [x] Dependency Injection
- [x] Application dependency container

## Capabilities

- [x] Language
- [x] Time
- [x] Calculator
- [x] Weather
- [x] Search
- [x] Browser
- [x] File System
- [x] Notes
- [x] Calendar
- [x] Alarm
- [x] Email

## Platform

- [x] Persistent Notes
- [x] Persistent Calendar
- [x] Persistent Alarms
- [x] API layer
- [x] Browser tools
- [x] File System tools
- [x] Domain models

## Engineering

- [x] Bootstrap architecture
- [x] Static typing
- [x] Ruff compliance
- [x] MyPy compliance
- [x] 110+ automated tests
- [x] Updated documentation

### Success Criteria

- [x] Provider-independent architecture
- [x] Modular capabilities
- [x] Real-world functionality

---

# v0.4.0 — Context Foundation 🚧

Build the foundation for trusted, persistent context.

## Goal

> **Give humans and AI agents the right context at the right time, with enough history and provenance to understand why it can be trusted.**

---

## Foundation

- [x] BrainContext
- [x] Entity-based Memory
- [x] EntityStore abstraction
- [x] JSON Entity Store
- [x] MemoryManager
- [x] MemoryRetriever
- [x] ContextItem
- [x] Context model
- [x] Deterministic context relevance
- [x] Relevant context retrieval
- [x] Context provenance
- [x] Temporal metadata
- [x] Context freshness
- [x] Context lifecycle

---

## Project Context

ASTRALIS should begin understanding a project as more than a collection of files.

- [x] Project identity
- [x] Current project resolution
- [x] Project goals
- [x] Architecture context
- [x] Constraints
- [x] Requirements
- [x] Important decisions
- [x] Current state

---

## Decision Context

ASTRALIS should preserve the reasoning behind important decisions.

- [x] Decision entity
- [x] Decision rationale
- [x] Decision evidence
- [x] Decision status
- [x] Decision relationships
- [x] Superseded decisions

---

## Context Retrieval

ASTRALIS should provide relevant context rather than returning everything it knows.

- [x] Relevant context retrieval
- [x] Context filtering
- [x] Context prioritization
- [x] Source-aware retrieval
- [x] Context assembly for Brain
- [x] Context-aware language generation

---

## Trust & Safety

Context should not automatically become truth.

- [x] Context provenance
- [x] Context freshness
- [x] Confidence representation
- [x] Conflicting context detection
- [x] User-controlled context updates
- [x] Context inspection
- [x] Context deletion

---

### Architectural Goal

Separate **knowledge, context, reasoning, and action**.

The Brain should reason over context without becoming responsible for storing or retrieving it.

Memory should manage accumulated knowledge.

The Request Pipeline should assemble the appropriate reasoning context.

Storage should remain responsible for persistence.

---

### Success Criteria

- [x] ASTRALIS can represent structured request context.
- [x] ASTRALIS can represent structured project context.
- [x] ASTRALIS can preserve important decisions and their rationale.
- [x] ASTRALIS can retrieve relevant context instead of all stored information.
- [x] Retrieved context includes enough provenance to understand its origin.
- [x] Stale or conflicting context can be identified.
- [x] The Brain receives context without directly accessing persistent storage.
- [x] Users can inspect and control stored context.
- [ ] The architecture is ready for future AI-agent integrations.

---

# v0.5.0 — Automation

Reduce repetitive work.

## Planned

- [ ] Background Scheduler
- [ ] Scheduled tasks
- [ ] Recurring jobs
- [ ] Smart reminders
- [ ] Workflow automation
- [ ] Permission-aware execution

### Architectural Goal

Separate user interaction from background execution.

---

# v0.6.0 — Voice

Enable natural conversations.

## Planned

- [ ] Speech-to-text
- [ ] Text-to-speech
- [ ] Wake word
- [ ] Streaming conversations
- [ ] Interrupt handling

### Architectural Goal

Support conversational interaction through interchangeable interfaces.

---

# v0.7.0 — Vision

Enable visual understanding.

## Planned

- [ ] OCR
- [ ] Screenshot understanding
- [ ] Image understanding
- [ ] Visual context
- [ ] Multi-modal reasoning

### Architectural Goal

Treat visual information as another reasoning context.

---

# v0.8.0 — Awareness

Improve contextual understanding.

## Planned

- [ ] Workspace awareness
- [ ] Active project awareness
- [ ] Environment awareness
- [ ] Intelligent suggestions
- [ ] Presence without interruption

### Architectural Goal

Provide assistance based on context rather than isolated requests.

---

# v0.9.0 — Reasoning

Strengthen intelligent decision making.

## Planned

- [ ] Multi-step planning
- [ ] Reflection
- [ ] Capability orchestration
- [ ] Explainable reasoning
- [ ] Multi-agent collaboration
- [ ] Adaptive provider selection

### Architectural Goal

Improve reasoning quality while preserving transparency.

---

# v1.0.0 — AI Operating System

The first stable release.

## Goals

- [ ] Reliable
- [ ] Modular
- [ ] Privacy-respecting
- [ ] Context-aware
- [ ] Extensible
- [ ] Provider-independent
- [ ] Production-ready

### Success Criteria

- [ ] Stable public architecture
- [ ] Fully documented
- [ ] Comprehensive automated tests
- [ ] Cross-platform support
- [ ] Long-term memory
- [ ] Automation
- [ ] Voice
- [ ] Vision
- [ ] Context-aware reasoning

---

# Beyond v1.0

Long-term research areas.

- [ ] Local language models
- [ ] Plugin ecosystem
- [ ] Multi-device synchronization
- [ ] Knowledge Graph
- [ ] Semantic Memory
- [ ] Native ASTRALIS language models
- [ ] Distributed intelligence

---

# Development Philosophy

ASTRALIS is built incrementally.

Every release should leave the project in a stable, tested, and maintainable state before moving to the next milestone.

Before marking any roadmap item as complete:

- Architecture is finalized.
- Implementation is complete.
- Tests pass.
- Documentation is updated.
- Quality checks pass.
- Changes are committed.

Build simple today.

Extend tomorrow.

---

**Current Release:** **v0.3.1 – Engineering Stability**

**Current Milestone:** **v0.4.0 – Context Foundation**

**Philosophy:**

> **Assist. Don't Control.**

**Vision:**

> **Build an intelligence people trust—not just another AI.**