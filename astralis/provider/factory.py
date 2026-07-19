from astralis.core.config import Config
from astralis.provider.mock import MockProvider
from astralis.provider.provider import Provider


class ProviderFactory:
    """Creates AI provider instances."""

    @staticmethod
    def create(config: Config) -> Provider:
        """Create the configured AI provider."""

        if config.provider == "mock":
            return MockProvider()

        raise ValueError(
            f"Unsupported provider: {config.provider}"
        )