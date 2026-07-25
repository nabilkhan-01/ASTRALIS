import json
from pathlib import Path

from astralis.models.calendar_event import CalendarEvent
from dataclasses import asdict
from datetime import date


class CalendarMemory:
    """Stores and retrieves calendar events."""

    DATA_FILE = Path(
        "data/calendar.json",
    )

    def __init__(
        self,
    ) -> None:
        self.DATA_FILE.parent.mkdir(
            exist_ok=True,
        )

        if not self.DATA_FILE.exists():
            self.DATA_FILE.write_text(
                "[]",
                encoding="utf-8",
            )

    def add_event(
        self,
        title: str,
        date: str,
        time: str,
    ) -> int:
        """Add a calendar event."""

        events = self._load()

        event = CalendarEvent(
            id=len(events) + 1,
            title=title,
            date=date,
            time=time,
        )

        events.append(event)
        self._save(events)

        return event.id

    def get_events(
        self,
    ) -> list[CalendarEvent]:
        """Returns all calendar events."""
        return self._load()

    def get_today_events(
        self,
    ) -> list[CalendarEvent]:
        """Return today's calendar events."""

        today = date.today().isoformat()

        return [
            event
            for event in self._load()
            if event.date == today
        ]

    
    def delete_event(
        self,
        event_id: int,
    ) -> bool:
        """Delete a calendar event."""

        events = self._load()

        new_events = [
            event
            for event in events
            if event.id != event_id
        ]

        if len(new_events) == len(events):
            return False

        renumbered = [
            CalendarEvent(
                id=index,
                title=event.title,
                date=event.date,
                time=event.time,
                completed=event.completed,
            )
            for index, event in enumerate(new_events, start=1)
        ]

        self._save(renumbered)
        return True


    def _load(
        self,
    ) -> list[CalendarEvent]:
        """Load calendar events."""

        with open(
            self.DATA_FILE,
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        return [
            CalendarEvent(**event)
            for event in data
        ]

    def _save(
        self,
        events: list[CalendarEvent],
    ) -> None:
        """Save calendar events."""

        with open(
            self.DATA_FILE,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                [asdict(event) 
                for event in events],
                file,
                indent=4,
            )