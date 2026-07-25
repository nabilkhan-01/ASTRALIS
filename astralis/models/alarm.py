from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class Alarm:
    """Represents an alarm."""

    id: int
    title: str
    time: str
    enabled: bool = True