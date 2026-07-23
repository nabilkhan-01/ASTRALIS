from astralis.brain.brain import Brain
from astralis.capability.capability_type import CapabilityType
from astralis.capability.language import LanguageCapability
from astralis.capability.manager import CapabilityManager
from astralis.capability.registry import CapabilityRegistry
from astralis.capability.time import TimeCapability
from astralis.core.config import Config
from astralis.core.health import HealthChecker
from astralis.core.lifecycle import (
    LifecycleManager,
    LifecycleState,
)
from astralis.core.loader import ModuleLoader
from astralis.core.logger import AstralisLogger
from astralis.core.registry import ModuleRegistry
from astralis.interfaces.cli import CommandLineInterface
from astralis.provider.factory import ProviderFactory
from astralis.capability.calculator import CalculatorCapability
from astralis.capability.weather import WeatherCapability
from astralis.capability.search import SearchCapability


class Engine:
    """Coordinates the startup and lifecycle of ASTRALIS."""

    def __init__(self) -> None:
        self.config = Config()
        self.logger = AstralisLogger().logger
        self.health = HealthChecker()

        self.module_registry = ModuleRegistry()

        self.loader = ModuleLoader(
            self.module_registry,
            self.logger,
        )

        self.lifecycle = LifecycleManager()

        # Initialize the language provider.
        self.provider = ProviderFactory.create(
            self.config,
        )

        # Initialize capability framework.
        self.capability_registry = CapabilityRegistry()

        self._register_capabilities()

        self.capability_manager = CapabilityManager(
            self.capability_registry,
        )

        # Initialize the Brain.
        self.brain = Brain(
            self.capability_manager,
        )

        # Initialize the CLI.
        self.cli = CommandLineInterface(
            self.brain,
        )

    def _register_capabilities(
        self,
    ) -> None:
        """Register all available capabilities."""

        self.capability_registry.register(
            CapabilityType.LANGUAGE,
            LanguageCapability(
                self.provider,
            ),
        )

        self.capability_registry.register(
            CapabilityType.TIME,
            TimeCapability(),
        )

        self.capability_registry.register(
            CapabilityType.CALCULATOR,
            CalculatorCapability(),
        )

        self.capability_registry.register(
            CapabilityType.WEATHER,
            WeatherCapability(),
        )

        self.capability_registry.register(
            CapabilityType.SEARCH,
            SearchCapability(
                self.config,
            ),
        )

    def start(
        self,
    ) -> None:
        """Start the ASTRALIS application."""

        self.logger.info(
            f"Starting {self.config.project_name}"
        )

        self.logger.info(
            f'Version {self.config.version} "{self.config.codename}"'
        )

        self.logger.info(
            f"Philosophy: {self.config.tagline}"
        )

        self.lifecycle.transition_to(
            LifecycleState.INITIALIZING,
        )

        self.logger.info(
            f"Lifecycle: {self.lifecycle.state.value}"
        )

        self.loader.load_modules()

        self.logger.info(
            "Running health checks...",
        )

        results = self.health.run_checks(
            config=self.config,
            logger=self.logger,
            registry=self.module_registry,
            loader=self.loader,
            lifecycle=self.lifecycle,
        )

        for service, healthy in results.items():
            status = "✓" if healthy else "✗"
            self.logger.info(
                f"{status} {service}"
            )

        if not all(
            results.values()
        ):
            raise RuntimeError(
                "ASTRALIS failed health checks. Startup aborted."
            )

        self.logger.info(
            "Health checks passed."
        )

        self.lifecycle.transition_to(
            LifecycleState.RUNNING,
        )

        self.logger.info(
            f"Lifecycle: {self.lifecycle.state.value}"
        )

        self.logger.info(
            "ASTRALIS is ready."
        )

    def run(
        self,
    ) -> None:
        """Run the ASTRALIS user interface."""

        self.cli.run()