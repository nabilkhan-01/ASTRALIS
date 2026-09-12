from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import Mock

from astralis.brain.brain import Brain
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.brain.source import RequestSource
from astralis.context.context import Context
from astralis.memory.confidence import ConfidenceLevel
from astralis.memory.conflict import detect_conflicts
from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
from astralis.memory.freshness import FreshnessStatus, assess_freshness
from astralis.memory.json_store import JsonEntityStore
from astralis.memory.manager import MemoryManager
from astralis.memory.provenance import Provenance
from astralis.memory.retriever import (
    MemoryRetriever,
    resolve_current_project,
)
from astralis.monitoring.monitor import Monitor
from astralis.pipeline.request_pipeline import RequestPipeline


class TestRequestPipeline:
    """Tests for the RequestPipeline."""

    @staticmethod
    def _request() -> Request:
        """Create a test request."""

        return Request(
            text="Hello",
            source=RequestSource.CLI,
        )

    def test_process_with_monitoring_enabled(
        self,
    ) -> None:
        """Process a request with monitoring enabled."""

        brain = Mock()
        brain.process.return_value = Response(
            text="Hello!",
            success=True,
        )

        retriever = Mock(
            spec=MemoryRetriever,
        )

        retriever.retrieve.return_value = Context(
            items=(),
        )

        pipeline = RequestPipeline(
            brain=brain,
            retriever=retriever,
            monitor=Monitor(
                enabled=True,
            ),
        )

        request = self._request()

        response = pipeline.process(
            request,
        )

        assert response.success is True
        assert response.text == "Hello!"
        brain.process.assert_called_once()

        retriever.retrieve.assert_called_once_with(
            request,
        )

    def test_process_with_monitoring_disabled(
        self,
    ) -> None:
        """Process a request with monitoring disabled."""

        brain = Mock()
        brain.process.return_value = Response(
            text="Hello!",
            success=True,
        )

        retriever = Mock(
            spec=MemoryRetriever,
        )

        retriever.retrieve.return_value = Context(
            items=(),
        )

        pipeline = RequestPipeline(
            brain=brain,
            retriever=retriever,
            monitor=Monitor(
                enabled=False,
            ),
        )

        request = self._request()

        response = pipeline.process(
            request,
        )

        assert response.success is True
        assert response.text == "Hello!"
        retriever.retrieve.assert_called_once_with(
            request,
        )
        brain.process.assert_called_once()


class TestCurrentProjectResolution:
    """Tests for resolving the current project in the pipeline."""

    def test_cwd_equals_project_root(
        self,
        tmp_path: Path,
    ) -> None:
        """Resolve project when cwd exactly matches the project root."""

        project_dir = tmp_path / "my_project"
        project_dir.mkdir()

        project = Entity(
            id="proj_1",
            type=EntityType.PROJECT,
            name="My Project",
            properties={
                "root_path": str(
                    project_dir,
                ),
            },
        )

        resolved = resolve_current_project(
            entities=[
                project,
            ],
            cwd=project_dir,
        )

        assert resolved == project

    def test_cwd_inside_project_subdirectory(
        self,
        tmp_path: Path,
    ) -> None:
        """Resolve project when cwd is a descendant subdirectory."""

        project_dir = tmp_path / "my_project"
        sub_dir = project_dir / "src" / "core"
        sub_dir.mkdir(
            parents=True,
        )

        project = Entity(
            id="proj_1",
            type=EntityType.PROJECT,
            name="My Project",
            properties={
                "root_path": str(
                    project_dir,
                ),
            },
        )

        resolved = resolve_current_project(
            entities=[
                project,
            ],
            cwd=sub_dir,
        )

        assert resolved == project

    def test_no_project_match(
        self,
        tmp_path: Path,
    ) -> None:
        """Return None when cwd is unrelated to any project root."""

        project_dir = tmp_path / "project_a"
        other_dir = tmp_path / "unrelated_dir"
        project_dir.mkdir()
        other_dir.mkdir()

        project = Entity(
            id="proj_1",
            type=EntityType.PROJECT,
            name="Project A",
            properties={
                "root_path": str(
                    project_dir,
                ),
            },
        )

        resolved = resolve_current_project(
            entities=[
                project,
            ],
            cwd=other_dir,
        )

        assert resolved is None

    def test_missing_or_empty_root_path_ignored(
        self,
        tmp_path: Path,
    ) -> None:
        """Ignore projects with missing or empty root_path property."""

        p1 = Entity(
            id="proj_1",
            type=EntityType.PROJECT,
            name="No Root",
            properties={},
        )

        p2 = Entity(
            id="proj_2",
            type=EntityType.PROJECT,
            name="Empty Root",
            properties={
                "root_path": "   ",
            },
        )

        p3 = Entity(
            id="proj_3",
            type=EntityType.PROJECT,
            name="Non-string Root",
            properties={
                "root_path": 12345,
            },
        )

        resolved = resolve_current_project(
            entities=[
                p1,
                p2,
                p3,
            ],
            cwd=tmp_path,
        )

        assert resolved is None

    def test_non_project_entities_ignored(
        self,
        tmp_path: Path,
    ) -> None:
        """Ignore entities whose type is not EntityType.PROJECT."""

        note = Entity(
            id="note_1",
            type=EntityType.NOTE,
            name="A Note",
            properties={
                "root_path": str(
                    tmp_path,
                ),
            },
        )

        user = Entity(
            id="user_1",
            type=EntityType.USER,
            name="Nabil",
            properties={
                "root_path": str(
                    tmp_path,
                ),
            },
        )

        resolved = resolve_current_project(
            entities=[
                note,
                user,
            ],
            cwd=tmp_path,
        )

        assert resolved is None

    def test_deepest_project_wins_among_nested_projects(
        self,
        tmp_path: Path,
    ) -> None:
        """Choose the most specific (deepest) project root when paths overlap."""

        monorepo_root = tmp_path / "monorepo"
        sub_package = monorepo_root / "packages" / "frontend"
        sub_package.mkdir(
            parents=True,
        )

        monorepo_proj = Entity(
            id="monorepo_proj",
            type=EntityType.PROJECT,
            name="Monorepo Root",
            properties={
                "root_path": str(
                    monorepo_root,
                ),
            },
        )

        package_proj = Entity(
            id="package_proj",
            type=EntityType.PROJECT,
            name="Frontend Package",
            properties={
                "root_path": str(
                    sub_package,
                ),
            },
        )

        resolved = resolve_current_project(
            entities=[
                monorepo_proj,
                package_proj,
            ],
            cwd=sub_package / "components",
        )

        assert resolved == package_proj

    def test_deterministic_id_tie_break_for_equal_depth(
        self,
        tmp_path: Path,
    ) -> None:
        """Break tie deterministically using entity.id ascending when depth is equal."""

        project_dir = tmp_path / "shared_root"
        project_dir.mkdir()

        p_beta = Entity(
            id="proj_beta",
            type=EntityType.PROJECT,
            name="Project Beta",
            properties={
                "root_path": str(
                    project_dir,
                ),
            },
        )

        p_alpha = Entity(
            id="proj_alpha",
            type=EntityType.PROJECT,
            name="Project Alpha",
            properties={
                "root_path": str(
                    project_dir,
                ),
            },
        )

        # Pass in reverse order to ensure sorting breaks tie by id ascending
        resolved = resolve_current_project(
            entities=[
                p_beta,
                p_alpha,
            ],
            cwd=project_dir,
        )

        assert resolved == p_alpha


