from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class CalendarEvent:
    """Represents a calendar event."""

    id: int
    title: str
    date: str
    time: str
    completed: bool = False
