from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType


def test_create_entity() -> None:
    """Create an entity."""

    entity = Entity(
        id="user",
        type=EntityType.USER,
        name="Nabil",
    )

    assert entity.id == "user"
    assert entity.type is EntityType.USER
    assert entity.name == "Nabil"
    assert entity.properties == {}
    assert entity.provenance is None
    assert entity.created_at is None
    assert entity.updated_at is None


def test_entity_properties() -> None:
    """Store entity properties."""

    entity = Entity(
        id="project",
        type=EntityType.PROJECT,
        name="ASTRALIS",
        properties={
            "language": "Python",
        },
    )

    assert entity.properties["language"] == "Python"


def test_entity_with_created_at() -> None:
    """Store created_at timestamp on entity."""

    entity = Entity(
        id="project",
        type=EntityType.PROJECT,
        name="ASTRALIS",
        created_at="2026-08-27T10:00:00Z",
    )

    assert entity.created_at == "2026-08-27T10:00:00Z"
    assert entity.updated_at is None


def test_entity_with_updated_at() -> None:
    """Store updated_at timestamp on entity."""

    entity = Entity(
        id="project",
        type=EntityType.PROJECT,
        name="ASTRALIS",
        created_at="2026-08-27T10:00:00Z",
        updated_at="2026-08-27T10:05:00Z",
    )

    assert entity.created_at == "2026-08-27T10:00:00Z"
    assert entity.updated_at == "2026-08-27T10:05:00Z"