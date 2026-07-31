from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class Response:
    """Represents the result of processing a user request."""

    text: str
    success: bool = True
