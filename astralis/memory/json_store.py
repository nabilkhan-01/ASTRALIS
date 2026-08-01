import json
from pathlib import Path

from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
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
            )
        )

        return [
            Entity(
                id=item["id"],
                type=EntityType(
                    item["type"],
                ),
                name=item["name"],
                properties=item["properties"],
            )
            for item in data
        ]

    def _write(
        self,
        entities: list[Entity],
    ) -> None:
        self._path.write_text(
            json.dumps(
                [
                    {
                        "id": entity.id,
                        "type": entity.type.value,
                        "name": entity.name,
                        "properties": entity.properties,
                    }
                    for entity in entities
                ],
                indent=4,
            ),
            encoding="utf-8",
        )