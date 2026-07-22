import pytest

from astralis.core.config import Config
from astralis.provider.factory import ProviderFactory
from astralis.provider.gemini import GeminiProvider
from astralis.provider.mock import MockProvider
from astralis.provider.openai import OpenAIProvider


class TestProviderFactory:
    """Tests for the ProviderFactory."""

    def test_create_mock_provider(self) -> None:
        """Create a mock provider."""

        config = Config(
            provider="mock",
        )

        provider = ProviderFactory.create(
            config,
        )

        assert isinstance(
            provider,
            MockProvider,
        )

    def test_create_openai_provider(self) -> None:
        """Create an OpenAI provider."""

        config = Config(
            provider="openai",
        )

        provider = ProviderFactory.create(
            config,
        )

        assert isinstance(
            provider,
            OpenAIProvider,
        )

    def test_create_gemini_provider(self) -> None:
        """Create a Gemini provider."""

        config = Config(
            provider="gemini",
        )

        provider = ProviderFactory.create(
            config,
        )

        assert isinstance(
            provider,
            GeminiProvider,
        )

    def test_invalid_provider(self) -> None:
        """Reject an unsupported provider."""

        config = Config(
            provider="astralis",
        )

        with pytest.raises(
            ValueError,
        ):
            ProviderFactory.create(
                config,
            )