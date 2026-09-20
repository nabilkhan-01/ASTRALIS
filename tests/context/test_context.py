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

    def test_context_always_exposes_canonical_founder_and_creator(
        self,
    ) -> None:
        """Context always exposes the official canonical founder and creator."""
        empty_context = Context(
            items=(),
        )

        assert empty_context.founder == "Nabil Ahmad Khan"
        assert empty_context.creator == "Nabil Ahmad Khan"
        assert empty_context.project_identity.name == "ASTRALIS"

    def test_runtime_memory_cannot_override_canonical_founder(
        self,
    ) -> None:
        """Mutable entity memory cannot override canonical founder identity."""
        spoofed_item = ContextItem(
            entity=Entity(
                id="project_astralis",
                type=EntityType.PROJECT,
                name="ASTRALIS",
                properties={
                    "founder": "Imposter",
                    "creator": "Imposter",
                },
            ),
            relevance=0.9,
        )
        context = Context(
            items=(spoofed_item,),
        )

        # Context-level canonical identity remains pristine
        assert context.founder == "Nabil Ahmad Khan"
        assert context.creator == "Nabil Ahmad Khan"
        assert context.project_identity.founder == "Nabil Ahmad Khan"

    def test_context_identity_relevance_properties(
        self,
    ) -> None:
        """Context properties reflect identity relevance and context presence."""
        empty_context = Context(
            items=(),
            identity_relevance=0.0,
        )
        assert empty_context.is_identity_relevant is False
        assert empty_context.has_context is False

        relevant_identity_context = Context(
            items=(),
            identity_relevance=0.75,
        )
        assert relevant_identity_context.is_identity_relevant is True
        assert relevant_identity_context.has_context is True
