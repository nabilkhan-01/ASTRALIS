from astralis.core.config import Config
from astralis.core.lifecycle import (
    LifecycleManager,
    LifecycleState,
)
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
        self.lifecycle = LifecycleManager()

    def start(self) -> None:
        """Start the ASTRALIS application."""

        self.logger.info(f"Starting {self.config.project_name}")
        self.logger.info(
            f'Version {self.config.version} "{self.config.codename}"'
        )
        self.logger.info(
            f"Philosophy: {self.config.tagline}"
        )

        # Transition to startup.
        self.lifecycle.transition_to(
            LifecycleState.INITIALIZING
        )
        self.logger.info(
            f"Lifecycle: {self.lifecycle.state.value}"
        )

        # TODO: Validate configuration
        # TODO: Run health checks

        # Initialize application modules.
        self.loader.load_modules()

        # Transition to running.
        self.lifecycle.transition_to(
            LifecycleState.RUNNING
        )
        self.logger.info(
            f"Lifecycle: {self.lifecycle.state.value}"
        )

        self.logger.info("ASTRALIS is ready.")