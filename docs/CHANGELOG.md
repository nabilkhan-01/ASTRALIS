# Changelog

All notable changes to ASTRALIS will be documented in this file.

The format is inspired by **Keep a Changelog** and follows **Semantic Versioning**.

---

## [Unreleased]

### Added

#### Capability Framework

- Introduced the Capability Framework
- Added Capability Registry and Capability Manager
- Added Language and Time capabilities
- Enabled execution planning through capabilities
- Implemented the first native capability independent of AI providers
- Finalized the Capability Framework
- Updated capabilities to receive request context
- Added Calculator capability
- Added native arithmetic execution

---

## [v0.2.0] - Brain Architecture

### Added

#### Brain

- Introduced the Request model
- Added the RequestSource enumeration
- Updated the Brain interface to process `Request` objects
- Introduced the Response model
- Updated the Brain interface to return `Response` objects
- Established the Brain processing pipeline
- Defined validation, interpretation, planning, and execution stages
- Introduced the ExecutionPlan model
- Introduced the Planner component
- Extracted execution planning from the Brain into the Planner
- Introduced the Intent enumeration
- Added the Interpretation model
- Introduced the Interpreter component
- Delegated request interpretation from the Brain to the Interpreter
- Implemented rule-based intent recognition
- Introduced the Conversation model
- Added Message and Role models
- Moved conversation ownership to the Brain
- Added session-based conversation history
- Updated the Brain to maintain conversation state
- Simplified the Brain into an orchestration component

#### Capability Framework

- Introduced the Capability abstraction
- Added the CapabilityType enumeration
- Implemented the CapabilityRegistry
- Implemented the CapabilityManager
- Introduced the LanguageCapability
- Refactored execution routing through the Capability Framework
- Decoupled the Brain from language providers

#### Provider

- Introduced the provider abstraction
- Defined a common interface for AI providers
- Added MockProvider implementation
- Added ProviderFactory
- Introduced configuration-based provider selection
- Added OpenAIProvider implementation
- Integrated the OpenAI SDK
- Implemented response generation through the OpenAI Responses API
- Added GeminiProvider implementation
- Integrated the Google Gen AI SDK
- Added Gemini API authentication
- Added shared provider system prompt
- Updated providers to consume Conversation objects
- Separated provider implementation from conversation state
- Introduced provider-independent conversation management
- Improved provider error handling

#### User Interface

- Introduced an interactive command-line interface
- Connected the CLI to the Brain processing pipeline

#### Configuration

- Added environment-based configuration
- Introduced support for loading AI settings from `.env`
- Added provider-specific configuration
- Added Gemini model configuration
- Added OpenAI model configuration

#### Documentation

- Expanded project architecture documentation
- Updated the engineering principles
- Updated the roadmap
- Updated architectural decisions (ADR)
- Updated future architectural decisions
- Added interface documentation
- Updated project history
- Updated changelog
- Synchronized documentation with the Capability Framework

---

## [v0.1.0] - Foundation

### Added

#### Project Foundation

- Initialized project repository
- Established project structure
- Added Founder's Note
- Defined engineering principles
- Created core project documentation
  - README
  - Architecture
  - Roadmap
  - Decisions (ADR)
  - Changelog
  - Future Decisions

#### Core Infrastructure

- Implemented centralized configuration system
- Implemented the Core Engine
- Added application startup sequence
- Implemented centralized logging system
- Implemented Module Registry
- Implemented Module Loader
- Implemented Lifecycle Manager
- Implemented Health Checker

#### Brain

- Established Brain foundation
- Added the Brain module
- Defined the Brain public interface
- Implemented Brain integration with the Core Engine

---

Project: **ASTRALIS**

Current Release: **v0.2.0 "Brain Architecture"**

Current Milestone: **v0.3.0 "Capabilities"**

Philosophy: **Assist. Don't Control.**