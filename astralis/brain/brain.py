from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.interpreter import Interpreter
from astralis.brain.plan import Plan
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

        # Stage 1 - validation
        request = self._validate(request)

        # Stage 2 - Conversation
        self.conversation.add(
            Role.USER,
            request.text,
        )

        # Stage 3 - Interpretation
        interpretation = self._interpret(request)

        # Stage 4 - Planning
        plan = self.planner.plan(
            interpretation,
        )

        # Stage 5 - Execution
        response = self._execute(
            request,
            interpretation,
            plan,
        )

        # Stage 6 - Conversation
        self.conversation.add(
            Role.ASSISTANT,
            response.text,
        )

        # Stage 7 - Response
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
        request: Request,
        interpretation: Interpretation,
        plan: Plan,
    ) -> Response:
        """Execute the processing plan."""

        return self.capability_manager.execute(
            request=request,
            conversation=self.conversation,
            interpretation=interpretation,
            plan=plan,
        )