from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.capability.capability import Capability
from astralis.memory.calendar import CalendarMemory


class CalendarCapability(Capability):
    """Manages calendar events."""

    def __init__(
        self,
        calendar: CalendarMemory,
    ) -> None:
        self.calendar = calendar

    def execute(
        self,
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        """Execute a calendar command."""

        _ = conversation, interpretation

        text = request.text.strip()
        lower = text.lower()

        if lower.startswith("add event"):
            return self._handle_add_event(
                text,
            )

        if lower == "calendar":
            return self._handle_list_events()

        if lower == "today":
            return self._handle_today()

        if lower.startswith("delete event"):
            return self._handle_delete_event(
                text,
            )

        return Response(
            text="Unknown calendar command.",
            success=False,
        )

    def _handle_add_event(
        self,
        text: str,
    ) -> Response:
        """Add a calendar event."""

        parts = text.split()

        if len(parts) < 5:
            return Response(
                text="Usage: add event <title> <date> <time>",
                success=False,
            )

        title = " ".join(
            parts[2:-2],
        )
        date = parts[-2]
        time = parts[-1]

        event_id = self.calendar.add_event(
            title=title,
            date=date,
            time=time,
        )

        return Response(
            text=f"Event {event_id} added.",
        )

    def _handle_list_events(
        self,
    ) -> Response:
        """List all calendar events."""

        events = self.calendar.get_events()

        if not events:
            return Response(
                text="No events found.",
            )

        lines = [
            f"{event.id}. {event.title} | {event.date} {event.time}" for event in events
        ]

        return Response(
            text="\n".join(
                lines,
            ),
        )

    def _handle_today(
        self,
    ) -> Response:
        """List today's events."""

        events = self.calendar.get_today_events()

        if not events:
            return Response(
                text="No events for today.",
            )

        lines = [f"{event.id}. {event.title} | {event.time}" for event in events]

        return Response(
            text="\n".join(
                lines,
            ),
        )

    def _handle_delete_event(
        self,
        text: str,
    ) -> Response:
        """Delete a calendar event."""

        event_id = self._parse_event_id(
            text,
        )

        if event_id is None:
            return Response(
                text="Usage: delete event <id>",
                success=False,
            )

        if not self.calendar.delete_event(
            event_id,
        ):
            return Response(
                text="Event not found.",
                success=False,
            )

        return Response(
            text="Event deleted.",
        )

    def _parse_event_id(
        self,
        text: str,
    ) -> int | None:
        """Extract an event ID from a command."""

        parts = text.split()

        if len(parts) != 3:
            return None

        if not parts[2].isdigit():
            return None

        return int(
            parts[2],
        )
