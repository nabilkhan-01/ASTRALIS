from time import perf_counter
from typing import Self


class Timer:
    """Measures elapsed execution time using a context manager."""

    def __init__(
        self,
    ) -> None:
        self._start = 0.0
        self._end = 0.0

    def start(
        self,
    ) -> None:
        """Start timing."""

        self._start = perf_counter()

    def stop(
        self,
    ) -> None:
        """Stop timing."""

        self._end = perf_counter()

    @property
    def elapsed_ms(
        self,
    ) -> float:
        """Return elapsed time in milliseconds."""

        return (self._end - self._start) * 1000

    def __enter__(
        self,
    ) -> Self:
        """Start timing."""

        self.start()

        return self

    def __exit__(
        self,
        exc_type,
        exc,
        traceback,
    ) -> None:
        """Stop timing."""

        self.stop()