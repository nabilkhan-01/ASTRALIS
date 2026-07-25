import json
from dataclasses import asdict
from pathlib import Path

from astralis.models.note import Note


class NotesMemory:
    """Stores and retrieves user notes."""

    DATA_FILE = Path("data/notes.json")

    def __init__(
        self,
    ) -> None:
        self.DATA_FILE.parent.mkdir(
            exist_ok=True,
        )

        if not self.DATA_FILE.exists():
            self.DATA_FILE.write_text(
                "[]",
                encoding="utf-8",
            )

    def add_note(
        self,
        text: str,
    ) -> int:
        """Add a note."""

        notes = self._load()

        note = Note(
            id=len(notes) + 1,
            text=text,
        )

        notes.append(
            note,
        )

        self._save(
            notes,
        )

        return note.id

    def get_notes(
        self,
    ) -> list[Note]:
        """Return all notes."""

        return self._load()

    def delete_note(
        self,
        note_id: int,
    ) -> bool:
        """Delete a note."""

        notes = self._load()

        new_notes = [
            note
            for note in notes
            if note.id != note_id
        ]

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

        self._save(
            renumbered,
        )

        return True

    def _load(
        self,
    ) -> list[Note]:
        """Load notes."""

        with open(
            self.DATA_FILE,
            encoding="utf-8",
        ) as file:
            data = json.load(
                file,
            )

        return [
            Note(
                **note,
            )
            for note in data
        ]

    def _save(
        self,
        notes: list[Note],
    ) -> None:
        """Save notes."""

        with open(
            self.DATA_FILE,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                [
                    asdict(
                        note,
                    )
                    for note in notes
                ],
                file,
                indent=4,
            )