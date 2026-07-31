from astralis.capability.notes import NotesCapability
from astralis.memory.note import NotesMemory
from tests.helpers.conversation_factory import (
    create_conversation,
)
from tests.helpers.interpretation_factory import (
    create_interpretation,
)
from tests.helpers.request_factory import (
    create_request,
)


class TestNotesCapability:
    """Tests for the NotesCapability."""

    @staticmethod
    def _create_capability() -> NotesCapability:
        """Create a clean notes capability."""

        notes = NotesMemory()
        notes.clear()

        return NotesCapability(
            notes,
        )

    def test_add_note(
        self,
    ) -> None:
        """Add a note."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "note Buy milk",
            ),
            create_conversation(),
            create_interpretation(
                entities=["notes"],
            ),
        )

        assert response.success is True
        assert response.text == "Note 1 saved."

    def test_list_notes(
        self,
    ) -> None:
        """List notes."""

        capability = self._create_capability()

        capability.notes.add_note(
            "Buy milk",
        )

        capability.notes.add_note(
            "Complete DSA",
        )

        response = capability.execute(
            create_request(
                "notes",
            ),
            create_conversation(),
            create_interpretation(
                entities=["notes"],
            ),
        )

        assert response.success is True
        assert "1. Buy milk" in response.text
        assert "2. Complete DSA" in response.text

    def test_delete_note(
        self,
    ) -> None:
        """Delete a note."""

        capability = self._create_capability()

        capability.notes.add_note(
            "Buy milk",
        )

        response = capability.execute(
            create_request(
                "delete note 1",
            ),
            create_conversation(),
            create_interpretation(
                entities=["notes"],
            ),
        )

        assert response.success is True
        assert response.text == "Note deleted."

    def test_empty_notes(
        self,
    ) -> None:
        """Handle empty notes."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "notes",
            ),
            create_conversation(),
            create_interpretation(
                entities=["notes"],
            ),
        )

        assert response.success is True
        assert response.text == "No notes found."

    def test_delete_missing_note(
        self,
    ) -> None:
        """Delete a missing note."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "delete note 5",
            ),
            create_conversation(),
            create_interpretation(
                entities=["notes"],
            ),
        )

        assert response.success is False
        assert response.text == "Note not found."

    def test_missing_note_text(
        self,
    ) -> None:
        """Handle missing note text."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "note",
            ),
            create_conversation(),
            create_interpretation(
                entities=["notes"],
            ),
        )

        assert response.success is False
        assert response.text == "Unknown notes command."

    def test_unknown_command(
        self,
    ) -> None:
        """Handle an unknown notes command."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "delete everything",
            ),
            create_conversation(),
            create_interpretation(
                entities=["notes"],
            ),
        )

        assert response.success is False
        assert response.text == "Unknown notes command."
