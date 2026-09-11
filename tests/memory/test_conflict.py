from astralis.memory.conflict import ConflictReport, detect_conflicts
from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType


class TestDetectConflicts:
    """Tests for detect_conflicts."""

    @staticmethod
    def _decision(
        entity_id: str,
        status: str,
        supersedes: str | None = None,
    ) -> Entity:
        """Create a minimal DECISION entity."""

        properties: dict[str, object] = {
            "status": status,
        }

        if supersedes is not None:
            properties["supersedes"] = supersedes

        return Entity(
            id=entity_id,
            type=EntityType.DECISION,
            name=entity_id,
            properties=properties,
        )

    def test_inconsistent_active_predecessor_is_detected(
        self,
    ) -> None:
        """Report a conflict when the superseded decision is still marked active."""

        newer = self._decision(
            entity_id="decision_sqlite",
            status="active",
            supersedes="decision_json",
        )
        older = self._decision(
            entity_id="decision_json",
            status="active",
        )

        reports = detect_conflicts(
            [newer, older],
        )

        assert len(reports) == 1
        assert isinstance(
            reports[0],
            ConflictReport,
        )
        assert reports[0].entity_a is newer
        assert reports[0].entity_b is older
        assert "decision_sqlite" in reports[0].reason
        assert "decision_json" in reports[0].reason

    def test_valid_supersession_is_not_detected(
        self,
    ) -> None:
        """Do not report a conflict when the predecessor is correctly marked superseded."""

        newer = self._decision(
            entity_id="decision_sqlite",
            status="active",
            supersedes="decision_json",
        )
        older = self._decision(
            entity_id="decision_json",
            status="superseded",
        )

        reports = detect_conflicts(
            [newer, older],
        )

        assert reports == []

    def test_non_decision_entities_are_ignored(
        self,
    ) -> None:
        """Ignore entities that are not DECISION type."""

        note = Entity(
            id="note_1",
            type=EntityType.NOTE,
            name="Some note",
            properties={
                "status": "active",
                "supersedes": "note_0",
            },
        )
        project = Entity(
            id="project_1",
            type=EntityType.PROJECT,
            name="ASTRALIS",
            properties={
                "status": "active",
            },
        )

        reports = detect_conflicts(
            [note, project],
        )

        assert reports == []

    def test_missing_referenced_decision_is_ignored(
        self,
    ) -> None:
        """Produce no report when the superseded ID is absent from the supplied entities."""

        newer = self._decision(
            entity_id="decision_sqlite",
            status="active",
            supersedes="decision_json",
        )

        reports = detect_conflicts(
            [newer],
        )

        assert reports == []

    def test_entities_are_not_mutated(
        self,
    ) -> None:
        """detect_conflicts must not modify any entity."""

        newer = self._decision(
            entity_id="decision_sqlite",
            status="active",
            supersedes="decision_json",
        )
        older = self._decision(
            entity_id="decision_json",
            status="active",
        )

        original_newer_id = newer.id
        original_newer_status = newer.properties["status"]
        original_older_id = older.id
        original_older_status = older.properties["status"]

        detect_conflicts(
            [newer, older],
        )

        assert newer.id == original_newer_id
        assert newer.properties["status"] == original_newer_status
        assert older.id == original_older_id
        assert older.properties["status"] == original_older_status

    def test_multiple_conflicts_are_detected(
        self,
    ) -> None:
        """Report all structurally confirmed conflicts in a single call."""

        a = self._decision(
            entity_id="decision_c",
            status="active",
            supersedes="decision_a",
        )
        b = self._decision(
            entity_id="decision_d",
            status="active",
            supersedes="decision_b",
        )
        old_a = self._decision(
            entity_id="decision_a",
            status="active",
        )
        old_b = self._decision(
            entity_id="decision_b",
            status="active",
        )

        reports = detect_conflicts(
            [a, b, old_a, old_b],
        )

        assert len(reports) == 2

        reported_pairs = {
            (r.entity_a.id, r.entity_b.id)
            for r in reports
        }
        assert ("decision_c", "decision_a") in reported_pairs
        assert ("decision_d", "decision_b") in reported_pairs

    def test_results_are_deterministic(
        self,
    ) -> None:
        """Return the same ordered result regardless of input order."""

        a = self._decision(
            entity_id="decision_c",
            status="active",
            supersedes="decision_a",
        )
        b = self._decision(
            entity_id="decision_d",
            status="active",
            supersedes="decision_b",
        )
        old_a = self._decision(
            entity_id="decision_a",
            status="active",
        )
        old_b = self._decision(
            entity_id="decision_b",
            status="active",
        )

        result_1 = detect_conflicts(
            [a, b, old_a, old_b],
        )
        result_2 = detect_conflicts(
            [old_b, old_a, b, a],
        )

        assert [
            (r.entity_a.id, r.entity_b.id)
            for r in result_1
        ] == [
            (r.entity_a.id, r.entity_b.id)
            for r in result_2
        ]
