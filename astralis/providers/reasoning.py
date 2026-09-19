from __future__ import annotations

from enum import Enum


class ReasoningMode(str, Enum):
    """Represents the reasoning intensity for language model providers.

    - FAST: Disables extended thinking/reasoning for responsive execution.
    - DEEP: Enables extended thinking/reasoning for complex problem solving.
    - AUTO: Default baseline mode; foundation for future task-aware routing.
    """

    FAST = "fast"
    DEEP = "deep"
    AUTO = "auto"

    @classmethod
    def from_string(
        cls,
        value: str | ReasoningMode,
    ) -> ReasoningMode:
        """Parse a string into a ReasoningMode case-insensitively.

        Raises:
            TypeError: If the value is not a string or ReasoningMode.
            ValueError: If the value cannot be mapped to a valid ReasoningMode.
        """

        if isinstance(value, cls):
            return value

        if not isinstance(value, str):
            raise TypeError(
                f"Invalid reasoning mode type: {type(value).__name__}. "
                "Expected str or ReasoningMode.",
            )

        cleaned = value.strip().lower()

        for mode in cls:
            if mode.value == cleaned:
                return mode

        raise ValueError(
            f"Invalid reasoning mode: {value!r}. Expected one of: "
            f"{', '.join(mode.value for mode in cls)}.",
        )
