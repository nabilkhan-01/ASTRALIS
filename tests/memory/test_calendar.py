from datetime import UTC, datetime

from astralis.memory.calendar import CalendarMemory


class TestCalendarMemory:
    """Tests for CalendarMemory."""

    def setup_method(
        self,
    ) -> None:
        self.memory = CalendarMemory()

        self.memory.clear()

    def test_add_event(
        self,
    ) -> None:
        """Add a calendar event."""

        event_id = self.memory.add_event(
            title="Meeting",
            date=datetime.now(UTC).date().isoformat(),
            time="10:00",
        )

        assert event_id == 1

    def test_get_events(
        self,
    ) -> None:
        """Return all events."""

        self.memory.add_event(
            "Meeting",
            datetime.now(UTC).date().isoformat(),
            "10:00",
        )

        events = self.memory.get_events()

        assert len(events) == 1
        assert events[0].title == "Meeting"

    def test_get_today_events(
        self,
    ) -> None:
        """Return today's events."""

        today = datetime.now(UTC).date().isoformat()

        self.memory.add_event(
            "Meeting",
            today,
            "10:00",
        )

        events = self.memory.get_today_events()

        assert len(events) == 1

    def test_delete_event(
        self,
    ) -> None:
        """Delete an event."""

        self.memory.add_event(
            "Meeting",
            datetime.now(UTC).date().isoformat(),
            "10:00",
        )

        assert self.memory.delete_event(
            1,
        )

        assert self.memory.get_events() == []

    def test_delete_invalid_event(
        self,
    ) -> None:
        """Deleting a missing event returns False."""

        assert not self.memory.delete_event(
            999,
        )

    def test_event_ids_are_renumbered(
        self,
    ) -> None:
        """Renumber event IDs after deletion."""

        today = datetime.now(UTC).date().isoformat()

        self.memory.add_event(
            "First",
            today,
            "10:00",
        )

        self.memory.add_event(
            "Second",
            today,
            "11:00",
        )

        self.memory.add_event(
            "Third",
            today,
            "12:00",
        )

        self.memory.delete_event(
            2,
        )

        events = self.memory.get_events()

        assert len(events) == 2
        assert events[0].id == 1
        assert events[1].id == 2
        assert events[1].title == "Third"

    def test_empty_calendar(
        self,
    ) -> None:
        """An empty calendar returns no events."""

        assert self.memory.get_events() == []
