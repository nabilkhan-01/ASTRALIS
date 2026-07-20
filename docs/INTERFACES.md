# ASTRALIS Interfaces

## Purpose

Interfaces are different ways for users and external systems to interact with ASTRALIS.

Regardless of how a request arrives, it should be processed by the same Brain.

The interface changes.

The intelligence does not.

---

## Design Principles

- The Brain must remain completely interface-independent.
- Every interface communicates through the Core Engine.
- Every request is represented using the Request model.
- Every response is represented using the Response model.
- Interfaces must never contain business logic.
- New interfaces should be added without modifying the Brain.
- Users should experience the same ASTRALIS regardless of the interface they choose.

---

## Interfaces

### Command-Line Interface (CLI)

**Status:** Implemented

Used for development, debugging, testing, and engineering.

Provides the fastest way to develop and validate new capabilities.

---

### Desktop Interface

**Status:** Planned

The primary experience for ASTRALIS.

Potential capabilities include:

- Natural conversations
- Memory management
- Capability management
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

The experience should feel like talking with ASTRALIS rather than issuing commands.

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

Provides a stable interface for third-party applications and future integrations.

Potential uses:

- Automation
- Plugins
- External applications
- System integrations

---

### Web Interface

**Status:** Future

Provides lightweight browser-based access to ASTRALIS without requiring installation.

---

## Long-Term Vision

ASTRALIS should not depend on a single interface.

Whether users interact through:

- Keyboard
- Voice
- Touch
- APIs
- Future interfaces

they should experience the same intelligence, memory, capabilities, and personality.

Changing the interface should never change who ASTRALIS is.

---

Project: **ASTRALIS**

Current Release: **v0.2.0 "Brain Architecture"**

Current Milestone: **v0.3.0 "Capabilities"**

Philosophy:

> **Assist. Don't Control.**