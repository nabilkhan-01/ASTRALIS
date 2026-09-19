# Changelog

All notable changes to ASTRALIS are documented here.

This project follows Semantic Versioning.

---

# Not Released

## Added

- `LocalProvider` abstract base class for local reasoning runtimes (`astralis/providers/local.py`)
  - Extends existing `Provider` abstraction and keeps `generate()` abstract for concrete runtimes
  - Exposes `model`, normalized `host` endpoint, and `is_local = True` flag
  - Reusable helper for local runtime connection/unavailability failures returning standard `Response(success=False)`
- Centralized configuration for local runtimes in `Config` (`ollama_host`, `ollama_model`, `ollama_timeout`, `ollama_reasoning_mode`) reading `OLLAMA_HOST`, `OLLAMA_MODEL`, `OLLAMA_TIMEOUT`, and `OLLAMA_REASONING_MODE` environment variables with neutral defaults and safe validation
- Provider-independent `ReasoningMode` abstraction (`FAST`, `DEEP`, `AUTO`) in `astralis/providers/reasoning.py`
  - Local reasoning is now configurable through reasoning modes
  - `FAST` and `DEEP` explicitly control local thinking where supported (`think: false` and `think: true` respectively in Ollama)
  - `AUTO` is the default reasoning mode; until task-aware routing is implemented, AUTO safely uses FAST local inference (`think: false`)
  - Future routing will allow AUTO to select FAST or DEEP according to task requirements
  - Automatic routing is NOT implemented in this step and will be introduced in a future v0.5.0 routing phase
- `OllamaProvider` concrete local AI provider (`astralis/providers/ollama.py`)
  - Subclasses `LocalProvider` to communicate directly with local Ollama HTTP API (`/api/chat`)
  - Maps ASTRALIS `Conversation`, `Message`, and `Role` models 1:1 to Ollama chat payload
  - Injects the shared ASTRALIS `SYSTEM_PROMPT` as the initial system message to guide concise, identity-aligned responses
  - Configurable request timeout (defaults to 60 seconds) to accommodate local inference speeds
  - Configurable local reasoning mode (`ReasoningMode`) translating into top-level `think` API parameter (`think: false` for FAST and AUTO, `think: true` for DEEP)
  - Robust exception and error handling translating network and HTTP errors into `Response(success=False)` without exposing raw exceptions
  - Registered in `ProviderFactory` under `"ollama"` key using configured host, model, timeout, and reasoning mode parameters


# [v0.4.0] - Context Foundation

## 🚀 Highlights

- Introduced the Context Foundation for persistent, trusted, request-aware context.
- Added structured project and decision context.
- Added deterministic context retrieval, filtering, prioritization, and provenance.
- Added context freshness, confidence, conflict detection, inspection, and deletion.
- Strengthened separation between knowledge, context, reasoning, and action.

## Added

- Context and ContextItem models
- Deterministic lexical relevance and context ranking
- Relevant context retrieval from persistent memory
- Project identity and current-project resolution
- Project goals, architecture, constraints, requirements, and current state
- Decision entities with rationale, evidence, status, and supersession
- Context provenance and temporal metadata
- Freshness assessment with `FRESH`, `STALE`, and `UNKNOWN` states
- Explicit confidence levels: `HIGH`, `MEDIUM`, and `LOW`
- Structural conflicting-context detection
- Source-aware context retrieval
- Read-only context inspection through `RequestPipeline.inspect_context()`
- Caller-controlled context updates through `MemoryManager.save()`
- Caller-controlled context deletion through `MemoryManager.delete()`

## Improved

- Brain now reasons over assembled request-scoped Context through `BrainContext`
- Context retrieval now prioritizes relevant information instead of exposing all stored knowledge
- Retrieval supports project scoping and source filtering
- Context metadata now preserves provenance, timestamps, confidence, and decision state
- Context lifecycle is explicitly request-scoped and separated from persistent Memory
- Memory updates and deletion remain explicitly controlled by the caller
- Context inspection is available without executing Brain reasoning
- Stale and conflicting context can be identified without automatic mutation
- Added comprehensive automated test coverage for Context, Memory, Pipeline, and Brain integration

## Refactored

- Established clear separation between knowledge, context, reasoning, and action
- Kept persistent Memory separate from ephemeral request-scoped Context
- Kept the Brain independent of persistent memory storage
- Extended the existing Entity model for project and decision context without introducing unnecessary domain abstractions
- Added context trust metadata without coupling it directly to retrieval ranking or execution policy
- Preserved provider independence from Context and Memory implementations

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

**Current Release:** **v0.4.0 – Context Foundation**

**Next Milestone:** **v0.5.0 – Local Intelligence**

**Philosophy:**

> **Assist. Don't Control.**