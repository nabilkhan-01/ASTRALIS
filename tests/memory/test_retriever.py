from unittest.mock import Mock

from astralis.brain.request import Request
from astralis.brain.source import RequestSource
from astralis.context.context import Context
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

    def test_retrieve_returns_context(
        self,
    ) -> None:
        """Retrieve relevant context from memory."""

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

        assert isinstance(
            result,
            Context,
        )
        assert len(result.items) == 1
        assert result.items[0].entity == entities[0]
        assert result.items[0].relevance > 0.0

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