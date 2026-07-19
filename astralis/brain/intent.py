from enum import Enum, auto


class Intent(Enum):
    """High-level request intent."""

    GENERAL = auto()
    GREETING = auto()
    QUESTION = auto()
    COMMAND = auto()