from dataclasses import FrozenInstanceError

import pytest

from astralis.context.context import Context
from astralis.context.context_item import ContextItem
from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType


class TestContext:
    """Tests for Context."""

    @staticmethod
    def _item(
        entity_id: str,
    ) -> ContextItem:
        """Create a context item."""

        return ContextItem(
            entity=Entity(
                id=entity_id,
                type=EntityType.PROJECT,
                name="ASTRALIS",
            ),
            relevance=0.5,
        )

    def test_create_context(
        self,
    ) -> None:
        """Create a context."""

        items = (
            self._item(
                "project",
            ),
        )

        context = Context(
            items=items,
        )

        assert context.items == items

    def test_context_preserves_item_order(
        self,
    ) -> None:
        """Preserve the order of context items."""

        first = self._item(
            "first",
        )
        second = self._item(
            "second",
        )

        context = Context(
            items=(
                first,
                second,
            ),
        )

        assert context.items == (
            first,
            second,
        )

    def test_context_is_immutable(
        self,
    ) -> None:
        """Prevent context field reassignment because Context is frozen."""

        context = Context(
            items=(),
        )

        with pytest.raises(
            FrozenInstanceError,
        ):
            context.items = ()

    def test_context_items_is_immutable_tuple(
        self,
    ) -> None:
        """Context items is an immutable tuple."""

        item = self._item(
            "item_1",
        )

        context = Context(
            items=(
                item,
            ),
        )

        assert isinstance(
            context.items,
            tuple,
        )
