from dataclasses import dataclass
from logging import Logger

from astralis.brain.brain import Brain
from astralis.capability.manager import CapabilityManager
from astralis.capability.registry import CapabilityRegistry
from astralis.core.config import Config
from astralis.core.health import HealthChecker
from astralis.core.lifecycle import LifecycleManager
from astralis.core.loader import ModuleLoader
from astralis.core.registry import ModuleRegistry
from astralis.interfaces.cli import CommandLineInterface
from astralis.memory.alarm import AlarmMemory
from astralis.memory.calendar import CalendarMemory
from astralis.memory.manager import MemoryManager
from astralis.memory.note import NotesMemory
from astralis.memory.retriever import MemoryRetriever
from astralis.pipeline.request_pipeline import RequestPipeline
from astralis.providers.provider import Provider


@dataclass(
    slots=True,
)
class Application:
    """Represents the assembled ASTRALIS application."""

    # Core
    config: Config
    logger: Logger

    health: HealthChecker
    lifecycle: LifecycleManager
    module_registry: ModuleRegistry
    loader: ModuleLoader

    # Brain
    ai_provider: Provider
    brain: Brain

    # Pipeline
    pipeline: RequestPipeline

    # Capabilities
    capability_registry: CapabilityRegistry
    capability_manager: CapabilityManager

    # Memory
    notes_memory: NotesMemory
    calendar_memory: CalendarMemory
    alarm_memory: AlarmMemory
    memory_manager: MemoryManager
    memory_retriever: MemoryRetriever

    # Interfaces
    cli: CommandLineInterface
