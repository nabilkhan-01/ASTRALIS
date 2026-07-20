from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.interpreter import Interpreter
from astralis.brain.execution_plan import ExecutionPlan
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.brain.role import Role
from astralis.capability.manager import CapabilityManager
from astralis.brain.planner import Planner


class Brain:
    """Coordinates intelligent request processing."""

    def __init__(
        self,
        capability_manager: CapabilityManager,
    ) -> None:
        
        # Brain components
        self.interpreter = Interpreter()
        self.planner = Planner()

        # Brain state
        self.conversation = Conversation()

        # Execution
        self.capability_manager = capability_manager

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
        plan = self.planner.plan(
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