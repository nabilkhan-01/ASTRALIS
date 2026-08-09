# ASTRALIS

> **Assist. Don't Control.**

**Current Release:** `v0.3.1 – Engineering Stability`  
**Current Milestone:** `v0.4.0 – Context Foundation`

ASTRALIS is a research and engineering project focused on building a personal AI Operating System that assists people while respecting their autonomy, privacy, and decisions.

Rather than becoming another chatbot, ASTRALIS is designed as a modular AI system capable of reasoning, planning, remembering, and interacting with the world through independent capabilities while ensuring the user always remains in control.

---

# Philosophy

ASTRALIS is built around one guiding principle:

> **Assist. Don't Control.**

Its purpose is to make people more capable—not more dependent.

Every architectural and engineering decision should reinforce this philosophy.

---

# Vision

Build an intelligence that:

- Assists rather than controls
- Protects user privacy
- Explains important decisions
- Learns responsibly over time
- Evolves through modular engineering
- Respects user autonomy

The long-term goal is to build an AI Operating System that people trust—not just another AI.

---

# Current Status

🚧 **Active Development**

## Completed

- ✅ Core Engine
- ✅ Brain Architecture
- ✅ Bootstrap & Dependency Injection
- ✅ Capability Platform
- ✅ Persistent Memory Foundation
- ✅ MemoryManager
- ✅ MemoryRetriever
- ✅ BrainContext
- ✅ Context Foundation
- ✅ Entity-based Knowledge Model
- ✅ External API Integrations
- ✅ Gemini, OpenAI & Mock Providers
- ✅ Browser & File System Tools
- ✅ Automated Testing
- ✅ Static Analysis (Ruff & MyPy)
- ✅ Project Documentation

## Current Focus

### v0.4.0 — Context Foundation

The current milestone focuses on building the foundation for trusted, persistent context.

Completed:

- [x] Entity-based Memory
- [x] EntityStore abstraction
- [x] JSON Entity Store
- [x] MemoryManager
- [x] MemoryRetriever
- [x] BrainContext
- [x] ContextItem
- [x] Context model

Planned:

- [ ] Context relevance
- [ ] Context provenance
- [ ] Context freshness
- [ ] Context lifecycle
- [ ] Project context
- [ ] Decision context
- [ ] Relevant context retrieval
- [ ] Context inspection and control
- [ ] Conflict detection

The goal is to allow ASTRALIS to provide humans and AI agents with the right context at the right time while preserving enough history and provenance to understand why that context can be trusted.

---

# Architecture

ASTRALIS follows a modular architecture built around clearly separated responsibilities.

```text
User
 │
 ▼
Interface
 │
 ▼
Request Pipeline
 │
 ▼
Memory
 │
 ▼
Context
 │
 ▼
BrainContext
 │
 ▼
Brain
 │
 ▼
Capability Manager
 │
 ▼
Capabilities
 │
 ├── Providers
 ├── Tools
 └── External Services
```

For a detailed overview, see **docs/architecture.md**.

---

# Project Structure

```text
ASTRALIS/
├── assets/
├── astralis/
│   ├── api/
│   ├── automation/
│   ├── bootstrap/
│   ├── brain/
│   ├── capability/
│   ├── context/
│   ├── core/
│   ├── interfaces/
│   ├── memory/
│   ├── models/
│   ├── monitoring/
│   ├── pipeline/
│   ├── providers/
│   ├── security/
│   ├── storage/
│   ├── tools/
│   ├── utils/
│   ├── vision/
│   ├── voice/
│   └── __init__.py
├── data/
├── docs/
├── scripts/
├── tests/
├── .env.example
├── main.py
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

# Documentation

Documentation is available in the **docs/** directory.

- Architecture
- Changelog
- Contributing Guide
- Architecture Decision Records (ADRs)
- Founder's Note
- Future Decisions
- History
- Interfaces
- Engineering Principles
- Roadmap

---

# Engineering Workflow

Every feature follows the same workflow:

1. Design
2. Implement
3. Test
4. Review
5. Document
6. Release

Design decisions always precede implementation.

---

# Engineering Principles

ASTRALIS emphasizes:

- Clean Architecture
- Modularity
- Dependency Injection
- Separation of Responsibilities
- Maintainability
- Testability
- Transparency
- Human-Centered AI
- User Autonomy

---

# Long-Term Goals

ASTRALIS is being built to:

- Understand natural language
- Maintain useful persistent knowledge
- Provide relevant context
- Learn responsibly from user interactions
- Plan before acting
- Reason through complex problems
- Interact safely with computers
- Respect privacy by design
- Assist without replacing human judgment

Every release should strengthen the existing architecture rather than replace it.

---

# Quality Standards

Every contribution should maintain:

- ✅ Automated testing
- ✅ Ruff compliance
- ✅ MyPy compliance
- ✅ Modular architecture
- ✅ Dependency Injection
- ✅ Comprehensive documentation

Run all quality checks before committing:

```bash
python scripts/check.py
```

---

# Roadmap

Current milestone:

**v0.4.0 — Context Foundation**

Upcoming milestones:

- Automation
- Voice
- Vision
- Context
- Reasoning
- AI Operating System

See **docs/roadmap.md** for the complete roadmap.

---

> *"Build an intelligence people trust—not just another AI."*