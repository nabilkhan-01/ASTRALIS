from pathlib import Path
from unittest.mock import Mock

from astralis.brain.request import Request
from astralis.brain.source import RequestSource
from astralis.context.context import Context
from astralis.memory.confidence import ConfidenceLevel
from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
from astralis.memory.manager import MemoryManager
from astralis.memory.provenance import Provenance
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

    def test_retrieve_creates_distinct_context_instances_per_call(
        self,
    ) -> None:
        """Create distinct, ephemeral Context instances for each retrieval call."""

        memory = Mock(
            spec=MemoryManager,
        )
        memory.get_all.return_value = [
            Entity(
                id="project_astralis",
                type=EntityType.PROJECT,
                name="ASTRALIS",
            ),
        ]

        retriever = MemoryRetriever(
            memory,
        )

        request = self._request(
            text="Tell me about ASTRALIS",
        )

        context_a = retriever.retrieve(
            request,
        )
        context_b = retriever.retrieve(
            request,
        )

        assert context_a is not context_b
        assert context_a.items == context_b.items

    def test_matching_request_retrieves_decision(
        self,
    ) -> None:
        """Retrieve relevant DECISION entity through standard lexical matching."""

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
        )

        memory = Mock(
            spec=MemoryManager,
        )
        memory.get_all.return_value = [
            decision,
        ]

        retriever = MemoryRetriever(
            memory,
        )

        result = retriever.retrieve(
            request=self._request(
                text="Why did we choose JSON storage?",
            ),
        )

        assert len(
            result.items,
        ) == 1
        assert result.items[0].entity.id == "decision_json_storage"
        assert result.items[0].entity.type is EntityType.DECISION
        assert result.items[0].relevance > 0.0

    def test_matching_request_retrieves_superseding_decision(
        self,
    ) -> None:
        """Retrieve superseding DECISION entity with supersedes property normally."""

        newer = Entity(
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

        memory = Mock(
            spec=MemoryManager,
        )
        memory.get_all.return_value = [
            newer,
        ]

        retriever = MemoryRetriever(
            memory,
        )

        result = retriever.retrieve(
            request=self._request(
                text="Tell me about SQLite entity storage",
            ),
        )

        assert len(
            result.items,
        ) == 1
        assert result.items[0].entity.id == "decision_sqlite_storage"
        assert result.items[0].entity.properties["supersedes"] == "decision_json_storage"

    def test_source_type_none_preserves_all_entities(
        self,
    ) -> None:
        """Include entities with or without provenance when source_type is None."""

        e1 = Entity(
            id="e1",
            type=EntityType.NOTE,
            name="Architecture Note",
            provenance=Provenance(
                source_type="file",
                source_identifier="docs/arch.md",
            ),
        )
        e2 = Entity(
            id="e2",
            type=EntityType.NOTE,
            name="User Architecture Note",
            provenance=Provenance(
                source_type="user",
                source_identifier="manual",
            ),
        )
        e3 = Entity(
            id="e3",
            type=EntityType.NOTE,
            name="Legacy Architecture Note",
            provenance=None,
        )

        memory = Mock(
            spec=MemoryManager,
        )
        memory.get_all.return_value = [
            e1,
            e2,
            e3,
        ]

        retriever = MemoryRetriever(
            memory,
        )

        result = retriever.retrieve(
            request=self._request(
                text="Architecture Note",
            ),
            source_type=None,
        )

        matched_ids = [item.entity.id for item in result.items]
        assert matched_ids == [
            "e1",
            "e2",
            "e3",
        ]

    def test_source_type_filtering_returns_matching_origin_only(
        self,
    ) -> None:
        """Return only entities whose provenance.source_type matches the filter."""

        e_file = Entity(
            id="e_file",
            type=EntityType.NOTE,
            name="Architecture Guide",
            provenance=Provenance(
                source_type="file",
                source_identifier="docs/guide.md",
            ),
        )
        e_user = Entity(
            id="e_user",
            type=EntityType.NOTE,
            name="Architecture Guide",
            provenance=Provenance(
                source_type="user",
                source_identifier="manual_prompt",
            ),
        )
        e_none = Entity(
            id="e_none",
            type=EntityType.NOTE,
            name="Architecture Guide",
            provenance=None,
        )

        memory = Mock(
            spec=MemoryManager,
        )
        memory.get_all.return_value = [
            e_file,
            e_user,
            e_none,
        ]

        retriever = MemoryRetriever(
            memory,
        )

        result = retriever.retrieve(
            request=self._request(
                text="Architecture Guide",
            ),
            source_type="file",
        )

        assert len(
            result.items,
        ) == 1
        assert result.items[0].entity.id == "e_file"

    def test_source_filtering_does_not_alter_relevance_scoring_or_ranking(
        self,
    ) -> None:
        """Preserve exact relevance scores and deterministic tie-breaking under source filtering."""

        e_alpha = Entity(
            id="e_alpha",
            type=EntityType.NOTE,
            name="Context Pipeline",
            provenance=Provenance(
                source_type="file",
                source_identifier="docs/a.md",
            ),
        )
        e_beta = Entity(
            id="e_beta",
            type=EntityType.NOTE,
            name="Context Pipeline",
            provenance=Provenance(
                source_type="file",
                source_identifier="docs/b.md",
            ),
        )

        memory = Mock(
            spec=MemoryManager,
        )
        memory.get_all.return_value = [
            e_alpha,
            e_beta,
        ]

        retriever = MemoryRetriever(
            memory,
        )

        result = retriever.retrieve(
            request=self._request(
                text="Context Pipeline",
            ),
            source_type="file",
        )

        assert len(
            result.items,
        ) == 2
        assert result.items[0].entity.id == "e_alpha"
        assert result.items[1].entity.id == "e_beta"
        assert result.items[0].relevance == result.items[1].relevance

    def test_project_scoping_and_source_filtering_combine_correctly(
        self,
        tmp_path: Path,
    ) -> None:
        """Apply project scoping and source filtering together in order."""

        current_root = tmp_path / "project_root"
        foreign_root = tmp_path / "foreign_root"
        current_root.mkdir()
        foreign_root.mkdir()

        current_proj = Entity(
            id="curr_proj",
            type=EntityType.PROJECT,
            name="ASTRALIS Core",
            properties={
                "root_path": str(
                    current_root,
                ),
            },
            provenance=Provenance(
                source_type="file",
                source_identifier="workspace_root",
            ),
        )
        foreign_proj = Entity(
            id="foreign_proj",
            type=EntityType.PROJECT,
            name="ASTRALIS Core",
            properties={
                "root_path": str(
                    foreign_root,
                ),
            },
            provenance=Provenance(
                source_type="file",
                source_identifier="workspace_root",
            ),
        )
        note_user = Entity(
            id="note_user",
            type=EntityType.NOTE,
            name="ASTRALIS Core Note",
            provenance=Provenance(
                source_type="user",
                source_identifier="chat",
            ),
        )
        note_file = Entity(
            id="note_file",
            type=EntityType.NOTE,
            name="ASTRALIS Core Note",
            provenance=Provenance(
                source_type="file",
                source_identifier="docs/core.md",
            ),
        )

        memory = Mock(
            spec=MemoryManager,
        )
        memory.get_all.return_value = [
            current_proj,
            foreign_proj,
            note_user,
            note_file,
        ]

        retriever = MemoryRetriever(
            memory,
        )

        result = retriever.retrieve(
            request=self._request(
                text="ASTRALIS Core",
            ),
            cwd=current_root,
            source_type="file",
        )

        matched_ids = [item.entity.id for item in result.items]
        assert "foreign_proj" not in matched_ids
        assert "note_user" not in matched_ids
        assert "curr_proj" in matched_ids
        assert "note_file" in matched_ids

    def test_source_filtering_does_not_inspect_source_identifier(
        self,
    ) -> None:
        """Match on source_type regardless of source_identifier value."""

        e1 = Entity(
            id="e1",
            type=EntityType.NOTE,
            name="Data",
            provenance=Provenance(
                source_type="custom_src",
                source_identifier="id_1",
            ),
        )
        e2 = Entity(
            id="e2",
            type=EntityType.NOTE,
            name="Data",
            provenance=Provenance(
                source_type="custom_src",
                source_identifier="id_2",
            ),
        )

        memory = Mock(
            spec=MemoryManager,
        )
        memory.get_all.return_value = [
            e1,
            e2,
        ]

        retriever = MemoryRetriever(
            memory,
        )

        result = retriever.retrieve(
            request=self._request(
                text="Data",
            ),
            source_type="custom_src",
        )

        assert len(
            result.items,
        ) == 2

    def test_confidence_does_not_alter_retrieval_ranking(
        self,
    ) -> None:
        """Verify confidence does not affect lexical retrieval ranking."""

        # HIGH confidence but only one query token in name → weaker match
        high_confidence_weak_match = Entity(
            id="e_high",
            type=EntityType.NOTE,
            name="Memory Manager",
            confidence=ConfidenceLevel.HIGH,
        )
        # LOW confidence but both query tokens in name → stronger match
        low_confidence_strong_match = Entity(
            id="e_low",
            type=EntityType.NOTE,
            name="Memory Architecture Pipeline",
            confidence=ConfidenceLevel.LOW,
        )

        memory = Mock(
            spec=MemoryManager,
        )
        memory.get_all.return_value = [
            high_confidence_weak_match,
            low_confidence_strong_match,
        ]

        retriever = MemoryRetriever(
            memory,
        )

        result = retriever.retrieve(
            request=self._request(
                text="Memory Architecture",
            ),
        )

        # Both entities have lexical overlap — both are retrieved
        assert len(result.items) == 2

        # LOW-confidence entity ranks first because its lexical score is higher
        assert result.items[0].entity.id == "e_low"
        assert result.items[1].entity.id == "e_high"

        # Relevance scores differ — ranking is driven by lexical match, not confidence
        assert result.items[0].relevance > result.items[1].relevance
