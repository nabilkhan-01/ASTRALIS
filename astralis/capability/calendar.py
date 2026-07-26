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

        if text.lower().startswith(
            "add event",
        ):
            return self._handle_add_event(
                text,
            )

        if text.lower() == "calendar":
            return self._handle_list_events()

        if text.lower() == "today":
            return self._handle_today()

        if text.lower().startswith(
            "delete event",
        ):
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
                text=("Usage: add event <title> <date> <time>"),
                success=False,
            )

        title = " ".join(parts[2:-2])
        date = parts[-2]
        time = parts[-1]

        event_id = self.calendar.add_event(
            title=title,
            date=date,
            time=time,
        )

        return Response(
            text=f"Event {event_id} added.",
            success=True,
        )

    def _handle_list_events(
        self,
    ) -> Response:
        """List all calendar events."""

        events = self.calendar.get_events()

        if not events:
            return Response(
                text="No events found.",
                success=True,
            )

        lines = []

        for event in events:
            lines.append(f"{event.id}. {event.title} | {event.date} {event.time}")

        return Response(
            text="\n".join(lines),
            success=True,
        )

    def _handle_today(
        self,
    ) -> Response:
        """List today's events."""

        events = self.calendar.get_today_events()

        if not events:
            return Response(
                text="No events for today.",
                success=True,
            )

        lines = []

        for event in events:
            lines.append(f"{event.id}. {event.title} | {event.time}")

        return Response(
            text="\n".join(lines),
            success=True,
        )

    def _handle_delete_event(
        self,
        text: str,
    ) -> Response:
        """Delete a calendar event."""

        parts = text.split()

        if len(parts) != 3:
            return Response(
                text="Please specify the event number",
                success=False,
            )

        event_id = int(
            parts[2],
        )

        deleted = self.calendar.delete_event(
            event_id,
        )

        if not deleted:
            return Response(
                text="Event not found.",
                success=False,
            )

        return Response(
            text="Event deleted.",
            success=True,
        )
