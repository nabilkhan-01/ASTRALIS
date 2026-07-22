from astralis.brain.intent import Intent
from astralis.brain.interpretation import Interpretation


def create_interpretation(
    intent: Intent = Intent.CONVERSATION,
    entities: list[str] | None = None,
) -> Interpretation:
    """Create an interpretation for testing."""

    return Interpretation(
        intent=intent,
        entities=entities or [],
    )