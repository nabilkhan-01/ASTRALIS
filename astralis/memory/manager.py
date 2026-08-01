from astralis.memory.entity import Entity
from astralis.memory.store import EntityStore


class MemoryManager:
    """Coordinates persistent memory operations."""

    def __init__(
        self,
        store: EntityStore,
    ) -> None:
        self._store = store

    def save(
        self,
        entity: Entity,
    ) -> None:
        """Store or update an entity."""

        self._store.save(
            entity,
        )

    def get(
        self,
        entity_id: str,
    ) -> Entity | None:
        """Return an entity by its identifier."""

        return self._store.get(
            entity_id,
        )

    def delete(
        self,
        entity_id: str,
    ) -> None:
        """Remove an entity."""

        self._store.delete(
            entity_id,
        )

    def get_all(
        self,
    ) -> list[Entity]:
        """Return all remembered entities."""

        return self._store.load_all()