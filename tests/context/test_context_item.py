from dataclasses import FrozenInstanceError

import pytest

from astralis.context.context_item import ContextItem
from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType


class TestContextItem:
    """Tests for ContextItem."""

    @staticmethod
    def _entity() -> Entity:
        """Create an entity."""

        return Entity(
            id="project",
            type=EntityType.PROJECT,
            name="ASTRALIS",
        )

    def test_create_context_item(
        self,
    ) -> None:
        """Create a context item."""

        entity = self._entity()

        item = ContextItem(
            entity=entity,
            relevance=0.5,
        )

        assert item.entity is entity
        assert item.relevance == 0.5

    def test_relevance_boundaries(
        self,
    ) -> None:
        """Store relevance boundary values."""

        entity = self._entity()

        lower = ContextItem(
            entity=entity,
            relevance=0.0,
        )
        upper = ContextItem(
            entity=entity,
            relevance=1.0,
        )

        assert lower.relevance == 0.0
        assert upper.relevance == 1.0

    def test_context_item_is_immutable(
        self,
    ) -> None:
        """Prevent context item mutation."""

        item = ContextItem(
            entity=self._entity(),
            relevance=0.5,
        )

        with pytest.raises(
            FrozenInstanceError,
        ):
            item.relevance = 1.0
