from enum import Enum, auto


class CapabilityType(Enum):
    """Identifies the capability selected by the Brain."""

    LANGUAGE = auto()

    SEARCH = auto()
    WEATHER = auto()
    TIME = auto()
    CALCULATOR = auto()

    NOTES = auto()
    MEMORY = auto()
    CALENDAR = auto()
    ALARM = auto()

    BROWSER = auto()
    FILE_SYSTEM = auto()
    EMAIL = auto()

    AUTOMATION = auto()
