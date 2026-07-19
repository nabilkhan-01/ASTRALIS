from astralis.brain.plan import ExecutionPlan
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.provider.provider import Provider


class Brain:
    """Coordinates intelligent request processing."""

    def __init__(
        self,
        provider: Provider,
    ) -> None:
        self.provider = provider

    def process(
        self,
        request: Request,
    ) -> Response:
        """Process a user request through the Brain pipeline."""

        # Execute the processing pipeline.
        request = self._validate(request)
        request = self._interpret(request)

        plan = self._plan(request)

        return self._execute(
            request,
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
    ) -> Request:
        """Interpret the user's request."""

        return request

    def _plan(
        self,
        request: Request,
    ) -> ExecutionPlan:
        """Create an execution plan for the request."""

        return ExecutionPlan()

    def _execute(
        self,
        request: Request,
        plan: ExecutionPlan,
    ) -> Response:
        """Execute the processing plan."""

        if plan.provider_required:
            return self.provider.generate(request)

        return Response(
            text="No execution strategy available.",
            success=False,
        )