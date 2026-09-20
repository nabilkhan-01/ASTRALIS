from dataclasses import dataclass, field
from typing import Any

from astralis.memory.confidence import ConfidenceLevel
from astralis.memory.entity_type import EntityType
from astralis.memory.provenance import Provenance


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
    provenance: Provenance | None = None
    created_at: str | None = None
    updated_at: str | None = None
    confidence: ConfidenceLevel | None = None

    @property
    def creator(self) -> str | None:
        """Return the creator property value if present and non-empty."""
        val = self.properties.get("creator")
        if isinstance(val, str) and val.strip():
            return val.strip()
        return None