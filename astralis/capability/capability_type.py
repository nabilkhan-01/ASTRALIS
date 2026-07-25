from enum import Enum
from enum import auto


class CapabilityType(Enum):
    """Identifies the capability selected by the Brain."""

    AUTOMATION = auto()
    ALARM = auto()
    BROWSER = auto()
    CALCULATOR = auto()
    CALENDAR = auto()
    EMAIL = auto()
    LANGUAGE = auto()
    FILE_SYSTEM = auto()
    MEMORY = auto()
    NOTES = auto()
    SEARCH = auto()
    TIME = auto()
    WEATHER = auto()