from astralis.bootstrap import Application
from astralis.core.lifecycle import LifecycleState


class Engine:
    """Coordinates the startup and lifecycle of ASTRALIS."""

    def __init__(
        self,
        app: Application,
    ) -> None:

        self.app = app

        # Core
        self.config = app.config
        self.logger = app.logger

        self.health = app.health
        self.lifecycle = app.lifecycle
        self.module_registry = app.module_registry
        self.loader = app.loader

        # AI
        self.ai_provider = app.ai_provider

        # Memory
        self.notes_memory = app.notes_memory
        self.calendar_memory = app.calendar_memory
        self.alarm_memory = app.alarm_memory

        # Capability framework
        self.capability_registry = app.capability_registry
        self.capability_manager = app.capability_manager

        # Brain
        self.brain = app.brain

        # Interface
        self.cli = app.cli

    def start(
        self,
    ) -> None:
        """Start the ASTRALIS application."""

        self.logger.info(
            f"Starting {self.config.project_name}",
        )

        self.logger.info(
            f'Version {self.config.version} "{self.config.codename}"',
        )

        self.logger.info(
            f"Philosophy: {self.config.tagline}",
        )

        self.lifecycle.transition_to(
            LifecycleState.INITIALIZING,
        )

        self.logger.info(
            f"Lifecycle: {self.lifecycle.state.value}",
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
                f"{status} {service}",
            )

        if not all(
            results.values(),
        ):
            raise RuntimeError(
                "ASTRALIS failed health checks. Startup aborted.",
            )

        self.logger.info(
            "Health checks passed.",
        )

        self.lifecycle.transition_to(
            LifecycleState.RUNNING,
        )

        self.logger.info(
            f"Lifecycle: {self.lifecycle.state.value}",
        )

        self.logger.info(
            "ASTRALIS is ready.",
        )

    def run(
        self,
    ) -> None:
        """Run the ASTRALIS user interface."""

        self.cli.run()
