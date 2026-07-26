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

    def setup_method(self) -> None:
        """Create a NotesCapability."""

        self.notes = NotesMemory()

        self.capability = NotesCapability(
            self.notes,
        )

        # Start every test with empty notes
        self.capability.notes.clear()

    def test_add_note(self) -> None:
        """Add a note."""

        response = self.capability.execute(
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

    def test_list_notes(self) -> None:
        """List notes."""

        self.capability.notes.add_note(
            "Buy milk",
        )

        self.capability.notes.add_note(
            "Complete DSA",
        )

        response = self.capability.execute(
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

    def test_delete_note(self) -> None:
        """Delete a note."""

        self.capability.notes.add_note(
            "Buy milk",
        )

        response = self.capability.execute(
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

    def test_empty_notes(self) -> None:
        """Handle empty notes."""

        response = self.capability.execute(
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

    def test_delete_missing_note(self) -> None:
        """Delete a missing note."""

        response = self.capability.execute(
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

    def test_missing_note_text(self) -> None:
        """Handle missing note text."""

        response = self.capability.execute(
            create_request(
                "note",
            ),
            create_conversation(),
            create_interpretation(
                entities=["notes"],
            ),
        )

        assert response.success is False

    def test_unknown_command(self) -> None:
        """Handle unknown notes command."""

        response = self.capability.execute(
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
