from astralis.memory.note import NotesMemory


class TestNotesMemory:
    """Tests for NotesMemory."""

    @staticmethod
    def _create_memory() -> NotesMemory:
        """Create an empty notes memory."""

        memory = NotesMemory()
        memory.clear()

        return memory

    def test_add_note(
        self,
    ) -> None:
        """Add a note."""

        memory = self._create_memory()

        note_id = memory.add_note(
            "Buy milk",
        )

        assert note_id == 1

    def test_get_notes(
        self,
    ) -> None:
        """Return all notes."""

        memory = self._create_memory()

        memory.add_note(
            "Buy milk",
        )

        memory.add_note(
            "Complete DSA",
        )

        notes = memory.get_notes()

        assert len(notes) == 2

        assert notes[0].id == 1
        assert notes[0].text == "Buy milk"

        assert notes[1].id == 2
        assert notes[1].text == "Complete DSA"

    def test_delete_note(
        self,
    ) -> None:
        """Delete a note."""

        memory = self._create_memory()

        memory.add_note(
            "Buy milk",
        )

        assert (
            memory.delete_note(
                1,
            )
            is True
        )

        assert memory.get_notes() == []

    def test_delete_invalid_note(
        self,
    ) -> None:
        """Deleting a missing note returns False."""

        memory = self._create_memory()

        assert (
            memory.delete_note(
                999,
            )
            is False
        )

    def test_note_ids_are_renumbered(
        self,
    ) -> None:
        """Renumber note IDs after deletion."""

        memory = self._create_memory()

        memory.add_note(
            "First",
        )

        memory.add_note(
            "Second",
        )

        memory.add_note(
            "Third",
        )

        memory.delete_note(
            2,
        )

        notes = memory.get_notes()

        assert len(notes) == 2

        assert notes[0].id == 1
        assert notes[0].text == "First"

        assert notes[1].id == 2
        assert notes[1].text == "Third"

    def test_empty_notes(
        self,
    ) -> None:
        """An empty notes list returns no notes."""

        memory = self._create_memory()

        assert memory.get_notes() == []
