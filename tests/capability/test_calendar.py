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

    @staticmethod
    def _create_capability() -> CalendarCapability:
        """Create a clean calendar capability."""

        calendar = CalendarMemory()
        calendar.clear()

        return CalendarCapability(
            calendar,
        )

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
        """Add an event."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                f"add event Meeting {self._today()} 10:00",
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

        capability = self._create_capability()

        capability.calendar.add_event(
            "Meeting",
            self._today(),
            "10:00",
        )

        response = capability.execute(
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

        capability = self._create_capability()

        capability.calendar.add_event(
            "Meeting",
            self._today(),
            "10:00",
        )

        response = capability.execute(
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

        capability = self._create_capability()

        capability.calendar.add_event(
            "Meeting",
            self._today(),
            "10:00",
        )

        response = capability.execute(
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
        """Handle an empty calendar."""

        capability = self._create_capability()

        response = capability.execute(
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

        capability = self._create_capability()

        response = capability.execute(
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
        """Handle an unknown calendar command."""

        capability = self._create_capability()

        response = capability.execute(
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
