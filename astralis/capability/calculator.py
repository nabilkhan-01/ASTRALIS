import operator
from collections.abc import Callable
from typing import ClassVar

from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.capability.capability import Capability


class CalculatorCapability(Capability):
    """Performs basic arithmetic calculations."""

    OPERATORS: ClassVar[dict[str, Callable[[float, float], float]]] = {
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

        _ = conversation, interpretation

        try:
            left, operator_symbol, right = self._parse_expression(
                request.text,
            )

            operation = self.OPERATORS.get(
                operator_symbol,
            )

            if operation is None:
                raise ValueError

            result = operation(
                float(left),
                float(right),
            )

            if result.is_integer():
                result = int(
                    result,
                )

            return Response(
                text=f"The result is {result}.",
            )

        except ZeroDivisionError:
            return Response(
                text="Cannot divide by zero.",
                success=False,
            )

        except ValueError:
            return Response(
                text=("Invalid calculation. Example: calculate 10 + 5"),
                success=False,
            )

    def _parse_expression(
        self,
        text: str,
    ) -> tuple[str, str, str]:
        """Parse an arithmetic expression."""

        expression = (
            text.lower()
            .replace("calculate", "")
            .replace("+", " + ")
            .replace("-", " - ")
            .replace("*", " * ")
            .replace("/", " / ")
            .strip()
        )

        return tuple(
            expression.split(),
        )  # type: ignore[return-value]
