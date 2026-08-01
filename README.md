# ASTRALIS

> **Assist. Don't Control.**

**Current Release:** `v0.3.1 – Engineering Stability`  
**Current Milestone:** `v0.4.0 – Memory`

ASTRALIS is an research and engineering project focused on building a personal AI Operating System that assists people while respecting their autonomy, privacy, and decisions.

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
- ✅ Memory Foundation
- ✅ Contextual Reasoning Pipeline
- ✅ BrainContext
- ✅ Entity-based Memory
- ✅ External API Integrations
- ✅ Gemini, OpenAI & Mock Providers
- ✅ Browser & File System Tools
- ✅ Automated Testing
- ✅ Static Analysis (Ruff & MyPy)
- ✅ Project Documentation

## Current Focus

### v0.4.0 — Memory

Current work includes:

- [x] Entity-based Memory
- [x] MemoryManager
- [x] MemoryRetriever
- [x] BrainContext
- [x] Contextual reasoning pipeline
- [ ] Working Memory
- [ ] Long-Term Memory
- [ ] Memory Policy
- [ ] User Profile
- [ ] Context-aware reasoning
- [ ] Preference learning
- [ ] Explainable memory

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
Memory Retrieval
 │
 ▼
Brain Context
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
 ▼
Providers / Tools / External Services
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
│   ├── core/
│   ├── interfaces/
│   ├── memory/
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

---

# Long-Term Goals

ASTRALIS is being built to:

- Understand natural language
- Remember important information
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

**v0.4.0 — Memory**

Upcoming milestones:

- Memory
- Automation
- Voice
- Vision
- Context
- Reasoning
- AI Operating System

See **docs/roadmap.md** for the complete roadmap.

---

> *"Build an intelligence people trust—not just another AI."*