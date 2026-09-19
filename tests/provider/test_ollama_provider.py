from unittest.mock import MagicMock, patch

import requests

from astralis.brain.conversation import Conversation
from astralis.brain.role import Role
from astralis.providers.local import LocalProvider
from astralis.providers.ollama import OllamaProvider
from astralis.providers.prompts import SYSTEM_PROMPT
from astralis.providers.provider import Provider
from astralis.providers.reasoning import ReasoningMode


class TestOllamaProvider:
    """Tests for the OllamaProvider implementation."""

    def test_provider_hierarchy_and_default_timeout(
        self,
    ) -> None:
        """OllamaProvider is a LocalProvider with default 60s timeout."""

        provider = OllamaProvider(
            model="test-model",
            host="http://localhost:11434",
        )

        assert isinstance(
            provider,
            LocalProvider,
        )
        assert isinstance(
            provider,
            Provider,
        )
        assert provider.is_local is True
        assert provider.model == "test-model"
        assert provider.host == "http://localhost:11434"
        assert provider.timeout == 60

    def test_explicit_timeout_parameter(
        self,
    ) -> None:
        """Explicit timeout parameter is stored and used."""

        provider = OllamaProvider(
            model="test-model",
            timeout=120,
        )

        assert provider.timeout == 120

    def test_unconfigured_model_returns_failure(
        self,
    ) -> None:
        """When model is empty, generation fails without making network calls."""

        provider = OllamaProvider(
            model="",
        )

        conversation = Conversation()
        conversation.add(
            Role.USER,
            "Hello",
        )

        with patch(
            "requests.post",
        ) as mock_post:
            response = provider.generate(
                conversation,
            )

            mock_post.assert_not_called()
            assert response.success is False
            assert "Ollama model is not configured" in response.text

    @patch("requests.post")
    def test_successful_generation_with_system_prompt(
        self,
        mock_post: MagicMock,
    ) -> None:
        """Payload includes SYSTEM_PROMPT as initial system message followed by user messages."""

        provider = OllamaProvider(
            model="custom-reasoner",
            host="http://my-host:11434/",
            timeout=45,
        )

        mock_response = MagicMock(
            spec=requests.Response,
        )
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "model": "custom-reasoner",
            "message": {
                "role": "assistant",
                "content": "Local model output.",
            },
            "done": True,
        }
        mock_post.return_value = mock_response

        conversation = Conversation()
        conversation.add(
            Role.USER,
            "Explain quantum computing.",
        )

        response = provider.generate(
            conversation,
        )

        assert response.success is True
        assert response.text == "Local model output."

        mock_post.assert_called_once_with(
            "http://my-host:11434/api/chat",
            json={
                "model": "custom-reasoner",
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": "Explain quantum computing.",
                    },
                ],
                "stream": False,
                "think": False,
            },
            timeout=45,
        )

    @patch("requests.post")
    def test_multi_message_conversation_preserves_order_after_system_prompt(
        self,
        mock_post: MagicMock,
    ) -> None:
        """Existing conversation messages remain in their exact order after SYSTEM_PROMPT."""

        provider = OllamaProvider(
            model="chat-model",
            host="http://localhost:11434",
        )

        mock_response = MagicMock(
            spec=requests.Response,
        )
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {
                "role": "assistant",
                "content": "I understand the rules.",
            },
        }
        mock_post.return_value = mock_response

        conversation = Conversation()
        conversation.add(
            Role.USER,
            "Hello",
        )
        conversation.add(
            Role.ASSISTANT,
            "Hi there!",
        )
        conversation.add(
            Role.USER,
            "What can you do?",
        )

        response = provider.generate(
            conversation,
        )

        assert response.success is True
        assert response.text == "I understand the rules."

        call_args = mock_post.call_args
        messages = call_args.kwargs["json"]["messages"]

        assert len(messages) == 4
        assert messages[0] == {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
        assert messages[1] == {
            "role": "user",
            "content": "Hello",
        }
        assert messages[2] == {
            "role": "assistant",
            "content": "Hi there!",
        }
        assert messages[3] == {
            "role": "user",
            "content": "What can you do?",
        }

    @patch("requests.post")
    def test_system_prompt_not_duplicated_when_conversation_contains_system_role(
        self,
        mock_post: MagicMock,
    ) -> None:
        """System prompt is sent only once at start, not duplicated if history contains system role."""

        provider = OllamaProvider(
            model="chat-model",
        )

        mock_response = MagicMock(
            spec=requests.Response,
        )
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {
                "role": "assistant",
                "content": "Understood.",
            },
        }
        mock_post.return_value = mock_response

        conversation = Conversation()
        conversation.add(
            Role.SYSTEM,
            "An existing system message in conversation.",
        )
        conversation.add(
            Role.USER,
            "Hello",
        )

        response = provider.generate(
            conversation,
        )

        assert response.success is True
        messages = mock_post.call_args.kwargs["json"]["messages"]

        system_messages = [
            m for m in messages if m["role"] == "system"
        ]
        assert len(system_messages) == 1
        assert system_messages[0]["content"] == SYSTEM_PROMPT
        assert len(messages) == 2
        assert messages[1] == {
            "role": "user",
            "content": "Hello",
        }

    @patch("requests.post")
    def test_empty_conversation_sends_only_system_message(
        self,
        mock_post: MagicMock,
    ) -> None:
        """Empty conversation sends exactly one system message without error."""

        provider = OllamaProvider(
            model="chat-model",
        )

        mock_response = MagicMock(
            spec=requests.Response,
        )
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {
                "role": "assistant",
                "content": "Greeting from model.",
            },
        }
        mock_post.return_value = mock_response

        response = provider.generate(
            Conversation(),
        )

        assert response.success is True
        assert response.text == "Greeting from model."
        assert mock_post.call_args.kwargs["json"]["messages"] == [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
        ]
        assert mock_post.call_args.kwargs["timeout"] == 60

    @patch("requests.post")
    def test_empty_response_text_returns_error(
        self,
        mock_post: MagicMock,
    ) -> None:
        """When Ollama returns empty content, returns failure response."""

        provider = OllamaProvider(
            model="chat-model",
        )

        mock_response = MagicMock(
            spec=requests.Response,
        )
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {
                "role": "assistant",
                "content": "",
            },
        }
        mock_post.return_value = mock_response

        conversation = Conversation()
        conversation.add(
            Role.USER,
            "Hi",
        )

        response = provider.generate(
            conversation,
        )

        assert response.success is False
        assert "empty response" in response.text

    @patch("requests.post")
    def test_connection_failure_does_not_raise_exception(
        self,
        mock_post: MagicMock,
    ) -> None:
        """ConnectionError returns safe Response(success=False) with host info."""

        provider = OllamaProvider(
            model="local-model",
            host="http://192.168.1.50:11434",
        )

        mock_post.side_effect = requests.exceptions.ConnectionError(
            "Connection refused",
        )

        conversation = Conversation()
        conversation.add(
            Role.USER,
            "Ping",
        )

        response = provider.generate(
            conversation,
        )

        assert response.success is False
        assert "192.168.1.50:11434" in response.text
        assert "unavailable" in response.text

    @patch("requests.post")
    def test_timeout_failure_does_not_raise_exception(
        self,
        mock_post: MagicMock,
    ) -> None:
        """Timeout returns safe Response(success=False)."""

        provider = OllamaProvider(
            model="local-model",
            host="http://localhost:11434",
        )

        mock_post.side_effect = requests.exceptions.Timeout(
            "Read timed out",
        )

        conversation = Conversation()
        conversation.add(
            Role.USER,
            "Ping",
        )

        response = provider.generate(
            conversation,
        )

        assert response.success is False
        assert "unavailable" in response.text

    @patch("requests.post")
    def test_ollama_api_error_response_preserves_error_details(
        self,
        mock_post: MagicMock,
    ) -> None:
        """When Ollama returns a non-200 JSON error, the error details are preserved."""

        provider = OllamaProvider(
            model="nonexistent-model",
            host="http://localhost:11434",
        )

        mock_response = MagicMock(
            spec=requests.Response,
        )
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "error": "model 'nonexistent-model' not found, try pulling it first",
        }
        mock_post.return_value = mock_response

        conversation = Conversation()
        conversation.add(
            Role.USER,
            "Hello",
        )

        response = provider.generate(
            conversation,
        )

        assert response.success is False
        assert "Ollama error:" in response.text
        assert "model 'nonexistent-model' not found" in response.text

    @patch("requests.post")
    def test_configured_model_and_host_are_used_dynamically(
        self,
        mock_post: MagicMock,
    ) -> None:
        """Provider strictly uses the configured model and host without hardcoding."""

        provider = OllamaProvider(
            model="my-arbitrary-model-name:v1",
            host="http://gpu-server:9999",
            timeout=90,
        )

        mock_response = MagicMock(
            spec=requests.Response,
        )
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {
                "content": "arbitrary output",
            },
        }
        mock_post.return_value = mock_response

        conversation = Conversation()
        conversation.add(
            Role.USER,
            "Test",
        )

        response = provider.generate(
            conversation,
        )

        assert response.success is True
        assert response.text == "arbitrary output"

        mock_post.assert_called_once_with(
            "http://gpu-server:9999/api/chat",
            json={
                "model": "my-arbitrary-model-name:v1",
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": "Test",
                    },
                ],
                "stream": False,
                "think": False,
            },
            timeout=90,
        )

    def test_default_reasoning_mode_is_auto(
        self,
    ) -> None:
        """OllamaProvider defaults reasoning_mode to ReasoningMode.AUTO."""
        provider = OllamaProvider(
            model="qwen3.5:4b",
        )
        assert provider.reasoning_mode is ReasoningMode.AUTO

    @patch("requests.post")
    def test_fast_reasoning_mode_sends_top_level_think_false(
        self,
        mock_post: MagicMock,
    ) -> None:
        """FAST mode includes top-level 'think': False in the Ollama payload."""
        provider = OllamaProvider(
            model="qwen3.5:4b",
            reasoning_mode=ReasoningMode.FAST,
        )

        mock_response = MagicMock(spec=requests.Response)
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {"content": "Fast reply."},
        }
        mock_post.return_value = mock_response

        conversation = Conversation()
        conversation.add(Role.USER, "Quick question")

        response = provider.generate(conversation)

        assert response.success is True
        assert response.text == "Fast reply."

        call_kwargs = mock_post.call_args[1]
        payload = call_kwargs["json"]

        # Verify top-level think: False
        assert "think" in payload
        assert payload["think"] is False
        assert "options" not in payload

        # Verify single system prompt and message ordering
        assert len(payload["messages"]) == 2
        assert payload["messages"][0]["role"] == "system"
        assert payload["messages"][0]["content"] == SYSTEM_PROMPT
        assert payload["messages"][1]["role"] == "user"
        assert payload["messages"][1]["content"] == "Quick question"

        # Verify conversation immutability
        assert len(conversation.messages) == 1
        assert conversation.messages[0].content == "Quick question"

    @patch("requests.post")
    def test_deep_reasoning_mode_sends_top_level_think_true(
        self,
        mock_post: MagicMock,
    ) -> None:
        """DEEP mode includes top-level 'think': True in the Ollama payload."""
        provider = OllamaProvider(
            model="qwen3.5:4b",
            reasoning_mode=ReasoningMode.DEEP,
        )

        mock_response = MagicMock(spec=requests.Response)
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {"content": "Deep reasoning output."},
        }
        mock_post.return_value = mock_response

        conversation = Conversation()
        conversation.add(Role.USER, "Complex question")

        response = provider.generate(conversation)

        assert response.success is True

        call_kwargs = mock_post.call_args[1]
        payload = call_kwargs["json"]

        # Verify top-level think: True
        assert "think" in payload
        assert payload["think"] is True
        assert "options" not in payload

    @patch("requests.post")
    def test_auto_reasoning_mode_resolves_to_fast_think_false(
        self,
        mock_post: MagicMock,
    ) -> None:
        """AUTO mode safely uses fast local inference ('think': False) until routing is implemented."""
        provider = OllamaProvider(
            model="qwen3.5:4b",
            reasoning_mode=ReasoningMode.AUTO,
        )

        mock_response = MagicMock(spec=requests.Response)
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {"content": "Default runtime output."},
        }
        mock_post.return_value = mock_response

        conversation = Conversation()
        conversation.add(Role.USER, "Hello")

        response = provider.generate(conversation)

        assert response.success is True

        call_kwargs = mock_post.call_args[1]
        payload = call_kwargs["json"]

        # Verify think parameter resolves to False
        assert "think" in payload
        assert payload["think"] is False
        assert "options" not in payload

