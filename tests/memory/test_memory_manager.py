from pathlib import Path
from unittest.mock import Mock

from astralis.brain.brain import Brain
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.brain.source import RequestSource
from astralis.capability.manager import CapabilityManager
from astralis.memory.confidence import ConfidenceLevel
from astralis.memory.conflict import detect_conflicts
from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
from astralis.memory.json_store import JsonEntityStore
from astralis.memory.manager import MemoryManager
from astralis.memory.retriever import MemoryRetriever
from astralis.memory.store import EntityStore
from astralis.monitoring.monitor import Monitor
from astralis.pipeline.request_pipeline import RequestPipeline


class TestMemoryManager:
    """Tests for the MemoryManager."""

    @staticmethod
    def _entity() -> Entity:
        """Create a test entity."""

        return Entity(
            id="user",
            type=EntityType.USER,
            name="Nabil",
        )

    def test_save(
        self,
    ) -> None:
        """Save an entity."""

        store = Mock(
            spec=EntityStore,
        )

        manager = MemoryManager(
            store,
        )

        entity = self._entity()

        manager.save(
            entity,
        )

        store.save.assert_called_once_with(
            entity,
        )

    def test_get(
        self,
    ) -> None:
        """Retrieve an entity."""

        store = Mock(
            spec=EntityStore,
        )

        entity = self._entity()

        store.get.return_value = entity

        manager = MemoryManager(
            store,
        )

        result = manager.get(
            entity.id,
        )

        assert result == entity

        store.get.assert_called_once_with(
            entity.id,
        )

    def test_delete(
        self,
    ) -> None:
        """Delete an entity."""

        store = Mock(
            spec=EntityStore,
        )

        manager = MemoryManager(
            store,
        )

        manager.delete(
            "user",
        )

        store.delete.assert_called_once_with(
            "user",
        )

    def test_get_all(
        self,
    ) -> None:
        """Retrieve all entities."""

        store = Mock(
            spec=EntityStore,
        )

        entities = [
            self._entity(),
        ]

        store.load_all.return_value = entities

        manager = MemoryManager(
            store,
        )

        result = manager.get_all()

        assert result == entities

        store.load_all.assert_called_once()

    def test_caller_updates_project_current_state(
        self,
        tmp_path: Path,
    ) -> None:
        """Caller can explicitly update a stored project's current_state property.

        No automatic mechanism updates stored context. The caller constructs a
        revised Entity sharing the same id and saves it through MemoryManager.
        Unrelated fields must remain unchanged after the update.
        """

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )

        manager = MemoryManager(
            store,
        )

        original = Entity(
            id="project_astralis",
            type=EntityType.PROJECT,
            name="ASTRALIS",
            properties={
                "description": "An intelligent personal assistant.",
                "root_path": str(tmp_path),
                "current_state": "Context Foundation is under active development.",
            },
        )

        manager.save(
            original,
        )

        updated = Entity(
            id="project_astralis",
            type=EntityType.PROJECT,
            name="ASTRALIS",
            properties={
                "description": "An intelligent personal assistant.",
                "root_path": str(tmp_path),
                "current_state": (
                    "Context Foundation is complete. "
                    "Trust and Safety features are being expanded."
                ),
            },
        )

        manager.save(
            updated,
        )

        result = manager.get(
            "project_astralis",
        )

        assert result is not None
        assert result.properties["current_state"] == (
            "Context Foundation is complete. "
            "Trust and Safety features are being expanded."
        )

        # Unrelated fields must remain unchanged
        assert result.properties["description"] == "An intelligent personal assistant."
        assert result.properties["root_path"] == str(tmp_path)
        assert result.id == "project_astralis"
        assert result.type is EntityType.PROJECT
        assert result.name == "ASTRALIS"

        # Only one entity must exist; save does not duplicate
        assert len(
            manager.get_all(),
        ) == 1

    def test_caller_resolves_conflict_by_updating_predecessor_status(
        self,
        tmp_path: Path,
    ) -> None:
        """Caller can resolve a detected decision conflict through explicit update.

        detect_conflicts() reports the conflict when the predecessor is still
        active. The caller explicitly updates predecessor status to 'superseded'
        through MemoryManager.save(). detect_conflicts() must then return [].
        No production code auto-resolves the conflict.
        """

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )

        manager = MemoryManager(
            store,
        )

        predecessor = Entity(
            id="decision_json_storage",
            type=EntityType.DECISION,
            name="Use JSON entity storage",
            properties={
                "status": "active",
            },
        )

        newer = Entity(
            id="decision_sqlite_storage",
            type=EntityType.DECISION,
            name="Use SQLite entity storage",
            properties={
                "status": "active",
                "supersedes": "decision_json_storage",
            },
        )

        manager.save(
            predecessor,
        )
        manager.save(
            newer,
        )

        # Conflict must be present before the caller acts
        reports_before = detect_conflicts(
            manager.get_all(),
        )

        assert len(reports_before) == 1
        assert reports_before[0].entity_b.id == "decision_json_storage"

        # Caller explicitly resolves the conflict by updating the predecessor
        resolved_predecessor = Entity(
            id="decision_json_storage",
            type=EntityType.DECISION,
            name="Use JSON entity storage",
            properties={
                "status": "superseded",
            },
        )

        manager.save(
            resolved_predecessor,
        )

        # Conflict must be gone after the explicit caller update
        reports_after = detect_conflicts(
            manager.get_all(),
        )

        assert reports_after == []

    def test_caller_updates_entity_confidence(
        self,
        tmp_path: Path,
    ) -> None:
        """Caller can explicitly update confidence on a stored entity.

        Confidence is not inferred or auto-assigned. The caller constructs
        a revised Entity with the new ConfidenceLevel and saves it.
        """

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )

        manager = MemoryManager(
            store,
        )

        entity = Entity(
            id="note_architecture",
            type=EntityType.NOTE,
            name="Architecture Decision",
            confidence=ConfidenceLevel.MEDIUM,
        )

        manager.save(
            entity,
        )

        upgraded = Entity(
            id="note_architecture",
            type=EntityType.NOTE,
            name="Architecture Decision",
            confidence=ConfidenceLevel.HIGH,
        )

        manager.save(
            upgraded,
        )

        result = manager.get(
            "note_architecture",
        )

        assert result is not None
        assert result.confidence is ConfidenceLevel.HIGH

        # Exactly one entity; no duplicates produced
        assert len(
            manager.get_all(),
        ) == 1


