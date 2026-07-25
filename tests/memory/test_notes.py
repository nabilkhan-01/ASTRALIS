from astralis.memory.note_memory import NotesMemory


class TestNotesMemory:
    """Tests for NotesMemory."""

    def setup_method(
        self,
    ) -> None:
        self.memory = NotesMemory()

        self.memory._save(
            [],
        )

    def test_add_note(
        self,
    ) -> None:
        """Add a note."""

        note_id = self.memory.add_note(
            "Buy milk",
        )

        assert note_id == 1

    def test_get_notes(
        self,
    ) -> None:
        """Return all notes."""

        self.memory.add_note(
            "Buy milk",
        )

        self.memory.add_note(
            "Complete DSA",
        )

        notes = self.memory.get_notes()

        assert len(
            notes,
        ) == 2

        assert notes[0].id == 1
        assert notes[0].text == "Buy milk"

        assert notes[1].id == 2
        assert notes[1].text == "Complete DSA"

    def test_delete_note(
        self,
    ) -> None:
        """Delete a note."""

        self.memory.add_note(
            "Buy milk",
        )

        assert self.memory.delete_note(
            1,
        )

        assert self.memory.get_notes() == []

    def test_delete_invalid_note(
        self,
    ) -> None:
        """Deleting a missing note returns False."""

        assert not self.memory.delete_note(
            999,
        )

    def test_note_ids_are_renumbered(
        self,
    ) -> None:
        """Renumber note IDs after deletion."""

        self.memory.add_note(
            "First",
        )

        self.memory.add_note(
            "Second",
        )

        self.memory.add_note(
            "Third",
        )

        self.memory.delete_note(
            2,
        )

        notes = self.memory.get_notes()

        assert len(
            notes,
        ) == 2

        assert notes[0].id == 1
        assert notes[0].text == "First"

        assert notes[1].id == 2
        assert notes[1].text == "Third"

    def test_empty_notes(
        self,
    ) -> None:
        """An empty notes list returns no notes."""

        assert self.memory.get_notes() == []