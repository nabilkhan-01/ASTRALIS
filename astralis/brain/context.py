from dataclasses import dataclass

from astralis.brain.request import Request
from astralis.memory.entity import Entity


@dataclass(
    frozen=True,
    slots=True,
)
class BrainContext:
    """Represents the context available to the Brain."""

    request: Request
    memory: list[Entity]