class TestContextInspection:
    """Tests for RequestPipeline.inspect_context()."""

    def test_inspect_context_returns_assembled_context(
        self,
        tmp_path: Path,
    ) -> None:
        """inspect_context() returns the assembled Context matching retrieval."""

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )
        manager = MemoryManager(
            store,
        )
        entity = Entity(
            id="proj_astralis",
            type=EntityType.PROJECT,
            name="ASTRALIS Core",
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
        pipeline = RequestPipeline(
            brain=brain,
            retriever=retriever,
            monitor=Monitor(
                enabled=False,
            ),
        )

        request = Request(
            text="Tell me about ASTRALIS Core",
            source=RequestSource.CLI,
        )

        inspected = pipeline.inspect_context(
            request,
        )

        assert isinstance(
            inspected,
            Context,
        )
        assert len(inspected.items) == 1
        assert inspected.items[0].entity.id == "proj_astralis"
        assert inspected.items[0].relevance > 0.0

    def test_inspect_context_does_not_execute_brain(
        self,
    ) -> None:
        """inspect_context() must never execute Brain.process()."""

        brain = Mock(
            spec=Brain,
        )
        retriever = Mock(
            spec=MemoryRetriever,
        )
        retriever.retrieve.return_value = Context(
            items=(),
        )

        pipeline = RequestPipeline(
            brain=brain,
            retriever=retriever,
            monitor=Monitor(
                enabled=False,
            ),
        )

        request = Request(
            text="Query text",
            source=RequestSource.CLI,
        )

        pipeline.inspect_context(
            request,
        )

        brain.process.assert_not_called()
        retriever.retrieve.assert_called_once_with(
            request,
        )

    def test_inspect_context_preserves_available_metadata(
        self,
        tmp_path: Path,
    ) -> None:
        """inspect_context() preserves entity fields, provenance, timestamps, confidence, freshness, and conflicts."""

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )
        manager = MemoryManager(
            store,
        )

        predecessor = Entity(
            id="dec_00",
            type=EntityType.DECISION,
            name="Architecture Decision Predecessor",
            properties={
                "status": "active",
            },
            created_at="2026-09-01T08:00:00+00:00",
            updated_at="2026-09-01T08:00:00+00:00",
            confidence=ConfidenceLevel.MEDIUM,
        )
        decision = Entity(
            id="dec_01",
            type=EntityType.DECISION,
            name="Architecture Decision Modern",
            properties={
                "status": "active",
                "supersedes": "dec_00",
                "rationale": "Separation of concerns.",
            },
            provenance=Provenance(
                source_type="user",
                source_identifier="architect",
            ),
            created_at="2026-09-05T10:00:00+00:00",
            updated_at="2026-09-10T12:00:00+00:00",
            confidence=ConfidenceLevel.HIGH,
        )

        manager.save(
            predecessor,
        )
        manager.save(
            decision,
        )

        retriever = MemoryRetriever(
            manager,
        )
        brain = Mock(
            spec=Brain,
        )
        pipeline = RequestPipeline(
            brain=brain,
            retriever=retriever,
            monitor=Monitor(
                enabled=False,
            ),
        )

        request = Request(
            text="Architecture Decision Modern",
            source=RequestSource.CLI,
        )

        inspected = pipeline.inspect_context(
            request,
        )

        item_map = {
            item.entity.id: item
            for item in inspected.items
        }

        assert "dec_01" in item_map
        item = item_map["dec_01"]

        # Relevance
        assert item.relevance > 0.0

        # Core entity fields
        assert item.entity.id == "dec_01"
        assert item.entity.name == "Architecture Decision Modern"
        assert item.entity.type == EntityType.DECISION
        assert item.entity.properties["status"] == "active"
        assert item.entity.properties["supersedes"] == "dec_00"

        # Provenance
        assert item.entity.provenance is not None
        assert item.entity.provenance.source_type == "user"
        assert item.entity.provenance.source_identifier == "architect"

        # Timestamps
        assert item.entity.created_at == "2026-09-05T10:00:00+00:00"
        assert item.entity.updated_at == "2026-09-10T12:00:00+00:00"

        # Confidence
        assert item.entity.confidence == ConfidenceLevel.HIGH

        # Dynamic freshness assessment through existing assess_freshness()
        ref_time = datetime(
            2026,
            9,
            12,
            12,
            0,
            0,
            tzinfo=timezone.utc,
        )
        fresh_status = assess_freshness(
            entity=item.entity,
            threshold=timedelta(
                days=7,
            ),
            reference_time=ref_time,
        )
        assert fresh_status == FreshnessStatus.FRESH

        stale_status = assess_freshness(
            entity=item.entity,
            threshold=timedelta(
                days=1,
            ),
            reference_time=ref_time,
        )
        assert stale_status == FreshnessStatus.STALE

        # Conflict evaluation through existing detect_conflicts()
        conflicts = detect_conflicts(
            [item.entity for item in inspected.items],
        )
        assert len(conflicts) == 1
        assert conflicts[0].entity_a.id == "dec_01"
        assert conflicts[0].entity_b.id == "dec_00"

    def test_inspect_context_is_read_only(
        self,
        tmp_path: Path,
    ) -> None:
        """inspect_context() leaves stored entities and persistent storage unchanged."""

        memory_file = tmp_path / "memory.json"
        store = JsonEntityStore(
            memory_file,
        )
        manager = MemoryManager(
            store,
        )

        entity = Entity(
            id="proj_stable",
            type=EntityType.PROJECT,
            name="Stable Project",
            properties={
                "state": "immutable",
            },
            created_at="2026-09-01T00:00:00+00:00",
            updated_at="2026-09-01T00:00:00+00:00",
            confidence=ConfidenceLevel.LOW,
        )
        manager.save(
            entity,
        )

        raw_before = memory_file.read_bytes()
        stored_before = manager.get(
            "proj_stable",
        )

        retriever = MemoryRetriever(
            manager,
        )
        brain = Mock(
            spec=Brain,
        )
        pipeline = RequestPipeline(
            brain=brain,
            retriever=retriever,
            monitor=Monitor(
                enabled=False,
            ),
        )

        request = Request(
            text="Stable Project query",
            source=RequestSource.CLI,
        )

        inspected = pipeline.inspect_context(
            request,
        )

        assert len(inspected.items) == 1

        raw_after = memory_file.read_bytes()
        stored_after = manager.get(
            "proj_stable",
        )

        assert raw_after == raw_before
        assert stored_after == stored_before

    def test_inspect_context_is_deterministic(
        self,
        tmp_path: Path,
    ) -> None:
        """Repeated calls with identical request and memory state yield identical contexts."""

        store = JsonEntityStore(
            tmp_path / "memory.json",
        )
        manager = MemoryManager(
            store,
        )

        manager.save(
            Entity(
                id="e1",
                type=EntityType.NOTE,
                name="Alpha Token Information",
            ),
        )
        manager.save(
            Entity(
                id="e2",
                type=EntityType.NOTE,
                name="Alpha Token Extended Information",
            ),
        )

        retriever = MemoryRetriever(
            manager,
        )
        brain = Mock(
            spec=Brain,
        )
        pipeline = RequestPipeline(
            brain=brain,
            retriever=retriever,
            monitor=Monitor(
                enabled=False,
            ),
        )

        request = Request(
            text="Alpha Token",
            source=RequestSource.CLI,
        )

        first = pipeline.inspect_context(
            request,
        )
        for _ in range(4):
            subsequent = pipeline.inspect_context(
                request,
            )
            assert [item.entity.id for item in subsequent.items] == [
                item.entity.id for item in first.items
            ]
            assert [item.relevance for item in subsequent.items] == [
                item.relevance for item in first.items
            ]
            assert subsequent == first
