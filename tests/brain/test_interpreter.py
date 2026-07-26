from astralis.brain.intent import Intent
from astralis.brain.interpreter import Interpreter
from tests.helpers.request_factory import create_request


class TestInterpreter:
    """Tests for the Interpreter."""

    def setup_method(self) -> None:
        """Create an interpreter."""

        self.interpreter = Interpreter()

    def test_greeting(self) -> None:
        """Recognize greetings."""

        interpretation = self.interpreter.interpret(
            create_request("hello"),
        )

        assert interpretation.intent is Intent.GREETING
        assert interpretation.entities == []

    def test_question(self) -> None:
        """Recognize questions."""

        interpretation = self.interpreter.interpret(
            create_request("what is python?"),
        )

        assert interpretation.intent is Intent.QUESTION

    def test_memory(self) -> None:
        """Recognize memory requests."""

        interpretation = self.interpreter.interpret(
            create_request("remember my birthday"),
        )

        assert interpretation.intent is Intent.MEMORY
        assert "memory" in interpretation.entities

    def test_time_entity(self) -> None:
        """Extract time entity."""

        interpretation = self.interpreter.interpret(
            create_request("what time is it"),
        )

        assert interpretation.intent is Intent.QUESTION
        assert "time" in interpretation.entities

    def test_date_entity(self) -> None:
        """Extract date entity."""

        interpretation = self.interpreter.interpret(
            create_request("what is today's date"),
        )

        assert interpretation.intent is Intent.QUESTION
        assert "date" in interpretation.entities

    def test_weather_entity(self) -> None:
        """Extract weather entity."""

        interpretation = self.interpreter.interpret(
            create_request("weather in delhi"),
        )

        assert "weather" in interpretation.entities

    def test_calculator_entity(self) -> None:
        """Extract calculator entity."""

        interpretation = self.interpreter.interpret(
            create_request("calculate 2 + 3"),
        )

        assert "calculator" in interpretation.entities

    def test_conversation(self) -> None:
        """Recognize normal conversation."""

        interpretation = self.interpreter.interpret(
            create_request("tell me something interesting"),
        )

        assert interpretation.intent is Intent.CONVERSATION
