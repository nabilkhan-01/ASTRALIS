from dataclasses import dataclass

from astralis.brain.role import Role


@dataclass(
    frozen=True,
    slots=True,
)
class Message:
    """Represents a message in a conversation."""

    role: Role
    content: str
