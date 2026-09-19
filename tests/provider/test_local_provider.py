import importlib
import os
from unittest.mock import patch

import astralis.core.config as config_module
from astralis.brain.conversation import Conversation
from astralis.brain.response import Response
from astralis.core.config import Config
from astralis.providers.local import LocalProvider
from astralis.providers.provider import Provider


class ConcreteLocalProvider(
    LocalProvider,
):
    """Minimal concrete implementation for testing the LocalProvider abstraction."""

    def generate(
        self,
        conversation: Conversation,
    ) -> Response:
        return Response(
            text="Local response.",
            success=True,
        )


class TestLocalProvider:
    """Tests for the LocalProvider abstraction."""

    def test_stores_model_and_normalized_host(
        self,
    ) -> None:
        """LocalProvider stores the model and strips trailing slash from host."""

        provider = ConcreteLocalProvider(
            model="custom-local-model",
            host="http://localhost:11434/",
        )

        assert provider.model == "custom-local-model"
        assert provider.host == "http://localhost:11434"

    def test_default_host(
        self,
    ) -> None:
        """LocalProvider defaults host to http://localhost:11434."""

        provider = ConcreteLocalProvider(
            model="custom-local-model",
        )

        assert provider.host == "http://localhost:11434"

    def test_is_local_returns_true(
        self,
    ) -> None:
        """LocalProvider.is_local property returns True."""

        provider = ConcreteLocalProvider(
            model="custom-local-model",
        )

        assert provider.is_local is True

    def test_is_instance_of_provider(
        self,
    ) -> None:
        """LocalProvider inherits from the existing Provider abstraction."""

        provider = ConcreteLocalProvider(
            model="custom-local-model",
        )

        assert isinstance(
            provider,
            Provider,
        )

    def test_generate_contract(
        self,
    ) -> None:
        """LocalProvider generate() adheres to the Provider return contract."""

        provider = ConcreteLocalProvider(
            model="custom-local-model",
        )

        response = provider.generate(
            Conversation(),
        )

        assert response.success is True
        assert response.text == "Local response."

    def test_connection_error_helper_formatting(
        self,
    ) -> None:
        """_connection_error returns Response(success=False) mentioning host and details."""

        provider = ConcreteLocalProvider(
            model="custom-local-model",
            host="http://127.0.0.1:11434",
        )

        response = provider._connection_error(
            details="connection refused",
        )

        assert response.success is False
        assert "http://127.0.0.1:11434" in response.text
        assert "connection refused" in response.text
        assert "Please ensure the local model runtime is running." in response.text

    def test_connection_error_helper_without_details(
        self,
    ) -> None:
        """_connection_error works cleanly when no extra details are supplied."""

        provider = ConcreteLocalProvider(
            model="custom-local-model",
        )

        response = provider._connection_error()

        assert response.success is False
        assert "http://localhost:11434" in response.text
        assert "Please ensure the local model runtime is running." in response.text

    def test_connection_error_does_not_raise_network_exception(
        self,
    ) -> None:
        """_connection_error handles simulated network failures safely without raising."""

        provider = ConcreteLocalProvider(
            model="custom-local-model",
        )

        try:
            raise ConnectionRefusedError(
                "Simulated socket refusal",
            )
        except OSError as err:
            response = provider._connection_error(
                details=str(
                    err,
                ),
            )

        assert response.success is False
        assert "Simulated socket refusal" in response.text


class TestLocalConfiguration:
    """Tests for local model settings in Config."""

    def test_default_configuration_is_neutral(
        self,
    ) -> None:
        """Default configuration does not hardcode a specific model dependency."""

        with patch.dict(
            os.environ,
            {},
            clear=True,
        ):
            config = Config()

            assert config.ollama_host == "http://localhost:11434"
            assert config.ollama_model == ""

    def test_configuration_reads_env_vars(
        self,
    ) -> None:
        """Config respects OLLAMA_HOST and OLLAMA_MODEL environment variables."""
        env = {
            "OLLAMA_HOST": "http://remote-gpu:11434",
            "OLLAMA_MODEL": "custom-model:latest",
        }

        try:
            with patch.dict(
                os.environ,
                env,
            ):
                importlib.reload(
                    config_module,
                )
                config = config_module.Config()

                assert config.ollama_host == "http://remote-gpu:11434"
                assert config.ollama_model == "custom-model:latest"
        finally:
            importlib.reload(
                config_module,
            )
