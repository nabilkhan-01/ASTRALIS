from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
from astralis.memory.provenance import Provenance


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

def test_project_identity_representation() -> None:
    """Represent project identity using Entity and EntityType.PROJECT."""

    provenance = Provenance(
        source_type="file",
        source_identifier="workspace_root",
    )

    project = Entity(
        id="project_astralis",
        type=EntityType.PROJECT,
        name="ASTRALIS",
        properties={
            "description": "Trusted context layer for AI-powered work",
            "root_path": "D:/ASTRALIS",
        },
        provenance=provenance,
        created_at="2026-08-27T10:00:00Z",
        updated_at="2026-08-27T10:00:00Z",
    )

    assert project.id == "project_astralis"
    assert project.type is EntityType.PROJECT
    assert project.name == "ASTRALIS"
    assert (
        project.properties["description"]
        == "Trusted context layer for AI-powered work"
    )
    assert project.properties["root_path"] == "D:/ASTRALIS"
    assert project.provenance == provenance
    assert project.created_at == "2026-08-27T10:00:00Z"
    assert project.updated_at == "2026-08-27T10:00:00Z"


def test_project_goals_representation() -> None:
    """Represent project goals as a list in PROJECT Entity properties."""

    project = Entity(
        id="project_astralis",
        type=EntityType.PROJECT,
        name="ASTRALIS",
        properties={
            "description": "Trusted context layer for AI-powered work",
            "root_path": "D:/ASTRALIS",
            "goals": [
                "Build a trusted context layer",
                "Preserve user autonomy",
            ],
        },
        provenance=Provenance(
            source_type="file",
            source_identifier="workspace_root",
        ),
        created_at="2026-08-27T10:00:00Z",
        updated_at="2026-08-27T10:00:00Z",
    )

    assert project.type is EntityType.PROJECT
    assert project.properties["description"] == "Trusted context layer for AI-powered work"
    assert project.properties["root_path"] == "D:/ASTRALIS"
    assert project.properties["goals"] == [
        "Build a trusted context layer",
        "Preserve user autonomy",
    ]
    assert len(project.properties["goals"]) == 2
    assert project.provenance is not None
    assert project.created_at == "2026-08-27T10:00:00Z"
    assert project.updated_at == "2026-08-27T10:00:00Z"


def test_project_architecture_context() -> None:
    """Represent project architecture context as a list in PROJECT Entity properties."""

    project = Entity(
        id="project_astralis",
        type=EntityType.PROJECT,
        name="ASTRALIS",
        properties={
            "description": "Trusted context layer for AI-powered work",
            "root_path": "D:/ASTRALIS",
            "goals": [
                "Build a trusted context layer",
                "Preserve user autonomy",
            ],
            "architecture": [
                "Engine coordinates application lifecycle",
                "Request Pipeline assembles reasoning context",
                "Brain owns reasoning",
                "Memory manages persistent knowledge",
                "Capabilities perform actions",
            ],
        },
        provenance=Provenance(
            source_type="file",
            source_identifier="workspace_root",
        ),
        created_at="2026-08-27T10:00:00Z",
        updated_at="2026-08-27T10:00:00Z",
    )

    assert project.type is EntityType.PROJECT
    assert project.properties["description"] == "Trusted context layer for AI-powered work"
    assert project.properties["root_path"] == "D:/ASTRALIS"
    assert project.properties["goals"] == [
        "Build a trusted context layer",
        "Preserve user autonomy",
    ]
    assert project.properties["architecture"] == [
        "Engine coordinates application lifecycle",
        "Request Pipeline assembles reasoning context",
        "Brain owns reasoning",
        "Memory manages persistent knowledge",
        "Capabilities perform actions",
    ]
    assert len(project.properties["architecture"]) == 5
    assert project.provenance is not None
    assert project.created_at == "2026-08-27T10:00:00Z"
    assert project.updated_at == "2026-08-27T10:00:00Z"