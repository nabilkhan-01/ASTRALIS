from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class Note:
    """Represents a user note."""

    id: int
    text: str