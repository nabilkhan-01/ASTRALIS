import json
from pathlib import Path

from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
from astralis.memory.json_store import JsonEntityStore
from astralis.memory.provenance import Provenance


class TestJsonEntityStore:
    """Tests for the JsonEntityStore."""

    @staticmethod
    def _entity() -> Entity:
        """Create a test entity."""

        return Entity(
            id="user",
            type=EntityType.USER,
            name="Nabil",
            properties={
                "language": "Java",
            },
        )

    def test_save_and_recall(
        self,
        tmp_path: Path,
    ) -> None:
        """Save and recall an entity."""

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )

        entity = self._entity()

        store.save(
            entity,
        )

        result = store.get(
            entity.id,
        )

        assert result == entity

    def test_save_and_recall_with_provenance(
        self,
        tmp_path: Path,
    ) -> None:
        """Save and recall an entity with provenance."""

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )

        entity = Entity(
            id="adr-004",
            type=EntityType.PROJECT,
            name="Context Architecture",
            properties={
                "status": "accepted",
            },
            provenance=Provenance(
                source_type="file",
                source_identifier="docs/DECISIONS.md",
            ),
        )

        store.save(
            entity,
        )

        result = store.get(
            entity.id,
        )

        assert result == entity
        assert result is not None
        assert result.provenance == Provenance(
            source_type="file",
            source_identifier="docs/DECISIONS.md",
        )

    def test_load_legacy_entities_without_provenance(
        self,
        tmp_path: Path,
    ) -> None:
        """Load legacy JSON file where entities lack a provenance field."""

        file_path = tmp_path / "memory.json"
        file_path.write_text(
            json.dumps(
                [
                    {
                        "id": "legacy_project",
                        "type": "project",
                        "name": "Legacy Project",
                        "properties": {
                            "version": "1.0",
                        },
                    },
                ],
            ),
            encoding="utf-8",
        )

        store = JsonEntityStore(
            file_path,
        )

        entities = store.load_all()

        assert len(
            entities,
        ) == 1
        assert entities[0].id == "legacy_project"
        assert entities[0].provenance is None

    def test_recall_missing_entity(
        self,
        tmp_path: Path,
    ) -> None:
        """Return None for an unknown entity."""

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )

        assert store.get(
            "missing",
        ) is None

    def test_update_existing_entity(
        self,
        tmp_path: Path,
    ) -> None:
        """Update an existing entity."""

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )

        entity = self._entity()

        store.save(
            entity,
        )

        updated = Entity(
            id="user",
            type=EntityType.USER,
            name="Nabil",
            properties={
                "language": "Python",
            },
        )

        store.save(
            updated,
        )

        result = store.get(
            "user",
        )

        assert result == updated

        assert len(
            store.load_all(),
        ) == 1

    def test_delete_entity(
        self,
        tmp_path: Path,
    ) -> None:
        """Delete an entity."""

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )

        entity = self._entity()

        store.save(
            entity,
        )

        store.delete(
            entity.id,
        )

        assert store.get(
            entity.id,
        ) is None

    def test_load_all(
        self,
        tmp_path: Path,
    ) -> None:
        """Load every stored entity."""

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )

        entity = self._entity()

        store.save(
            entity,
        )

        entities = store.load_all()

        assert len(
            entities,
        ) == 1

        assert entities[0] == entity

    def test_empty_store(
        self,
        tmp_path: Path,
    ) -> None:
        """Return an empty list for a new store."""

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )

        assert store.load_all() == []