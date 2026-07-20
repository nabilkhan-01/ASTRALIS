# ASTRALIS Interfaces

## Purpose

Interfaces are different ways for users and external systems to interact with ASTRALIS.

Regardless of how a request arrives, it should be processed by the same Brain.

The interface changes.

The intelligence does not.

---

## Design Principles

- The Brain must remain completely interface-independent.
- Every interface communicates through the Engine.
- Every request is represented using the Request model.
- Every response is represented using the Response model.
- Interfaces must never contain business logic.
- New interfaces should be added without modifying the Brain.
- Users should experience the same ASTRALIS regardless of the interface they choose.

---

## Planned Interfaces

### Command-Line Interface (CLI)

**Status:** Implemented

Used for development, debugging, testing, and engineering.

Provides the fastest way to experiment with new capabilities.

---

### Desktop Interface

**Status:** Planned

The primary experience for ASTRALIS.

Features may include:

- Natural conversations
- Memory management
- Capabilities
- Notifications
- Project awareness
- Settings
- Permission management

---

### Voice Interface

**Status:** Planned

Natural speech interaction.

Goals:

- Wake word
- Continuous conversation
- Low-latency responses
- Hands-free operation

The voice interface should feel like speaking naturally with ASTRALIS rather than issuing commands.

---

### Mobile Interface

**Status:** Planned

Companion application.

Goals:

- Notifications
- Quick conversations
- Remote access
- Synchronization
- Emergency interactions

The mobile interface complements the desktop experience rather than replacing it.

---

### API Interface

**Status:** Planned

Provides a stable interface for third-party applications.

Potential uses:

- Automation
- Plugins
- Integrations
- Custom applications

---

### Web Interface

**Status:** Future

Browser-based access to ASTRALIS.

Useful for remote access and lightweight usage without requiring installation.

---

## Long-Term Vision

ASTRALIS should not depend on a single interface.

Users should be able to interact through:

- Keyboard
- Voice
- Touch
- APIs
- Future interfaces

while experiencing the same intelligence, memory, and personality.

Changing the interface should never change who ASTRALIS is.

---

Project: **ASTRALIS**

Philosophy:

> **Assist. Don't Control.**