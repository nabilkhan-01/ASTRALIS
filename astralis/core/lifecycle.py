from enum import Enum
from typing import ClassVar


class LifecycleState(Enum):
    """Represents the lifecycle state of ASTRALIS."""

    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"


class LifecycleManager:
    """Maintains the lifecycle state of ASTRALIS."""

    _ALLOWED_TRANSITIONS: ClassVar[dict[LifecycleState, set[LifecycleState]]] = {
        LifecycleState.STOPPED: {
            LifecycleState.INITIALIZING,
        },
        LifecycleState.INITIALIZING: {
            LifecycleState.RUNNING,
        },
        LifecycleState.RUNNING: {
            LifecycleState.STOPPING,
        },
        LifecycleState.STOPPING: {
            LifecycleState.STOPPED,
        },
    }

    def __init__(
        self,
    ) -> None:
        self._state = LifecycleState.STOPPED

    @property
    def state(
        self,
    ) -> LifecycleState:
        """Return the current lifecycle state."""

        return self._state

    def transition_to(
        self,
        state: LifecycleState,
    ) -> None:
        """Transition ASTRALIS to a new lifecycle state."""

        allowed = self._ALLOWED_TRANSITIONS[self._state]

        if state not in allowed:
            raise ValueError(
                f"Invalid lifecycle transition: {self._state.value} -> {state.value}"
            )

        self._state = state
