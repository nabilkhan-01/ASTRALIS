from datetime import datetime, timedelta, timezone
from enum import Enum

from astralis.memory.entity import Entity


class FreshnessStatus(
    Enum,
):
    """Represents the freshness assessment of a retrieved entity."""

    FRESH = "fresh"
    STALE = "stale"
    UNKNOWN = "unknown"


def assess_freshness(
    entity: Entity,
    threshold: timedelta,
    reference_time: datetime | None = None,
) -> FreshnessStatus:
    """Assess whether an entity's knowledge is fresh relative to a threshold.

    Returns UNKNOWN when updated_at is absent or unparseable.
    Returns FRESH when updated_at is within the threshold.
    Returns STALE when updated_at is beyond the threshold.

    The caller supplies the threshold and owns all freshness policy.
    This function does not modify the entity or affect retrieval.
    """

    if entity.updated_at is None:
        return FreshnessStatus.UNKNOWN

    try:
        updated = datetime.fromisoformat(entity.updated_at)
    except (ValueError, TypeError):
        return FreshnessStatus.UNKNOWN

    if updated.tzinfo is None:
        updated = updated.replace(
            tzinfo=timezone.utc,
        )

    reference = reference_time or datetime.now(
        timezone.utc,
    )

    if (reference - updated) <= threshold:
        return FreshnessStatus.FRESH

    return FreshnessStatus.STALE
