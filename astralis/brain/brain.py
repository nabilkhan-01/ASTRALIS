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
from astralis.context.context import Context


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

        # Stage 1 - Validation
        request = self._validate(
            context.request,
        )

        # Stage 2 - Conversation (records clean user request)
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
            request=request,
            interpretation=interpretation,
            plan=plan,
            context=context.context,
        )

        # Stage 6 - Conversation (records assistant response)
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
        context: Context,
    ) -> Response:
        """Execute the processing plan."""

        conversation = self._build_execution_conversation(
            request=request,
            context=context,
        )

        return self._capability_manager.execute(
            request=request,
            conversation=conversation,
            interpretation=interpretation,
            plan=plan,
        )

    def _build_execution_conversation(
        self,
        request: Request,
        context: Context,
    ) -> Conversation:
        """Construct temporary conversation input for capability execution."""

        if not context.items:
            return self._conversation

        context_lines: list[str] = []
        for item in context.items:
            if item.entity.properties:
                props = ", ".join(
                    f"{key}={value}"
                    for key, value in item.entity.properties.items()
                )
                context_lines.append(
                    f"- {item.entity.name}: {props}",
                )
            else:
                context_lines.append(
                    f"- {item.entity.name}",
                )

        augmented_content = (
            "[ASTRALIS Retrieved Context]\n"
            + "\n".join(context_lines)
            + "\n[End Retrieved Context]\n\n"
            + "[User Request]\n"
            + request.text
        )

        execution_conversation = Conversation()
        for message in self._conversation.messages[:-1]:
            execution_conversation.add(
                message.role,
                message.content,
            )

        execution_conversation.add(
            Role.USER,
            augmented_content,
        )

        return execution_conversation