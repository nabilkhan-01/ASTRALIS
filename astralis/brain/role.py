from enum import Enum


class Role(Enum):
    """Represents the role of a conversation message."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"