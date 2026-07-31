from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

from astralis.memory.base import BaseMemory
from astralis.models.calendar_event import CalendarEvent
from astralis.storage.json import JsonStorage


class CalendarMemory(BaseMemory[CalendarEvent]):
    """Stores and retrieves calendar events."""

    MODEL = CalendarEvent

    DATA_FILE = Path(
        "data/calendar.json",
    )

    def __init__(
        self,
    ) -> None:
        super().__init__(
            JsonStorage(
                self.DATA_FILE,
            ),
        )

    def add_event(
        self,
        title: str,
        date: str,
        time: str,
    ) -> int:
        """Add a calendar event."""

        events = self._load_models()

        event = CalendarEvent(
            id=len(events) + 1,
            title=title,
            date=date,
            time=time,
        )

        events.append(
            event,
        )

        self._save_models(
            events,
        )

        return event.id

    def get_events(
        self,
    ) -> list[CalendarEvent]:
        """Return all calendar events."""

        return self._load_models()

    def clear(
        self,
    ) -> None:
        """Remove all stored calendar events."""

        self._save_models(
            [],
        )

    def get_today_events(
        self,
    ) -> list[CalendarEvent]:
        """Return today's calendar events."""

        today = (
            datetime.now(
                UTC,
            )
            .date()
            .isoformat()
        )

        return [event for event in self._load_models() if event.date == today]

    def delete_event(
        self,
        event_id: int,
    ) -> bool:
        """Delete a calendar event."""

        events = self._load_models()

        new_events = [event for event in events if event.id != event_id]

        if len(new_events) == len(events):
            return False

        renumbered = [
            replace(
                event,
                id=index,
            )
            for index, event in enumerate(
                new_events,
                start=1,
            )
        ]

        self._save_models(
            renumbered,
        )

        return True
