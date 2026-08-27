# Changelog

All notable changes to ASTRALIS are documented here.

This project follows Semantic Versioning.

---

# Not Released

## Added

### Context

- Introduced `ContextItem` as a request-scoped wrapper around persistent entities and relevance.
- Introduced `Context` as an immutable, request-scoped collection of relevant context items.
- Added deterministic lexical relevance scoring.
- Added deterministic context ranking and filtering.
- Added relevant context retrieval from persistent memory.
- Added context-to-language generation integration.

### Brain

- Introduced `BrainContext` as the unified reasoning context for the Brain.
- Updated the Brain to consume request-scoped Context.
- Connected retrieved Context to language generation without changing the Provider interface.
- Preserved clean permanent conversation history while using temporary retrieved context during generation.

### Memory

- Added `MemoryRetriever` support for relevance-ranked Context.
- Added optional provenance metadata to persistent entities.
- Added JSON persistence support for entity provenance.
- Preserved backward compatibility with entities stored without provenance.
- Preserved the separation between persistent Memory and ephemeral Context.

### Pipeline

- Request Pipeline now retrieves relevant Context before reasoning.
- Request Pipeline now assembles `BrainContext`.

### Architecture

- Established separation between knowledge, context, reasoning, and action.
- Brain no longer retrieves persistent memory directly.
- Providers remain independent of the Context and Memory domain models.
- Context remains ephemeral and is not persisted as conversation history.
- Established origin provenance as part of persistent knowledge without coupling provenance to request-time relevance.

### Testing

- Added Context model tests.
- Added ContextItem tests.
- Added lexical relevance tests.
- Added provenance model tests.
- Added provenance persistence and legacy-compatibility tests.
- Updated MemoryRetriever tests.
- Updated Brain tests for BrainContext and Context integration.
- Added integration coverage for temporary Context during language generation.

---

# [v0.3.0] - Capability Platform

## 🚀 Highlights

This release introduces the Capability Platform, transforming ASTRALIS from a conversational AI prototype into a modular AI operating system.

### Added

- Bootstrap-based application composition
- Dependency Injection architecture
- Application dependency container
- Capability Framework
- Language, Weather, Search, Browser, Calculator, Notes, Calendar, Alarm, Email, Time, and File System capabilities
- Persistent Memory system (Notes, Calendar, Alarm)
- API layer (Weather, Search, Email)
- Browser and File System tools
- Domain models for application data
- Gemini, OpenAI, and Mock providers
- Comprehensive unit tests (110+)
- CONTRIBUTING guide
- Project quality check script

### Improved

- Brain request interpretation
- Capability routing
- Error handling
- Startup architecture
- Dependency management
- Static typing
- Overall code quality
- Documentation

### Refactored

- Introduced Bootstrap as the composition root
- Engine now focuses only on application orchestration
- Memory migrated to strongly typed models
- Improved separation of responsibilities throughout the project

---

# [v0.2.0] - Brain Architecture

## 🚀 Highlights

- Introduced the Brain architecture
- Added Request, Response, Conversation, Planner, and Interpreter models
- Introduced the Capability Framework
- Added Gemini, OpenAI, and Mock providers
- Added interactive CLI
- Added environment-based configuration
- Expanded project documentation

---

# [v0.1.0] - Foundation

## 🚀 Highlights

- Initialized the project
- Established the project structure
- Implemented the Core Engine
- Added configuration, logging, lifecycle, and module management
- Established the Brain foundation
- Added initial project documentation

---

**Current Release:** **v0.3.1 – Engineering Stability**

**Next Milestone:** **v0.4.0 – Context Foundation**

**Philosophy:**

> **Assist. Don't Control.**