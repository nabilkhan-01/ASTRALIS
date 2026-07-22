import operator

from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.capability.capability import Capability


class CalculatorCapability(Capability):
    """Performs basic arithmetic calculations."""

    OPERATORS = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }

    def execute(
        self,
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        """Evaluate a simple arithmetic expression."""

        expression = (
            request.text.lower()
            .replace("calculate", "")
            .replace("+"," + ")
            .replace("-"," - ")
            .replace("*"," * ")
            .replace("/"," / ")
            .strip()
        )

        try:
            left, operator_symbol, right = expression.split()

            operation = self.OPERATORS.get(
                operator_symbol,
            )

            if operation is None:
                raise KeyError

            result = operation(
                float(left),
                float(right),
            )

            if result.is_integer():
                result = int(result)

            return Response(
                text=f"The result is {result}.",
                success=True,
            )

        except ZeroDivisionError:
            return Response(
                text="Cannot divide by zero.",
                success=False,
            )

        except (
            ValueError,
            KeyError,
        ):
            return Response(
                text="Invalid calculation.",
                success=False,
            )