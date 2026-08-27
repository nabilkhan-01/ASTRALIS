import json
from pathlib import Path

from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
from astralis.memory.provenance import Provenance
from astralis.memory.store import EntityStore


class JsonEntityStore(
    EntityStore,
):
    """Stores entities in a JSON file."""

    def __init__(
        self,
        path: Path,
    ) -> None:
        self._path = path

        if not self._path.exists():
            self._path.write_text(
                "[]",
                encoding="utf-8",
            )

    def get(
        self,
        entity_id: str,
    ) -> Entity | None:
        for entity in self.load_all():
            if entity.id == entity_id:
                return entity

        return None

    def save(
        self,
        entity: Entity,
    ) -> None:
        entities = self.load_all()

        for index, existing in enumerate(
            entities,
        ):
            if existing.id == entity.id:
                entities[index] = entity
                self._write(
                    entities,
                )
                return

        entities.append(
            entity,
        )

        self._write(
            entities,
        )

    def delete(
        self,
        entity_id: str,
    ) -> None:
        entities = [
            entity
            for entity in self.load_all()
            if entity.id != entity_id
        ]

        self._write(
            entities,
        )

    def load_all(
        self,
    ) -> list[Entity]:
        data = json.loads(
            self._path.read_text(
                encoding="utf-8",
            ),
        )

        return [
            Entity(
                id=item["id"],
                type=EntityType(
                    item["type"],
                ),
                name=item["name"],
                properties=item.get(
                    "properties",
                    {},
                ),
                provenance=Provenance(
                    source_type=item["provenance"]["source_type"],
                    source_identifier=item["provenance"]["source_identifier"],
                )
                if item.get("provenance") is not None
                else None,
                created_at=item.get(
                    "created_at",
                ),
                updated_at=item.get(
                    "updated_at",
                ),
            )
            for item in data
        ]

    def _write(
        self,
        entities: list[Entity],
    ) -> None:
        serialized: list[dict[str, object]] = []

        for entity in entities:
            item_data: dict[str, object] = {
                "id": entity.id,
                "type": entity.type.value,
                "name": entity.name,
                "properties": entity.properties,
            }

            if entity.provenance is not None:
                item_data["provenance"] = {
                    "source_type": entity.provenance.source_type,
                    "source_identifier": entity.provenance.source_identifier,
                }

            if entity.created_at is not None:
                item_data["created_at"] = entity.created_at

            if entity.updated_at is not None:
                item_data["updated_at"] = entity.updated_at

            serialized.append(
                item_data,
            )

        self._path.write_text(
            json.dumps(
                serialized,
                indent=4,
            ),
            encoding="utf-8",
        )