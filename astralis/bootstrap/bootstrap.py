from astralis.api.email import EmailApi
from astralis.api.search import SearchApi
from astralis.api.weather import WeatherApi
from astralis.bootstrap import Application
from astralis.brain.brain import Brain
from astralis.capability.alarm import AlarmCapability
from astralis.capability.browser import BrowserCapability
from astralis.capability.calculator import CalculatorCapability
from astralis.capability.calendar import CalendarCapability
from astralis.capability.capability_type import CapabilityType
from astralis.capability.email import EmailCapability
from astralis.capability.file_system import FileSystemCapability
from astralis.capability.language import LanguageCapability
from astralis.capability.manager import CapabilityManager
from astralis.capability.notes import NotesCapability
from astralis.capability.registry import CapabilityRegistry
from astralis.capability.search import SearchCapability
from astralis.capability.time import TimeCapability
from astralis.capability.weather import WeatherCapability
from astralis.core.config import Config
from astralis.core.engine import Engine
from astralis.core.health import HealthChecker
from astralis.core.lifecycle import LifecycleManager
from astralis.core.loader import ModuleLoader
from astralis.core.logger import AstralisLogger
from astralis.core.registry import ModuleRegistry
from astralis.interfaces.cli import CommandLineInterface
from astralis.memory.alarm import AlarmMemory
from astralis.memory.calendar import CalendarMemory
from astralis.memory.note import NotesMemory
from astralis.monitoring.monitor import Monitor
from astralis.pipeline.request_pipeline import RequestPipeline
from astralis.providers.factory import ProviderFactory
from astralis.tools.browser import BrowserTool
from astralis.tools.file_system import FileSystemTool


class Bootstrap:
    """Builds and configures the ASTRALIS application."""

    def build(
        self,
    ) -> Engine:
        """Build the application."""

        app = self._build_application()

        self._build_capabilities(
            app,
        )

        return Engine(
            app,
        )

    def _build_application(
        self,
    ) -> Application:
        """Assemble the application."""

        # Core
        config = Config()
        logger = AstralisLogger().logger
        health = HealthChecker()
        module_registry = ModuleRegistry()

        loader = ModuleLoader(
            module_registry,
            logger,
        )

        lifecycle = LifecycleManager()

        # Memory
        notes_memory = NotesMemory()
        calendar_memory = CalendarMemory()
        alarm_memory = AlarmMemory()

        # AI
        ai_provider = ProviderFactory.create(
            config,
        )

        capability_registry = CapabilityRegistry()

        capability_manager = CapabilityManager(
            capability_registry,
        )

        brain = Brain(
            capability_manager,
        )

        monitor = Monitor(
            enabled=config.monitoring_enabled,
        )

        pipeline = RequestPipeline(
            brain=brain,
            monitor=monitor,
        )

        # Interface
        cli = CommandLineInterface(
            pipeline,
        )

        return Application(
            config=config,
            logger=logger,
            health=health,
            lifecycle=lifecycle,
            module_registry=module_registry,
            loader=loader,
            ai_provider=ai_provider,
            capability_registry=capability_registry,
            capability_manager=capability_manager,
            brain=brain,
            notes_memory=notes_memory,
            calendar_memory=calendar_memory,
            alarm_memory=alarm_memory,
            cli=cli,
            pipeline=pipeline,
        )

    def _build_capabilities(
        self,
        app: Application,
    ) -> None:
        """Register all available capabilities."""

        # Shared services
        browser = BrowserTool()
        file_system = FileSystemTool()
        email = EmailApi()
        search = SearchApi(
            app.config,
        )
        weather = WeatherApi(
            app.config,
        )

        app.capability_registry.register(
            CapabilityType.LANGUAGE,
            LanguageCapability(
                app.ai_provider,
            ),
        )

        app.capability_registry.register(
            CapabilityType.TIME,
            TimeCapability(),
        )

        app.capability_registry.register(
            CapabilityType.CALCULATOR,
            CalculatorCapability(),
        )

        app.capability_registry.register(
            CapabilityType.WEATHER,
            WeatherCapability(
                weather,
            ),
        )

        app.capability_registry.register(
            CapabilityType.SEARCH,
            SearchCapability(
                search,
            ),
        )

        app.capability_registry.register(
            CapabilityType.NOTES,
            NotesCapability(
                app.notes_memory,
            ),
        )

        app.capability_registry.register(
            CapabilityType.CALENDAR,
            CalendarCapability(
                app.calendar_memory,
            ),
        )

        app.capability_registry.register(
            CapabilityType.BROWSER,
            BrowserCapability(
                browser,
            ),
        )

        app.capability_registry.register(
            CapabilityType.FILE_SYSTEM,
            FileSystemCapability(
                file_system,
            ),
        )

        app.capability_registry.register(
            CapabilityType.ALARM,
            AlarmCapability(
                app.alarm_memory,
            ),
        )

        app.capability_registry.register(
            CapabilityType.EMAIL,
            EmailCapability(
                email,
            ),
        )
