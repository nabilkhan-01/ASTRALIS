from abc import ABC
from typing import ClassVar

from astralis.brain.response import Response
from astralis.providers.provider import Provider


class LocalProvider(
    Provider,
    ABC,
):
    """Base class for local AI model providers.

    Local providers execute models on local hardware without requiring
    external API keys or cloud services. They encapsulate local runtime
    connection details (host endpoint and model identifier) while adhering
    to the common Provider abstraction.
    """

    DEFAULT_HOST: ClassVar[str] = "http://localhost:11434"

    def __init__(
        self,
        model: str,
        host: str = DEFAULT_HOST,
    ) -> None:
        self.model = model
        self.host = host.rstrip(
            "/",
        )

    @property
    def is_local(
        self,
    ) -> bool:
        """Return True indicating this provider executes on local hardware."""
        return True

    def _connection_error(
        self,
        details: str | None = None,
    ) -> Response:
        """Create a standardized error response when the local runtime is unreachable."""

        message = f"Local model service is unavailable at {self.host}."
        if details:
            message = f"{message} ({details})"

        return Response(
            text=f"{message} Please ensure the local model runtime is running.",
            success=False,
        )
