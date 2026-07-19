# Changelog

All notable changes to ASTRALIS will be documented in this file.

The format is inspired by **Keep a Changelog** and follows **Semantic Versioning**.

---

## [Unreleased]

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
- Updated the Brain to generate execution plans before execution

#### Provider

- Introduced the provider abstraction
- Defined a common interface for AI providers
- Added MockProvider implementation
- Connected the Brain to the provider abstraction
- Added ProviderFactory
- Introduced configuration-based provider selection
- Added OpenAIProvider implementation
- Extended ProviderFactory to support multiple AI providers
- Integrated OpenAI SDK
- Added OpenAI client initialization
- Implemented response generation through the OpenAI Responses API
- Added GeminiProvider implementation
- Integrated the Google Gen AI SDK
- Added support for Gemini API authentication
- Enabled real AI-powered conversations through Gemini

#### User Interface

- Introduced an interactive command-line interface
- Connected the CLI to the Brain processing pipeline

#### Configuration

- Added environment-based configuration
- Introduced support for loading AI settings from `.env`

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
- Implemented Core Engine
- Added application startup sequence
- Implemented centralized logging system
- Implemented Module Registry
- Implemented Module Loader
- Implemented Lifecycle Manager
- Implemented Health Checker

#### Brain

- Established Brain foundation
- Added Brain module
- Defined Brain public interface
- Implemented Brain integration with the Core Engine

---



Project: **ASTRALIS**

Current Release: **v0.1.0 "Foundation"**

Current Milestone: **v0.2.0 "Brain Architecture"**

Philosophy: **Assist. Don't Control.**