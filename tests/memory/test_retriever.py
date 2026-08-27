from pathlib import Path
from unittest.mock import Mock

from astralis.brain.request import Request
from astralis.brain.source import RequestSource
from astralis.context.context import Context
from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
from astralis.memory.manager import MemoryManager
from astralis.memory.retriever import MemoryRetriever


class TestMemoryRetriever:
    """Tests for the MemoryRetriever."""

    @staticmethod
    def _request(
        text: str = "Tell me about ASTRALIS.",
    ) -> Request:
        """Create a test request."""

        return Request(
            text=text,
            source=RequestSource.CLI,
        )

    def test_retrieve_returns_context(
        self,
    ) -> None:
        """Retrieve relevant context from memory."""

        memory = Mock(
            spec=MemoryManager,
        )

        entities = [
            Entity(
                id="project",
                type=EntityType.PROJECT,
                name="ASTRALIS",
            ),
        ]

        memory.get_all.return_value = entities

        retriever = MemoryRetriever(
            memory,
        )

        result = retriever.retrieve(
            self._request(),
        )

        assert isinstance(
            result,
            Context,
        )
        assert len(
            result.items,
        ) == 1
        assert result.items[0].entity == entities[0]
        assert result.items[0].relevance > 0.0

    def test_retrieve_calls_memory_manager(
        self,
    ) -> None:
        """Retrieve entities through the memory manager."""

        memory = Mock(
            spec=MemoryManager,
        )

        memory.get_all.return_value = []

        retriever = MemoryRetriever(
            memory,
        )

        retriever.retrieve(
            self._request(),
        )

        memory.get_all.assert_called_once_with()

    def test_foreign_projects_excluded_when_current_project_active(
        self,
        tmp_path: Path,
    ) -> None:
        """Exclude foreign PROJECT entities from retrieval when inside a project."""

        current_root = tmp_path / "active_project"
        foreign_root = tmp_path / "foreign_project"
        current_root.mkdir()
        foreign_root.mkdir()

        current_proj = Entity(
            id="current_proj",
            type=EntityType.PROJECT,
            name="Alpha Project",
            properties={
                "root_path": str(
                    current_root,
                ),
                "description": "Alpha description",
            },
        )

        foreign_proj = Entity(
            id="foreign_proj",
            type=EntityType.PROJECT,
            name="Beta Project",
            properties={
                "root_path": str(
                    foreign_root,
                ),
                "description": "Beta description",
            },
        )

        memory = Mock(
            spec=MemoryManager,
        )
        memory.get_all.return_value = [
            current_proj,
            foreign_proj,
        ]

        retriever = MemoryRetriever(
            memory,
        )

        # Request mentions Beta (foreign project), but CWD is in Alpha Project
        result = retriever.retrieve(
            request=self._request(
                text="Tell me about Beta Project",
            ),
            cwd=current_root,
        )

        # Foreign project must be excluded from candidates
        matched_ids = [item.entity.id for item in result.items]
        assert "foreign_proj" not in matched_ids

    def test_non_project_entities_remain_eligible(
        self,
        tmp_path: Path,
    ) -> None:
        """Keep non-PROJECT entities eligible when a current project exists."""

        project_dir = tmp_path / "project_root"
        project_dir.mkdir()

        project = Entity(
            id="proj_1",
            type=EntityType.PROJECT,
            name="ASTRALIS",
            properties={
                "root_path": str(
                    project_dir,
                ),
            },
        )

        note = Entity(
            id="note_1",
            type=EntityType.NOTE,
            name="Architecture Note",
            properties={
                "content": "Modular context pipeline design",
            },
        )

        memory = Mock(
            spec=MemoryManager,
        )
        memory.get_all.return_value = [
            project,
            note,
        ]

        retriever = MemoryRetriever(
            memory,
        )

        result = retriever.retrieve(
            request=self._request(
                text="What is in the architecture note?",
            ),
            cwd=project_dir,
        )

        assert len(
            result.items,
        ) == 1
        assert result.items[0].entity.id == "note_1"

    def test_no_current_project_preserves_existing_retrieval(
        self,
        tmp_path: Path,
    ) -> None:
        """Preserve all entity candidate eligibility when no project matches CWD."""

        p1 = Entity(
            id="proj_1",
            type=EntityType.PROJECT,
            name="Alpha",
            properties={
                "root_path": str(
                    tmp_path / "dir_1",
                ),
            },
        )

        p2 = Entity(
            id="proj_2",
            type=EntityType.PROJECT,
            name="Beta",
            properties={
                "root_path": str(
                    tmp_path / "dir_2",
                ),
            },
        )

        memory = Mock(
            spec=MemoryManager,
        )
        memory.get_all.return_value = [
            p1,
            p2,
        ]

        retriever = MemoryRetriever(
            memory,
        )

        # CWD outside any project root
        unrelated_cwd = tmp_path / "unrelated_workspace"
        unrelated_cwd.mkdir()

        result = retriever.retrieve(
            request=self._request(
                text="Tell me about Alpha",
            ),
            cwd=unrelated_cwd,
        )

        assert len(
            result.items,
        ) == 1
        assert result.items[0].entity.id == "proj_1"

    def test_current_project_not_unconditionally_injected(
        self,
        tmp_path: Path,
    ) -> None:
        """Do not inject current project into Context when query has zero relevance."""

        project_dir = tmp_path / "my_project"
        project_dir.mkdir()

        project = Entity(
            id="proj_1",
            type=EntityType.PROJECT,
            name="ASTRALIS",
            properties={
                "root_path": str(
                    project_dir,
                ),
                "description": "AI operating system",
            },
        )

        memory = Mock(
            spec=MemoryManager,
        )
        memory.get_all.return_value = [
            project,
        ]

        retriever = MemoryRetriever(
            memory,
        )

        # Unrelated arithmetic query
        result = retriever.retrieve(
            request=self._request(
                text="What is 2 + 2?",
            ),
            cwd=project_dir,
        )

        # Zero lexical overlap -> empty Context
        assert len(
            result.items,
        ) == 0

    def test_matching_request_retrieves_current_project(
        self,
        tmp_path: Path,
    ) -> None:
        """Retrieve current project when request matches its name or properties."""

        project_dir = tmp_path / "astralis_repo"
        project_dir.mkdir()

        project = Entity(
            id="project_astralis",
            type=EntityType.PROJECT,
            name="ASTRALIS",
            properties={
                "root_path": str(
                    project_dir,
                ),
                "description": "Context Foundation",
            },
        )

        memory = Mock(
            spec=MemoryManager,
        )
        memory.get_all.return_value = [
            project,
        ]

        retriever = MemoryRetriever(
            memory,
        )

        result = retriever.retrieve(
            request=self._request(
                text="What is ASTRALIS?",
            ),
            cwd=project_dir,
        )

        assert len(
            result.items,
        ) == 1
        assert result.items[0].entity.id == "project_astralis"
        assert result.items[0].relevance > 0.0