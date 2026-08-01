from astralis.brain.context import BrainContext
from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.interpreter import Interpreter
from astralis.brain.plan import Plan
from astralis.brain.planner import Planner
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.brain.role import Role
from astralis.capability.manager import CapabilityManager


class Brain:
    """Coordinates intelligent request processing."""

    def __init__(
        self,
        capability_manager: CapabilityManager,
    ) -> None:
        # Brain components
        self._interpreter = Interpreter()
        self._planner = Planner()

        # Brain state
        self._conversation = Conversation()

        # Execution
        self._capability_manager = capability_manager

    def process(
        self,
        context: BrainContext,
    ) -> Response:
        """Process a user request through the Brain pipeline."""

        # Memory is intentionally unused for now.
        # Future versions will use it to build richer
        # reasoning context before interpretation.
        _ = context.memory

        # Stage 1 - Validation
        request = self._validate(
            context.request,
        )

        # Stage 2 - Conversation
        self._conversation.add(
            Role.USER,
            request.text,
        )

        # Stage 3 - Interpretation
        interpretation = self._interpret(
            request,
        )

        # Stage 4 - Planning
        plan = self._planner.plan(
            interpretation,
        )

        # Stage 5 - Execution
        response = self._execute(
            request,
            interpretation,
            plan,
        )

        # Stage 6 - Conversation
        self._conversation.add(
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

        return self._interpreter.interpret(
            request,
        )

    def _execute(
        self,
        request: Request,
        interpretation: Interpretation,
        plan: Plan,
    ) -> Response:
        """Execute the processing plan."""

        return self._capability_manager.execute(
            request=request,
            conversation=self._conversation,
            interpretation=interpretation,
            plan=plan,
        )