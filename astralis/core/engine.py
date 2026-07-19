from astralis.brain.brain import Brain
from astralis.brain.request import Request
from astralis.brain.source import RequestSource
from astralis.core.config import Config
from astralis.core.health import HealthChecker
from astralis.core.lifecycle import (
    LifecycleManager,
    LifecycleState,
)
from astralis.core.loader import ModuleLoader
from astralis.core.logger import AstralisLogger
from astralis.core.registry import ModuleRegistry
from astralis.provider.mock import MockProvider
from astralis.provider.provider import Provider


class Engine:
    """Coordinates the startup and lifecycle of ASTRALIS."""

    def __init__(self) -> None:
        self.config = Config()
        self.logger = AstralisLogger().logger
        self.health = HealthChecker()
        self.registry = ModuleRegistry()
        self.loader = ModuleLoader(
            self.registry,
            self.logger,
        )
        self.lifecycle = LifecycleManager()

        # Initialize the AI provider.
        self.provider: Provider = MockProvider()

        # Initialize the Brain.
        self.brain = Brain(self.provider,)

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

        # Initialize application modules.
        self.loader.load_modules()

        # Run health checks.
        self.logger.info("Running health checks...")

        results = self.health.run_checks(
            config=self.config,
            logger=self.logger,
            registry=self.registry,
            loader=self.loader,
            lifecycle=self.lifecycle,
        )

        for service, healthy in results.items():
            status = "✓" if healthy else "✗"
            self.logger.info(f"{status} {service}")

        if not all(results.values()):
            raise RuntimeError(
                "ASTRALIS failed health checks. Startup aborted."
            )

        self.logger.info("Health checks passed.")

        # Transition to running.
        self.lifecycle.transition_to(
            LifecycleState.RUNNING
        )
        self.logger.info(
            f"Lifecycle: {self.lifecycle.state.value}"
        )

        # Verify the request processing pipeline.
        self.logger.info(
            "Verifying request processing pipeline..."
        )
        self._verify_processing_pipeline()

        self.logger.info("ASTRALIS is ready.")

    def _verify_processing_pipeline(
        self,
    ) -> None:
        """Verify the Brain request processing pipeline."""

        request = Request(
            text="Hello, ASTRALIS!",
            source=RequestSource.CLI,
        )

        response = self.brain.process(request)

        self.logger.info(
            f"Brain response: {response.text}"
        )