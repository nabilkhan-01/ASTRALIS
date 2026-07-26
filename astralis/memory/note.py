from pathlib import Path

from astralis.memory.base import BaseMemory
from astralis.models.note import Note
from astralis.storage import JsonStorage


class NotesMemory(BaseMemory[Note]):
    """Stores and retrieves user notes."""

    MODEL = Note

    DATA_FILE = Path(
        "data/notes.json",
    )

    def __init__(
        self,
    ) -> None:
        super().__init__(
            JsonStorage(
                self.DATA_FILE,
            ),
        )

    def add_note(
        self,
        text: str,
    ) -> int:
        """Add a note."""

        notes = self._load_models()

        note = Note(
            id=len(notes) + 1,
            text=text,
        )

        notes.append(
            note,
        )

        self._save_models(
            notes,
        )

        return note.id

    def get_notes(
        self,
    ) -> list[Note]:
        """Return all notes."""

        return self._load_models()

    def delete_note(
        self,
        note_id: int,
    ) -> bool:
        """Delete a note."""

        notes = self._load_models()

        new_notes = [note for note in notes if note.id != note_id]

        if len(new_notes) == len(notes):
            return False

        renumbered = [
            Note(
                id=index,
                text=note.text,
            )
            for index, note in enumerate(
                new_notes,
                start=1,
            )
        ]

        self._save_models(
            renumbered,
        )

        return True
