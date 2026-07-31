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

    @staticmethod
    def _create_capability() -> CalculatorCapability:
        """Create a calculator capability."""

        return CalculatorCapability()

    @staticmethod
    def _execute(
        capability: CalculatorCapability,
        text: str,
    ):
        """Execute a calculator request."""

        return capability.execute(
            create_request(
                text,
            ),
            create_conversation(),
            create_interpretation(
                entities=["calculator"],
            ),
        )

    def test_addition(
        self,
    ) -> None:
        """Calculator adds two numbers."""

        capability = self._create_capability()

        response = self._execute(
            capability,
            "calculate 2 + 3",
        )

        assert response.success is True
        assert response.text == "The result is 5."

    def test_subtraction(
        self,
    ) -> None:
        """Calculator subtracts two numbers."""

        capability = self._create_capability()

        response = self._execute(
            capability,
            "calculate 10 - 4",
        )

        assert response.success is True
        assert response.text == "The result is 6."

    def test_multiplication(
        self,
    ) -> None:
        """Calculator multiplies two numbers."""

        capability = self._create_capability()

        response = self._execute(
            capability,
            "calculate 4 * 5",
        )

        assert response.success is True
        assert response.text == "The result is 20."

    def test_division(
        self,
    ) -> None:
        """Calculator divides two numbers."""

        capability = self._create_capability()

        response = self._execute(
            capability,
            "calculate 20 / 5",
        )

        assert response.success is True
        assert response.text == "The result is 4."

    def test_divide_by_zero(
        self,
    ) -> None:
        """Calculator handles division by zero."""

        capability = self._create_capability()

        response = self._execute(
            capability,
            "calculate 5 / 0",
        )

        assert response.success is False
        assert response.text == "Cannot divide by zero."

    def test_invalid_expression(
        self,
    ) -> None:
        """Calculator rejects invalid expressions."""

        capability = self._create_capability()

        response = self._execute(
            capability,
            "calculate abc",
        )

        assert response.success is False
        assert (
            response.text
            == "Invalid calculation. Example: calculate 10 + 5"
        )
