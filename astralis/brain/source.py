from enum import Enum


class RequestSource(Enum):
    """Represents the origin of a user request."""

    CLI = "cli"
    DESKTOP = "desktop"
    VOICE = "voice"
    API = "api"
