from enum import Enum


class ConfidenceLevel(
    Enum,
):
    """Represents the certainty assigned to a knowledge artifact at record time.

    Confidence reflects the author's or source's certainty when the knowledge
    was recorded. It is not a system-verified truth claim and is not inferred
    from provenance, freshness, or relevance.
    """

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