class TestContextImmutability:
    """Verify stored entities are never mutated by retrieval, pipeline, or Brain."""

    def test_retrieval_does_not_mutate_stored_entities(
        self,
        tmp_path: Path,
    ) -> None:
        """MemoryRetriever.retrieve() must not alter the stored state of entities.

        Retrieval is a read-only operation. The entity in storage must be
        byte-for-byte identical before and after retrieve() is called.
        """

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )

        manager = MemoryManager(
            store,
        )

        entity = Entity(
            id="project_astralis",
            type=EntityType.PROJECT,
            name="ASTRALIS",
            properties={
                "current_state": "Development is active.",
            },
        )

        manager.save(
            entity,
        )

        retriever = MemoryRetriever(
            manager,
        )

        request = Request(
            text="What is the current state of ASTRALIS?",
            source=RequestSource.CLI,
        )

        retriever.retrieve(
            request,
        )

        stored_after = manager.get(
            "project_astralis",
        )

        assert stored_after is not None
        assert stored_after == entity

    def test_pipeline_processing_does_not_mutate_stored_entities(
        self,
        tmp_path: Path,
    ) -> None:
        """RequestPipeline.process() must not alter the stored state of entities.

        The pipeline assembles context for the Brain but must never write back
        to persistent storage as a side-effect of processing a request.
        """

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )

        manager = MemoryManager(
            store,
        )

        entity = Entity(
            id="project_astralis",
            type=EntityType.PROJECT,
            name="ASTRALIS",
            properties={
                "current_state": "Development is active.",
            },
        )

        manager.save(
            entity,
        )

        retriever = MemoryRetriever(
            manager,
        )

        brain = Mock()
        brain.process.return_value = Response(
            text="Current state acknowledged.",
            success=True,
        )

        pipeline = RequestPipeline(
            brain=brain,
            retriever=retriever,
            monitor=Monitor(
                enabled=False,
            ),
        )

        request = Request(
            text="What is the current state of ASTRALIS?",
            source=RequestSource.CLI,
        )

        pipeline.process(
            request,
        )

        stored_after = manager.get(
            "project_astralis",
        )

        assert stored_after is not None
        assert stored_after == entity

    def test_brain_execution_does_not_mutate_stored_entities(
        self,
        tmp_path: Path,
    ) -> None:
        """Brain.process() must not alter persistent storage.

        Brain does not hold a reference to MemoryManager or EntityStore.
        The stored entity must be identical before and after Brain execution.
        """

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )

        manager = MemoryManager(
            store,
        )

        entity = Entity(
            id="project_astralis",
            type=EntityType.PROJECT,
            name="ASTRALIS",
            properties={
                "current_state": "Development is active.",
            },
        )

        manager.save(
            entity,
        )

        capability_manager = Mock(
            spec=CapabilityManager,
        )

        capability_manager.execute.return_value = Response(
            text="Current state acknowledged.",
            success=True,
        )

        brain = Brain(
            capability_manager,
        )

        retriever = MemoryRetriever(
            manager,
        )

        request = Request(
            text="What is the current state of ASTRALIS?",
            source=RequestSource.CLI,
        )

        context = retriever.retrieve(
            request,
        )

        from astralis.brain.context import BrainContext

        brain_context = BrainContext(
            request=request,
            context=context,
        )

        brain.process(
            brain_context,
        )

        stored_after = manager.get(
            "project_astralis",
        )

        assert stored_after is not None
        assert stored_after == entity
