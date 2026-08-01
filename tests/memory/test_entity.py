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