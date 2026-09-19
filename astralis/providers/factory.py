from collections.abc import Callable
from typing import ClassVar

from astralis.core.config import Config
from astralis.providers.gemini import GeminiProvider
from astralis.providers.mock import MockProvider
from astralis.providers.ollama import OllamaProvider
from astralis.providers.openai import OpenAIProvider
from astralis.providers.provider import Provider


class ProviderFactory:
    """Creates AI provider instances."""

    _PROVIDERS: ClassVar[dict[str, Callable[[Config], Provider]]] = {
        "gemini": GeminiProvider,
        "openai": OpenAIProvider,
        "mock": lambda _config: MockProvider(),
        "ollama": lambda config: OllamaProvider(
            model=config.ollama_model,
            host=config.ollama_host,
            timeout=config.ollama_timeout,
            reasoning_mode=config.ollama_reasoning_mode,
        ),
    }

    @staticmethod
    def create(
        config: Config,
    ) -> Provider:
        """Create the configured AI provider."""

        provider = ProviderFactory._PROVIDERS.get(
            config.provider,
        )

        if provider is None:
            raise ValueError(
                f"Unsupported provider: {config.provider}",
            )

        return provider(
            config,
        )
