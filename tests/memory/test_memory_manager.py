from unittest.mock import Mock

from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
from astralis.memory.manager import MemoryManager
from astralis.memory.store import EntityStore


class TestMemoryManager:
    """Tests for the MemoryManager."""

    @staticmethod
    def _entity() -> Entity:
        """Create a test entity."""

        return Entity(
            id="user",
            type=EntityType.USER,
            name="Nabil",
        )

    def test_save(
        self,
    ) -> None:
        """Save an entity."""

        store = Mock(
            spec=EntityStore,
        )

        manager = MemoryManager(
            store,
        )

        entity = self._entity()

        manager.save(
            entity,
        )

        store.save.assert_called_once_with(
            entity,
        )

    def test_get(
        self,
    ) -> None:
        """Retrieve an entity."""

        store = Mock(
            spec=EntityStore,
        )

        entity = self._entity()

        store.get.return_value = entity

        manager = MemoryManager(
            store,
        )

        result = manager.get(
            entity.id,
        )

        assert result == entity

        store.get.assert_called_once_with(
            entity.id,
        )

    def test_delete(
        self,
    ) -> None:
        """Delete an entity."""

        store = Mock(
            spec=EntityStore,
        )

        manager = MemoryManager(
            store,
        )

        manager.delete(
            "user",
        )

        store.delete.assert_called_once_with(
            "user",
        )

    def test_get_all(
        self,
    ) -> None:
        """Retrieve all entities."""

        store = Mock(
            spec=EntityStore,
        )

        entities = [
            self._entity(),
        ]

        store.load_all.return_value = entities

        manager = MemoryManager(
            store,
        )

        result = manager.get_all()

        assert result == entities

        store.load_all.assert_called_once()