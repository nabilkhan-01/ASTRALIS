from dataclasses import dataclass

from astralis.brain.source import RequestSource


@dataclass
class Request:
    """Represents a request received by ASTRALIS."""

    text: str
    source: RequestSource