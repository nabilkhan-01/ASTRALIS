from datetime import datetime, timedelta, timezone

from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
from astralis.memory.freshness import FreshnessStatus, assess_freshness


class TestFreshnessAssessment:
    """Tests for assess_freshness."""

    def _entity(
        self,
        updated_at: str | None = None,
    ) -> Entity:
        """Create a minimal entity with the given updated_at."""

        return Entity(
            id="e1",
            type=EntityType.NOTE,
            name="Test Entity",
            updated_at=updated_at,
        )

    def test_missing_updated_at_returns_unknown(
        self,
    ) -> None:
        """Return UNKNOWN when updated_at is None."""

        entity = self._entity(
            updated_at=None,
        )

        result = assess_freshness(
            entity=entity,
            threshold=timedelta(days=7),
            reference_time=datetime(
                2026,
                8,
                27,
                12,
                0,
                0,
                tzinfo=timezone.utc,
            ),
        )

        assert result is FreshnessStatus.UNKNOWN

    def test_malformed_updated_at_returns_unknown(
        self,
    ) -> None:
        """Return UNKNOWN when updated_at cannot be parsed."""

        entity = self._entity(
            updated_at="not-a-date",
        )

        result = assess_freshness(
            entity=entity,
            threshold=timedelta(days=7),
            reference_time=datetime(
                2026,
                8,
                27,
                12,
                0,
                0,
                tzinfo=timezone.utc,
            ),
        )

        assert result is FreshnessStatus.UNKNOWN

    def test_within_threshold_returns_fresh(
        self,
    ) -> None:
        """Return FRESH when updated_at is within the threshold."""

        reference = datetime(
            2026,
            8,
            27,
            12,
            0,
            0,
            tzinfo=timezone.utc,
        )

        entity = self._entity(
            updated_at="2026-08-27T10:00:00+00:00",
        )

        result = assess_freshness(
            entity=entity,
            threshold=timedelta(hours=3),
            reference_time=reference,
        )

        assert result is FreshnessStatus.FRESH

    def test_exactly_at_threshold_returns_fresh(
        self,
    ) -> None:
        """Return FRESH when updated_at is exactly at the threshold boundary."""

        reference = datetime(
            2026,
            8,
            27,
            12,
            0,
            0,
            tzinfo=timezone.utc,
        )

        entity = self._entity(
            updated_at="2026-08-27T09:00:00+00:00",
        )

        result = assess_freshness(
            entity=entity,
            threshold=timedelta(hours=3),
            reference_time=reference,
        )

        assert result is FreshnessStatus.FRESH

    def test_beyond_threshold_returns_stale(
        self,
    ) -> None:
        """Return STALE when updated_at is beyond the threshold."""

        reference = datetime(
            2026,
            8,
            27,
            12,
            0,
            0,
            tzinfo=timezone.utc,
        )

        entity = self._entity(
            updated_at="2026-08-20T12:00:00+00:00",
        )

        result = assess_freshness(
            entity=entity,
            threshold=timedelta(days=3),
            reference_time=reference,
        )

        assert result is FreshnessStatus.STALE

    def test_explicit_reference_time_is_deterministic(
        self,
    ) -> None:
        """Explicit reference_time produces repeatable results."""

        entity = self._entity(
            updated_at="2026-08-25T12:00:00+00:00",
        )

        reference = datetime(
            2026,
            8,
            27,
            12,
            0,
            0,
            tzinfo=timezone.utc,
        )

        result_a = assess_freshness(
            entity=entity,
            threshold=timedelta(days=7),
            reference_time=reference,
        )

        result_b = assess_freshness(
            entity=entity,
            threshold=timedelta(days=7),
            reference_time=reference,
        )

        assert result_a is result_b is FreshnessStatus.FRESH

    def test_timezone_aware_iso8601_timestamp(
        self,
    ) -> None:
        """Accept and correctly interpret a timezone-aware ISO-8601 timestamp."""

        reference = datetime(
            2026,
            8,
            27,
            12,
            0,
            0,
            tzinfo=timezone.utc,
        )

        entity = self._entity(
            updated_at="2026-08-27T17:00:00+05:30",
        )

        result = assess_freshness(
            entity=entity,
            threshold=timedelta(hours=2),
            reference_time=reference,
        )

        assert result is FreshnessStatus.FRESH

    def test_does_not_mutate_entity(
        self,
    ) -> None:
        """assess_freshness must not modify the entity."""

        entity = self._entity(
            updated_at="2026-08-20T00:00:00+00:00",
        )

        original_updated_at = entity.updated_at
        original_id = entity.id

        assess_freshness(
            entity=entity,
            threshold=timedelta(days=1),
            reference_time=datetime(
                2026,
                8,
                27,
                12,
                0,
                0,
                tzinfo=timezone.utc,
            ),
        )

        assert entity.updated_at == original_updated_at
        assert entity.id == original_id
