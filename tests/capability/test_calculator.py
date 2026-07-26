from astralis.capability.calculator import (
    CalculatorCapability,
)
from tests.helpers.conversation_factory import (
    create_conversation,
)
from tests.helpers.interpretation_factory import (
    create_interpretation,
)
from tests.helpers.request_factory import (
    create_request,
)


class TestCalculatorCapability:
    """Tests for the CalculatorCapability."""

    def setup_method(self) -> None:
        """Create shared objects for each test."""

        self.capability = CalculatorCapability()

        self.conversation = create_conversation()

        self.interpretation = create_interpretation(
            entities=["calculator"],
        )

    def test_addition(self) -> None:
        """Calculator adds two numbers."""

        response = self.capability.execute(
            create_request(
                "calculate 2 + 3",
            ),
            self.conversation,
            self.interpretation,
        )

        assert response.success is True
        assert response.text == "The result is 5."

    def test_subtraction(self) -> None:
        """Calculator subtracts two numbers."""

        response = self.capability.execute(
            create_request(
                "calculate 10 - 4",
            ),
            self.conversation,
            self.interpretation,
        )

        assert response.success is True
        assert response.text == "The result is 6."

    def test_multiplication(self) -> None:
        """Calculator multiplies two numbers."""

        response = self.capability.execute(
            create_request(
                "calculate 4 * 5",
            ),
            self.conversation,
            self.interpretation,
        )

        assert response.success is True
        assert response.text == "The result is 20."

    def test_division(self) -> None:
        """Calculator divides two numbers."""

        response = self.capability.execute(
            create_request(
                "calculate 20 / 5",
            ),
            self.conversation,
            self.interpretation,
        )

        assert response.success is True
        assert response.text == "The result is 4."

    def test_divide_by_zero(self) -> None:
        """Calculator handles division by zero."""

        response = self.capability.execute(
            create_request(
                "calculate 5 / 0",
            ),
            self.conversation,
            self.interpretation,
        )

        assert response.success is False
        assert response.text == "Cannot divide by zero."

    def test_invalid_expression(self) -> None:
        """Calculator rejects invalid expressions."""

        response = self.capability.execute(
            create_request(
                "calculate abc",
            ),
            self.conversation,
            self.interpretation,
        )

        assert response.success is False
        assert response.text == "Invalid calculation."
