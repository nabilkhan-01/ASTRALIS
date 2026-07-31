from datetime import UTC, datetime

from astralis.memory.calendar import CalendarMemory


class TestCalendarMemory:
    """Tests for CalendarMemory."""

    @staticmethod
    def _create_memory() -> CalendarMemory:
        """Create an empty calendar memory."""

        memory = CalendarMemory()
        memory.clear()

        return memory

    @staticmethod
    def _today() -> str:
        """Return today's date."""

        return (
            datetime.now(
                UTC,
            )
            .date()
            .isoformat()
        )

    def test_add_event(
        self,
    ) -> None:
        """Add a calendar event."""

        memory = self._create_memory()

        event_id = memory.add_event(
            title="Meeting",
            date=self._today(),
            time="10:00",
        )

        assert event_id == 1

    def test_get_events(
        self,
    ) -> None:
        """Return all events."""

        memory = self._create_memory()

        memory.add_event(
            "Meeting",
            self._today(),
            "10:00",
        )

        events = memory.get_events()

        assert len(events) == 1
        assert events[0].title == "Meeting"

    def test_get_today_events(
        self,
    ) -> None:
        """Return today's events."""

        memory = self._create_memory()

        memory.add_event(
            "Meeting",
            self._today(),
            "10:00",
        )

        events = memory.get_today_events()

        assert len(events) == 1

    def test_delete_event(
        self,
    ) -> None:
        """Delete an event."""

        memory = self._create_memory()

        memory.add_event(
            "Meeting",
            self._today(),
            "10:00",
        )

        assert (
            memory.delete_event(
                1,
            )
            is True
        )

        assert memory.get_events() == []

    def test_delete_invalid_event(
        self,
    ) -> None:
        """Deleting a missing event returns False."""

        memory = self._create_memory()

        assert (
            memory.delete_event(
                999,
            )
            is False
        )

    def test_event_ids_are_renumbered(
        self,
    ) -> None:
        """Renumber event IDs after deletion."""

        memory = self._create_memory()

        memory.add_event(
            "First",
            self._today(),
            "10:00",
        )

        memory.add_event(
            "Second",
            self._today(),
            "11:00",
        )

        memory.add_event(
            "Third",
            self._today(),
            "12:00",
        )

        memory.delete_event(
            2,
        )

        events = memory.get_events()

        assert len(events) == 2

        assert events[0].id == 1
        assert events[0].title == "First"

        assert events[1].id == 2
        assert events[1].title == "Third"

    def test_empty_calendar(
        self,
    ) -> None:
        """An empty calendar returns no events."""

        memory = self._create_memory()

        assert memory.get_events() == []
