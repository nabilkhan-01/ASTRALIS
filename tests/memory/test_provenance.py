from dataclasses import FrozenInstanceError

import pytest

from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
from astralis.memory.provenance import Provenance


class TestProvenance:
    """Tests for Provenance."""

    def test_create_provenance(
        self,
    ) -> None:
        """Create a provenance record."""

        provenance = Provenance(
            source_type="file",
            source_identifier="docs/ARCHITECTURE.md",
        )

        assert provenance.source_type == "file"
        assert provenance.source_identifier == "docs/ARCHITECTURE.md"

    def test_provenance_is_immutable(
        self,
    ) -> None:
        """Prevent provenance mutation."""

        provenance = Provenance(
            source_type="user",
            source_identifier="manual",
        )

        with pytest.raises(
            FrozenInstanceError,
        ):
            provenance.source_type = "file"

    def test_entity_without_provenance_defaults_to_none(
        self,
    ) -> None:
        """Entity created without provenance defaults to None."""

        entity = Entity(
            id="e1",
            type=EntityType.PROJECT,
            name="ASTRALIS",
        )

        assert entity.provenance is None

    def test_entity_with_provenance(
        self,
    ) -> None:
        """Entity stores associated provenance."""

        provenance = Provenance(
            source_type="git",
            source_identifier="commit:abcdef",
        )

        entity = Entity(
            id="e2",
            type=EntityType.NOTE,
            name="Release Note",
            provenance=provenance,
        )

        assert entity.provenance == provenance
