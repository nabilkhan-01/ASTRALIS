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
from astralis.memory.entity_type import EntityType


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

        if not context.has_context:
            return self._conversation

        context_lines: list[str] = []
        project_represented = False

        for item in context.items:
            props_dict = dict(item.entity.properties)
            if (
                item.entity.type is EntityType.PROJECT
                and item.entity.name.upper() == context.project_identity.name.upper()
            ):
                project_represented = True
                # Anti-spoof: canonical identity takes precedence over mutable memory
                if "creator" in props_dict and props_dict["creator"] != context.creator:
                    props_dict["creator"] = context.creator
                if "founder" in props_dict and props_dict["founder"] not in (
                    context.founder,
                    "Nabil",
                ):
                    props_dict["founder"] = context.founder
                if context.is_identity_relevant and "founder" not in props_dict:
                    props_dict["founder"] = context.founder

            if props_dict:
                props = ", ".join(
                    f"{key}={value}"
                    for key, value in props_dict.items()
                )
                context_lines.append(
                    f"- {item.entity.name}: {props}",
                )
            else:
                context_lines.append(
                    f"- {item.entity.name}",
                )

        if context.is_identity_relevant and not project_represented:
            context_lines.insert(
                0,
                f"- {context.project_identity.name}: founder={context.project_identity.founder}",
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