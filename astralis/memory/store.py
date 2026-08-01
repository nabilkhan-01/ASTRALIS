from abc import ABC, abstractmethod

from astralis.memory.entity import Entity


class EntityStore(
    ABC,
):
    """Defines the persistence contract for entities."""

    @abstractmethod
    def get(
        self,
        entity_id: str,
    ) -> Entity | None:
        """Return an entity by its identifier."""

    @abstractmethod
    def save(
        self,
        entity: Entity,
    ) -> None:
        """Persist an entity."""

    @abstractmethod
    def delete(
        self,
        entity_id: str,
    ) -> None:
        """Delete an entity."""

    @abstractmethod
    def load_all(
        self,
    ) -> list[Entity]:
        """Return all stored entities."""