from pathlib import Path
from unittest.mock import Mock

from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.brain.source import RequestSource
from astralis.context.context import Context
from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
from astralis.memory.retriever import MemoryRetriever
from astralis.monitoring.monitor import Monitor
from astralis.pipeline.request_pipeline import (
    RequestPipeline,
    resolve_current_project,
)


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