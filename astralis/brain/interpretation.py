from dataclasses import dataclass, field

from astralis.brain.intent import Intent


@dataclass(
    frozen=True,
    slots=True,
)
class Interpretation:
    """Represents the Brain's understanding of a request."""

    intent: Intent
    entities: list[str] = field(
        default_factory=list,
    )
