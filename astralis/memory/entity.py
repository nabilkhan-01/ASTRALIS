from dataclasses import dataclass, field
from typing import Any

from astralis.memory.entity_type import EntityType


@dataclass(
    slots=True,
)
class Entity:
    """Represents a persistent entity known to ASTRALIS."""

    id: str
    type: EntityType
    name: str
    properties: dict[str, Any] = field(
        default_factory=dict,
    )