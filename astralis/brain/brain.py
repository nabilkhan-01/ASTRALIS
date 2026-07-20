from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.interpreter import Interpreter
from astralis.brain.plan import ExecutionPlan
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.brain.role import Role
from astralis.capability.manager import CapabilityManager
from astralis.capability.capability_type import CapabilityType


class Brain:
    """Coordinates intelligent request processing."""

    def __init__(
        self,
        capability_manager: CapabilityManager,
    ) -> None:
        self.capability_manager = capability_manager
        self.interpreter = Interpreter()
        self.conversation = Conversation()

    def process(
        self,
        request: Request,
    ) -> Response:
        """Process a user request through the Brain pipeline."""

        # validation
        request = self._validate(request)

        # Conversation
        self.conversation.add(
            Role.USER,
            request.text,
        )

        # Interpretation
        interpretation = self._interpret(request)

        # Planning
        plan = self._plan(
            interpretation,
        )

        # Execution
        response = self._execute(
            interpretation,
            plan,
        )

        # Conversation
        self.conversation.add(
            Role.ASSISTANT,
            response.text,
        )

        return response

    def _validate(
        self,
        request: Request,
    ) -> Request:
        """Validate the incoming request."""

        return request

    def _interpret(
        self,
        request: Request,
    ) -> Interpretation:
        """Interpret the user's request."""

        return self.interpreter.interpret(request)

    def _plan(
        self,
        interpretation: Interpretation,
    ) -> ExecutionPlan:
        """Create an execution plan for the request."""

        return ExecutionPlan(
            capability=CapabilityType.LANGUAGE,
        )

    def _execute(
        self,
        interpretation: Interpretation,
        plan: ExecutionPlan,
    ) -> Response:
        """Execute the processing plan."""

        return self.capability_manager.execute(
            conversation=self.conversation,
            interpretation=interpretation,
            plan=plan,
        )