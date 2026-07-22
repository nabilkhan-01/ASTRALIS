from astralis.brain.request import Request
from astralis.brain.source import RequestSource


def create_request(
    text: str,
) -> Request:
    """Create a CLI request for testing."""

    return Request(
        text=text,
        source=RequestSource.CLI,
    )