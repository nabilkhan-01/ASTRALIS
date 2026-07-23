import json
from pathlib import Path


class NotesMemory:
    """Stores and retrieves user notes."""

    DATA_FILE = Path("data/notes.json")

    def __init__(self) -> None:
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

        notes.append(
            text,
        )

        self._save(
            notes,
        )

        return len(notes)

    def get_notes(self) -> list[str]:
        """Return all notes."""

        return self._load()

    def delete_note(
        self,
        note_id: int,
    ) -> bool:
        """Delete a note."""

        notes = self._load()

        index = note_id - 1

        if index < 0 or index >= len(notes):
            return False

        del notes[index]

        self._save(
            notes, 
        )

        return True

    def _load(
        self,
    ) -> list[str]:
        """Load notes."""

        with open(
            self.DATA_FILE,
            encoding="utf-8",
        ) as file:
            return json.load(
                file,
            )

    def _save(
        self,
        notes: list[str],
    ) -> None:
        """Save notes."""

        with open(
            self.DATA_FILE,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                notes,
                file,
                indent=4,
            )