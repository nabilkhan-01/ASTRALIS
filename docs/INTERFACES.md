# ASTRALIS Interfaces

## Purpose

Interfaces define how users and external systems interact with ASTRALIS.

Regardless of where a request originates, it follows the same processing pipeline and reaches the same Brain.

The interface changes.

The intelligence does not.

---

## Design Principles

- The Brain must remain completely interface-independent.
- Interfaces communicate through the Application.
- Every request is represented by a `Request`.
- Every response is represented by a `Response`.
- Interfaces must never contain business logic.
- New interfaces should be added without modifying the Brain.
- Users should experience consistent behavior across every interface.

---

## Current Interface

### Command-Line Interface (CLI)

**Status:** Implemented

The CLI is the primary interface for development, testing, and debugging.

It provides direct access to every capability while keeping the interaction simple and lightweight.

---

## Planned Interfaces

### Desktop

**Status:** Planned

The primary long-term interface for ASTRALIS.

Potential features:

- Natural conversations
- Memory management
- Capability management
- Notifications
- Project awareness
- Settings
- Permission management

---

### Voice

**Status:** Planned

Natural speech interaction.

Goals:

- Wake word
- Continuous conversations
- Low-latency responses
- Hands-free operation

The experience should feel conversational rather than command-driven.

---

### Mobile

**Status:** Planned

A companion application providing:

- Notifications
- Quick conversations
- Remote access
- Synchronization
- Emergency interactions

The mobile experience complements the desktop application rather than replacing it.

---

### API

**Status:** Planned

Provides a stable interface for:

- External applications
- Automation
- Plugins
- System integrations

---

### Web

**Status:** Future

Provides browser-based access without requiring local installation.

---

## Long-Term Vision

ASTRALIS should remain independent of any single interface.

Whether users interact through:

- Keyboard
- Voice
- Touch
- APIs
- Future interfaces

they should experience the same Brain, memory, capabilities, and philosophy.

Changing the interface should never change how ASTRALIS thinks.

---

**Current Release:** **v0.3.0 – Capability Platform**

**Next Milestone:** **v0.4.0 – Memory**

**Philosophy:**

> **Assist. Don't Control.**