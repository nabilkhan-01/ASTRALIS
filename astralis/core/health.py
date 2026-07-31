from logging import Logger

from astralis.core.config import Config
from astralis.core.lifecycle import LifecycleManager
from astralis.core.loader import ModuleLoader
from astralis.core.registry import ModuleRegistry


class HealthChecker:
    """Verifies the health of ASTRALIS core services."""

    def run_checks(
        self,
        *,
        config: Config,
        logger: Logger,
        registry: ModuleRegistry,
        loader: ModuleLoader,
        lifecycle: LifecycleManager,
    ) -> dict[str, bool]:
        """Run health checks for core services."""

        results = {
            "Config": bool(
                config.project_name,
            ),
            "Logger": bool(
                logger.name,
            ),
            "Module Registry": registry is not None,
            "Module Loader": loader is not None,
            "Lifecycle Manager": lifecycle.state is not None,
        }

        return results
