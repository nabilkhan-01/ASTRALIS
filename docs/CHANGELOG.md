# Changelog

All notable changes to ASTRALIS will be documented in this file.

The format is inspired by **Keep a Changelog** and follows **Semantic Versioning**.

---

## [Unreleased]

### Added

#### API Layer

- Introduced the API layer for external service integrations
- Added the reusable `ApiClient`
- Added GET and POST request support
- Added the `WeatherApi`
- Added the `SearchApi`
- Introduced the `WeatherData` model
- Introduced the `SearchResult` model
- Integrated the Open-Meteo API for live weather retrieval
- Integrated the Tavily Search API for web search

#### Models

- Introduced the `models` package
- Added the `Note` model
- Added the `CalendarEvent` model
- Moved `WeatherData` into the models package
- Moved `SearchResult` into the models package

#### Capability Framework

- Finalized the Capability Framework
- Updated capabilities to receive the request context

#### Capabilities

- Added Time capability
- Added Calculator capability
- Added Weather capability
- Added Search capability
- Added Notes capability
- Added Browser capability
- Added File System capability
- Added Calendar capability
- Implemented native date and time retrieval
- Implemented native arithmetic execution
- Implemented live weather retrieval
- Implemented web search
- Implemented persistent note management
- Implemented persistent calendar event management
- Implemented local file system navigation and file reading
- Implemented browser URL and shortcut launching

#### Memory System

- Introduced the Notes memory component
- Introduced the Calendar memory component
- Added persistent local note storage
- Added persistent local calendar storage
- Added note creation
- Added note listing
- Added note deletion
- Added calendar event creation
- Added calendar event listing
- Added today's event retrieval
- Added calendar event deletion
- Refactored Notes memory to use typed models instead of dictionaries

#### Tools

- Added BrowserTool
- Added FileSystemTool
- Added browser shortcut resolution
- Added local directory navigation
- Added local file listing
- Added local file reading

#### Brain

- Improved capability routing through entity-based planning
- Enhanced intent interpretation for weather requests
- Added explicit command recognition for search requests
- Added explicit command recognition for notes requests
- Added calendar command recognition
- Added entity extraction for:
  - Date
  - Time
  - Calculator
  - Weather
  - Search
  - Notes
  - Calendar

#### Testing

- Added Weather API tests
- Added Search API tests
- Added Calculator capability tests
- Added Time capability tests
- Added Weather capability tests
- Added Search capability tests
- Added Notes capability tests
- Added Browser capability tests
- Added File System capability tests
- Added Calendar capability tests
- Added Notes memory tests
- Added Calendar memory tests
- Added Browser tool tests
- Added File System tool tests

#### Engineering

- Introduced the domain models layer
- Separated domain models from API implementations
- Adopted typed models across the Memory layer
- Established a dedicated memory testing structure
- Established a dedicated models package for shared domain objects

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