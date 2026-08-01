from contextlib import AbstractContextManager, nullcontext
from typing import Any

from astralis.monitoring.timer import Timer


class Monitor:
    """Controls performance monitoring."""

    def __init__(
        self,
        enabled: bool = False,
    ) -> None:
        self._enabled = enabled

    @property
    def enabled(
        self,
    ) -> bool:
        """Return whether monitoring is enabled."""

        return self._enabled

    def measure(
        self,
    ) -> AbstractContextManager[Any]:
        """Return a timing context when monitoring is enabled."""

        if not self._enabled:
            return nullcontext()

        return Timer()