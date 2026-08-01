from astralis.monitoring.monitor import Monitor
from astralis.monitoring.timer import Timer


class TestMonitor:
    """Tests for Monitor."""

    def test_enabled(
        self,
    ) -> None:
        """Return a Timer when monitoring is enabled."""

        monitor = Monitor(
            enabled=True,
        )

        with monitor.measure() as timer:
            pass

        assert isinstance(
            timer,
            Timer,
        )

    def test_disabled(
        self,
    ) -> None:
        """Return a no-op context when monitoring is disabled."""

        monitor = Monitor()

        with monitor.measure() as value:
            pass

        assert value is None