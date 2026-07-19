from astralis.core.config import Config
from astralis.provider.mock import MockProvider
from astralis.provider.openai import OpenAIProvider
from astralis.provider.provider import Provider
from astralis.provider.gemini import GeminiProvider

class ProviderFactory:
    """Creates AI provider instances."""

    @staticmethod
    def create(
        config: Config,
    ) -> Provider:
        """Create the configured AI provider."""

        if config.provider == "gemini":
            return GeminiProvider(config)
        
        if config.provider == "mock":
            return MockProvider()

        if config.provider == "openai":
            return OpenAIProvider(config)

        raise ValueError(
            f"Unsupported provider: {config.provider}"
        )