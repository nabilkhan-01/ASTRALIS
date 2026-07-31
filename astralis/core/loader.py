from logging import Logger

from astralis.core.registry import ModuleRegistry


class ModuleLoader:
    """Initializes and registers ASTRALIS modules."""

    def __init__(
        self,
        registry: ModuleRegistry,
        logger: Logger,
    ) -> None:
        self._registry = registry
        self._logger = logger

    def load_modules(
        self,
    ) -> int:
        """Load and register application modules."""

        self._logger.info(
            "Loading application modules...",
        )

        loaded = 0

        self._logger.info(
            f"Loaded {loaded} module(s).",
        )

        return loaded
