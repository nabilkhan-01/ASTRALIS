from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import Mock

from astralis.brain.brain import Brain
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.brain.source import RequestSource
from astralis.capability.manager import CapabilityManager
from astralis.context.context import Context
from astralis.memory.confidence import ConfidenceLevel
from astralis.memory.conflict import detect_conflicts
from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
from astralis.memory.freshness import FreshnessStatus, assess_freshness
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


class TestContextDeletion:
    """Tests for caller-controlled context deletion (Step 22)."""

    def test_caller_deletes_entity_removes_from_storage(
        self,
        tmp_path: Path,
    ) -> None:
        """MemoryManager.delete() removes an entity from persistent storage and preserves others."""

        memory_file = tmp_path / "memory.json"
        store = JsonEntityStore(
            memory_file,
        )
        manager = MemoryManager(
            store,
        )

        entity_to_delete = Entity(
            id="dec_obsolete",
            type=EntityType.DECISION,
            name="Obsolete Decision",
            properties={
                "status": "deprecated",
            },
        )
        entity_to_keep = Entity(
            id="proj_active",
            type=EntityType.PROJECT,
            name="Active Project",
            properties={
                "state": "active",
            },
        )

        manager.save(
            entity_to_delete,
        )
        manager.save(
            entity_to_keep,
        )

        assert manager.get("dec_obsolete") is not None
        assert manager.get("proj_active") is not None

        manager.delete(
            "dec_obsolete",
        )

        assert manager.get("dec_obsolete") is None
        assert manager.get("proj_active") == entity_to_keep

        # Verify raw file persistence across a fresh store instance
        fresh_store = JsonEntityStore(
            memory_file,
        )
        assert fresh_store.get("dec_obsolete") is None
        assert fresh_store.get("proj_active") == entity_to_keep

        raw_json = memory_file.read_text(
            encoding="utf-8",
        )
        assert "dec_obsolete" not in raw_json
        assert "proj_active" in raw_json

    def test_deleted_entity_excluded_from_subsequent_retrieval(
        self,
        tmp_path: Path,
    ) -> None:
        """Deleted entity is immediately excluded from subsequent retrieval while others remain."""

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )
        manager = MemoryManager(
            store,
        )

        e1 = Entity(
            id="arch_01",
            type=EntityType.DECISION,
            name="ASTRALIS Core Architecture",
            properties={
                "detail": "first architecture",
            },
        )
        e2 = Entity(
            id="arch_02",
            type=EntityType.DECISION,
            name="ASTRALIS Core Framework",
            properties={
                "detail": "second framework",
            },
        )

        manager.save(
            e1,
        )
        manager.save(
            e2,
        )

        retriever = MemoryRetriever(
            manager,
        )
        request = Request(
            text="ASTRALIS Core Architecture",
            source=RequestSource.CLI,
        )

        initial_context = retriever.retrieve(
            request,
        )
        retrieved_ids = [
            item.entity.id
            for item in initial_context.items
        ]
        assert "arch_01" in retrieved_ids
        assert "arch_02" in retrieved_ids

        manager.delete(
            "arch_01",
        )

        subsequent_context = retriever.retrieve(
            request,
        )
        subsequent_ids = [
            item.entity.id
            for item in subsequent_context.items
        ]

        assert "arch_01" not in subsequent_ids
        assert "arch_02" in subsequent_ids
        assert len(subsequent_context.items) == 1
        assert subsequent_context.items[0].entity.id == "arch_02"

    def test_deleted_entity_excluded_from_pipeline_inspection_and_processing(
        self,
        tmp_path: Path,
    ) -> None:
        """Deleted entity is excluded from RequestPipeline inspection and processing."""

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )
        manager = MemoryManager(
            store,
        )

        entity = Entity(
            id="project_delete_target",
            type=EntityType.PROJECT,
            name="Target Project For Deletion",
            properties={
                "root_path": str(
                    tmp_path,
                ),
            },
        )
        manager.save(
            entity,
        )

        retriever = MemoryRetriever(
            manager,
        )
        brain = Mock(
            spec=Brain,
        )
        brain.process.return_value = Response(
            text="Response text",
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
            text="Tell me about Target Project For Deletion",
            source=RequestSource.CLI,
        )

        # Before deletion: present in inspection
        before_inspect = pipeline.inspect_context(
            request,
        )
        assert len(before_inspect.items) == 1
        assert before_inspect.items[0].entity.id == "project_delete_target"

        # Explicit caller deletion
        manager.delete(
            "project_delete_target",
        )

        # After deletion: absent in inspection
        after_inspect = pipeline.inspect_context(
            request,
        )
        assert len(after_inspect.items) == 0

        # Processing executes Brain with empty context
        response = pipeline.process(
            request,
        )
        assert response.success is True
        brain.process.assert_called_once()

        passed_brain_context = brain.process.call_args[0][0]
        assert len(passed_brain_context.context.items) == 0

    def test_deletion_does_not_mutate_existing_ephemeral_context(
        self,
        tmp_path: Path,
    ) -> None:
        """Persistent deletion does not alter previously assembled ephemeral Context instances."""

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )
        manager = MemoryManager(
            store,
        )

        entity = Entity(
            id="snapshot_target",
            type=EntityType.NOTE,
            name="Snapshot Information",
        )
        manager.save(
            entity,
        )

        retriever = MemoryRetriever(
            manager,
        )
        request = Request(
            text="Snapshot Information",
            source=RequestSource.CLI,
        )

        # Retrieve ephemeral Context before deletion
        prior_context = retriever.retrieve(
            request,
        )
        assert isinstance(
            prior_context,
            Context,
        )
        assert len(prior_context.items) == 1

        prior_items = prior_context.items
        prior_first_item = prior_items[0]

        # Delete entity from persistent storage
        manager.delete(
            "snapshot_target",
        )
        assert manager.get("snapshot_target") is None

        # Prior Context must remain completely unchanged
        assert prior_context.items == prior_items
        assert len(prior_context.items) == 1
        assert prior_context.items[0] is prior_first_item
        assert prior_context.items[0].entity.id == "snapshot_target"

        # Fresh retrieval confirms absence
        new_context = retriever.retrieve(
            request,
        )
        assert len(new_context.items) == 0

    def test_delete_nonexistent_entity_is_safe_noop(
        self,
        tmp_path: Path,
    ) -> None:
        """Deleting a nonexistent entity raises no error and preserves existing storage."""

        memory_file = tmp_path / "memory.json"
        store = JsonEntityStore(
            memory_file,
        )
        manager = MemoryManager(
            store,
        )

        existing = Entity(
            id="existing_note",
            type=EntityType.NOTE,
            name="Existing Note",
        )
        manager.save(
            existing,
        )

        raw_before = memory_file.read_bytes()

        # Delete non-existent ID
        manager.delete(
            "nonexistent_id",
        )

        assert manager.get("existing_note") == existing
        assert memory_file.read_bytes() == raw_before

    def test_no_automatic_deletion_of_stale_or_conflicting_context(
        self,
        tmp_path: Path,
    ) -> None:
        """Stale or conflicting entities are never automatically deleted by assessment or detection."""

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )
        manager = MemoryManager(
            store,
        )

        # Stale entity
        stale_entity = Entity(
            id="stale_decision",
            type=EntityType.DECISION,
            name="Stale Architecture Decision",
            properties={
                "status": "active",
            },
            created_at="2026-01-01T00:00:00+00:00",
            updated_at="2026-01-01T00:00:00+00:00",
            confidence=ConfidenceLevel.LOW,
        )
        manager.save(
            stale_entity,
        )

        # Freshness evaluation reports STALE
        status = assess_freshness(
            entity=stale_entity,
            threshold=timedelta(
                days=7,
            ),
            reference_time=datetime(
                2026,
                9,
                12,
                tzinfo=timezone.utc,
            ),
        )
        assert status == FreshnessStatus.STALE

        # Entity must remain stored
        assert manager.get("stale_decision") is not None

        # Conflicting decisions
        predecessor = Entity(
            id="dec_v1",
            type=EntityType.DECISION,
            name="Decision V1",
            properties={
                "status": "active",
            },
        )
        successor = Entity(
            id="dec_v2",
            type=EntityType.DECISION,
            name="Decision V2",
            properties={
                "status": "active",
                "supersedes": "dec_v1",
            },
        )
        manager.save(
            predecessor,
        )
        manager.save(
            successor,
        )

        # Conflict detection reports conflict
        conflicts = detect_conflicts(
            manager.get_all(),
        )
        assert len(conflicts) == 1

        # Neither entity is deleted
        assert manager.get("dec_v1") is not None
        assert manager.get("dec_v2") is not None
