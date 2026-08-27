from dataclasses import dataclass

from astralis.brain.request import Request
from astralis.context.context import Context


@dataclass(
    frozen=True,
    slots=True,
)
class BrainContext:
    """Represents the context available to the Brain."""

    request: Request
    context: Context