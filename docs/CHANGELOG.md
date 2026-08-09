# Changelog

All notable changes to ASTRALIS are documented here.

This project follows Semantic Versioning.

---

# Not Released

## Added

### Brain

- Introduced `BrainContext` as the unified reasoning context for the Brain.
- Updated the Brain to consume contextual information instead of raw requests.
- Established a stable Brain API for future context expansion.

### Memory

- Introduced the Entity-based Memory architecture.
- Added EntityStore abstraction.
- Added JSON-backed EntityStore implementation.
- Added MemoryManager.
- Added MemoryRetriever.
- Integrated Memory into the application bootstrap.
- Integrated Memory Retrieval into the Request Pipeline.

### Pipeline

- Request Pipeline now retrieves relevant memory before reasoning.
- Request Pipeline now assembles the BrainContext.

### Architecture

- Introduced contextual reasoning architecture.
- Brain no longer retrieves persistent memory directly.
- Established separation between reasoning and persistence.
- Updated architecture and engineering documentation.

### Testing

- Expanded unit test coverage for the Memory subsystem.
- Updated Brain and Pipeline tests for BrainContext integration.

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