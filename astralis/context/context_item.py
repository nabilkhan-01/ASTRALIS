from dataclasses import dataclass

from astralis.memory.entity import Entity


@dataclass(
    frozen=True,
    slots=True,
)
class ContextItem:
    """Represents an entity included in request context."""

    entity: Entity
    relevance: float
