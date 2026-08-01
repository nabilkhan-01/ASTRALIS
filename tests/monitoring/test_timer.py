from time import sleep

from astralis.monitoring.timer import Timer


class TestTimer:
    """Tests for Timer."""

    def test_context_manager(
        self,
    ) -> None:
        """Measure elapsed time."""

        with Timer() as timer:
            sleep(
                0.05,
            )

        assert timer.elapsed_ms >= 50

    def test_manual_start_stop(
        self,
    ) -> None:
        """Measure elapsed time manually."""

        timer = Timer()

        timer.start()

        sleep(
            0.02,
        )

        timer.stop()

        assert timer.elapsed_ms >= 20