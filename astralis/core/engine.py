from astralis.brain.brain import Brain
from astralis.core.config import Config
from astralis.core.health import HealthChecker
from astralis.core.lifecycle import (
    LifecycleManager,
    LifecycleState,
)
from astralis.core.loader import ModuleLoader
from astralis.core.logger import AstralisLogger
from astralis.core.registry import ModuleRegistry
from astralis.provider.factory import ProviderFactory
from astralis.interfaces.cli import CommandLineInterface
from astralis.capability.capability_type import CapabilityType
from astralis.capability.language import LanguageCapability
from astralis.capability.manager import CapabilityManager
from astralis.capability.registry import CapabilityRegistry


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

        # Initialize the language provider.
        provider = ProviderFactory.create(
            self.config,
        )

        # Intialize capabilities.
        registry = CapabilityRegistry()

        registry.register(
            CapabilityType.LANGUAGE,
            LanguageCapability(provider),
        )

        manager = CapabilityManager(
            registry,
        )

        # Initialize the Brain.
        self.brain = Brain(
            manager,
        )

        # Initialize the CLI.
        self.cli = CommandLineInterface(
            self.brain,
        )

        
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

        self.logger.info("ASTRALIS is ready.")

    def run(self) -> None:
        """Run the ASTRALIS user interface."""

        self.cli.run()