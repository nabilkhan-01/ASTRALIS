from dataclasses import dataclass

from astralis.brain.intent import Intent


@dataclass
class Interpretation:
    """Represents the Brain's understanding of a request."""

    intent: Intent
    