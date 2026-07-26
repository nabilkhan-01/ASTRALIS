from enum import Enum


class LifecycleState(Enum):
    """Represents the lifecycle state of ASTRALIS."""

    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"


class LifecycleManager:
    """Maintains the lifecycle state of ASTRALIS."""

    def __init__(self) -> None:
        self._state = LifecycleState.STOPPED

    @property
    def state(self) -> LifecycleState:
        """Return the current lifecycle state."""
        return self._state

    def transition_to(self, state: LifecycleState) -> None:
        """Transition ASTRALIS to a new lifecycle state."""
        self._state = state
