from dataclasses import dataclass


@dataclass
class Response:
    """Represents the result of processing a user request."""

    text: str
    success: bool = True