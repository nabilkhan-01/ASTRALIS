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


def test_project_constraints() -> None:
    """Represent project constraints as a list in PROJECT Entity properties."""

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
            "constraints": [
                "Preserve provider independence",
                "Prefer simple architecture",
                "Do not modify user files without permission",
                "Avoid unnecessary external dependencies",
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
    assert len(project.properties["goals"]) == 2
    assert len(project.properties["architecture"]) == 5
    assert project.properties["constraints"] == [
        "Preserve provider independence",
        "Prefer simple architecture",
        "Do not modify user files without permission",
        "Avoid unnecessary external dependencies",
    ]
    assert project.provenance is not None
    assert project.created_at == "2026-08-27T10:00:00Z"
    assert project.updated_at == "2026-08-27T10:00:00Z"


def test_project_requirements() -> None:
    """Represent project requirements as a list in PROJECT Entity properties."""

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
            "constraints": [
                "Preserve provider independence",
                "Prefer simple architecture",
                "Do not modify user files without permission",
                "Avoid unnecessary external dependencies",
            ],
            "requirements": [
                "Context retrieval must be deterministic",
                "Providers must remain independent of Memory",
                "Users must be able to delete stored knowledge",
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
    assert len(project.properties["goals"]) == 2
    assert len(project.properties["architecture"]) == 5
    assert len(project.properties["constraints"]) == 4
    assert project.properties["requirements"] == [
        "Context retrieval must be deterministic",
        "Providers must remain independent of Memory",
        "Users must be able to delete stored knowledge",
    ]
    assert project.provenance is not None
    assert project.created_at == "2026-08-27T10:00:00Z"
    assert project.updated_at == "2026-08-27T10:00:00Z"


def test_decision_representation() -> None:
    """Represent an important decision using Entity and EntityType.DECISION."""

    provenance = Provenance(
        source_type="file",
        source_identifier="docs/decisions/001-json-storage.md",
    )

    decision = Entity(
        id="decision_json_storage",
        type=EntityType.DECISION,
        name="Use JSON entity storage",
        properties={
            "rationale": "Keep infrastructure simple and dependency-free.",
            "evidence": [
                "Small current project scale",
                "Need easy local portability",
            ],
            "status": "active",
        },
        provenance=provenance,
        created_at="2026-08-27T10:00:00Z",
        updated_at="2026-08-27T10:00:00Z",
    )

    assert decision.id == "decision_json_storage"
    assert decision.type is EntityType.DECISION
    assert decision.name == "Use JSON entity storage"
    assert (
        decision.properties["rationale"]
        == "Keep infrastructure simple and dependency-free."
    )
    assert decision.properties["evidence"] == [
        "Small current project scale",
        "Need easy local portability",
    ]
    assert decision.properties["status"] == "active"
    assert decision.provenance == provenance
    assert decision.created_at == "2026-08-27T10:00:00Z"
    assert decision.updated_at == "2026-08-27T10:00:00Z"


def test_decision_supersession_representation() -> None:
    """Represent decision supersession via the optional supersedes property."""

    older_decision = Entity(
        id="decision_json_storage",
        type=EntityType.DECISION,
        name="Use JSON entity storage",
        properties={
            "rationale": "Keep infrastructure simple and dependency-free.",
            "evidence": [
                "Small current project scale",
            ],
            "status": "superseded",
        },
    )

    newer_decision = Entity(
        id="decision_sqlite_storage",
        type=EntityType.DECISION,
        name="Use SQLite entity storage",
        properties={
            "rationale": "Need concurrency and indexing.",
            "evidence": [
                "Higher write load",
            ],
            "status": "active",
            "supersedes": "decision_json_storage",
        },
    )

    assert "supersedes" not in older_decision.properties
    assert newer_decision.properties["supersedes"] == "decision_json_storage"
    assert newer_decision.properties["status"] == "active"


def test_project_current_state() -> None:
    """Represent project current state as a string in PROJECT Entity properties."""

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
            "constraints": [
                "Preserve provider independence",
                "Prefer simple architecture",
                "Do not modify user files without permission",
                "Avoid unnecessary external dependencies",
            ],
            "requirements": [
                "Context retrieval must be deterministic",
                "Providers must remain independent of Memory",
                "Users must be able to delete stored knowledge",
            ],
            "current_state": (
                "ASTRALIS v0.4.0 Context Foundation is under active development. "
                "Core context is complete and Project Context is being expanded."
            ),
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
    assert len(project.properties["goals"]) == 2
    assert len(project.properties["architecture"]) == 5
    assert len(project.properties["constraints"]) == 4
    assert len(project.properties["requirements"]) == 3
    assert project.properties["current_state"] == (
        "ASTRALIS v0.4.0 Context Foundation is under active development. "
        "Core context is complete and Project Context is being expanded."
    )
    assert project.provenance is not None
    assert project.created_at == "2026-08-27T10:00:00Z"
    assert project.updated_at == "2026-08-27T10:00:00Z"
