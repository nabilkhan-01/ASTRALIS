from datetime import UTC, datetime

from astralis.capability.calendar import CalendarCapability
from astralis.memory.calendar import CalendarMemory
from tests.helpers.conversation_factory import (
    create_conversation,
)
from tests.helpers.interpretation_factory import (
    create_interpretation,
)
from tests.helpers.request_factory import (
    create_request,
)


class TestCalendarCapability:
    """Tests for CalendarCapability."""

    def setup_method(
        self,
    ) -> None:

        self.calendar = CalendarMemory()

        self.capability = CalendarCapability(
            self.calendar,
        )

        self.capability.calendar.clear()

    def test_add_event(
        self,
    ) -> None:
        """Add an event."""

        today = datetime.now(tz=UTC).date().isoformat()

        response = self.capability.execute(
            create_request(
                f"add event Meeting {today} 10:00",
            ),
            create_conversation(),
            create_interpretation(
                entities=["calendar"],
            ),
        )

        assert response.success is True
        assert response.text == "Event 1 added."

    def test_list_events(
        self,
    ) -> None:
        """List events."""

        today = datetime.now(UTC).date().isoformat()

        self.capability.calendar.add_event(
            "Meeting",
            today,
            "10:00",
        )

        response = self.capability.execute(
            create_request(
                "calendar",
            ),
            create_conversation(),
            create_interpretation(
                entities=["calendar"],
            ),
        )

        assert response.success is True
        assert "Meeting" in response.text

    def test_today(
        self,
    ) -> None:
        """List today's events."""

        today = datetime.now(UTC).date().isoformat()

        self.capability.calendar.add_event(
            "Meeting",
            today,
            "10:00",
        )

        response = self.capability.execute(
            create_request(
                "today",
            ),
            create_conversation(),
            create_interpretation(
                entities=["calendar"],
            ),
        )

        assert response.success is True
        assert "Meeting" in response.text

    def test_delete_event(
        self,
    ) -> None:
        """Delete an event."""

        today = datetime.now(UTC).date().isoformat()

        self.capability.calendar.add_event(
            "Meeting",
            today,
            "10:00",
        )

        response = self.capability.execute(
            create_request(
                "delete event 1",
            ),
            create_conversation(),
            create_interpretation(
                entities=["calendar"],
            ),
        )

        assert response.success is True
        assert response.text == "Event deleted."

    def test_empty_calendar(
        self,
    ) -> None:
        """Handle empty calendar."""

        response = self.capability.execute(
            create_request(
                "calendar",
            ),
            create_conversation(),
            create_interpretation(
                entities=["calendar"],
            ),
        )

        assert response.success is True
        assert response.text == "No events found."

    def test_delete_missing_event(
        self,
    ) -> None:
        """Delete a missing event."""

        response = self.capability.execute(
            create_request(
                "delete event 5",
            ),
            create_conversation(),
            create_interpretation(
                entities=["calendar"],
            ),
        )

        assert response.success is False
        assert response.text == "Event not found."

    def test_unknown_command(
        self,
    ) -> None:
        """Handle unknown calendar command."""

        response = self.capability.execute(
            create_request(
                "delete everything",
            ),
            create_conversation(),
            create_interpretation(
                entities=["calendar"],
            ),
        )

        assert response.success is False
        assert response.text == "Unknown calendar command."
