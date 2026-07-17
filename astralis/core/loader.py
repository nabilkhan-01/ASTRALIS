from astralis.core.registry import ModuleRegistry


class ModuleLoader:
    """
    Initializes and registers ASTRALIS modules.

    The Module Loader is responsible for creating
    application modules and registering them with
    the Module Registry.
    """

    def __init__(self, registry: ModuleRegistry, logger):
        self._registry = registry
        self._logger = logger

    def load_modules(self) -> None:
        """
        Load and register application modules.
        """

        self._logger.info("Loading application modules...")

        # Future modules will be initialized here.

        self._logger.info("No modules available to load.")