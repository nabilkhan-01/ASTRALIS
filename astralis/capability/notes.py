from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.capability.capability import Capability
from astralis.memory.note import NotesMemory


class NotesCapability(Capability):
    """Manages user notes."""

    def __init__(
        self,
        notes: NotesMemory,
    ) -> None:
        self.notes = notes

    def execute(
        self,
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        """Execute a notes command."""

        _ = conversation, interpretation

        text = request.text.strip()
        lower = text.lower()

        if lower.startswith(
            "note ",
        ):
            return self._handle_add_note(
                text,
            )

        if lower == "notes":
            return self._handle_list_notes()

        if lower.startswith(
            "delete note",
        ):
            return self._handle_delete_note(
                text,
            )

        return Response(
            text="Unknown notes command.",
            success=False,
        )

    def _handle_add_note(
        self,
        text: str,
    ) -> Response:
        """Add a note."""

        note_text = text[5:].strip()

        if not note_text:
            return Response(
                text="Please provide a note.",
                success=False,
            )

        note_id = self.notes.add_note(
            note_text,
        )

        return Response(
            text=f"Note {note_id} saved.",
        )

    def _handle_list_notes(
        self,
    ) -> Response:
        """List all notes."""

        notes = self.notes.get_notes()

        if not notes:
            return Response(
                text="No notes found.",
            )

        lines = [f"{note.id}. {note.text}" for note in notes]

        return Response(
            text="\n".join(
                lines,
            ),
        )

    def _handle_delete_note(
        self,
        text: str,
    ) -> Response:
        """Delete a note."""

        note_id = self._parse_note_id(
            text,
        )

        if note_id is None:
            return Response(
                text="Usage: delete note <id>",
                success=False,
            )

        if not self.notes.delete_note(
            note_id,
        ):
            return Response(
                text="Note not found.",
                success=False,
            )

        return Response(
            text="Note deleted.",
        )

    def _parse_note_id(
        self,
        text: str,
    ) -> int | None:
        """Extract a note ID from a command."""

        parts = text.split()

        if len(parts) != 3:
            return None

        if not parts[2].isdigit():
            return None

        return int(
            parts[2],
        )
