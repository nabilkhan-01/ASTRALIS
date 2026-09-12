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
- Added dynamic context freshness assessment with `FRESH`, `STALE`, and `UNKNOWN` states.
- Added caller-defined freshness thresholds without introducing a global freshness policy.
- Added persistent decision entities through `EntityType.DECISION`.
- Added decision rationale, evidence, and status representation.
- Enabled decisions to participate in standard lexical context retrieval.
- Added explicit confidence metadata for persistent knowledge.
- Added typed `HIGH`, `MEDIUM`, and `LOW` confidence levels.
- Preserved confidence independently from relevance, freshness, and provenance.
- Added structural conflicting-context detection for decision supersession states.
- Detects when a decision supersedes a predecessor that is still marked active.
- Added deterministic conflict reports without mutating stored entities or retrieval behavior.

### Brain

- Introduced `BrainContext` as the unified reasoning context for the Brain.
- Updated the Brain to consume request-scoped Context.
- Connected retrieved Context to language generation without changing the Provider interface.
- Preserved clean permanent conversation history while using temporary retrieved context during generation.

### Memory

- Added `MemoryRetriever` support for relevance-ranked Context.
- Added optional provenance metadata to persistent entities.
- Added JSON persistence support for entity provenance.
- Added temporal metadata through `created_at` and `updated_at`.
- Added JSON persistence support for entity timestamps.
- Added current-project-aware retrieval scoping.
- Preserved backward compatibility with entities stored without provenance or timestamps.
- Preserved the separation between persistent Memory and ephemeral Context.
- Added freshness assessment based on entity `updated_at` metadata.
- Preserved retrieval behavior independently from freshness assessment.
- Added support for persisting decision supersession metadata through existing entity properties.
- Added optional source-aware retrieval using provenance source type.
- Preserved lexical relevance ranking independently from source filtering.
- Added optional confidence metadata to persistent entities.
- Added JSON persistence support for entity confidence.
- Preserved `None` as the default for entities without explicit confidence.
- Verified caller-controlled context updates through existing `MemoryManager` primitives.
- Callers can update project `current_state`, decision status, and confidence by constructing a revised `Entity` with the same `id` and saving it through `MemoryManager.save()`.
- Callers can explicitly resolve detected decision conflicts by updating the predecessor status to `"superseded"` through `MemoryManager.save()`.
- Callers can explicitly upgrade or downgrade entity confidence through `MemoryManager.save()`.
- Verified that `MemoryRetriever.retrieve()`, `RequestPipeline.process()`, and `Brain.process()` never mutate stored entities as a side-effect of processing a request.
- Verified caller-controlled persistent context deletion through `MemoryManager.delete(entity_id)`.
- Deleted entities are immediately and permanently excluded from subsequent retrieval (`MemoryRetriever.retrieve()`), pipeline inspection (`RequestPipeline.inspect_context()`), and Brain reasoning (`RequestPipeline.process()`).
- Established the lifecycle guarantee that persistent deletion does not mutate previously created ephemeral `Context` objects (preserving `Context` as an immutable request-scoped snapshot).
- Verified that deleting a non-existent entity is a safe, deterministic no-op.
- Established that stale or conflicting context entities are never automatically deleted by freshness assessment or conflict detection.

### Decision Context

- Introduced `EntityType.DECISION` for discrete persistent decisions.
- Represented decision statements using `Entity.name`.
- Added decision rationale, evidence, and status representation.
- Added lightweight decision supersession through the optional `supersedes` property.
- Preserved existing provenance and temporal metadata for decisions.
- Kept decision retrieval within the existing lexical relevance system.
- Deferred relationship traversal, referential integrity, automatic status updates, and conflict detection.

### Project Context

- Established project identity using the existing `EntityType.PROJECT` and Entity model.
- Established the `description` and `root_path` project property conventions.
- Added current-project resolution based on the active working directory.
- Added support for project roots and descendant directories.
- Added deterministic handling for nested and equally specific project matches.
- Added project goals as curated project context.
- Added project architecture as curated project context.
- Added project constraints as advisory project context.
- Added project requirements as advisory project context.
- Added project current state as a curated narrative snapshot.
- Excluded foreign PROJECT entities when a current project is active while keeping non-project entities eligible for retrieval.

### Pipeline

- Request Pipeline now retrieves relevant Context before reasoning.
- Request Pipeline now assembles `BrainContext`.
- Added read-only context inspection through `RequestPipeline.inspect_context()`, allowing callers to inspect the exact context assembled for a request without executing Brain reasoning or mutating memory.
- Context inspection exposes actual recorded system metadata (relevance, provenance, timestamps, confidence, and entity properties) without generating synthetic explanations.
- Preserved the Pipeline as a request-processing coordinator without direct persistent-memory access.

### Architecture

- Established separation between knowledge, context, reasoning, and action.
- Brain no longer retrieves persistent memory directly.
- Providers remain independent of the Context and Memory domain models.
- Context remains ephemeral and is not persisted as conversation history.
- Established origin provenance as part of persistent knowledge without coupling provenance to request-time relevance.
- Established temporal metadata without introducing automatic freshness policies.
- Established project identity without introducing a dedicated Project abstraction.
- Established current-project resolution within the memory retrieval boundary without introducing a separate project-resolution service.
- Established freshness as an advisory assessment rather than a retrieval or execution policy.
- Preserved `UNKNOWN` when freshness cannot be determined from available metadata.
- Established one-way decision supersession references without introducing a relationship framework.

### Testing

- Added Context model tests.
- Added ContextItem tests.
- Added lexical relevance tests.
- Added provenance model tests.
- Added provenance persistence and legacy-compatibility tests.
- Added temporal metadata tests.
- Added timestamp persistence and legacy-compatibility tests.
- Added project identity representation tests.
- Added current-project resolution tests.
- Added current-project retrieval scoping tests.
- Updated MemoryRetriever tests.
- Updated Brain tests for BrainContext and Context integration.
- Added integration coverage for temporary Context during language generation.
- Added freshness assessment tests covering fresh, stale, unknown, boundary, timezone, and immutability behavior.
- Added decision entity representation tests.
- Added decision persistence tests.
- Added decision retrieval tests.
- Added decision supersession representation tests.
- Added decision supersession persistence tests.
- Added retrieval coverage for superseding decisions.
- Added project current-state representation tests.
- Added source-aware retrieval tests covering source filtering, missing provenance, ranking preservation, and project scoping.
- Added confidence representation tests.
- Added confidence persistence and legacy-compatibility tests.
- Verified confidence does not affect retrieval ranking.

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