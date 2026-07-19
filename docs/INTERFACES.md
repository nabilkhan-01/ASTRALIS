# ASTRALIS Interfaces

## Purpose

Interfaces provide different ways for users and external systems to interact with ASTRALIS.

The Brain remains independent of any specific interface.

Every interface communicates using the same Request and Response models.

---

## Design Principles

- The Brain must remain UI-independent.
- All interfaces communicate through the Engine.
- Every request is represented by a Request object.
- Every response is represented by a Response object.
- Interfaces should never contain business logic.

---

## Planned Interfaces

### Command-Line Interface (CLI)

Status: Implemented

Used for development, debugging, and early interaction.

---

### Desktop Interface

Status: Planned

Primary user experience for ASTRALIS.

Will expose conversation, memory, tools, and system capabilities.

---

### Voice Interface

Status: Planned

Natural speech interaction through wake-word activation.

---

### Mobile Interface

Status: Planned

Lightweight companion for notifications, quick conversations, and remote access.

---

### API Interface

Status: Planned

Allows third-party applications to communicate with ASTRALIS through a stable API.