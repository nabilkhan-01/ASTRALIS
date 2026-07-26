from enum import Enum, auto


class Intent(Enum):
    """High-level request intent."""

    GREETING = auto()
    QUESTION = auto()
    CONVERSATION = auto()
    MEMORY = auto()
    SYSTEM = auto()
    UNKNOWN = auto()
