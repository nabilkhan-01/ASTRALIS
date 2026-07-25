from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.capability.capability import Capability
from astralis.memory.note_memory import NotesMemory


class NotesCapability(Capability):
    """Manages user notes."""

    def __init__(self) -> None:
        self.notes = NotesMemory()

    def execute(
        self,
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        """Execute a notes command."""

        _ = conversation, interpretation

        text = request.text.strip()

        try:
            if text.lower().startswith("note "):
                note = text[5:].strip()

                if not note:
                    raise ValueError(
                        "Please provide a note."
                    )

                number = self.notes.add_note(
                    note,
                )

                return Response(
                    text=f"Note {number} saved.",
                    success=True,
                )

            if text.lower() == "notes":
                notes = self.notes.get_notes()

                if not notes:
                    return Response(
                        text="No notes found.",
                        success=True,
                    )

                lines = []

                for note in notes:
                    lines.append(
                        f"{note.id}. {note.text}",
                    )

                return Response(
                    text="\n".join(lines),
                    success=True,
                )

            if text.lower().startswith("delete note"):
                parts = text.split()

                if len(parts) != 3:
                    raise ValueError(
                        "Please specify the note number."
                    )

                number = int(
                    parts[2],
                )

                deleted = self.notes.delete_note(
                    number,
                )

                if not deleted:
                    return Response(
                        text="Note not found.",
                        success=False,
                    )

                return Response(
                    text="Note deleted.",
                    success=True,
                )

            return Response(
                text="Unknown notes command.",
                success=False,
            )

        except Exception as error:
            return Response(
                text=str(error),
                success=False,
            )