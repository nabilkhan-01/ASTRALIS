from astralis.brain.intent import Intent
from astralis.brain.interpretation import Interpretation
from astralis.brain.interpreter import Interpreter
from astralis.brain.plan import ExecutionPlan
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.provider.provider import Provider
from astralis.brain.conversation import Conversation
from astralis.brain.role import Role


class Brain:
    """Coordinates intelligent request processing."""

    def __init__(
        self,
        provider: Provider,
    ) -> None:
        self.provider = provider
        self.interpreter = Interpreter()
        self.conversation = Conversation()

    def process(
        self,
        request: Request,
    ) -> Response:
        """Process a user request through the Brain pipeline."""

        # Execute the processing pipeline.
        request = self._validate(request)

        self.conversation.add(
            Role.USER,
            request.text,
        )

        interpretation = self._interpret(request)

        plan = self._plan(
            request,
            interpretation,
        )

        return self._execute(
            plan,
        )

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
        request: Request,
        interpretation: Interpretation,
    ) -> ExecutionPlan:
        """Create an execution plan for the request."""

        plan = ExecutionPlan()

        if interpretation.intent == Intent.GREETING:
            plan.greeting_required = True
        
        elif interpretation.intent == Intent.QUESTION:
            plan.provider_required = True

        elif interpretation.intent == Intent.CONVERSATION:
            plan.provider_required = True

        elif interpretation.intent == Intent.TOOL:
            plan.tools_required = True

        elif interpretation.intent == Intent.MEMORY:
            plan.memory_required = True

        return plan
        

    def _execute(
        self,
        plan: ExecutionPlan,
    ) -> Response:
        """Execute the processing plan."""

        if plan.provider_required:
            response = self.provider.generate(
                self.conversation,
            )

            self.conversation.add(
                Role.ASSISTANT,
                response.text,
            )

        return response