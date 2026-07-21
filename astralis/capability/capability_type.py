from enum import Enum
from enum import auto


class CapabilityType(Enum):
    """Identifies the capability selected by the Brain."""

    LANGUAGE = auto()
    MEMORY = auto()
    TIME = auto()
    WEATHER = auto()
    BROWSER = auto()
    CALENDAR = auto()
    EMAIL = auto()
    AUTOMATION = auto()