import pytest

from astralis.core.config import Config
from astralis.providers.factory import ProviderFactory
from astralis.providers.gemini import GeminiProvider
from astralis.providers.mock import MockProvider
from astralis.providers.ollama import OllamaProvider
from astralis.providers.openai import OpenAIProvider
from astralis.providers.reasoning import ReasoningMode


class TestProviderFactory:
    """Tests for the ProviderFactory."""

    def test_creates_ollama_provider(
        self,
    ) -> None:
        """ProviderFactory resolves 'ollama' to OllamaProvider with config."""

        config = Config()
        config.provider = "ollama"
        config.ollama_host = "http://custom-host:11434"
        config.ollama_model = "test-local-model"
        config.ollama_timeout = 45
        config.ollama_reasoning_mode = ReasoningMode.DEEP

        provider = ProviderFactory.create(
            config,
        )

        assert isinstance(
            provider,
            OllamaProvider,
        )
        assert provider.host == "http://custom-host:11434"
        assert provider.model == "test-local-model"
        assert provider.timeout == 45
        assert provider.reasoning_mode is ReasoningMode.DEEP
        assert provider.is_local is True

    def test_creates_ollama_provider_with_default_reasoning_mode(
        self,
    ) -> None:
        """ProviderFactory passes default AUTO reasoning mode to OllamaProvider."""

        config = Config()
        config.provider = "ollama"
        config.ollama_model = "test-local-model"

        provider = ProviderFactory.create(
            config,
        )

        assert isinstance(
            provider,
            OllamaProvider,
        )
        assert provider.reasoning_mode is ReasoningMode.AUTO

    def test_creates_mock_provider(
        self,
    ) -> None:
        """ProviderFactory resolves 'mock' to MockProvider."""

        config = Config()
        config.provider = "mock"

        provider = ProviderFactory.create(
            config,
        )

        assert isinstance(
            provider,
            MockProvider,
        )

    def test_creates_gemini_provider(
        self,
    ) -> None:
        """ProviderFactory resolves 'gemini' to GeminiProvider."""

        config = Config()
        config.provider = "gemini"

        provider = ProviderFactory.create(
            config,
        )

        assert isinstance(
            provider,
            GeminiProvider,
        )

    def test_creates_openai_provider(
        self,
    ) -> None:
        """ProviderFactory resolves 'openai' to OpenAIProvider."""

        config = Config()
        config.provider = "openai"

        provider = ProviderFactory.create(
            config,
        )

        assert isinstance(
            provider,
            OpenAIProvider,
        )

    def test_unsupported_provider_raises_error(
        self,
    ) -> None:
        """ProviderFactory raises ValueError for unknown providers."""

        config = Config()
        config.provider = "nonexistent_provider"

        with pytest.raises(
            ValueError,
            match="Unsupported provider: nonexistent_provider",
        ):
            ProviderFactory.create(
                config,
            )
