from unittest.mock import Mock

from astralis.brain.request import Request
from astralis.brain.source import RequestSource
from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
from astralis.memory.manager import MemoryManager
from astralis.memory.retriever import MemoryRetriever


class TestMemoryRetriever:
    """Tests for the MemoryRetriever."""

    @staticmethod
    def _request() -> Request:
        """Create a test request."""

        return Request(
            text="Tell me about ASTRALIS.",
            source=RequestSource.CLI,
        )

    @staticmethod
    def _entities() -> list[Entity]:
        """Create test entities."""

        return [
            Entity(
                id="project",
                type=EntityType.PROJECT,
                name="ASTRALIS",
            ),
        ]

    def test_retrieve_returns_entities(
        self,
    ) -> None:
        """Retrieve entities from memory."""

        memory = Mock(
            spec=MemoryManager,
        )

        entities = self._entities()

        memory.get_all.return_value = entities

        retriever = MemoryRetriever(
            memory,
        )

        result = retriever.retrieve(
            self._request(),
        )

        assert result == entities

    def test_retrieve_calls_memory_manager(
        self,
    ) -> None:
        """Retrieve entities through the memory manager."""

        memory = Mock(
            spec=MemoryManager,
        )

        memory.get_all.return_value = []

        retriever = MemoryRetriever(
            memory,
        )

        retriever.retrieve(
            self._request(),
        )

        memory.get_all.assert_called_once_with()