from astralis.core.config import Config
from astralis.core.loader import ModuleLoader
from astralis.core.logger import AstralisLogger
from astralis.core.registry import ModuleRegistry


class Engine:
    """Coordinates the startup and lifecycle of ASTRALIS."""

    def __init__(self) -> None:
        self.config = Config()
        self.logger = AstralisLogger().logger
        self.registry = ModuleRegistry()
        self.loader = ModuleLoader(
            self.registry,
            self.logger,
        )

    def start(self) -> None:
        """Start the ASTRALIS application."""

        # TODO: Validate configuration
        # TODO: Run health checks

        self.logger.info(f"Starting {self.config.project_name}")
        self.logger.info(
            f'Version {self.config.version} "{self.config.codename}"'
        )
        self.logger.info(f"Philosophy: {self.config.tagline}")

        # Initialize application modules.
        self.loader.load_modules()

        self.logger.info("ASTRALIS is ready.")